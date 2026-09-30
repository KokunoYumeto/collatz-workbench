import ClockAndRanks

/-!
Joint actual-witness and exceptional-count transfer.
The shortcut/raw formulas and recursive iteration are imported without change
from the separately pinned ClockAndRanks certificate. All quantifiers below
range over literal natural times and positive-integer prefixes.
No real density estimate or source package is assumed to be kernel checked.
-/
set_option autoImplicit false
set_option maxRecDepth 1024
namespace CollatzJointCertificate
open CollatzClockCertificate

def TaggedWitness (n H S Y B : Nat) : Prop :=
  ∃ h, h≤H ∧ oddCount n h≤S ∧ iterate shortcut h n≤Y ∧
    ∀ j, j≤h → iterate shortcut j n≤B

def RawWitness (n H Y B : Nat) : Prop :=
  ∃ h, h≤H ∧ iterate raw h n≤Y ∧ ∀ j, j≤h → iterate raw j n≤B

instance taggedDecidable (n H S Y B : Nat) :
    Decidable (TaggedWitness n H S Y B) := by
  unfold TaggedWitness
  infer_instance

instance rawDecidable (n H Y B : Nat) :
    Decidable (RawWitness n H Y B) := by
  unfold RawWitness
  infer_instance

theorem tagged_to_raw (n H S Y B : Nat)
    (hw : TaggedWitness n H S Y B) : RawWitness n (H+S) Y (2*B) := by
  obtain ⟨h, hh, hs, hy, hb⟩ := hw
  refine ⟨clock n h, ?_, ?_, height_transfer n h B hb⟩
  · unfold clock
    omega
  · simpa only [exact_clock] using hy

/-- First passage is retained, not just some later endpoint. -/
theorem tagged_first_passage_to_raw (n H S Y B h : Nat)
    (hh : h≤H) (hs : oddCount n h≤S)
    (hp : FirstPassage shortcut n Y h)
    (hb : ∀ j, j≤h → iterate shortcut j n≤B) :
    clock n h≤H+S ∧ FirstPassage raw n Y (clock n h) ∧
      ∀ j, j≤clock n h → iterate raw j n≤2*B := by
  refine ⟨?_, (first_passage_iff n Y h).1 hp, height_transfer n h B hb⟩
  unfold clock
  omega

/-- Positive starts 1,...,X, with no zero start. -/
def missingCount (P : Nat → Prop) [DecidablePred P] (X : Nat) : Nat :=
  finiteSum X (fun i => if P (i+1) then 0 else 1)

theorem finiteSum_mono (X : Nat) (f g : Nat → Nat)
    (hfg : ∀ i, i<X → f i≤g i) : finiteSum X f≤finiteSum X g := by
  induction X with
  | zero => exact Nat.le_refl 0
  | succ X ih =>
    change finiteSum X f+f X≤finiteSum X g+g X
    exact Nat.add_le_add (ih (fun i hi => hfg i (by omega))) (hfg X (by omega))

theorem missingCount_mono (P Q : Nat → Prop) [DecidablePred P] [DecidablePred Q]
    (X : Nat) (hPQ : ∀ n, 1≤n → n≤X → P n → Q n) :
    missingCount Q X≤missingCount P X := by
  apply finiteSum_mono
  intro i hi
  by_cases hp : P (i+1)
  · have hq := hPQ (i+1) (by omega) (by omega) hp
    simp [hp, hq]
  · simp [hp]
    split <;> omega

theorem missingCount_startup (P Q : Nat → Prop)
    [DecidablePred P] [DecidablePred Q] (X N : Nat)
    (hPQ : ∀ n, N≤n → P n → Q n) :
    missingCount Q X≤missingCount P X+min X (N-1) := by
  unfold missingCount
  apply finite_startup_count_bound
  · intro i
    split <;> omega
  · intro i hi
    by_cases hp : P (i+1)
    · have hq := hPQ (i+1) (by omega) hp
      simp [hp, hq]
    · simp [hp]
      split <;> omega

theorem raw_exception_count (H S Y B : Nat → Nat) (X : Nat) :
    missingCount (fun n => RawWitness n (H n+S n) (Y n) (2*B n)) X ≤
      missingCount (fun n => TaggedWitness n (H n) (S n) (Y n) (B n)) X := by
  apply missingCount_mono
  intro n _hn _hX hw
  exact tagged_to_raw n (H n) (S n) (Y n) (B n) hw

theorem raw_exception_count_of_retained
    (P : Nat → Prop) [DecidablePred P] (H S Y B : Nat → Nat) (X N : Nat)
    (hP : ∀ n, N≤n → P n → TaggedWitness n (H n) (S n) (Y n) (B n)) :
    missingCount (fun n => RawWitness n (H n+S n) (Y n) (2*B n)) X ≤
      missingCount P X+min X (N-1) := by
  apply missingCount_startup
  intro n hn hp
  exact tagged_to_raw n (H n) (S n) (Y n) (B n) (hP n hn hp)

/-- Cost of the actual successive blocks, including zero-length blocks. -/
def blockClock (G l : Nat → Nat) (n : Nat) : Nat → Nat
  | 0 => 0
  | R+1 => blockClock G l n R+l (iterate G R n)

theorem actual_block_concat (G l : Nat → Nat)
    (hG : ∀ x, G x=iterate shortcut (l x) x) (n R : Nat) :
    iterate G R n=iterate shortcut (blockClock G l n R) n := by
  induction R with
  | zero => rfl
  | succ R ih =>
    change G (iterate G R n)=
      iterate shortcut (blockClock G l n R+l (iterate G R n)) n
    rw [hG, Nat.add_comm (blockClock G l n R), iterate_add, ← ih]

theorem zero_block_absorbs (G l : Nat → Nat) (n : Nat)
    (hG : G n=n) (hl : l n=0) (R : Nat) :
    iterate G R n=n ∧ blockClock G l n R=0 := by
  induction R with
  | zero => exact ⟨rfl,rfl⟩
  | succ R ih =>
    constructor
    · change G (iterate G R n)=n
      rw [ih.1, hG]
    · change blockClock G l n R+l (iterate G R n)=0
      rw [ih.2, ih.1, hl]

#print axioms tagged_to_raw
#print axioms tagged_first_passage_to_raw
#print axioms finiteSum_mono
#print axioms missingCount_mono
#print axioms missingCount_startup
#print axioms raw_exception_count
#print axioms raw_exception_count_of_retained
#print axioms actual_block_concat
#print axioms zero_block_absorbs
end CollatzJointCertificate
