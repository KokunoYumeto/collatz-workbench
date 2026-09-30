/-!
Finite reflection and exact integer barrier counts.
The coordinate reflection is the classical first-hit involution written
explicitly in audit.tex, lem:shaik-exact-reflection. Recursive count
comparisons are reconstructed from Idris Ali Shaik's Apache-2.0 source
Extras/Unreachable/SharpEntropyBarrier.lean at ef341084.
This standalone certificate uses only Lean Init, not Mathlib.
It does not certify the real-variable entropy or natural-density theorem.
-/
set_option autoImplicit false
set_option maxRecDepth 2048
namespace CollatzReflectionCertificate

def step (b : Bool) : Int := if b then 1 else -1

def endpoint (y : Int) : List Bool → Int
  | [] => y
  | b::w => endpoint (y + step b) w

def hit (a y : Int) : List Bool → Prop
  | [] => y = a
  | b::w => y = a ∨ hit a (y + step b) w

def flip : List Bool → List Bool
  | [] => []
  | b::w => (!b)::flip w

def reflect (a y : Int) : List Bool → List Bool
  | [] => []
  | b::w => if y = a then flip (b::w)
            else b::reflect a (y + step b) w

theorem step_flip (b : Bool) : step (!b) = -step b := by
  cases b <;> decide

theorem flip_involution (w : List Bool) : flip (flip w) = w := by
  induction w with
  | nil => rfl
  | cons b w ih => cases b <;> simp [flip, ih]

theorem flip_length (w : List Bool) : (flip w).length = w.length := by
  induction w with
  | nil => rfl
  | cons b w ih => simp [flip, ih]

theorem reflect_at_barrier (a : Int) (w : List Bool) :
    reflect a a w = flip w := by
  cases w <;> simp [reflect, flip]

theorem reflect_involution (a y : Int) (w : List Bool) :
    reflect a y (reflect a y w) = w := by
  induction w generalizing y with
  | nil => rfl
  | cons b w ih =>
    by_cases h : y = a
    · subst y
      rw [reflect_at_barrier, reflect_at_barrier, flip_involution]
    · simp only [reflect, if_neg h]
      rw [ih]

theorem reflect_length (a y : Int) (w : List Bool) :
    (reflect a y w).length = w.length := by
  induction w generalizing y with
  | nil => rfl
  | cons b w ih =>
    by_cases h : y = a
    · subst y
      rw [reflect_at_barrier, flip_length]
    · simp [reflect, h, ih]

theorem endpoint_translate (w : List Bool) (y z : Int) :
    endpoint y w - y = endpoint z w - z := by
  induction w generalizing y z with
  | nil => simp [endpoint]
  | cons b w ih =>
    have e := ih (y + step b) (z + step b)
    simp only [endpoint]
    omega

theorem endpoint_flip (w : List Bool) (y z : Int) :
    endpoint y (flip w) + endpoint z w = y + z := by
  induction w generalizing y z with
  | nil => simp [endpoint]
  | cons b w ih =>
    simp only [flip, endpoint]
    have e := ih (y + step (!b)) (z + step b)
    have s := step_flip b
    omega

theorem reflect_endpoint_of_hit (a y : Int) (w : List Bool)
    (h : hit a y w) : endpoint y (reflect a y w) = 2*a-endpoint y w := by
  induction w generalizing y with
  | nil => simp only [hit] at h; simp [endpoint, reflect, h]; omega
  | cons b w ih =>
    by_cases hy : y = a
    · subst y
      rw [reflect_at_barrier]
      have e := endpoint_flip (b::w) a a
      omega
    · have ht : hit a (y+step b) w := by
        simpa [hit, hy] using h
      simp only [reflect, if_neg hy, endpoint]
      exact ih (y+step b) ht

theorem hit_of_endpoint_gt (a y : Int) (w : List Bool)
    (hy : y ≤ a) (he : a < endpoint y w) : hit a y w := by
  induction w generalizing y with
  | nil =>
    simp only [endpoint] at he
    have hf : False := by omega
    exact False.elim hf
  | cons b w ih =>
    by_cases ha : y = a
    · exact Or.inl ha
    · apply Or.inr
      apply ih (y+step b)
      · cases b <;> simp [step] <;> omega
      · exact he

def LeftWords (a : Int) (M : Nat) :=
  {w : List Bool // w.length = M ∧ hit a 0 w ∧ endpoint 0 w < a}
def RightWords (a : Int) (M : Nat) :=
  {w : List Bool // w.length = M ∧ a < endpoint 0 w}

def toRight (a : Int) (M : Nat) (w : LeftWords a M) : RightWords a M :=
  ⟨reflect a 0 w.val, by
    constructor
    · rw [reflect_length]; exact w.property.1
    · have e := reflect_endpoint_of_hit a 0 w.val w.property.2.1
      have h := w.property.2.2
      omega⟩

def toLeft (a : Int) (ha : 0 < a) (M : Nat) (w : RightWords a M) :
    LeftWords a M :=
  ⟨reflect a 0 w.val, by
    have h := hit_of_endpoint_gt a 0 w.val (by omega) w.property.2
    have e := reflect_endpoint_of_hit a 0 w.val h
    have ih := reflect_involution a 0 w.val
    have href : hit a 0 (reflect a 0 w.val) := by
      -- First-hit presence is transported by the unchanged pre-hit prefix.
      clear e ih
      have preserve : ∀ (xs : List Bool) (y : Int),
          hit a y xs → hit a y (reflect a y xs) := by
        intro xs
        induction xs with
        | nil => intro y hx; exact hx
        | cons b xs ih =>
          intro y hx
          by_cases hy : y = a
          · subst y
            simp [reflect, flip, hit]
          · have ht : hit a (y+step b) xs := by simpa [hit, hy] using hx
            simp only [reflect, if_neg hy, hit]
            exact Or.inr (ih (y+step b) ht)
      exact preserve w.val 0 h
    refine ⟨?_, href, ?_⟩
    · rw [reflect_length]; exact w.property.1
    · have hp := w.property.2; omega⟩

theorem left_inverse (a : Int) (ha : 0<a) (M : Nat) (w : LeftWords a M) :
    toLeft a ha M (toRight a M w) = w := by
  apply Subtype.eq
  exact reflect_involution a 0 w.val

theorem right_inverse (a : Int) (ha : 0<a) (M : Nat) (w : RightWords a M) :
    toRight a M (toLeft a ha M w) = w := by
  apply Subtype.eq
  exact reflect_involution a 0 w.val

def mass : Nat → Nat | 0 => 1 | r+1 => mass r+mass r

def upperEnd (a : Int) : Nat → Int → Nat
  | 0,y => if a≤y then 1 else 0
  | r+1,y => upperEnd a r (y-1)+upperEnd a r (y+1)

def upperHit (a : Int) : Nat → Int → Nat
  | 0,y => if a≤y then 1 else 0
  | r+1,y => if a≤y then mass (r+1)
              else upperHit a r (y-1)+upperHit a r (y+1)

def twoHit (a : Int) : Nat → Int → Nat
  | 0,y => if a≤y ∨ a≤-y then 1 else 0
  | r+1,y => if a≤y ∨ a≤-y then mass (r+1)
              else twoHit a r (y-1)+twoHit a r (y+1)

def upperTail : Nat → Int → Nat
  | 0,k => if k≤0 then 1 else 0
  | r+1,k => upperTail r k + upperTail r (k-1)

def threshold (r : Nat) (a y : Int) : Int := ((r:Int)+a-y+1)/2

theorem mass_eq_pow (r : Nat) : mass r = 2^r := by
  induction r with
  | zero => rfl
  | succ r ih => simp [mass, ih, Nat.pow_succ, Nat.mul_two]

theorem endpoint_complement (a y : Int) (r : Nat) :
    upperEnd a r y + upperEnd (a+1) r (2*a-y) = mass r := by
  induction r generalizing y with
  | zero => simp only [upperEnd, mass]; split <;> split <;> omega
  | succ r ih =>
    have hm := ih (y-1)
    have hp := ih (y+1)
    have em : 2*a-(y-1) = 2*a-y+1 := by omega
    have ep : 2*a-(y+1) = 2*a-y-1 := by omega
    rw [em] at hm; rw [ep] at hp
    simp only [upperEnd, mass]
    omega

theorem upperHit_eq_mass (a y : Int) (r : Nat) (hy : a≤y) :
    upperHit a r y = mass r := by
  cases r <;> simp [upperHit, mass, hy]

theorem exact_upper_hit (a y : Int) (r : Nat) (hy : y≤a) :
    upperHit a r y = upperEnd a r y + upperEnd (a+1) r y := by
  induction r generalizing y with
  | zero => simp only [upperHit, upperEnd]; split <;> split <;> omega
  | succ r ih =>
    by_cases h : y=a
    · subst y
      have e := endpoint_complement a a (r+1)
      have ea : 2*a-a=a := by omega
      rw [ea] at e
      rw [upperHit_eq_mass a a (r+1) (by omega)]
      exact e.symm
    · have hm := ih (y-1) (by omega)
      have hp := ih (y+1) (by omega)
      simp only [upperHit, if_neg (show ¬a≤y by omega), upperEnd]
      omega

theorem upperEnd_antitone (a b y : Int) (r : Nat) (h : a≤b) :
    upperEnd b r y ≤ upperEnd a r y := by
  induction r generalizing y with
  | zero => simp only [upperEnd]; split <;> split <;> omega
  | succ r ih =>
    simp only [upperEnd]
    exact Nat.add_le_add (ih (y-1)) (ih (y+1))

theorem two_hit_union (a y : Int) (r : Nat) :
    twoHit a r y ≤ upperHit a r y + upperHit a r (-y) := by
  induction r generalizing y with
  | zero =>
    simp only [twoHit, upperHit]
    split <;> split <;> split <;> omega
  | succ r ih =>
    by_cases h : a≤y ∨ a≤-y
    · simp only [twoHit, if_pos h]
      cases h with
      | inl h => rw [upperHit_eq_mass a y (r+1) h]; omega
      | inr h => rw [upperHit_eq_mass a (-y) (r+1) h]; omega
    · have h1 : ¬a≤y := by omega
      have h2 : ¬a≤-y := by omega
      have hm := ih (y-1)
      have hp := ih (y+1)
      have em : -(y-1) = -y+1 := by omega
      have ep : -(y+1) = -y-1 := by omega
      rw [em] at hm; rw [ep] at hp
      simp only [twoHit, if_neg h, upperHit, if_neg h1, if_neg h2]
      omega

theorem endpoint_tail (a y : Int) (r : Nat) :
    upperEnd a r y = upperTail r (threshold r a y) := by
  induction r generalizing y with
  | zero =>
    simp only [upperEnd, upperTail, threshold]
    split <;> split <;> omega
  | succ r ih =>
    simp only [upperEnd, ih, upperTail]
    have em : threshold r a (y-1) = threshold (r+1) a y := by
      unfold threshold
      omega
    have ep : threshold r a (y+1) = threshold (r+1) a y - 1 := by
      unfold threshold
      omega
    rw [em, ep]

theorem exact_two_tail_identity (a : Int) (r : Nat) (ha : 0≤a) :
    upperHit a r 0 =
      upperTail r (((r:Int)+a+1)/2) + upperTail r (((r:Int)+a)/2+1) := by
  rw [exact_upper_hit a 0 r ha, endpoint_tail, endpoint_tail]
  have hp : threshold r (a+1) 0 = ((r:Int)+a)/2+1 := by
    unfold threshold
    omega
  rw [hp]
  simp [threshold]

theorem two_sided_tail_bound (a : Int) (r : Nat) (ha : 0≤a) :
    twoHit a r 0 ≤ 4*upperTail r (((r:Int)+a+1)/2) := by
  have hu := two_hit_union a 0 r
  have he := exact_upper_hit a 0 r ha
  have hm := upperEnd_antitone a (a+1) 0 r (by omega)
  have ht := endpoint_tail a 0 r
  have hzero : -(0:Int)=0 := by rfl
  rw [hzero] at hu
  simp only [threshold, Int.sub_zero] at ht
  omega


/- Literal histories: enumeration, uniqueness and predicate counts. -/
def words : Nat → List (List Bool)
  | 0 => [[]]
  | r+1 => (words r).map (false :: ·) ++ (words r).map (true :: ·)

theorem words_length (r : Nat) : (words r).length = mass r := by
  induction r with
  | zero => rfl
  | succ r ih => simp [words, mass, ih]

theorem words_mem (r : Nat) (w : List Bool) :
    w ∈ words r ↔ w.length = r := by
  induction r generalizing w with
  | zero =>
    constructor
    · intro h
      have hw : w = [] := List.mem_singleton.mp h
      rw [hw]; rfl
    · intro h
      cases w with
      | nil => exact List.mem_singleton_self []
      | cons b w => simp only [List.length_cons] at h; omega
  | succ r ih =>
    constructor
    · intro h
      cases List.mem_append.mp h with
      | inl h =>
        obtain ⟨v, hv, he⟩ := List.mem_map.mp h
        rw [← he, List.length_cons, (ih v).mp hv]
      | inr h =>
        obtain ⟨v, hv, he⟩ := List.mem_map.mp h
        rw [← he, List.length_cons, (ih v).mp hv]
    · intro h
      cases w with
      | nil => simp only [List.length_nil] at h; omega
      | cons b w =>
        have hw : w ∈ words r := (ih w).mpr (by
          simp only [List.length_cons] at h; omega)
        cases b with
        | false => exact List.mem_append_left _ (List.mem_map_of_mem (false :: ·) hw)
        | true => exact List.mem_append_right _ (List.mem_map_of_mem (true :: ·) hw)

theorem words_nodup (r : Nat) : (words r).Nodup := by
  induction r with
  | zero => simp [words]
  | succ r ih =>
    unfold words
    rw [List.Nodup, List.pairwise_append]
    constructor
    · simpa [List.pairwise_map] using ih
    constructor
    · simpa [List.pairwise_map] using ih
    · intro x hx y hy
      obtain ⟨u, _, rfl⟩ := List.mem_map.mp hx
      obtain ⟨v, _, rfl⟩ := List.mem_map.mp hy
      simp

def reaches (a y : Int) : List Bool → Bool
  | [] => decide (a≤y)
  | b::w => decide (a≤y) || reaches a (y+step b) w

def reachesTwo (a y : Int) : List Bool → Bool
  | [] => decide (a≤y ∨ a≤-y)
  | b::w => decide (a≤y ∨ a≤-y) || reachesTwo a (y+step b) w

theorem reaches_of_ge (a y : Int) (w : List Bool) (h : a≤y) :
    reaches a y w = true := by cases w <;> simp [reaches, h]

theorem reachesTwo_of_ge (a y : Int) (w : List Bool) (h : a≤y ∨ a≤-y) :
    reachesTwo a y w = true := by cases w <;> simp [reachesTwo, h]

theorem upperEnd_counts (a y : Int) (r : Nat) :
    (words r).countP (fun w => decide (a≤endpoint y w)) = upperEnd a r y := by
  induction r generalizing y with
  | zero => simp [words, upperEnd, endpoint, List.countP_singleton]
  | succ r ih =>
    simp [words, List.countP_map, Function.comp_def, endpoint, step,
      Int.sub_eq_add_neg, upperEnd, ih]

theorem upperHit_counts (a y : Int) (r : Nat) :
    (words r).countP (reaches a y) = upperHit a r y := by
  induction r generalizing y with
  | zero => simp [words, upperHit, reaches, List.countP_singleton]
  | succ r ih =>
    by_cases h : a≤y
    · have hc : (words (r+1)).countP (reaches a y) = (words (r+1)).length :=
        List.countP_eq_length.mpr (by intro w _; exact reaches_of_ge a y w h)
      rw [hc, words_length]
      simp [upperHit, h]
    · simp [words, List.countP_map, Function.comp_def, reaches, step,
        Int.sub_eq_add_neg, h, upperHit, ih]

theorem twoHit_counts (a y : Int) (r : Nat) :
    (words r).countP (reachesTwo a y) = twoHit a r y := by
  induction r generalizing y with
  | zero => simp [words, twoHit, reachesTwo, List.countP_singleton]
  | succ r ih =>
    by_cases h : a≤y ∨ a≤-y
    · have hc : (words (r+1)).countP (reachesTwo a y) = (words (r+1)).length :=
        List.countP_eq_length.mpr (by intro w _; exact reachesTwo_of_ge a y w h)
      rw [hc, words_length]
      simp [twoHit, h]
    · simp [words, List.countP_map, Function.comp_def, reachesTwo, step,
        Int.sub_eq_add_neg, h, twoHit, ih]

def ups : List Bool → Int
  | [] => 0
  | b::w => (if b then 1 else 0) + ups w

theorem endpoint_ups (y : Int) (w : List Bool) :
    endpoint y w = y + 2*ups w - (w.length:Int) := by
  induction w generalizing y with
  | nil => simp [endpoint, ups]
  | cons b w ih =>
    have h := ih (y+step b)
    cases b <;> simp [endpoint, ups, step] at * <;> omega

theorem upperTail_counts (r : Nat) (k : Int) :
    (words r).countP (fun w => decide (k≤ups w)) = upperTail r k := by
  induction r generalizing k with
  | zero => simp [words, upperTail, ups, List.countP_singleton]
  | succ r ih =>
    have he : (fun w => decide (k≤1+ups w)) =
        (fun w => decide (k-1≤ups w)) := by
      funext w
      have h : (k≤1+ups w) ↔ (k-1≤ups w) := by
        constructor <;> intro hk <;> omega
      simp only [h]
    simp only [words, List.countP_append, List.countP_map, Function.comp_def, ups]
    simp only [Bool.false_eq_true, ↓reduceIte, Int.zero_add, he]
    rw [ih, ih]
    rfl

theorem literal_two_tail_identity (a : Int) (r : Nat) (ha : 0≤a) :
    (words r).countP (reaches a 0) =
      (words r).countP (fun w => decide (((r:Int)+a+1)/2≤ups w)) +
      (words r).countP (fun w => decide (((r:Int)+a)/2+1≤ups w)) := by
  rw [upperHit_counts, upperTail_counts, upperTail_counts]
  exact exact_two_tail_identity a r ha

theorem literal_two_sided_bound (a : Int) (r : Nat) (ha : 0≤a) :
    (words r).countP (reachesTwo a 0) ≤
      4*(words r).countP (fun w => decide (((r:Int)+a+1)/2≤ups w)) := by
  rw [twoHit_counts, upperTail_counts]
  exact two_sided_tail_bound a r ha


end CollatzReflectionCertificate

#print axioms CollatzReflectionCertificate.step_flip
#print axioms CollatzReflectionCertificate.flip_involution
#print axioms CollatzReflectionCertificate.flip_length
#print axioms CollatzReflectionCertificate.reflect_at_barrier
#print axioms CollatzReflectionCertificate.reflect_involution
#print axioms CollatzReflectionCertificate.reflect_length
#print axioms CollatzReflectionCertificate.endpoint_translate
#print axioms CollatzReflectionCertificate.endpoint_flip
#print axioms CollatzReflectionCertificate.reflect_endpoint_of_hit
#print axioms CollatzReflectionCertificate.hit_of_endpoint_gt
#print axioms CollatzReflectionCertificate.left_inverse
#print axioms CollatzReflectionCertificate.right_inverse
#print axioms CollatzReflectionCertificate.mass_eq_pow
#print axioms CollatzReflectionCertificate.endpoint_complement
#print axioms CollatzReflectionCertificate.upperHit_eq_mass
#print axioms CollatzReflectionCertificate.exact_upper_hit
#print axioms CollatzReflectionCertificate.upperEnd_antitone
#print axioms CollatzReflectionCertificate.two_hit_union
#print axioms CollatzReflectionCertificate.endpoint_tail
#print axioms CollatzReflectionCertificate.exact_two_tail_identity
#print axioms CollatzReflectionCertificate.two_sided_tail_bound
#print axioms CollatzReflectionCertificate.words_length
#print axioms CollatzReflectionCertificate.words_mem
#print axioms CollatzReflectionCertificate.words_nodup
#print axioms CollatzReflectionCertificate.upperEnd_counts
#print axioms CollatzReflectionCertificate.upperHit_counts
#print axioms CollatzReflectionCertificate.twoHit_counts
#print axioms CollatzReflectionCertificate.endpoint_ups
#print axioms CollatzReflectionCertificate.upperTail_counts
#print axioms CollatzReflectionCertificate.literal_two_tail_identity
#print axioms CollatzReflectionCertificate.literal_two_sided_bound
