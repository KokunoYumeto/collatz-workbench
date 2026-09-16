# Ordered turn periods and the complete unit-excess cycle sector

14 September 2026. Continuation of `note.md`, with the same original coefficients and source checkpoint. The definitions of T, a, eta, m, A, k and the source bound s=99781 are unchanged. No inferred convergence from a budget exit is used.

## 1. Two consecutive original edges and their exact product

Take an actual positive orbit segment

\[
 x\xrightarrow{b} n\xrightarrow{1} z,\qquad b\ge2,\quad n>1.
\]

The labels are exact valuations; in particular

\[
 x=\frac{2^b n-1}{3},\qquad z=\frac{3n+1}{2}.
 \tag{T1}
\]

These formulas and the intermediate n are retained, with the original two edges and their boundary v_x-v_z. The anchored character from (P1) gives

\[
 \eta(x)\eta(n)
 =\frac{2^b(n-1)}{2^bn-4}\frac{3n-1}{3(n-1)}
 =1+\frac{12-2^b}{3\cdot2^b n-12}.
 \tag{T2}
\]

Both equalities follow by cross-multiplication of the displayed positive denominators. Formula (T2) is the value of the original character on e_x+e_n, not the replacement of the two-edge path by an unmarked edge. Its fibers retain the original b and n; (T1) recovers both endpoints. For b=2 the factor is the outgoing exponent-1 factor, since the incoming exponent-2 factor is 1. For b=3 it is

\[
 1+\frac1{6n-3}.
 \tag{T3}
\]

For b>=4 it is positive and strictly less than 1. The signs follow from 12-2^b; positivity also follows from the two positive original factors. No affine coefficient, edge or valuation has been removed.

### Theorem T. An ordered-turn refinement for every positive nontrivial cycle

Let h_3 count the original cyclic adjacent patterns (3,1), and let h_4 count patterns (b,1) with b>=4. Then

\[
 \frac{2^A}{3^m}
 \le
 \left(\frac{3s-1}{3s-3}\right)^{k-h_3-h_4}
 \left(1+\frac1{6s-3}\right)^{h_3},
 \qquad s\le\min_i x_i,
 \tag{T4}
\]

for s>=3.

**Proof.** These pairs are disjoint: the first edge of a pair has exponent at least 3, and its second has exponent 1, so an edge cannot occupy both roles. Group exactly those original edge factors. Their values are given by (T2). For b=3, (T3) decreases with the intermediate vertex and is at most its value at s; for b>=4 the product is at most 1. The remaining k-h_3-h_4 exponent-1 factors obey (P5). Every unpaired exponent at least 3 contributes a positive factor less than 1, and every exponent 2 contributes 1. Apply the original cycle period identity (P4). QED.

The projection to (m,A,k,h_3,h_4) keeps its fiber: all ordered original words with these counts and their integral, positive marked primitives. Nothing here declares every such aggregate tuple realizable. In particular, the adjacency counts cannot be inferred from the marginal exponent counts alone.

## 2. The incoming exponent at a minimum gives an exact additional bound

For a minimum n of a positive nontrivial cycle, its outgoing exponent is 1. When its incoming exponent is 3, those two edges give (T3), and hence

\[
 \frac{2^A}{3^m}
 \le
 \left(\frac{3n-1}{3n-3}\right)^{k-1}
 \left(1+\frac1{6n-3}\right).
 \tag{T5}
\]

Equivalently, retaining the original incoming factor explicitly,

\[
 \frac{2^A}{3^m}
 \le
 \left(\frac{3n-1}{3n-3}\right)^k\frac{2n-2}{2n-1}.
 \tag{T6}
\]

Equality of the two right sides is the exact multiplication identity in (T2) for b=3. Both factors in (T5) decrease for n>1, so the expression strictly decreases. For (m,A,k)=(971,1539,404), its exact integer ceiling is 274717. The verifier checks (T6) at 274717 and failure at 274718 on integers. With the incoming exponent unrestricted, the original anchored ceiling for this triple is 275227.

## 3. Prefix excess as a retained observation

For an original finite word q define

\[
 E(q)=\sum_{a\text{ in }q}\max(0,a-2).
 \tag{T7}
\]

This is an additive map from word concatenation to nonnegative integers: E(uv)=E(u)+E(v). The original ordered word remains attached; the fiber over e is exactly the set of those words whose displayed sum is e. Both exponent 1 and exponent 2 have zero contribution, but are not identified. Their original affine maps and full labels remain.

On a prefix q with E(q)<=E_0, put R=E_0-E(q). The next allowable exponents are the finite list 1<=a<=R+2. Every other next exponent satisfies a>=R+3 and exceeds the total budget. The exact source progression for this last tail is the original (C3) with B=R+3 and 4 replaced by 2^(B-1):

\[
 t=t_0+2^{B-1}v,\qquad
 t_0\equiv-\frac{3u+1}{2}(3L)^{-1}\pmod{2^{B-1}},
\]
\[
 n=r+2Ut_0+2U2^{B-1}v.
 \tag{T8}
\]

Divisibility of 3u+1+6Lt by 2^B proves this identity and its inverse v=(n-r-2Ut_0)/(2U2^(B-1)). The exact next exponent is still (C4). The finite exact-exponent children plus (T8) partition the whole original prefix source. Each permissible child has the unchanged affine descent split (C5). Every branch, including empty ones, remains recorded.

A prefix excess budget is not a cyclic-state quotient. An actual cycle can be read for one full traversal with cumulative excess increasing from 0 to E_0. It cannot be required to return that counter to 0. We use the budget only on explicitly bounded prefixes within the first traversal. The underlying original source and endpoint are connected by the same path chain as before; no acyclicity of an auxiliary counter is used to rule out a cycle.

## 4. Discharge of the full 404-rise sector

### Theorem U. No nontrivial positive cycle has at most 404 exponent-1 positions in its primitive odd-return word

**Proof.** Theorem Q has discharged at most 403. At rise budget 404, the integer inequality (Q1) bounds m by 973: the strict integer comparison at m=974 persists for every larger m. The complete period comparisons leave only (m,A)=(971,1539). The implementation recomputes these inequalities without floating-point logarithms. The original exponent equation gives E=k-403. Thus the still-unexcluded case has k=404, E=1. It contains exactly 404 ones, 566 twos, and one three, in their original order.

Let n be its actual minimum. The outgoing exponent is 1, so n=3 mod4. The incoming exponent is not 1 and is either 2 or 3. Its actual equation 2^b n=3x+1 determines n mod3: it is 1 for b=2 and 2 for b=3. Therefore the two cases have exact residue classes 7 and 11 modulo 12.

**Incoming exponent 2.** Its minimum lies in [99781,275227] by (P5), and n=7 mod12. The finite cover uses excess budget 1, allowing the original exponent-3 step once. An excess exit is either an exponent at least 4 or a second exponent 3. The full source has 14621 points. Its tree has 7267 nonempty branching nodes, and the independent replay gives

\[
 5798\text{ descents}+8823\text{ excess exits}=14621.
 \tag{T9}
\]

No allowed prefix exceeds 39 returns. Thus every exit is witnessed within the first 40 returns, strictly inside one traversal of the prescribed 971-return word. No contradiction is inferred from a second traversal.

**Incoming exponent 3.** The sharper (T5) bounds the minimum by 274717, and n=11 mod12. Starting at the retained minimum, the unique exponent 3 is the last, 971st edge of that traversal. Hence its first 970 edges must lie in {1,2}. The zero-excess cover is applied only inside that justified prefix. The full source has 14578 points, its tree has 2857 nonempty branching nodes, and independent replay gives

\[
 1168\text{ descents}+13410\text{ forbidden-prefix exits}=14578.
 \tag{T10}
\]

No allowed prefix exceeds 32 returns; every exit is therefore witnessed by return 33, before the last permissible exponent-3 position. Those exits contradict this original marked incoming-edge case. They are not declared convergence certificates.

For both cases, every node is the exact partition (C5)-(C7), (T8). Independent enumeration along the original dyadic progression verifies the terminal fibers and their disjoint complete coverage. A repeated-division interpreter verifies every original exponent and every source-to-endpoint chain. Descent contradicts a cycle minimum; an excess exit within the justified prefix contradicts the retained word counts or the specified last-edge position. All 29199 possible minima in the two cases are covered. This excludes the remaining 404 sector and proves the theorem. QED.

The common convergence certificate remains only the inherited odd-source range through 99779. The 22233 excess-exit counts in (T9)-(T10) are not additions to that range. The result is an exact exclusion of the specified cycle fiber and a workbench improvement, not a claim to exceed established published cycle bounds.

## 5. The next retained fiber and scope of the calculation

The next budget 405 still leaves m=971 and A=1539 in the executed period range. After the exclusions above, k=405 gives E=2. Its full original alphabet data have exactly two possibilities: two threes and 564 twos, or one four and 565 twos, together with the 405 ones. Their placement and the actual incoming minimum edge remain retained. Equation (T2) supplies the original pair factor for incoming four; (T8) supplies the full tail partition at every remaining budget. No exhaustion of those two fibers is claimed in this contribution.

The ordered-turn bound (T4) applies at arbitrary lengths, with arbitrary positive exponents, to every actual nontrivial positive cycle. The finite exclusions Q and U have the stated count scope. None of these assertions removes a nonperiodic component of the original graph. The source-complete nonnegative primitive required by the predecessor remains unconstructed here.
