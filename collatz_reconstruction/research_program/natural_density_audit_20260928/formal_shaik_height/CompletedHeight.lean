import JointWitness
/-! Completed-block height, using the pinned literal Collatz maps.
Source application: Idris Ali Shaik, revision ef341084, TimeoutRun and
TimeoutOrbitCeiling. No real analytic density theorem is certified here. -/
set_option autoImplicit false
set_option maxRecDepth 1024
namespace CollatzCompletedHeight
open CollatzClockCertificate

theorem pow_positive (a k : Nat) (ha : 0<a) : 0<a^k := by
  induction k with
  | zero => simp
  | succ k ih => rw [Nat.pow_succ]; exact Nat.mul_pos ih ha

theorem shortcut_forward (n : Nat) : 2*(shortcut n+1)≤3*(n+1) := by
  unfold shortcut
  split <;> omega

theorem shortcut_backward (n : Nat) : n≤2*shortcut n := by
  unfold shortcut
  split <;> omega

theorem forward_scaled (x v : Nat) :
    2^v*(iterate shortcut v x+1)≤3^v*(x+1) := by
  induction v with
  | zero => simp [iterate]
  | succ v ih =>
    have hs := Nat.mul_le_mul_left (2^v) (shortcut_forward (iterate shortcut v x))
    have hi := Nat.mul_le_mul_left 3 ih
    calc
      2^(v+1)*(iterate shortcut (v+1) x+1)
          ≤ 3*(2^v*(iterate shortcut v x+1)) := by
            simpa [iterate, Nat.pow_succ, Nat.mul_assoc, Nat.mul_left_comm, Nat.mul_comm] using hs
      _ ≤ 3^(v+1)*(x+1) := by
            simpa [Nat.pow_succ, Nat.mul_assoc, Nat.mul_left_comm, Nat.mul_comm] using hi

theorem backward_scaled (x k : Nat) : x≤2^k*iterate shortcut k x := by
  induction k with
  | zero => simp [iterate]
  | succ k ih =>
    have hs := Nat.mul_le_mul_left (2^k) (shortcut_backward (iterate shortcut k x))
    exact Nat.le_trans ih (by simpa [iterate, Nat.pow_succ, Nat.mul_assoc] using hs)

theorem prefix_backward (x h v : Nat) (hv : v≤h) :
    iterate shortcut v x≤2^(h-v)*iterate shortcut h x := by
  have hh := backward_scaled (iterate shortcut v x) (h-v)
  rw [←iterate_add, Nat.sub_add_cancel hv] at hh
  exact hh

theorem prefix_forward_floor (x v : Nat) :
    iterate shortcut v x≤3^v*(x+1)/2^v-1 := by
  have hp := pow_positive 2 v (by decide)
  have hh : iterate shortcut v x+1≤3^v*(x+1)/2^v :=
    (Nat.le_div_iff_mul_le hp).2 (by
      simpa [Nat.mul_comm] using forward_scaled x v)
  omega

theorem two_sided_height (x h v : Nat) (hv : v≤h) :
    iterate shortcut v x≤min (3^v*(x+1)/2^v-1)
      (2^(h-v)*iterate shortcut h x) := by
  have hf := prefix_forward_floor x v
  have hb := prefix_backward x h v hv
  omega

def forward (m v : Nat) : Nat := 3^v*2^(m+1-v)-1
def backward (m q v : Nat) : Nat := 2^(m+q-v)
def maxThrough (f : Nat → Nat) : Nat → Nat
  | 0 => f 0
  | k+1 => max (maxThrough f k) (f (k+1))
def budget (m q : Nat) : Nat := maxThrough (fun v => min (forward m v) (backward m q v)) m

theorem le_maxThrough (f : Nat → Nat) (m v : Nat) (hv : v≤m) :
    f v≤maxThrough f m := by
  induction m with
  | zero =>
    have : v=0 := by omega
    subst v
    exact Nat.le_refl _
  | succ m ih =>
    by_cases hh : v≤m
    · have := ih hh
      change f v≤max (maxThrough f m) (f (m+1))
      omega
    · have : v=m+1 := by omega
      subst v
      change f (m+1)≤max (maxThrough f m) (f (m+1))
      omega

theorem maxThrough_le (f : Nat → Nat) (m b : Nat)
    (hb : ∀ v, v≤m → f v≤b) : maxThrough f m≤b := by
  induction m with
  | zero => exact hb 0 (by omega)
  | succ m ih =>
    have hh := ih (fun v hv => hb v (by omega))
    have hl := hb (m+1) (by omega)
    change max (maxThrough f m) (f (m+1))≤b
    omega

theorem forward_weight (m v : Nat) (hv : v≤m) :
    2^v*(forward m v+1)=3^v*2^(m+1) := by
  have hp := Nat.mul_pos (pow_positive 3 v (by decide))
    (pow_positive 2 (m+1-v) (by decide))
  unfold forward
  rw [Nat.sub_add_cancel (by omega : 1≤3^v*2^(m+1-v))]
  calc
    2^v*(3^v*2^(m+1-v))=3^v*(2^v*2^(m+1-v)) := by
      simp [Nat.mul_assoc, Nat.mul_left_comm, Nat.mul_comm]
    _=3^v*2^(v+(m+1-v)) := by rw [Nat.pow_add]
    _=3^v*2^(m+1) := by congr 2; omega

theorem shell_forward (x m v : Nat) (hx : x<2^(m+1)) (hv : v≤m) :
    iterate shortcut v x≤forward m v := by
  have hs := forward_scaled x v
  have hx' := Nat.mul_le_mul_left (3^v) (show x+1≤2^(m+1) by omega)
  have hle := Nat.le_trans hs hx'
  rw [←forward_weight m v hv] at hle
  have hh := Nat.le_of_mul_le_mul_left hle (pow_positive 2 v (by decide))
  omega

theorem shell_backward (x h m q v : Nat) (hv : v≤h) (hh : h≤m)
    (hy : iterate shortcut h x≤2^q) :
    iterate shortcut v x≤backward m q v := by
  have hs := prefix_backward x h v hv
  have hy' := Nat.mul_le_mul_left (2^(h-v)) hy
  have hp : 2^(h-v)*2^q≤2^(m+q-v) := by
    rw [←Nat.pow_add]
    exact Nat.pow_le_pow_right (by decide) (by omega)
  exact Nat.le_trans hs (Nat.le_trans hy' hp)

theorem completed_block_height (x h m q v : Nat)
    (hx : x<2^(m+1)) (hh : h≤m) (hy : iterate shortcut h x≤2^q) (hv : v≤h) :
    iterate shortcut v x≤budget m q := by
  have hf := shell_forward x m v hx (by omega)
  have hb := shell_backward x h m q v hv hh hy
  have hm := le_maxThrough (fun w => min (forward m w) (backward m q w)) m v (by omega)
  change min (forward m v) (backward m q v)≤budget m q at hm
  omega

theorem forward_step (m v : Nat) (hv : v<m) : forward m v≤forward m (v+1) := by
  have e : m+1-v=(m+1-(v+1))+1 := by omega
  have rel : 2*(3^(v+1)*2^(m+1-(v+1)))=3*(3^v*2^(m+1-v)) := by
    rw [e, Nat.pow_succ, Nat.pow_succ]
    simp [Nat.mul_assoc, Nat.mul_left_comm, Nat.mul_comm]
  unfold forward
  omega

theorem mono_from_steps (f : Nat → Nat) (m : Nat)
    (hs : ∀ i, i<m → f i≤f (i+1)) :
    ∀ b, b≤m → ∀ a, a≤b → f a≤f b := by
  intro b
  induction b with
  | zero =>
    intro hb a ha
    have : a=0 := by omega
    subst a
    exact Nat.le_refl _
  | succ b ih =>
    intro hb a ha
    by_cases hab : a≤b
    · exact Nat.le_trans (ih (by omega) a hab) (hs b (by omega))
    · have : a=b+1 := by omega
      subst a
      exact Nat.le_refl _

theorem forward_mono (m a b : Nat) (hab : a≤b) (hbm : b≤m) :
    forward m a≤forward m b :=
  mono_from_steps (forward m) m (forward_step m) b hbm a hab

theorem backward_anti (m q a b : Nat) (hab : a≤b) :
    backward m q b≤backward m q a := by
  unfold backward
  exact Nat.pow_le_pow_right (by decide) (by omega)

def lastGood (p : Nat → Prop) [DecidablePred p] : Nat → Nat
  | 0 => 0
  | k+1 => if p (k+1) then k+1 else lastGood p k
def crossing (m q : Nat) : Nat := lastGood (fun v => forward m v≤backward m q v) m

theorem lastGood_spec (p : Nat → Prop) [DecidablePred p] (hp : p 0) (m : Nat) :
    lastGood p m≤m ∧ p (lastGood p m) ∧ ∀ v, v≤m → p v → v≤lastGood p m := by
  induction m with
  | zero => exact ⟨Nat.le_refl _, hp, fun v hv _ => hv⟩
  | succ m ih =>
    by_cases hh : p (m+1)
    · rw [lastGood, if_pos hh]
      exact ⟨Nat.le_refl _, hh, fun v hv _ => hv⟩
    · rw [lastGood, if_neg hh]
      refine ⟨by omega, ih.2.1, ?_⟩
      intro v hv hpv
      have hm : v≤m := by
        by_cases hn : v≤m
        · exact hn
        · have he : v=m+1 := by omega
          exact False.elim (hh (he ▸ hpv))
      exact ih.2.2 v hm hpv

theorem crossing_start (m q : Nat) (hq : 1≤q) : forward m 0≤backward m q 0 := by
  have hh : 2^(m+1)≤2^(m+q) := Nat.pow_le_pow_right (by decide) (by omega)
  simp only [forward, backward, Nat.sub_zero, Nat.pow_zero, Nat.one_mul]
  exact Nat.le_trans (Nat.sub_le (2^(m+1)) 1) hh

theorem crossing_end (m q : Nat) (hq : q<m) : backward m q m<forward m m := by
  have h23 : 2^m≤3^m := Nat.pow_le_pow_left (by decide) m
  have hq' : 2^q<2^m := Nat.pow_lt_pow_of_lt (by decide) hq
  have he : m+1-m=1 := by omega
  have heq : m+q-m=q := by omega
  simp only [forward, backward, he, heq, Nat.pow_one]
  omega

theorem crossing_spec (m q : Nat) (hql : 1≤q) (hqu : q<m) :
    crossing m q<m ∧ forward m (crossing m q)≤backward m q (crossing m q) ∧
    backward m q (crossing m q+1)<forward m (crossing m q+1) := by
  have hs := lastGood_spec (fun v => forward m v≤backward m q v) (crossing_start m q hql) m
  have he := crossing_end m q hqu
  change crossing m q≤m ∧
    forward m (crossing m q)≤backward m q (crossing m q) ∧
    (∀ v, v≤m → forward m v≤backward m q v → v≤crossing m q) at hs
  have hlt : crossing m q<m := by
    have hh := hs.2.1
    by_cases hn : crossing m q<m
    · exact hn
    · have eq : crossing m q=m := by omega
      rw [eq] at hh
      omega
  refine ⟨hlt, hs.2.1, ?_⟩
  by_cases hh : forward m (crossing m q+1)≤backward m q (crossing m q+1)
  · have hc := hs.2.2 (crossing m q+1) (by omega) hh
    omega
  · omega

theorem two_candidate_budget (m q : Nat) (hql : 1≤q) (hqu : q<m) :
    budget m q=max (forward m (crossing m q)) (backward m q (crossing m q+1)) := by
  let a := crossing m q
  change budget m q=max (forward m a) (backward m q (a+1))
  have hs := crossing_spec m q hql hqu
  have ha : a<m := hs.1
  have hlo : forward m a≤backward m q a := hs.2.1
  have hhi : backward m q (a+1)≤forward m (a+1) := by
    exact Nat.le_of_lt hs.2.2
  apply Nat.le_antisymm
  · apply maxThrough_le
    intro v hv
    by_cases hva : v≤a
    · have hf := forward_mono m v a hva (by omega)
      omega
    · have hb := backward_anti m q (a+1) v (by omega)
      omega
  · have h0 := le_maxThrough (fun v => min (forward m v) (backward m q v)) m a (by omega)
    have h1 := le_maxThrough (fun v => min (forward m v) (backward m q v)) m (a+1) (by omega)
    change min (forward m a) (backward m q a)≤budget m q at h0
    change min (forward m (a+1)) (backward m q (a+1))≤budget m q at h1
    omega

theorem crossing_integer_iff (m q v : Nat) (hv : v≤m) :
    forward m v≤backward m q v ↔ 2^(m+1)*3^v-2^v≤2^(m+q) := by
  have hw := forward_weight m v hv
  have hb : 2^v*backward m q v=2^(m+q) := by
    unfold backward
    rw [←Nat.pow_add]
    congr 1
    omega
  have hp := pow_positive 2 v (by decide)
  have hw' : 2^v*forward m v+2^v=2^(m+1)*3^v := by
    simpa [Nat.mul_add, Nat.add_mul, Nat.mul_comm] using hw
  constructor
  · intro hh
    have hm := Nat.mul_le_mul_left (2^v) hh
    rw [hb] at hm
    omega
  · intro hh
    apply Nat.le_of_mul_le_mul_left (c:=2^v) _ hp
    rw [hb]
    omega

theorem crossing_greatest (m q : Nat) (hql : 1≤q) :
    crossing m q≤m ∧
    2^(m+1)*3^(crossing m q)-2^(crossing m q)≤2^(m+q) ∧
    ∀ v, v≤m → 2^(m+1)*3^v-2^v≤2^(m+q) → v≤crossing m q := by
  have hs := lastGood_spec (fun v => forward m v≤backward m q v) (crossing_start m q hql) m
  refine ⟨hs.1, (crossing_integer_iff m q _ hs.1).1 hs.2.1, ?_⟩
  intro v hv hh
  exact hs.2.2 v hv ((crossing_integer_iff m q v hv).2 hh)

theorem budget_mono (m M q Q : Nat) (hm : m≤M) (hq : q≤Q) :
    budget m q≤budget M Q := by
  apply maxThrough_le
  intro v hv
  have hp : 2^(m+1-v)≤2^(M+1-v) := Nat.pow_le_pow_right (by decide) (by omega)
  have hf : forward m v≤forward M v := by
    have hh := Nat.mul_le_mul_left (3^v) hp
    unfold forward
    omega
  have hb : backward m q v≤backward M Q v := by
    unfold backward
    exact Nat.pow_le_pow_right (by decide) (by omega)
  have hh := le_maxThrough (fun w => min (forward M w) (backward M Q w)) M v (by omega)
  change min (forward M v) (backward M Q v)≤budget M Q at hh
  omega

theorem completed_uniform_height (x h m q S v : Nat)
    (hx : x<2^(m+1)) (hh : h≤m) (hy : iterate shortcut h x≤2^q)
    (hm : m<S) (hq : q<m) (hv : v≤h) :
    iterate shortcut v x≤budget (S-1) (S-2) :=
  Nat.le_trans (completed_block_height x h m q v hx hh hy hv)
    (budget_mono m (S-1) q (S-2) (by omega) (by omega))

theorem completed_raw_height (x h m q : Nat)
    (hx : x<2^(m+1)) (hh : h≤m) (hy : iterate shortcut h x≤2^q) :
    ∀ j, j≤clock x h → iterate raw j x≤2*budget m q :=
  height_transfer x h (budget m q) (fun v hv => completed_block_height x h m q v hx hh hy hv)

theorem completed_raw_endpoint (x h : Nat) :
    iterate raw (h+oddCount x h) x=iterate shortcut h x := exact_clock x h

end CollatzCompletedHeight

#print axioms CollatzCompletedHeight.pow_positive
#print axioms CollatzCompletedHeight.shortcut_forward
#print axioms CollatzCompletedHeight.shortcut_backward
#print axioms CollatzCompletedHeight.forward_scaled
#print axioms CollatzCompletedHeight.backward_scaled
#print axioms CollatzCompletedHeight.prefix_backward
#print axioms CollatzCompletedHeight.prefix_forward_floor
#print axioms CollatzCompletedHeight.two_sided_height
#print axioms CollatzCompletedHeight.le_maxThrough
#print axioms CollatzCompletedHeight.maxThrough_le
#print axioms CollatzCompletedHeight.forward_weight
#print axioms CollatzCompletedHeight.shell_forward
#print axioms CollatzCompletedHeight.shell_backward
#print axioms CollatzCompletedHeight.completed_block_height
#print axioms CollatzCompletedHeight.forward_step
#print axioms CollatzCompletedHeight.mono_from_steps
#print axioms CollatzCompletedHeight.forward_mono
#print axioms CollatzCompletedHeight.backward_anti
#print axioms CollatzCompletedHeight.lastGood_spec
#print axioms CollatzCompletedHeight.crossing_start
#print axioms CollatzCompletedHeight.crossing_end
#print axioms CollatzCompletedHeight.crossing_spec
#print axioms CollatzCompletedHeight.two_candidate_budget
#print axioms CollatzCompletedHeight.crossing_integer_iff
#print axioms CollatzCompletedHeight.crossing_greatest
#print axioms CollatzCompletedHeight.budget_mono
#print axioms CollatzCompletedHeight.completed_uniform_height
#print axioms CollatzCompletedHeight.completed_raw_height
#print axioms CollatzCompletedHeight.completed_raw_endpoint
