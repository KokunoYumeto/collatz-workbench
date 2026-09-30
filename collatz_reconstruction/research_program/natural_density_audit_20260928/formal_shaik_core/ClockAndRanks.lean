import Init

/-!
Exact raw/shortcut first-passage and height correspondence.
Primary comparison: Idris Ali Shaik, Basic.lean and RawDynamics.lean,
commit ef3410843bf58d69f771f5ba2c0571d54b54da59.
This independent Lean 4.15 core certificate uses the identical map formulas,
with recursive iteration. It does not import or certify Shaik's Mathlib package.
The source's orbit_zero/orbit_succ identify its iteration with this one by induction.
No density estimate or analytic constant is assumed or certified here.
-/
set_option autoImplicit false
set_option maxRecDepth 1024
namespace CollatzClockCertificate

def shortcut (n : Nat) : Nat :=
  if n % 2 = 0 then n / 2 else (3*n+1)/2
def raw (n : Nat) : Nat :=
  if n % 2 = 0 then n / 2 else 3*n+1
def iterate (f : Nat → Nat) : Nat → Nat → Nat
  | 0, n => n
  | k+1, n => f (iterate f k n)
def oddCount (n : Nat) : Nat → Nat
  | 0 => 0
  | k+1 => oddCount n k + iterate shortcut k n % 2
def clock (n k : Nat) : Nat := k + oddCount n k

theorem clock_zero (n : Nat) : clock n 0 = 0 := rfl
theorem clock_succ (n k : Nat) :
    clock n (k+1) = clock n k + 1 + iterate shortcut k n % 2 := by
  simp only [clock, oddCount]
  omega

theorem iterate_add (f : Nat → Nat) (a b n : Nat) :
    iterate f (a+b) n = iterate f a (iterate f b n) := by
  induction a with
  | zero => simp [iterate]
  | succ a ih =>
    rw [Nat.succ_add]
    simp only [iterate, ih]

theorem raw_one_even (n : Nat) (hn : n % 2 = 0) :
    raw n = shortcut n := by simp [raw, shortcut, hn]

theorem raw_two_odd (n : Nat) (hn : n % 2 = 1) :
    iterate raw 2 n = shortcut n := by
  have he : (3*n+1) % 2 = 0 := by omega
  simp [iterate, raw, shortcut, hn, he]

theorem odd_inserted_height (n : Nat) (hn : n % 2 = 1) :
    raw n = 2 * shortcut n := by
  have he : (3*n+1) % 2 = 0 := by omega
  simp only [raw, shortcut, hn, show (1:Nat) ≠ 0 by decide, if_false]
  omega

theorem exact_clock (n k : Nat) :
    iterate raw (clock n k) n = iterate shortcut k n := by
  induction k with
  | zero => rfl
  | succ k ih =>
    have hp := Nat.mod_lt (iterate shortcut k n) (by decide : 0<2)
    by_cases he : iterate shortcut k n % 2 = 0
    · rw [clock_succ, he, Nat.add_zero]
      simp only [iterate, ih]
      exact raw_one_even _ he
    · have ho : iterate shortcut k n % 2 = 1 := by omega
      have ht : clock n (k+1) = 2 + clock n k := by rw [clock_succ, ho]; omega
      rw [ht, iterate_add, ih]
      exact raw_two_odd _ ho

theorem clock_strict (n h k : Nat) (hhk : h < k) :
    clock n h < clock n k := by
  induction k with
  | zero => omega
  | succ k ih =>
    by_cases he : h=k
    · subst h
      rw [clock_succ]
      omega
    · have hi : h<k := by omega
      have hr := ih hi
      rw [clock_succ]
      omega

/-- Every raw time strictly inside an expanded prefix is a shortcut
source or its inserted odd image. The source index is strictly before k. -/
theorem prefix_cover (n k j : Nat) (hj : j < clock n k) :
    ∃ i, i<k ∧
      (iterate raw j n = iterate shortcut i n ∨
       (iterate shortcut i n % 2 = 1 ∧
        iterate raw j n = 3*iterate shortcut i n+1)) := by
  induction k with
  | zero => simp [clock, oddCount] at hj
  | succ k ih =>
    by_cases hold : j < clock n k
    · obtain ⟨i, hi, hv⟩ := ih hold
      exact ⟨i, by omega, hv⟩
    · have hp := Nat.mod_lt (iterate shortcut k n) (by decide : 0<2)
      have hc := clock_succ n k
      by_cases he : j=clock n k
      · exact ⟨k, by omega, Or.inl (he ▸ exact_clock n k)⟩
      · have ho : iterate shortcut k n % 2 = 1 := by omega
        have ht : j=clock n k+1 := by omega
        refine ⟨k, by omega, Or.inr ⟨ho, ?_⟩⟩
        rw [ht]
        simp only [iterate, exact_clock]
        simp [raw, ho]

def FirstPassage (f : Nat → Nat) (n Y h : Nat) : Prop :=
  iterate f h n ≤ Y ∧ ∀ i, i<h → Y < iterate f i n

/-- Concatenation retains literal first passage, not merely an endpoint. -/
theorem first_passage_nested (f : Nat → Nat) (n Y Z a b : Nat)
    (hZY : Z ≤ Y) (ha : FirstPassage f n Y a)
    (hb : FirstPassage f (iterate f a n) Z b) :
    FirstPassage f n Z (a+b) := by
  constructor
  · simpa [Nat.add_comm a b, iterate_add] using hb.1
  · intro j hj
    by_cases hja : j<a
    · exact Nat.lt_of_le_of_lt hZY (ha.2 j hja)
    · have hdiff : j-a<b := by omega
      have heq : j=(j-a)+a := by omega
      rw [heq, iterate_add]
      exact hb.2 (j-a) hdiff

theorem shortcut_two_pow_succ (q : Nat) : shortcut (2^(q+1)) = 2^q := by
  simp [shortcut, Nat.pow_succ, Nat.mul_mod]

theorem iterate_two_pow (q i : Nat) (hi : i≤q) :
    iterate shortcut i (2^q) = 2^(q-i) := by
  induction i with
  | zero => rfl
  | succ i ih =>
    have hii : i≤q := by omega
    simp only [iterate, ih hii]
    have heq : q-i=(q-(i+1))+1 := by omega
    rw [heq, shortcut_two_pow_succ]

theorem dyadic_first_passage (q L : Nat) (hL : L≤q) :
    FirstPassage shortcut (2^q) (2^L) (q-L) := by
  constructor
  · rw [iterate_two_pow q (q-L) (by omega)]
    have heq : q-(q-L)=L := by omega
    rw [heq]
    exact Nat.le_refl _
  · intro i hi
    rw [iterate_two_pow q i (by omega)]
    have hp := Nat.two_pow_pos L
    have hs : 2^L < 2^(L+1) := by rw [Nat.pow_succ]; omega
    exact Nat.lt_of_lt_of_le hs
      (Nat.pow_le_pow_right (by decide : 0<2) (by omega : L+1≤q-i))

/-- Complete a reached dyadic endpoint to the lower threshold on the same
path; all preceding orbit points remain above that lower threshold. -/
theorem dyadic_completion (n h q L : Nat) (hL : L≤q)
    (hp : FirstPassage shortcut n (2^q) h)
    (heq : iterate shortcut h n = 2^q) :
    FirstPassage shortcut n (2^L) (h+(q-L)) := by
  apply first_passage_nested shortcut n (2^q) (2^L) h (q-L)
  · exact Nat.pow_le_pow_right (by decide : 0<2) hL
  · exact hp
  · rw [heq]
    exact dyadic_first_passage q L hL

theorem first_passage_iff (n Y h : Nat) :
    FirstPassage shortcut n Y h ↔ FirstPassage raw n Y (clock n h) := by
  constructor
  · intro hp
    refine ⟨?_, ?_⟩
    · simpa [exact_clock] using hp.1
    · intro j hj
      obtain ⟨i, hi, hv⟩ := prefix_cover n h j hj
      have hx := hp.2 i hi
      rcases hv with hv | ⟨_,hv⟩ <;> rw [hv] <;> omega
  · intro hp
    refine ⟨?_, ?_⟩
    · simpa [exact_clock] using hp.1
    · intro i hi
      have htime := clock_strict n i h hi
      simpa [exact_clock] using hp.2 (clock n i) htime

/-- Prefix height doubles at most; this retains all intermediate raw times. -/
theorem height_transfer (n h B : Nat)
    (hB : ∀ i, i≤h → iterate shortcut i n ≤ B) :
    ∀ j, j≤clock n h → iterate raw j n ≤ 2*B := by
  intro j hj
  by_cases he : j=clock n h
  · rw [he, exact_clock]
    have hb := hB h (by omega)
    omega
  · have hj' : j<clock n h := by omega
    obtain ⟨i, hi, hv⟩ := prefix_cover n h j hj'
    rcases hv with hv | ⟨ho,hv⟩
    · rw [hv]
      have hb := hB i (by omega)
      omega
    · rw [hv]
      have hb := hB (i+1) (by omega)
      have hh := odd_inserted_height (iterate shortcut i n) ho
      have hr : raw (iterate shortcut i n) = 3*iterate shortcut i n+1 := by
        simp [raw, ho]
      rw [hr] at hh
      change shortcut (iterate shortcut i n) ≤ B at hb
      omega

/-- The ordinary prefix contains every shortcut prefix point. -/
theorem shortcut_height_of_raw_height (n h B : Nat)
    (hB : ∀ j, j≤clock n h → iterate raw j n ≤ B) :
    ∀ i, i≤h → iterate shortcut i n ≤ B := by
  intro i hi
  have hc : clock n i ≤ clock n h := by
    by_cases he : i=h
    · subst i; omega
    · exact Nat.le_of_lt (clock_strict n i h (by omega))
  simpa [exact_clock] using hB (clock n i) hc

/-- Uniqueness of the recursively specified iterate is the definitional
crosswalk to the source's proved orbit_zero/orbit_succ equations. -/
theorem iterate_unique (f : Nat → Nat) (a : Nat → Nat → Nat)
    (h0 : ∀ n, a 0 n=n)
    (hs : ∀ k n, a (k+1) n=f (a k n)) :
    ∀ k n, a k n=iterate f k n := by
  intro k
  induction k with
  | zero => intro n; exact h0 n
  | succ k ih =>
    intro n
    rw [hs, ih]
    rfl

/-- Sum of rank debits; no division or discarded endpoint shift. -/
def debit (m q : Nat → Nat) : Nat → Nat
  | 0 => 0
  | k+1 => debit m q k + (m k - q k)

theorem rank_telescope (m q : Nat → Nat) (j : Nat)
    (hparent : ∀ i, i≤j → q i≤m i)
    (hnext : ∀ i, i<j → m (i+1)+1=q i) :
    debit m q (j+1) + q j + j = m 0 := by
  induction j with
  | zero =>
    simp only [debit, Nat.zero_add, Nat.add_zero]
    have := hparent 0 (by omega)
    omega
  | succ j ih =>
    have hpa : ∀ i, i≤j → q i≤m i := by
      intro i hi
      exact hparent i (by omega)
    have hn : ∀ i, i<j → m (i+1)+1=q i := by
      intro i hi
      exact hnext i (by omega)
    have ht := ih hpa hn
    have hm := hnext j (by omega)
    have hq := hparent (j+1) (by omega)
    simp only [debit]
    change debit m q j + (m j - q j) + (m (j+1)-q (j+1)) + q (j+1) + (j+1) = m 0
    change debit m q j + (m j-q j) + q j+j=m 0 at ht
    omega

theorem oddCount_le (n k : Nat) : oddCount n k ≤ k := by
  induction k with
  | zero => simp [oddCount]
  | succ k ih =>
    have hp := Nat.mod_lt (iterate shortcut k n) (by decide : 0<2)
    simp only [oddCount]
    omega

def affineNumerator (n : Nat) : Nat → Nat
  | 0 => 0
  | k+1 => if iterate shortcut k n % 2 = 0 then affineNumerator n k
           else 3 * affineNumerator n k + 2^k

theorem scaled_affine_exact (n k : Nat) :
    2^k * iterate shortcut k n =
      3^(oddCount n k)*n + affineNumerator n k := by
  induction k with
  | zero => simp [iterate, oddCount, affineNumerator]
  | succ k ih =>
    have hp := Nat.mod_lt (iterate shortcut k n) (by decide : 0<2)
    by_cases he : iterate shortcut k n % 2 = 0
    · have hstep : 2 * shortcut (iterate shortcut k n) = iterate shortcut k n := by
        simp only [shortcut, he, if_pos]
        omega
      simp only [oddCount, affineNumerator, he, if_pos, Nat.add_zero, iterate]
      rw [Nat.pow_succ, Nat.mul_assoc, hstep, ih]
    · have ho : iterate shortcut k n % 2 = 1 := by omega
      have hstep : 2 * shortcut (iterate shortcut k n) =
          3*iterate shortcut k n+1 := by
        simp only [shortcut, he, if_false]
        omega
      simp only [oddCount, affineNumerator, ho, show (1:Nat) ≠ 0 by decide, if_false, iterate]
      calc
        2^(k+1) * shortcut (iterate shortcut k n) =
            2^k * (3*iterate shortcut k n+1) := by
              rw [Nat.pow_succ, Nat.mul_assoc, hstep]
        _ = 3*(2^k*iterate shortcut k n)+2^k := by
              simp [Nat.mul_add, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
        _ = 3*(3^(oddCount n k)*n+affineNumerator n k)+2^k := by rw [ih]
        _ = 3^(oddCount n k+1)*n+(3*affineNumerator n k+2^k) := by
              simp [Nat.pow_succ, Nat.mul_add, Nat.mul_assoc, Nat.mul_comm,
                Nat.mul_left_comm, Nat.add_assoc]

theorem affine_numerator_envelope (n k : Nat) :
    affineNumerator n k + 2^k ≤ 3^(oddCount n k) * 2^(k-oddCount n k) := by
  induction k with
  | zero => simp [affineNumerator, oddCount]
  | succ k ih =>
    have hs := oddCount_le n k
    have hp := Nat.mod_lt (iterate shortcut k n) (by decide : 0<2)
    by_cases he : iterate shortcut k n % 2 = 0
    · simp only [affineNumerator, oddCount, he, if_pos, Nat.add_zero]
      have heq : k+1-oddCount n k = (k-oddCount n k)+1 := by omega
      rw [heq]
      calc
        affineNumerator n k+2^(k+1) ≤ 2*(affineNumerator n k+2^k) := by
          rw [Nat.pow_succ]
          omega
        _ ≤ 2*(3^(oddCount n k)*2^(k-oddCount n k)) := Nat.mul_le_mul_left 2 ih
        _ = 3^(oddCount n k)*2^((k-oddCount n k)+1) := by
          simp [Nat.pow_succ, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
    · have ho : iterate shortcut k n % 2 = 1 := by omega
      simp only [affineNumerator, oddCount, ho, show (1:Nat) ≠ 0 by decide, if_false]
      have heq : k+1-(oddCount n k+1) = k-oddCount n k := by omega
      rw [heq]
      calc
        3*affineNumerator n k+2^k+2^(k+1) = 3*(affineNumerator n k+2^k) := by
          rw [Nat.pow_succ]
          omega
        _ ≤ 3*(3^(oddCount n k)*2^(k-oddCount n k)) := Nat.mul_le_mul_left 3 ih
        _ = 3^(oddCount n k+1)*2^(k-oddCount n k) := by
          simp [Nat.pow_succ, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]

theorem integer_affine_envelope (n k : Nat) :
    2^k * (iterate shortcut k n + 1) ≤
      3^(oddCount n k) * (n + 2^(k-oddCount n k)) := by
  have h := affine_numerator_envelope n k
  rw [Nat.mul_add, Nat.mul_one, scaled_affine_exact, Nat.mul_add]
  omega

theorem shell_integer_affine_envelope (n k : Nat) (hn : n<2^(k+1)) :
    2^k * (iterate shortcut k n+1) ≤
      3^(oddCount n k) * (2^(k+1)-1+2^(k-oddCount n k)) := by
  have hs : n≤2^(k+1)-1 := by omega
  exact Nat.le_trans (integer_affine_envelope n k)
    (Nat.mul_le_mul_left _ (Nat.add_le_add_right hs _))

/-- The literal integer envelope in ND-080, retaining the floor and final -1. -/
def shellEnvelope (k s : Nat) : Nat :=
  (3^s * (2^(k+1)-1+2^(k-s))) / 2^k - 1

theorem shell_endpoint_bound (n k : Nat) (hn : n<2^(k+1)) :
    iterate shortcut k n ≤ shellEnvelope k (oddCount n k) := by
  have h := shell_integer_affine_envelope n k hn
  have hp : 0 < 2^k := Nat.two_pow_pos k
  have hdiv : iterate shortcut k n+1 ≤
      (3^(oddCount n k)*(2^(k+1)-1+2^(k-oddCount n k))) / 2^k := by
    apply (Nat.le_div_iff_mul_le hp).2
    simpa [Nat.mul_comm] using h
  unfold shellEnvelope
  omega

/-- A timeout is the failure to enter the closed target at every time,
including time zero and the prescribed terminal time. -/
def Timeout (n Y k : Nat) : Prop :=
  ∀ j, j≤k → Y < iterate shortcut j n

theorem timeout_implies_envelope_cut (n q k : Nat)
    (hn : n<2^(k+1)) (ht : Timeout n (2^q) k) :
    2^q < shellEnvelope k (oddCount n k) := by
  exact Nat.lt_of_lt_of_le (ht k (Nat.le_refl k)) (shell_endpoint_bound n k hn)


/-- Adding an even offset preserves parity and changes one shortcut step
by the actual branch multiplier. -/
theorem shortcut_even_shift (n d : Nat) :
    shortcut (n+2*d) = shortcut n + 3^(n%2)*d := by
  have hp : (n+2*d)%2=n%2 := by omega
  have hn := Nat.mod_lt n (by decide : 0<2)
  by_cases he : n%2=0
  · simp only [shortcut, hp, he, if_pos, Nat.pow_zero, Nat.one_mul]
    omega
  · have ho : n%2=1 := by omega
    simp only [shortcut, hp, ho, show (1:Nat)≠0 by decide, if_false, Nat.pow_one]
    omega

/-- The full integer lift, with every intermediate state and count retained. -/
theorem shifted_orbit (n d k i : Nat) (hi : i≤k) :
    oddCount (n+2^k*d) i = oddCount n i ∧
    iterate shortcut i (n+2^k*d) =
      iterate shortcut i n + 2^(k-i)*3^(oddCount n i)*d := by
  induction i with
  | zero => simp [oddCount, iterate]
  | succ i ih =>
    obtain ⟨hc,hv⟩ := ih (by omega)
    have hexp : k-i=(k-(i+1))+1 := by omega
    let D := 2^(k-(i+1))*3^(oddCount n i)*d
    have hv' : iterate shortcut i (n+2^k*d) = iterate shortcut i n+2*D := by
      rw [hv, hexp]
      simp [D, Nat.pow_succ, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
    have hp : iterate shortcut i (n+2^k*d)%2 = iterate shortcut i n%2 := by
      rw [hv']
      omega
    constructor
    · simp only [oddCount, hc, hp]
    · simp only [iterate]
      rw [hv', shortcut_even_shift]
      simp [D, oddCount, Nat.pow_add, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]

/-- The first k parity bits encoded as a natural number, earliest bit lowest. -/
def parityCode (n : Nat) : Nat → Nat
  | 0 => 0
  | k+1 => parityCode n k + 2^k * (iterate shortcut k n % 2)

theorem parityCode_bound (n k : Nat) : parityCode n k < 2^k := by
  induction k with
  | zero => simp [parityCode]
  | succ k ih =>
    have hp := Nat.mod_lt (iterate shortcut k n) (by decide : 0<2)
    have hm : 2^k * (iterate shortcut k n%2) ≤ 2^k := by
      have h := Nat.mul_le_mul_left (2^k) (show iterate shortcut k n%2≤1 by omega)
      simpa using h
    simp only [parityCode, Nat.pow_succ]
    omega

theorem parityCode_shift (n d k i : Nat) (hi : i≤k) :
    parityCode (n+2^k*d) i = parityCode n i := by
  induction i with
  | zero => rfl
  | succ i ih =>
    have hc := ih (by omega)
    have hv := (shifted_orbit n d k i (by omega)).2
    have hexp : k-i=(k-(i+1))+1 := by omega
    have heven : (2^(k-i)*3^(oddCount n i)*d)%2=0 := by
      rw [hexp, Nat.pow_succ]
      simp [Nat.mul_mod, Nat.mul_assoc]
    have hp : iterate shortcut i (n+2^k*d)%2=iterate shortcut i n%2 := by
      rw [hv, Nat.add_mod, heven]
      simp
    simp only [parityCode, hc, hp]

/-- The two next lifts preserve the prefix and have opposite next bits. -/
theorem parityCode_two_lifts (n k : Nat) :
    (parityCode n (k+1)=parityCode n k ∧
      parityCode (n+2^k) (k+1)=parityCode n k+2^k) ∨
    (parityCode n (k+1)=parityCode n k+2^k ∧
      parityCode (n+2^k) (k+1)=parityCode n k) := by
  have hc : parityCode (n+2^k) k=parityCode n k := by
    simpa using parityCode_shift n 1 k k (Nat.le_refl k)
  have hv : iterate shortcut k (n+2^k)=iterate shortcut k n+3^(oddCount n k) := by
    simpa using (shifted_orbit n 1 k k (Nat.le_refl k)).2
  have hodd : ∀ s : Nat, 3^s%2=1 := by
    intro s
    induction s with
    | zero => rfl
    | succ s ih => simp [Nat.pow_succ, Nat.mul_mod, ih]
  have hthree := hodd (oddCount n k)
  have hp : iterate shortcut k (n+2^k)%2=(iterate shortcut k n%2+1)%2 := by
    rw [hv, Nat.add_mod, hthree]
  have hb := Nat.mod_lt (iterate shortcut k n) (by decide : 0<2)
  by_cases he : iterate shortcut k n%2=0
  · apply Or.inl
    simp [parityCode, hc, hp, he]
  · have ho : iterate shortcut k n%2=1 := by omega
    apply Or.inr
    simp [parityCode, hc, hp, ho]



theorem parityCode_prefix_mod (n k : Nat) :
    parityCode n (k+1) % 2^k = parityCode n k := by
  simp [parityCode, Nat.add_mod, Nat.mul_mod,
    Nat.mod_eq_of_lt (parityCode_bound n k)]

theorem two_halves (D a : Nat) (_hD : 0<D) (ha : a<2*D) :
    ∃ r, r<D ∧ (a=r ∨ a=r+D) := by
  by_cases h : a<D
  · exact ⟨a,h,Or.inl rfl⟩
  · exact ⟨a-D, by omega, Or.inr (by omega)⟩

/-- Executable low-bit decoder. No choice or finite-cardinality principle. -/
def parityDecode : Nat → Nat → Nat
  | 0, _ => 0
  | k+1, w =>
    let v := if w<2^k then w else w-2^k
    let r := parityDecode k v
    if parityCode r (k+1)=w then r else r+2^k

theorem parityDecode_spec (k w : Nat) (hw : w<2^k) :
    parityDecode k w < 2^k ∧ parityCode (parityDecode k w) k = w := by
  induction k generalizing w with
  | zero =>
    have hz : w=0 := by simpa using hw
    subst w
    simp [parityDecode, parityCode]
  | succ k ih =>
    have hp := Nat.two_pow_pos k
    have hw' : w<2*2^k := by simpa [Nat.pow_succ, Nat.mul_comm] using hw
    let v := if w<2^k then w else w-2^k
    let r := parityDecode k v
    have hv : v<2^k := by
      dsimp [v]
      split <;> omega
    obtain ⟨hr,hc⟩ := ih v hv
    change r<2^k at hr
    change parityCode r k=v at hc
    have hword : w=v ∨ w=v+2^k := by
      dsimp [v]
      split <;> omega
    have pair := parityCode_two_lifts r k
    have hcand : parityCode r (k+1)=w ∨ parityCode (r+2^k) (k+1)=w := by
      rcases pair with ⟨h0,h1⟩ | ⟨h1,h0⟩ <;>
        rcases hword with hw0 | hw1 <;> omega
    change (if parityCode r (k+1)=w then r else r+2^k)<2^(k+1) ∧
      parityCode (if parityCode r (k+1)=w then r else r+2^k) (k+1)=w
    by_cases h : parityCode r (k+1)=w
    · simp only [h, if_pos]
      exact ⟨by rw [Nat.pow_succ]; omega,True.intro⟩
    · have ho : parityCode (r+2^k) (k+1)=w := by omega
      simp only [h, if_false]
      exact ⟨by rw [Nat.pow_succ]; omega,ho⟩

theorem parityCode_injective (k a b : Nat) (ha : a<2^k) (hb : b<2^k)
    (hcode : parityCode a k=parityCode b k) : a=b := by
  induction k generalizing a b with
  | zero => simp at ha hb; omega
  | succ k ih =>
    have hp := Nat.two_pow_pos k
    have ha' : a<2*2^k := by simpa [Nat.pow_succ, Nat.mul_comm] using ha
    have hb' : b<2*2^k := by simpa [Nat.pow_succ, Nat.mul_comm] using hb
    obtain ⟨ra,hra,haa⟩ := two_halves (2^k) a hp ha'
    obtain ⟨rb,hrb,hbb⟩ := two_halves (2^k) b hp hb'
    have hpa : parityCode a k=parityCode ra k := by
      rcases haa with h|h
      · rw [h]
      · rw [h]
        simpa using parityCode_shift ra 1 k k (Nat.le_refl k)
    have hpb : parityCode b k=parityCode rb k := by
      rcases hbb with h|h
      · rw [h]
      · rw [h]
        simpa using parityCode_shift rb 1 k k (Nat.le_refl k)
    have hpre := congrArg (fun x => x%2^k) hcode
    simp only [parityCode_prefix_mod, hpa, hpb] at hpre
    have hrab := ih ra rb hra hrb hpre
    subst rb
    have hdiff : parityCode ra (k+1)≠parityCode (ra+2^k) (k+1) := by
      rcases parityCode_two_lifts ra k with ⟨h0,h1⟩|⟨h1,h0⟩ <;> omega
    rcases haa with ha0|ha1 <;> rcases hbb with hb0|hb1 <;>
      simp_all only <;> omega

theorem parityDecode_code (n k : Nat) (hn : n<2^k) :
    parityDecode k (parityCode n k)=n := by
  obtain ⟨hd,hc⟩ := parityDecode_spec k (parityCode n k) (parityCode_bound n k)
  exact parityCode_injective k _ n hd hn hc



/-- Executable decoding onto the positive dyadic shell, not just residues. -/
theorem shellParityDecode_spec (k w : Nat) (hw : w<2^k) :
    2^k ≤ 2^k+parityDecode k w ∧
    2^k+parityDecode k w < 2^(k+1) ∧
    parityCode (2^k+parityDecode k w) k = w := by
  obtain ⟨hr,hc⟩ := parityDecode_spec k w hw
  have hshift := parityCode_shift (parityDecode k w) 1 k k (Nat.le_refl k)
  simp only [Nat.mul_one] at hshift
  refine ⟨by omega,by rw [Nat.pow_succ]; omega,?_⟩
  rw [Nat.add_comm, hshift, hc]

theorem shellParityDecode_code (k n : Nat) (hl : 2^k≤n) (hu : n<2^(k+1)) :
    2^k+parityDecode k (parityCode n k)=n := by
  let r := n-2^k
  have hr : r<2^k := by dsimp [r]; rw [Nat.pow_succ] at hu; omega
  have heq : n=r+2^k := by dsimp [r]; omega
  have hshift := parityCode_shift r 1 k k (Nat.le_refl k)
  simp only [Nat.mul_one] at hshift
  rw [heq, hshift, parityDecode_code r k hr]
  omega

/-- Hamming weight of the low k binary digits, with the top bit split off. -/
def bitWeight : Nat → Nat → Nat
  | 0, _ => 0
  | k+1, w => bitWeight k (w%2^k) + w/2^k

theorem bitWeight_parityCode (n k : Nat) :
    bitWeight k (parityCode n k) = oddCount n k := by
  induction k with
  | zero => rfl
  | succ k ih =>
    have hdiv : parityCode n (k+1)/2^k=iterate shortcut k n%2 := by
      rw [parityCode, Nat.add_mul_div_left _ _ (Nat.two_pow_pos k),
        Nat.div_eq_of_lt (parityCode_bound n k), Nat.zero_add]
    simp only [bitWeight, parityCode_prefix_mod, hdiv, ih, oddCount]



theorem iterate_shortcut_start (n k : Nat) :
    iterate shortcut k (shortcut n)=iterate shortcut (k+1) n := by
  exact (iterate_add shortcut k 1 n).symm

theorem parityCode_head (n k : Nat) :
    parityCode n (k+1)=n%2+2*parityCode (shortcut n) k := by
  induction k with
  | zero => simp [parityCode,iterate]
  | succ k ih =>
    have hiter := iterate_shortcut_start n k
    change parityCode n (k+1)+2^(k+1)*(iterate shortcut (k+1) n%2) =
      n%2+2*parityCode (shortcut n) (k+1)
    rw [ih, ← hiter]
    simp [parityCode, Nat.pow_succ, Nat.mul_add, Nat.mul_assoc,
      Nat.mul_comm, Nat.mul_left_comm, Nat.add_assoc]

theorem parityCode_step (n k : Nat) :
    parityCode (shortcut n) (k+1)=
      parityCode n (k+1)/2+2^k*(iterate shortcut (k+1) n%2) := by
  have hh := parityCode_head n k
  have hb := Nat.mod_lt n (by decide : 0<2)
  have hd : parityCode n (k+1)/2=parityCode (shortcut n) k := by omega
  rw [parityCode, iterate_shortcut_start, hd]

theorem parityCode_mod (n k : Nat) :
    parityCode (n%2^k) k=parityCode n k := by
  have h := parityCode_shift (n%2^k) (n/2^k) k k (Nat.le_refl k)
  rw [Nat.mod_add_div] at h
  exact h.symm


/-- The complete natural-number fibre, with its explicit residue and quotient. -/
theorem parityCode_fibre (n k w : Nat) (hw : w<2^k) :
    parityCode n k=w ↔ ∃ d, n=parityDecode k w+2^k*d := by
  constructor
  · intro h
    have heq : parityDecode k w=n%2^k := by
      rw [← h, ← parityCode_mod n k]
      exact parityDecode_code (n%2^k) k (Nat.mod_lt _ (Nat.two_pow_pos k))
    exact ⟨n/2^k, by rw [heq, Nat.mod_add_div]⟩
  · rintro ⟨d, hn⟩
    rw [hn, parityCode_shift (parityDecode k w) d k k (Nat.le_refl k)]
    exact (parityDecode_spec k w hw).2

/-- Finite sum over the literal integers 0,...,N-1. -/
def finiteSum (N : Nat) (f : Nat → Nat) : Nat :=
  match N with
  | 0 => 0
  | N+1 => finiteSum N f+f N

theorem finiteSum_ext (N : Nat) (f g : Nat → Nat)
    (h : ∀ n, n<N → f n=g n) : finiteSum N f=finiteSum N g := by
  induction N with
  | zero => rfl
  | succ N ih =>
    simp only [finiteSum]
    rw [ih (fun n hn => h n (by omega)), h N (by omega)]

theorem finiteSum_add (N : Nat) (f g : Nat → Nat) :
    finiteSum N (fun n => f n+g n)=finiteSum N f+finiteSum N g := by
  induction N with
  | zero => rfl
  | succ N ih => simp only [finiteSum, ih]; omega

theorem finiteSum_split (N K : Nat) (f : Nat → Nat) :
    finiteSum (N+K) f=finiteSum N f+finiteSum K (fun n => f (n+N)) := by
  induction K with
  | zero => simp [finiteSum]
  | succ K ih =>
    change finiteSum (N+K) f+f (N+K) =
      finiteSum N f+(finiteSum K (fun n => f (n+N))+f (K+N))
    rw [ih, Nat.add_comm K N]
    omega

/-- Exact reindexing of every natural-valued weight by the parity code. -/
theorem parity_weighted_sum (m : Nat) (f : Nat → Nat) :
    finiteSum (2^m) (fun n => f (parityCode n m))=finiteSum (2^m) f := by
  induction m generalizing f with
  | zero => simp [finiteSum, parityCode]
  | succ m ih =>
    have hpow : 2^(m+1)=2^m+2^m := by rw [Nat.pow_succ]; omega
    rw [hpow, finiteSum_split, finiteSum_split]
    rw [← finiteSum_add, ← finiteSum_add]
    calc
      finiteSum (2^m) (fun n => f (parityCode n (m+1))+
          f (parityCode (n+2^m) (m+1))) =
        finiteSum (2^m) (fun n => f (parityCode n m)+f (parityCode n m+2^m)) := by
          apply finiteSum_ext
          intro n _hn
          rcases parityCode_two_lifts n m with ⟨h0,h1⟩|⟨h1,h0⟩
          · rw [h0,h1]
          · rw [h0,h1,Nat.add_comm]
      _ = finiteSum (2^m) (fun n => f n+f (n+2^m)) :=
        ih (fun n => f n+f (n+2^m))

/-- The same reindexing uses every actual positive shell point once. -/
theorem shell_parity_weighted_sum (m : Nat) (f : Nat → Nat) :
    finiteSum (2^m) (fun r => f (parityCode (2^m+r) m))=finiteSum (2^m) f := by
  calc
    _ = finiteSum (2^m) (fun r => f (parityCode r m)) := by
      apply finiteSum_ext
      intro r _hr
      have h := parityCode_shift r 1 m m (Nat.le_refl m)
      simpa [Nat.mul_one, Nat.add_comm] using congrArg f h
    _ = _ := parity_weighted_sum m f

/-- Standard Pascal recursion, independent of the orbit definitions. -/
def binomial : Nat → Nat → Nat
  | 0 => fun s => if s=0 then 1 else 0
  | m+1 => fun s => match s with
    | 0 => 1
    | s+1 => binomial m s+binomial m (s+1)

def weightCount (m s : Nat) : Nat :=
  finiteSum (2^m) (fun w => if bitWeight m w=s then 1 else 0)

theorem bitWeight_low (m w : Nat) (hw : w<2^m) :
    bitWeight (m+1) w=bitWeight m w := by
  simp [bitWeight, Nat.mod_eq_of_lt hw, Nat.div_eq_of_lt hw]

theorem bitWeight_high (m w : Nat) (hw : w<2^m) :
    bitWeight (m+1) (w+2^m)=bitWeight m w+1 := by
  have hdiv : (w+2^m)/2^m=1 := by
    simpa [Nat.div_eq_of_lt hw] using Nat.add_mul_div_left w 1 (Nat.two_pow_pos m)
  simp [bitWeight, Nat.add_mod, Nat.mod_eq_of_lt hw, hdiv]

theorem binomial_zero (m : Nat) : binomial m 0=1 := by
  cases m <;> rfl

theorem indicator_succ (a b : Nat) :
    (if a+1=b+1 then 1 else 0)=(if a=b then 1 else 0) := by
  by_cases h : a=b
  · subst b
    simp
  · have h' : a+1≠b+1 := by omega
    simp only [h,h',if_false]

/-- Exact binary-weight count for all lengths, not a finite sample. -/
theorem weightCount_binomial (m s : Nat) : weightCount m s=binomial m s := by
  induction m generalizing s with
  | zero => cases s <;> rfl
  | succ m ih =>
    have hpow : 2^(m+1)=2^m+2^m := by rw [Nat.pow_succ]; omega
    unfold weightCount
    rw [hpow,finiteSum_split,← finiteSum_add]
    have heq : ∀ n, n<2^m →
        (if bitWeight (m+1) n=s then 1 else 0)+
          (if bitWeight (m+1) (n+2^m)=s then 1 else 0) =
        (if bitWeight m n=s then 1 else 0)+
          (if bitWeight m n+1=s then 1 else 0) := by
      intro n hn
      rw [bitWeight_low m n hn,bitWeight_high m n hn]
    rw [finiteSum_ext _ _ _ heq]
    cases s with
    | zero =>
      simp only [Nat.add_one_ne_zero,if_false,Nat.add_zero]
      change weightCount m 0=binomial (m+1) 0
      rw [ih,binomial_zero,binomial_zero]
    | succ s =>
      change finiteSum (2^m) (fun n =>
        (if bitWeight m n=s+1 then 1 else 0)+
        (if bitWeight m n+1=s+1 then 1 else 0))=binomial (m+1) (s+1)
      have hs : ∀ n, n<2^m →
          (if bitWeight m n=s+1 then 1 else 0)+
            (if bitWeight m n+1=s+1 then 1 else 0) =
          (if bitWeight m n=s+1 then 1 else 0)+
            (if bitWeight m n=s then 1 else 0) := by
        intro n _hn
        rw [indicator_succ]
      rw [finiteSum_ext _ _ _ hs]
      rw [finiteSum_add]
      change weightCount m (s+1)+weightCount m s=binomial (m+1) (s+1)
      rw [ih,ih,binomial,Nat.add_comm]

/-- Literal number of shell starts with s odd inputs among the first m steps. -/
def shellOddCountCard (m s : Nat) : Nat :=
  finiteSum (2^m) (fun r => if oddCount (2^m+r) m=s then 1 else 0)

theorem shellOddCountCard_binomial (m s : Nat) :
    shellOddCountCard m s=binomial m s := by
  unfold shellOddCountCard
  calc
    _ = finiteSum (2^m) (fun r =>
          if bitWeight m (parityCode (2^m+r) m)=s then 1 else 0) := by
          apply finiteSum_ext
          intro r _hr
          rw [bitWeight_parityCode]
    _ = weightCount m s :=
      shell_parity_weighted_sum m (fun w => if bitWeight m w=s then 1 else 0)
    _ = _ := weightCount_binomial m s

/-- A finite initial discrepancy costs exactly at most the initial index count.
For positive integer sets apply this to f(i),g(i) at integer i+1. -/
theorem finite_startup_count_bound (X N : Nat) (f g : Nat → Nat)
    (hf : ∀ i, f i≤1) (hfg : ∀ i, N≤i → f i≤g i) :
    finiteSum X f≤finiteSum X g+min X N := by
  induction X with
  | zero => simp [finiteSum]
  | succ X ih =>
    change finiteSum X f+f X≤finiteSum X g+g X+min (X+1) N
    by_cases h : X<N
    · rw [Nat.min_eq_left (by omega : X+1≤N)]
      rw [Nat.min_eq_left (by omega : X≤N)] at ih
      have hx := hf X
      omega
    · have hNX : N≤X := by omega
      rw [Nat.min_eq_right (by omega : N≤X+1)]
      rw [Nat.min_eq_right hNX] at ih
      have hx := hfg X hNX
      omega

#print axioms finite_startup_count_bound
#print axioms parity_weighted_sum
#print axioms shell_parity_weighted_sum
#print axioms weightCount_binomial
#print axioms shellOddCountCard_binomial

#print axioms parityCode_fibre
#print axioms parityCode_head
#print axioms parityCode_step
#print axioms parityCode_mod
#print axioms shellParityDecode_spec
#print axioms shellParityDecode_code
#print axioms bitWeight_parityCode
#print axioms parityDecode_spec
#print axioms parityCode_injective
#print axioms parityDecode_code
#print axioms shifted_orbit
#print axioms parityCode_bound
#print axioms parityCode_shift
#print axioms parityCode_two_lifts
#print axioms scaled_affine_exact
#print axioms affine_numerator_envelope
#print axioms integer_affine_envelope
#print axioms shell_integer_affine_envelope
#print axioms shell_endpoint_bound
#print axioms timeout_implies_envelope_cut

#print axioms exact_clock
#print axioms first_passage_nested
#print axioms iterate_two_pow
#print axioms dyadic_first_passage
#print axioms dyadic_completion
#print axioms prefix_cover
#print axioms first_passage_iff
#print axioms height_transfer
#print axioms shortcut_height_of_raw_height
#print axioms iterate_unique
#print axioms rank_telescope
end CollatzClockCertificate
