# Exact analytic reconstruction of the affine packet sum family

Proposed proof and source crosswalk, 2026-09-04. This is an audit-only reconstruction, not a new claim-ledger admission, manuscript edit, novelty claim, or source-PDF verification.

## Result

Keep the antecedent's argument \(q\) and the definitions of \(F_m\) and \(X_m\) unchanged. Then:

| Family | Taylor radius at zero | Poles of its continuation |
| --- | --- | --- |
| \(F_1\) | \(2\) | \(2\), simple |
| \(F_m,\ m\ge2\) | \(1\) | \(1\), order \(m-1\); \(2\), order \(m\) |
| \(X_1\) | \(2\) | \(2^j,\ j\ge1\), simple |
| \(X_m,\ m\ge2\) | \(1\) | \(1\), order \(m-1\); \(2^j,\ j\ge1\), order \(m\) |

All the \(X_m\) continue constructively and meromorphically to the whole finite complex plane. There are no other finite singularities. In particular, every \(X_m\) is nonrational.

The equation
\[
 X_m(2q)-3^mX_m(q)=F_m(2q)
 \tag{1}
\]
holds formally. When its entries mean their original Taylor series, its exact common convergence domain is
\[
 |q|<1\quad(m=1),\qquad |q|<\tfrac12\quad(m\ge2).
 \tag{2}
\]
The Taylor series do not acquire extra boundary points of convergence: the obstructing summands fail the term test everywhere on the boundary circle. After continuation, (1) is a meromorphic identity; it is not an assertion that its separate Taylor series converge on a larger disc.

## 1. Original coordinates and the rational offset family

Let \(m\ge1\), \(A\ge m\), and
\[
 \Pi_{m,A}=\{(a_1,\ldots,a_m)\in\mathbb N_{>0}^m:
                    a_1+\cdots+a_m=A\}.
\]
With \(S_0=0\), \(S_j=a_1+\cdots+a_j\), write
\[
 C(p)=\sum_{j=0}^{m-1}3^{m-1-j}2^{S_j},\quad
 c(p)=\frac{C(p)}{2^A},\quad
 x_p=\frac{C(p)}{2^A-3^m}.
\]
The denominator is nonzero, since an even power of two cannot equal the odd integer \(3^m\). Put
\[
 s_{m,A}=\sum_{p\in\Pi_{m,A}}c(p),\qquad
 x_{m,A}=\sum_{p\in\Pi_{m,A}}x_p
        =\frac{s_{m,A}}{1-3^m2^{-A}},
 \tag{3}
\]
and retain the source's generating series
\[
 F_m(q)=\sum_{A\ge m}s_{m,A}q^A,\qquad
 X_m(q)=\sum_{A\ge m}x_{m,A}q^A.
\]
No quotient by cyclic rotation is taken in these sums: they count all pointed positive compositions with multiplicity.

Set
\[
 u(q)=\frac q{1-q},\qquad v(q)=\frac q{2-q}.
\]
Appending a letter gives
\(c(p,a)=(3c(p)+1)/2^a\). As the composition-count series is \(G_m(q)=u(q)^m\), summing over the last letter gives
\[
 F_1=v,\qquad F_{m+1}=v(3F_m+u^m).
 \tag{4}
\]
Induction therefore proves the finite rational expression
\[
 F_m(q)=\sum_{k=0}^{m-1}3^{m-1-k}u(q)^k v(q)^{m-k}.
 \tag{5}
\]
This proves rationality directly; no transfer theorem about other automata or other functional equations is needed.

For completeness, the source's alternate closed expression is equivalent:
\[
 F_m(q)=\frac{q^m}{2q-1}
   \left(\frac1{(1-q)^{m-1}}
             -\frac{3^m(1-q)}{(2-q)^m}\right).
 \tag{6}
\]
The apparent singularity at \(q=1/2\) in (6) is removable, not a pole:
in (5), \(u(1/2)=1\), \(v(1/2)=1/3\), so each of its \(m\) terms is \(1/3\), and
\[
 F_m(1/2)=m/3.
 \tag{7}
\]

At \(q=1\), for \(m\ge2\), only the term \(k=m-1\) in (5) has pole order \(m-1\); its leading coefficient is nonzero:
\[
 \lim_{q\to1}(1-q)^{m-1}F_m(q)=1.
 \tag{8}
\]
The remaining terms have strictly lower order. At \(q=2\), only the term \(k=0\) has order \(m\), and
\[
 \lim_{q\to2}(1-q/2)^mF_m(q)=3^{m-1}.
 \tag{9}
\]
For \(m=1\), \(F_1=v\) is regular at \(1\). Expression (5) has no other finite poles. Thus (8) and (9) prove both exact orders and the absence of possible highest-order cancellations.

## 2. Coefficient asymptotics and exact Taylor radii

For \(m\ge2\), partial fractions of (5), using (8), give a pole-at-one part
\[
 \frac1{(1-q)^{m-1}}
   +\sum_{r=1}^{m-2}\frac{b_{m,r}}{(1-q)^r},
 \tag{10}
\]
plus a pole-at-two part and a polynomial part. The sum in (10) is empty when \(m=2\). The pole-at-two part has order at most \(m\), so its \(q^A\) coefficient is \(2^{-A}\) times a polynomial in \(A\) of degree at most \(m-1\). The polynomial part affects only finitely many coefficients. Since
\[
 [q^A](1-q)^{-r}=\binom{A+r-1}{r-1},
\]
we obtain, for each fixed \(m\ge2\),
\[
 s_{m,A}\sim \frac{A^{m-2}}{(m-2)!}.
 \tag{11}
\]
Equation (3) has multiplicative correction
\((1-3^m2^{-A})^{-1}\to1\); hence
\[
 x_{m,A}\sim \frac{A^{m-2}}{(m-2)!}.
 \tag{12}
\]
The finitely many \(A\) with \(2^A<3^m\) do not affect this asymptotic. This proves that \(F_m\) and \(X_m\) have radius exactly \(1\) for \(m\ge2\).

For \(m=1\), the only word is \((A)\), so
\[
 s_{1,A}=2^{-A},\qquad
 x_{1,A}=\frac1{2^A-3},\qquad
 2^Ax_{1,A}\longrightarrow1.
 \tag{13}
\]
Both radii are exactly \(2\).

These asymptotics also settle the boundary. At a point of modulus \(1\), the terms of \(X_m\) and \(F_m\), \(m\ge2\), have magnitudes asymptotic to a nonzero constant when \(m=2\), and grow polynomially when \(m>2\). At a point of modulus \(2\), the \(m=1\) terms have magnitudes tending to \(1\) (exactly \(1\) for \(F_1\)). None tends to zero. In particular the rescaled entries \(X_m(2q)\), \(F_m(2q)\) fail the term test at every boundary point in (2).

An exact small case, independently useful for checking the source error, is
\[
 \begin{aligned}
 \sum_{a=1}^{A-1}C(a,A-a)&=2^A+3A-5,\\
 s_{2,A}&=1+(3A-5)2^{-A},\\
 x_{2,A}&=\frac{2^A+3A-5}{2^A-9}\longrightarrow1.
 \end{aligned}
 \tag{14}
\]
Thus \(X_2(2q)\) cannot be given by its defining series at \(q=3/4\).

## 3. Formal identity and its precise analytic reading

By (3),
\[
 (2^A-3^m)x_{m,A}=2^A s_{m,A}.
 \tag{15}
\]
Comparing coefficients proves (1) formally. Conversely, (15) determines every coefficient of a solution in \(q^m\mathbb C[[q]]\), since \(2^A-3^m\ne0\); hence the formal solution is unique.

Within (2), all series converge absolutely and the formal calculation is an identity of holomorphic functions. Section 2 proves that (2) is the exact domain where all the displayed original series converge. The possible cancellation of singular principal parts after analytic continuation does not alter their original Taylor radii.

The equivalent inward-dilation equation is
\[
 X_m(q)-\gamma X_m(q/2)=F_m(q),\qquad \gamma=3^m.
 \tag{16}
\]
One cannot justify continuation by the unregularized infinite sum
\(\sum_{j\ge0}\gamma^jF_m(q/2^j)\): \(F_m\) starts in degree \(m\), while
\(\gamma/2^m=(3/2)^m>1\). The low Taylor degrees must be handled explicitly.

## 4. Constructive regularized dilation sum

Choose an integer \(L\) with
\[
 2^L>\gamma=3^m.
 \tag{17}
\]
The least such \(L\) is available by exact integer comparison, so no logarithmic rounding is needed. In particular \(L>m\). Define the two explicitly known polynomials
\[
 E_{m,L}(q)=\sum_{A=m}^{L-1}s_{m,A}q^A,\qquad
 P_{m,L}(q)=\sum_{A=m}^{L-1}
       \frac{s_{m,A}}{1-\gamma2^{-A}}q^A,
 \tag{18}
\]
and the rational remainder
\[
 R_{m,L}(q)=F_m(q)-E_{m,L}(q)=O(q^L).
 \tag{19}
\]
The coefficients in (18) are rational and computable from (4) or (5). Direct comparison gives
\[
 P_{m,L}(q)-\gamma P_{m,L}(q/2)=E_{m,L}(q).
 \tag{20}
\]

Define
\[
 \boxed{\quad
 \widetilde X_m(q)=P_{m,L}(q)
       +\sum_{j=0}^{\infty}\gamma^jR_{m,L}(q/2^j).
 \quad}
 \tag{21}
\]

Here is an explicit normal-convergence estimate. The Taylor coefficients of \(R_{m,L}\) at degrees \(A\ge L\) are the positive \(s_{m,A}\). Since \(F_m\) is analytic on \(|q|<1\) for every \(m\), put
\[
 B_{m,L}=2^L R_{m,L}(1/2)>0,\qquad
 r=\gamma/2^L<1.
\]
For \(|z|\le1/2\), positivity of the Taylor coefficients implies
\[
 |R_{m,L}(z)|\le B_{m,L}|z|^L.
 \tag{22}
\]
For a compact set with \(|q|\le M\), choose \(J\) such that \(M/2^J\le1/2\). Then for every \(N\ge J\),
\[
 \sup_{|q|\le M}
 \left|\sum_{j=N}^{\infty}\gamma^jR_{m,L}(q/2^j)\right|
 \le \frac{B_{m,L}M^L r^N}{1-r}.
 \tag{23}
\]
The tail terms in this estimate are holomorphic throughout that disc. The finitely many earlier terms are rational functions. Therefore (21) is meromorphic on every finite disc, and hence on \(\mathbb C\). The only possible finite poles are scaled poles of \(F_m\), namely \(2^j\) for \(j\ge0\) when \(m\ge2\), and \(2^j\) for \(j\ge1\) when \(m=1\). These sets have no finite accumulation point.

Near zero, coefficient extraction in the normally convergent sum gives, for \(A\ge L\),
\[
 [q^A]\sum_{j\ge0}\gamma^jR_{m,L}(q/2^j)
 =s_{m,A}\sum_{j\ge0}(\gamma2^{-A})^j
 =\frac{s_{m,A}}{1-\gamma2^{-A}}.
\]
The lower coefficients are exactly (18). Thus \(\widetilde X_m\) has the original Taylor germ \(X_m\). Formula (21) is its meromorphic continuation, not a changed definition of its coefficients.

The same calculation proves independence of the chosen admissible cutoff \(L\): any two choices give meromorphic functions with the same germ and hence the same continuation. Alternatively, each extra removed monomial is restored by its convergent scalar geometric sum.

Finally, shifting the normally convergent tail in (21) gives
\[
 \widetilde X_m(q)-\gamma\widetilde X_m(q/2)
 =E_{m,L}(q)+R_{m,L}(q)=F_m(q)
\]
off the discrete pole set. This proves (16), and thus (1), globally as a meromorphic identity.

## 5. Exact poles, orders and cancellation analysis

Subtracting a polynomial does not change principal parts, so \(R_{m,L}\) and \(F_m\) have identical principal parts.

For \(m\ge2\), at \(q=1\) only the \(j=0\) summand in (21) is singular. Consequently
\[
 \lim_{q\to1}(1-q)^{m-1}\widetilde X_m(q)=1.
 \tag{24}
\]
For \(m=1\), every summand is regular at \(q=1\), and the normal convergence argument makes their sum regular there.

At \(q=2^j\) with \(j\ge1\), precisely the following summands can be singular:

- The summand indexed \(j-1\), because its argument tends to \(2\), has pole order \(m\).
- The summand indexed \(j\), because its argument tends to \(1\), has pole order \(m-1\) for \(m\ge2\), and is regular for \(m=1\).

Every other summand is regular near this point, with the infinite tail normally convergent there. The order-\(m\) contribution is therefore unique and cannot cancel. Equation (9) yields
\[
 \boxed{\quad
 \lim_{q\to2^j}(1-q/2^j)^m\widetilde X_m(q)
     =\gamma^{j-1}3^{m-1}=3^{mj-1}\ne0.
 \quad}
 \tag{25}
\]
This proves the full pole list and every asserted order. Infinite nonzero poles also prove that \(X_m\) is not rational. No claim of another transcendence property is needed.

There are genuine cancellations in the functional equation, and they can be specified completely without guessing lower Laurent coefficients. Let \(A_1(q)\) and \(A_2(q)\) denote the principal-part rational functions of \(F_m\) at \(1\) and \(2\), respectively; set \(A_1=0\) when \(m=1\). At \(q=2^j\), \(j\ge1\), the full principal part of \(\widetilde X_m\) is
\[
 \gamma^{j-1}A_2(q/2^{j-1})
       +\gamma^j A_1(q/2^j).
 \tag{26}
\]
At \(q=1\) it is \(A_1(q)\).

For (16), at \(q=2^j\), \(j\ge2\), the principal part of
\(\gamma\widetilde X_m(q/2)\) is exactly the same expression (26). Thus *every* negative Laurent coefficient cancels there, not only the leading coefficient. At \(q=2\), its contribution \(\gamma A_1(q/2)\) cancels the second term of (26), leaving exactly \(A_2(q)\). At \(q=1\), it is regular, leaving \(A_1(q)\). These are precisely the poles of \(F_m(q)\).

Equivalently, in the original equation (1), the poles at all \(q=2^j,\ j\ge1\), cancel between its two left-hand terms. The only poles of the difference are those of \(F_m(2q)\): \(q=1/2\), order \(m-1\), and \(q=1\), order \(m\), for \(m\ge2\); only \(q=1\), simple, for \(m=1\). The removable \(q=1/2\) artifact in the alternate formula for \(F_m(q)\) must not be confused with the actual pole at \(q=1/2\) of \(F_m(2q)\) when \(m\ge2\).

## 6. Recovery of the source's one-letter Lambert expansion

For \(m=1\), the minimal cutoff is \(L=2\). Here
\[
 P_{1,2}(q)=-q,\qquad
 E_{1,2}(q)=q/2,\qquad
 R_{1,2}(q)=\frac{(q/2)^2}{1-q/2}.
\]
Thus (21) becomes exactly
\[
 X_1(q)=-q+
 \sum_{j\ge0}3^j
    \frac{(q/2^{j+1})^2}{1-q/2^{j+1}}.
\]
This agrees with raw lines 438–456. Formula (25) gives its simple-pole residue at \(q=2^j\), \(j\ge1\), as
\[
 -2^j3^{j-1},
\]
again agreeing with the one-letter expansion. The general continuation is a regularized dilation-sum extension of that specific calculation, not an appeal to a general theorem about all Collatz trajectories.

## 7. Source, terminology and attribution crosswalk

The direct local source is:

- Raw export: C:/Users/LOCAL_USER/Documents/Papors/Chatnotes/more col thread/ChatGPT-Implications of Affine Formula.md, 143053 bytes, SHA-256 abb1abbb948dc140394de3d35f0efbde9b3facdf718c24b065b8d0adb951366e. Raw lines 432–475 were reread in this task. They state the one-letter meromorphic result and the general formal equation; they do not assert the erroneous general analytic disc.
- Indexed local antecedent: C:/Users/LOCAL_USER/Documents/Papors/Chatnotes/automata/V5/odd_step_collatz_orbit_packets_note.tex, 114074 bytes, SHA-256 406ef13e43ae0af68fabdbda4dd16145d313407f7d38ea22311803c7533cfec7. Lines 3101–3424 were read in full in this task. Definitions and rational recursion: 3103–3189; finite closed form: 3191–3251; two-state representation: 3305–3344; \(X_m\), formal equation and uniqueness: 3347–3424.
- The specific source defect is line 3376 in the indexed TeX, label thm:Xm-Mahler: the added general open-unit-disc assertion must be replaced by (2) when its entries mean convergent Taylor series. The formal theorem and uniqueness survive unchanged.
- This task does not inspect the controlling 61-page PDF. It does not assert that the exact same wording occurs there, or use a twelve-block collation to identify whole manifestations.
- Formulas (3)–(6), the formal relation and the one-letter Lambert expansion are reconstructed source content. The all-\(m\) radius/continuation/pole proof above is an independently checked proposed consequence of those formulas. No claim is made that these elementary analytic consequences are historically new.

There is a terminology boundary worth retaining. The source calls (1) a Mahler equation, but its substitution is \(q\mapsto2q\), a linear dilation. It is not the substitution \(z\mapsto z^\ell\) in the usual Mahler-equation theory. For example, the directly read primary article by C. Faverjon and J. Roques, *Hahn series and Mahler equations: Algorithmic aspects*, J. London Math. Soc. 110 (2024), e12945, [DOI 10.1112/jlms.12945](https://doi.org/10.1112/jlms.12945), defines that theory by the power substitutions \(y(z^{\ell^i})\), \(\ell\ge2\), at source lines 243–247 and again 425–441. Accordingly, this report uses “dilation equation” descriptively; it does not import their Hahn-series theorems or any Mahler arithmetic theorem into (1).

Exact directly read manifestation of this terminology source:

C:/Users/LOCAL_USER/Documents/arxiv_latex/library/surreal_numbers_transseries/2412.04928__Hahn series and Mahler equations Algorithmic aspects/Faverjon_Roques_HAL.tex

- Canonical unit: PUBUNIT-CD27AF1D772BF6FF33C3D1EC.
- 194040 bytes; SHA-256 9fc70f2cc6fa719a5001e45f3b68e6c0c260145b303c5374ba7c39ea99c4522c.
- Content read: 216–251, 351–356, 425–462; section structure checked.
- Only the definition, publication identity and organization are used. No full-paper coverage is claimed.

## 8. Query and verification record

The canonical index entrypoint and its two-layer contract were read before derivation. All queries used the existing local query script with --layer all --index-level canonical --json; there was no rebuild. The initial three-query output was too large and truncated, so the same three queries were repeated once with compact result fields:

| Query | Direct execution start UTC | Completion UTC | Exit | Returned research/local hits |
| --- | --- | --- | --- | --- |
| Mahler Collatz | 2026-09-04T16:33:20.9554328Z | 2026-09-04T16:33:21.0614792Z | 0 | 16 / 2 |
| Lambert Collatz | 2026-09-04T16:33:21.0734475Z | 2026-09-04T16:33:21.1676541Z | 0 | 5 / 2 |
| Mahler | 2026-09-04T16:33:21.1684673Z | 2026-09-04T16:33:21.2668510Z | 0 | 25 / 2 |

The result cap is 25 per layer, so a count of 25 is not an exhaustive match count. The exact affine antecedent appeared as PUBUNIT-CF4FD708E6C6DE523385FD85; the older local dyadic note appeared as PUBUNIT-004F3DB5D12B4A71C77EDE18. The latter was not content-read or used in this task. Research hits in the first query included Siegel and Lagarias works; those hits were not treated as proofs or newly read.

A targeted “Hahn Mahler” query ran from 2026-09-04T16:34:24.1129366Z to 2026-09-04T16:34:24.2331459Z. Its first directly observed result was PUBUNIT-CD27AF1D772BF6FF33C3D1EC with the exact primary TeX path subsequently read above. Other hits in that larger output are not admitted reading coverage.

One infrastructure discrepancy was directly detected while pinning this record:

- The entrypoint records query-script SHA-256 904f23920418086cd1a8532b406f4db4cb6a4099bfb80c9102235a57bd96b7a7.
- The live executed script, C:/Users/LOCAL_USER/Documents/Papors/Chatnotes/Zeta-Function-Foundation/scripts/query_corpus.py, instead hashes to 9120bb88b23b62d3b998fedb9e44c95f21103542e3f21eb4edfb13c4411eaf4d; its last-write timestamp is 2026-09-01T18:30:34.3968394Z.
- No cause or historical reconciliation is inferred. This task did not change either file. Directly inspected script lines 1–74, 184–226 and 231–343 confirm the selected canonical database paths, SQLite mode=ro, literal-AND query handling and canonical-only selection under the supplied flag. The discrepancy is recorded for root review; it is not silently called a matching pin or a full-index validation.
- The entrypoint file itself hashes to 0992419e4490901d1651194f63cccbecd6fdef42366160620faadcb1f3bf67c1. The current directive file was rehashed as ff8d581c649e9a393c3d5ab9722d5c49dfae65da0e392dc1a2a5dbcb5b7783c3, unchanged from its direct read.

A bounded independent symbolic check used SymPy in memory for \(m=1,\ldots,6\), with Python bytecode writes disabled. It verified the recurrence (4), equality (5)=(6), removable value \(F_m(1/2)=m/3\), coefficient (8) for \(m\ge2\), and coefficient (9). All checks passed. For \(m=2\), its partial fraction output was
\[
 F_2(q)=4-\frac1{q-1}+\frac{16}{q-2}+\frac{12}{(q-2)^2},
\]
which also yields (14). These finite symbolic checks support the algebra but do not replace the general proofs above.

Only this new Markdown audit file was written. No source, reader TeX, ledger, state, checkpoint, AGENTS, goal, remote object, Lean session or build was changed or started.

## 9. Independent review of the root's proposed reader section

After completing the independent derivation above, root asked for a read-only comparison with its new section. I read every line 1–220 of:

C:/Users/LOCAL_USER/Documents/Erdos Strauss and related/collatz_reconstruction/research_companion/chapters/05_packet_fixed_point_series.tex

The inspected file is 9289 bytes, SHA-256 0a70c4bafa06e082bef91a6349b9cf06bad33e4c42775b61a919919e0285520f.

Result: no mathematical defect found in that exact file. In particular:

- Lines 34–76 correctly derive the all-word rational recurrence, finite closed expression and bivariate formal series, and prove both pole orders without a cancellation assumption.
- Lines 80–131 correctly give the coefficientwise inverse of the dilation map. Its continuity is with respect to the usual formal-series topology; preserving order proves this for it and its inverse. The elementary polynomial upper bound and the last-letter-one lower bound establish the exact radii.
- Lines 144–208 use the same regularization as (21). Their admissible example \(L=2m\) works because \(4^m>3^m\). The absolute-convergence interchange and the compact geometric tail estimate are valid.
- Their leading coefficient \(3^{mj-1}2^{jm}\) is taken relative to \((2^j-q)^{-m}\); it agrees exactly with (25), which uses \((1-q/2^j)^{-m}\). No sign discrepancy exists: both denominators have the positive orientation \(2^j-q\), not \(q-2^j\).
- Only the \(r=j-1\) summand has order \(m\) at \(2^j\); the \(r=j\) summand has strictly lower order or is regular. Thus their noncancellation proof is complete.
- Lines 210–220 correctly distinguish meromorphic equality from Taylor convergence and recover the \(m=1\) source formula.

The present audit supplies optional strengthening/detail, not necessary repairs to that section: no convergence on the relevant boundary circles; the explicit coefficient asymptotic (12); the removable \(F_m(1/2)=m/3\) value; and the complete principal-part cancellations (26). Naming the formal topology explicitly would be a minor expository clarification, not a mathematical correction.

Root separately reports inspecting all three source witnesses for the original domain error. That is root's witness verification, not a new direct PDF read by this task. No source-witness attribution beyond my directly read indexed TeX is asserted here.

