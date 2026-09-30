import JointWitness

/-!
Exact dyadic counts up to arbitrary integer cutoffs, including an incomplete last shell.
The counted points are positive integers 1,...,X. Theorems quantify over
all lengths and natural weights; the count bounds require weights <= 1.
No logarithmic asymptotics or analytic Collatz estimate is assumed proved.
-/
set_option autoImplicit false
set_option maxRecDepth 1024
namespace CollatzDyadicCertificate
open CollatzClockCertificate CollatzJointCertificate

def span (f : Nat → Nat) (a len : Nat) : Nat :=
  finiteSum len (fun i => f (a+i))
def prefixCount (f : Nat → Nat) (X : Nat) : Nat := span f 1 X
def shell (f : Nat → Nat) (m : Nat) : Nat := span f (2^m) (2^m)
def blocks (f : Nat → Nat) (K J : Nat) : Nat :=
  finiteSum J (fun j => shell f (K+j))

theorem span_split (f : Nat → Nat) (a len extra : Nat) :
    span f a (len+extra)=span f a len+span f (a+len) extra := by
  unfold span
  rw [finiteSum_split]
  congr 1
  apply finiteSum_ext
  intro i _
  congr 1
  omega

theorem span_length_mono (f : Nat → Nat) (a l u : Nat) (h : l≤u) :
    span f a l≤span f a u := by
  have hs := span_split f a l (u-l)
  have he : l+(u-l)=u := by omega
  rw [he] at hs
  omega

theorem span_le_length (f : Nat → Nat) (hf : ∀ n, f n≤1) (a len : Nat) :
    span f a len≤len := by
  induction len with
  | zero => exact Nat.le_refl 0
  | succ len ih =>
    change span f a len+f (a+len)≤len+1
    have hi := hf (a+len)
    omega

theorem two_power_positive (m : Nat) : 0<2^m := by
  induction m with
  | zero => decide
  | succ m ih =>
    rw [Nat.pow_succ]
    omega

theorem prefix_split_at (f : Nat → Nat) (a X : Nat)
    (ha : 1≤a) (hX : a≤X+1) :
    prefixCount f X=prefixCount f (a-1)+span f a (X+1-a) := by
  have hx : a-1+(X+1-a)=X := by omega
  have hs := span_split f 1 (a-1) (X+1-a)
  have hh : 1+(a-1)=a := by omega
  simpa only [prefixCount, hx, hh] using hs

theorem complete_shell_split (f : Nat → Nat) (m : Nat) :
    prefixCount f (2^(m+1)-1)=prefixCount f (2^m-1)+shell f m := by
  have hp := two_power_positive m
  have he : 2^(m+1)=2^m+2^m := by rw [Nat.pow_succ]; omega
  have hx : 2^m≤(2^(m+1)-1)+1 := by omega
  have hs := prefix_split_at f (2^m) (2^(m+1)-1) (by omega) hx
  have ht : (2^(m+1)-1)+1-2^m=2^m := by omega
  simpa only [ht, shell] using hs

theorem complete_shells_partition (f : Nat → Nat) (K J : Nat) :
    prefixCount f (2^(K+J)-1)=prefixCount f (2^K-1)+blocks f K J := by
  induction J with
  | zero => simp [blocks, finiteSum]
  | succ J ih =>
    have hs := complete_shell_split f (K+J)
    have hidx : K+(J+1)=K+J+1 := by omega
    rw [hidx, hs, ih]
    change (prefixCount f (2^K-1)+blocks f K J)+shell f (K+J)=
      prefixCount f (2^K-1)+(blocks f K J+shell f (K+J))
    omega

theorem dyadic_prefix_partition (f : Nat → Nat) (K J X : Nat)
    (hlo : 2^(K+J)≤X) :
    prefixCount f X=prefixCount f (2^K-1)+blocks f K J+
      span f (2^(K+J)) (X+1-2^(K+J)) := by
  have hp := two_power_positive (K+J)
  rw [prefix_split_at f (2^(K+J)) X (by omega) (by omega),
      complete_shells_partition]

theorem top_shell_length (K J X : Nat)
    (hlo : 2^(K+J)≤X) (hhi : X<2^(K+J+1)) :
    1≤X+1-2^(K+J) ∧ X+1-2^(K+J)≤2^(K+J) := by
  have he : 2^(K+J+1)=2^(K+J)+2^(K+J) := by
    rw [Nat.pow_succ]
    omega
  constructor <;> omega

theorem partial_shell_cap (f : Nat → Nat) (hf : ∀ n, f n≤1)
    (m len b : Nat) (hlen : len≤2^m) (hb : shell f m≤b) :
    span f (2^m) len≤min len b := by
  have hl := span_le_length f hf (2^m) len
  have hs := span_length_mono f (2^m) len (2^m) hlen
  change span f (2^m) (2^m)≤b at hb
  omega

theorem blocks_budget (f b : Nat → Nat) (hf : ∀ n, f n≤1)
    (K J : Nat) (hb : ∀ j, j<J → shell f (K+j)≤b (K+j)) :
    blocks f K J≤finiteSum J (fun j => min (2^(K+j)) (b (K+j))) := by
  apply finiteSum_mono
  intro j hj
  have hc := span_le_length f hf (2^(K+j)) (2^(K+j))
  have hbj := hb j hj
  change shell f (K+j)≤2^(K+j) at hc
  omega

theorem dyadic_prefix_bound (f b : Nat → Nat) (hf : ∀ n, f n≤1)
    (K J X : Nat) (hlo : 2^(K+J)≤X) (hhi : X<2^(K+J+1))
    (hb : ∀ j, j≤J → shell f (K+j)≤b (K+j)) :
    prefixCount f X≤2^K-1+
      finiteSum J (fun j => min (2^(K+j)) (b (K+j)))+
      min (X+1-2^(K+J)) (b (K+J)) := by
  rw [dyadic_prefix_partition f K J X hlo]
  have hstart := span_le_length f hf 1 (2^K-1)
  change prefixCount f (2^K-1)≤2^K-1 at hstart
  have hfull := blocks_budget f b hf K J (fun j hj => hb j (by omega))
  have hlast := partial_shell_cap f hf (K+J) (X+1-2^(K+J)) (b (K+J))
    (top_shell_length K J X hlo hhi).2 (hb J (Nat.le_refl J))
  omega

def absent (P : Nat → Prop) [DecidablePred P] (n : Nat) : Nat :=
  if P n then 0 else 1

theorem absent_le_one (P : Nat → Prop) [DecidablePred P] (n : Nat) :
    absent P n≤1 := by
  unfold absent
  split <;> omega

theorem prefix_absent (P : Nat → Prop) [DecidablePred P] (X : Nat) :
    prefixCount (absent P) X=missingCount P X := by
  unfold prefixCount span missingCount
  apply finiteSum_ext
  intro i _
  simp only [absent, Nat.add_comm 1 i]

theorem missing_dyadic_bound (P : Nat → Prop) [DecidablePred P]
    (b : Nat → Nat) (K J X : Nat)
    (hlo : 2^(K+J)≤X) (hhi : X<2^(K+J+1))
    (hb : ∀ j, j≤J → shell (absent P) (K+j)≤b (K+j)) :
    missingCount P X≤2^K-1+
      finiteSum J (fun j => min (2^(K+j)) (b (K+j)))+
      min (X+1-2^(K+J)) (b (K+J)) := by
  rw [← prefix_absent P X]
  exact dyadic_prefix_bound (absent P) b (absent_le_one P) K J X hlo hhi hb

theorem raw_dyadic_exception_bound (H S Y B b : Nat → Nat) (K J X : Nat)
    (hlo : 2^(K+J)≤X) (hhi : X<2^(K+J+1))
    (hb : ∀ j, j≤J →
      shell (absent (fun n => TaggedWitness n (H n) (S n) (Y n) (B n))) (K+j)
      ≤b (K+j)) :
    missingCount (fun n => RawWitness n (H n+S n) (Y n) (2*B n)) X≤2^K-1+
      finiteSum J (fun j => min (2^(K+j)) (b (K+j)))+
      min (X+1-2^(K+J)) (b (K+J)) := by
  exact Nat.le_trans (raw_exception_count H S Y B X)
    (missing_dyadic_bound (fun n => TaggedWitness n (H n) (S n) (Y n) (B n))
      b K J X hlo hhi hb)


/-- Scaled shell budgets telescope without monotonicity of the budgets. -/
theorem scaled_blocks_budget (f : Nat → Nat) (D R K J : Nat)
    (hb : ∀ j, j<J → D*shell f (K+j)≤R*2^(K+j)) :
    D*blocks f K J+R*2^K≤R*2^(K+J) := by
  induction J with
  | zero => simp [blocks, finiteSum]
  | succ J ih =>
    have old := ih (fun j hj => hb j (by omega))
    have last := hb J (by omega)
    have he : 2^(K+(J+1))=2^(K+J)+2^(K+J) := by
      rw [show K+(J+1)=K+J+1 by omega, Nat.pow_succ]
      omega
    change D*(blocks f K J+shell f (K+J))+R*2^K≤R*2^(K+(J+1))
    rw [he, Nat.mul_add, Nat.mul_add]
    omega

theorem scaled_dyadic_tail_bound (f : Nat → Nat) (hf : ∀ n, f n≤1)
    (D R K J X : Nat) (hlo : 2^(K+J)≤X) (hhi : X<2^(K+J+1))
    (hb : ∀ j, j≤J → D*shell f (K+j)≤R*2^(K+j)) :
    D*prefixCount f X≤D*(2^K-1)+2*X*R := by
  have hstart := Nat.mul_le_mul_left D (span_le_length f hf 1 (2^K-1))
  change D*prefixCount f (2^K-1)≤D*(2^K-1) at hstart
  have hfull := scaled_blocks_budget f D R K J (fun j hj => hb j (by omega))
  have hpartial := span_length_mono f (2^(K+J)) (X+1-2^(K+J)) (2^(K+J))
    (top_shell_length K J X hlo hhi).2
  have hlast := Nat.le_trans (Nat.mul_le_mul_left D hpartial) (hb J (Nat.le_refl J))
  have htwice : R*2^(K+J)+R*2^(K+J)≤2*X*R := by
    have ht := Nat.mul_le_mul_left (2*R) hlo
    have hl : (2*R)*2^(K+J)=R*2^(K+J)+R*2^(K+J) := by
      rw [Nat.mul_assoc, Nat.two_mul]
    have hr : (2*R)*X=2*X*R := by
      simp [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
    simpa only [hl, hr] using ht
  rw [dyadic_prefix_partition f K J X hlo, Nat.mul_add, Nat.mul_add]
  omega

theorem missing_scaled_tail_bound (P : Nat → Prop) [DecidablePred P]
    (D R K J X : Nat) (hlo : 2^(K+J)≤X) (hhi : X<2^(K+J+1))
    (hb : ∀ j, j≤J → D*shell (absent P) (K+j)≤R*2^(K+j)) :
    D*missingCount P X≤D*(2^K-1)+2*X*R := by
  rw [← prefix_absent P X]
  exact scaled_dyadic_tail_bound (absent P) (absent_le_one P) D R K J X hlo hhi hb

/-- The hypothesis is restricted to the exact shell being counted. -/
theorem missing_shell_mono (P Q : Nat → Prop) [DecidablePred P] [DecidablePred Q]
    (m : Nat) (hPQ : ∀ i, i<2^m → P (2^m+i) → Q (2^m+i)) :
    shell (absent Q) m≤shell (absent P) m := by
  apply finiteSum_mono
  intro i hi
  by_cases hp : P (2^m+i)
  · have hq := hPQ i hi hp
    simp [absent, hp, hq]
  · simp [absent, hp]
    split <;> omega

/-- No implication is requested below the finite startup prefix. -/
theorem retained_dyadic_bound (P Q : Nat → Prop) [DecidablePred P] [DecidablePred Q]
    (b : Nat → Nat) (K J X : Nat)
    (hlo : 2^(K+J)≤X) (hhi : X<2^(K+J+1))
    (hPQ : ∀ j, j≤J → ∀ i, i<2^(K+j) → P (2^(K+j)+i) → Q (2^(K+j)+i))
    (hb : ∀ j, j≤J → shell (absent P) (K+j)≤b (K+j)) :
    missingCount Q X≤2^K-1+
      finiteSum J (fun j => min (2^(K+j)) (b (K+j)))+
      min (X+1-2^(K+J)) (b (K+J)) := by
  apply missing_dyadic_bound Q b K J X hlo hhi
  intro j hj
  exact Nat.le_trans (missing_shell_mono P Q (K+j) (hPQ j hj)) (hb j hj)

theorem retained_raw_dyadic_bound (P : Nat → Prop) [DecidablePred P]
    (H S Y B b : Nat → Nat) (K J X : Nat)
    (hlo : 2^(K+J)≤X) (hhi : X<2^(K+J+1))
    (hP : ∀ j, j≤J → ∀ i, i<2^(K+j) → P (2^(K+j)+i) →
      TaggedWitness (2^(K+j)+i) (H (2^(K+j)+i)) (S (2^(K+j)+i))
        (Y (2^(K+j)+i)) (B (2^(K+j)+i)))
    (hb : ∀ j, j≤J → shell (absent P) (K+j)≤b (K+j)) :
    missingCount (fun n => RawWitness n (H n+S n) (Y n) (2*B n)) X≤2^K-1+
      finiteSum J (fun j => min (2^(K+j)) (b (K+j)))+
      min (X+1-2^(K+J)) (b (K+J)) := by
  apply retained_dyadic_bound P (fun n => RawWitness n (H n+S n) (Y n) (2*B n))
    b K J X hlo hhi _ hb
  intro j hj i hi hp
  exact tagged_to_raw _ _ _ _ _ (hP j hj i hi hp)

theorem retained_raw_scaled_tail_bound (P : Nat → Prop) [DecidablePred P]
    (H S Y B : Nat → Nat) (D R K J X : Nat)
    (hlo : 2^(K+J)≤X) (hhi : X<2^(K+J+1))
    (hP : ∀ j, j≤J → ∀ i, i<2^(K+j) → P (2^(K+j)+i) →
      TaggedWitness (2^(K+j)+i) (H (2^(K+j)+i)) (S (2^(K+j)+i))
        (Y (2^(K+j)+i)) (B (2^(K+j)+i)))
    (hb : ∀ j, j≤J → D*shell (absent P) (K+j)≤R*2^(K+j)) :
    D*missingCount (fun n => RawWitness n (H n+S n) (Y n) (2*B n)) X
      ≤D*(2^K-1)+2*X*R := by
  apply missing_scaled_tail_bound (fun n => RawWitness n (H n+S n) (Y n) (2*B n))
    D R K J X hlo hhi
  intro j hj
  have hmono := missing_shell_mono P (fun n => RawWitness n (H n+S n) (Y n) (2*B n))
    (K+j) (by
      intro i hi hp
      exact tagged_to_raw _ _ _ _ _ (hP j hj i hi hp))
  exact Nat.le_trans (Nat.mul_le_mul_left D hmono) (hb j hj)

#print axioms missing_shell_mono
#print axioms retained_dyadic_bound
#print axioms retained_raw_dyadic_bound
#print axioms retained_raw_scaled_tail_bound
#print axioms scaled_blocks_budget
#print axioms scaled_dyadic_tail_bound
#print axioms missing_scaled_tail_bound
#print axioms span_split
#print axioms span_length_mono
#print axioms span_le_length
#print axioms two_power_positive
#print axioms prefix_split_at
#print axioms complete_shell_split
#print axioms complete_shells_partition
#print axioms dyadic_prefix_partition
#print axioms top_shell_length
#print axioms partial_shell_cap
#print axioms blocks_budget
#print axioms dyadic_prefix_bound
#print axioms absent_le_one
#print axioms prefix_absent
#print axioms missing_dyadic_bound
#print axioms raw_dyadic_exception_bound
end CollatzDyadicCertificate
