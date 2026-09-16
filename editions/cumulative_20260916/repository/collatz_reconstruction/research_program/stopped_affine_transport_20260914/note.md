# Stopped Collatz transport on the original arithmetic lattices

## Exact restart charts, image cohomology, synchronized marks, and a completed stopping law

**Date:** 14 September 2026  
**Status:** self-contained mathematical continuation with exact-arithmetic replay; not externally reviewed.  
**Intended repository:** `KokunoYumeto/collatz-workbench`  
**Publication status:** local add-only contribution. No repository checkout, commit, branch, pull request, or CI result is asserted.

### What this contribution changes

The source problem is to continue Collatz histories without replacing an actual arithmetic output by an unmarked, uniformly sampled odd interval. The output of a prescribed word retains a power-of-three lattice step. This note constructs the original source and target lattices, their exact inverse charts, their affine image cosets, and their integral two-term complexes. It then restarts on the **actual target progression**. Neither the affine offset nor the target lattice is discarded.

The stopping observation retains every exponent until an actual universal affine descent certificate has been obtained. It retains the original first-descent index, all synchronized residue readouts, congruence incompatibility masks, and declared labels of weight zero. A full countable stopped law has an explicit finite-sample error bound, proved below; this law is not a law for the discarded post-stop history. Its relation to the full history is the explicit stopping map and its fibers.

The square-root estimate developed in Section 7 retains the translation through the invertible coordinate map `x -> x-1`. The two conjugated affine branches and the inverse coordinate map are displayed. No hypothesis about random deterministic Collatz trajectories is used.

### Source status

The author-supplied conversation contains the earlier affine-packet and full-history-cutoff statements and claimed GitHub locators. Those claims were not independently recovered from the current Collatz repository. The current GitHub pages and raw Collatz files did not return readable content in this session. A cached Zeta README was readable, but not its requested methodology section or the current Collatz handoff.

Historical records in the connected Drive were readable: the original instructions about exact morphisms, retained coefficients, and constructive continuation after an obstruction, and an older Collatz note defining the original maps. The detailed private locators are in the local intake record outside the repository patch. These historical records are not represented as the current GitHub methodology section. The Collatz, lattice, counting, and chain-map results used here are proved in this note; the standard Hurwitz special-value identity is explicitly cited in [R3]. No mathematical dependency is silently imported from the Zeta arithmetic-weight programme.

This is a self-contained continuation, not a priority claim. Stopping-time methods have a classical literature, including Terras [R1]. Tao's orbit-minimum result and its first-passage/3-adic transport formulation are a major existing reference [R2]. This note makes no claim to strengthen that result.

---

## 1. Original words, affine numerators, and legal cylinders

Write the positive odd-return map as

\[
 T(n)=\frac{3n+1}{2^{\nu _2(3n+1)}}\qquad(n\in 2\mathbb Z_{\ge0}+1).
\]

For a finite exponent word \(p=(a_1,\ldots,a_m)\), every \(a_i\ge1\), retain

\[
 A_j=\sum_{i=1}^j a_i,\quad A_0=0,\quad L_j=3^j,
 \qquad C_j=\sum_{i=1}^j3^{j-i}2^{A_{i-1}}.
 \tag{1.1}
\]

Set \(A=A_m\), \(L=L_m\), \(C=C_m\), and \(U=2^A\). Empty words have \((A,L,C)=(0,1,0)\). The formal branch is

\[
 F_p(x)=\frac{Lx+C}{U},\qquad
 F_j(x)=\frac{L_jx+C_j}{2^{A_j}}.
 \tag{1.2}
\]

### Proposition 1.1 — Literal append and composition maps

Appending an exponent \(a\) gives

\[
 (A,L,C)\longmapsto(A+a,3L,3C+2^A).
 \tag{1.3}
\]

For words \(p,v\), in chronological order,

\[
 A(pv)=A(p)+A(v),\quad L(pv)=L(v)L(p),
\]
\[
 C(pv)=L(v)C(p)+2^{A(p)}C(v),\qquad F_{pv}=F_v\circ F_p.
 \tag{1.4}
\]

**Proof.** Substituting \(F_p(x)\) into \((3x+1)/2^a\) gives
\((3Lx+3C+2^A)/2^{A+a}\). Substitution into the full map \(F_v\) gives (1.4), with its original denominator \(2^{A(p)+A(v)}\). Induction gives (1.1). ∎

The integral matrix

\[
 \mathcal M_p=\begin{pmatrix}L&C\\0&U\end{pmatrix}
 \tag{1.5}
\]

satisfies \(\mathcal M_{pv}=\mathcal M_v\mathcal M_p\). The equation

\[
 \mathcal M_p\binom n1=U\binom{F_p(n)}1
 \tag{1.6}
\]

records the denominator; it does not replace the integral matrix by its diagonal spectrum.

### Proposition 1.2 — Exact positive-integer cylinder

There is exactly one odd residue \(\rho_p\) modulo \(2^{A+1}\) whose positive representatives have first exponent word \(p\). In the explicitly selected section \(1\le\rho_p<2^{A+1}\), it is

\[
 \rho_p\equiv (2^A-C)L^{-1}\pmod {2^{A+1}}.
 \tag{1.7}
\]

All positive odd starts with that word are exactly

\[
 n=\rho_p+2^{A+1}k,\qquad k\in\mathbb Z,\quad n>0.
 \tag{1.8}
\]

For every prefix, including \(j=0\),

\[
 T^j(n)=F_j(\rho_p)+2^{A+1-A_j}L_jk.
 \tag{1.9}
\]

**Proof.** First prove cylinder uniqueness by extension, rather than infer every intermediate valuation merely from final integrality. The empty word is the odd class modulo 2. On a legal word cylinder of exponent sum \(B\), its odd terminal value, as the integer lift varies, has the form \(u+2\cdot3^j k\), with \(u\) odd. Requiring the next exponent to equal \(a\) is the congruence

\[
 3(u+2\cdot3^jk)+1\equiv 2^a\pmod {2^{a+1}}.
\]

After division of this congruence by 2, the coefficient of \(k\) is odd. There is exactly one solution for \(k\bmod 2^a\). This refines the original cylinder to one odd class modulo \(2^{B+a+1}\), and proves every intermediate exponent is exact.

For a legal final word, its odd terminal value implies
\(Ln+C\equiv2^A\pmod {2^{A+1}}\). The odd integer \(L\) is invertible modulo this power of two, so the unique class already constructed is (1.7). Its representative is odd. Formula (1.9) is direct substitution in (1.2). ∎

### Section changes are explicit

Another section \(\rho'_p=\rho_p+2^{A+1}h\) has lift \(k'=k-h\). In (1.9), the base value changes by
\(2^{A+1-A_j}L_jh\), and the lift term changes by its negative. All original values are identical. For a modulus \(M\), the mark changes by \(k'\equiv k-h\pmod M\); the integer quotient changes by the corresponding division algorithm. The section is a coordinate choice with this transition map, not a discarded arithmetic datum.

---

## 2. A stopping observation certified by the entire affine expression

For a nonempty prefix define

\[
 D_j=2^{A_j}-L_j.
\]

For every positive real \(n\), exact subtraction gives

\[
 F_j(n)<n
 \quad\Longleftrightarrow\quad D_j>0\text{ and }D_jn>C_j.
 \tag{2.1}
\]

In particular, a multiplier \(L_j/2^{A_j}<1\) alone does not decide descent. For \(p=(1,1,3)\), \((L,U,C)=(27,32,19)\): the multiplier is below one, but \(F_p(3)=100/32>3\).

Fix the literal reference value **3**. Let \(\mathcal L\) be the following prefix-free set of words:

\[
 p\in\mathcal L
 \quad\Longleftrightarrow\quad
 F_j(3)\ge3\ (0\le j<m),\qquad F_m(3)<3.
 \tag{2.2}
\]

Here \(F_j(3)\) is evaluation of the original formal affine prefix. An arbitrary prescribed word is not asserted to be an actual exponent word of the integer 3.

### Theorem 2.1 — Universal actual descent on every supported leaf

For every \(p\in\mathcal L\),

\[
 3D_m>C_m>0.
 \tag{2.3}
\]

Every actual positive odd start \(n\ge3\) in the cylinder (1.8) satisfies

\[
 0<T^m(n)<n.
 \tag{2.4}
\]

**Proof.** Equation (2.2) says \(3L+C<3U\), which is (2.3). Then \(D_mn\ge3D_m>C_m\) for every \(n\ge3\). Equation (2.1) and legality of the cylinder give (2.4). Positivity follows from the original positive numerator and denominator. ∎

This stopping time is the first **reference-certified** return, not necessarily the actual first return below the starting integer. Section 5 retains the genuine first-descent index separately.

### The history map and its fibers

Let \(\Omega=\mathbb N_{\ge1}^{\mathbb N}\). The stopping map

\[
 \sigma:\Omega\longrightarrow\mathcal L\sqcup\{\infty\}
 \tag{2.5}
\]

returns the first prefix satisfying (2.2), or \(\infty\) when no such prefix occurs. Its fiber above a finite leaf is precisely

\[
 \sigma^{-1}(p)=\{p\}\times\Omega
 \tag{2.6}
\]

under concatenation. Thus the post-stop tail is exactly the data forgotten by this map. No claim is made that the stopped observation recovers that tail.

On actual integer starts the source is the image of the actual itinerary map \(n\mapsto(a_1(n),a_2(n),\ldots)\). Its fiber is the literal intersection with (2.6), namely (1.8). The symbol \(\infty\) remains a declared symbol for the actual source as well. No probability-zero argument deletes it.

For finite \(H\ge0\), let

\[
 \mathcal L_H=\{p\in\mathcal L:A(p)\le H\}.
 \tag{2.7}
\]

The finite observer returns these leaves or an explicit **cutoff overflow** symbol. Overflow includes both later stopping and never stopping; those possibilities have not been identified.

---

## 3. Exact restart on arbitrary original arithmetic progressions

Retain the complete source chart

\[
 n(t)=a+2dt,\qquad t=b,b+1,\ldots,b+N-1,
 \tag{3.1}
\]

where \(a\) is odd, \(d,N\) are positive integers, \(b\in\mathbb Z\), and \(a+2db\ge3\). The odd factor of \(d\), its power of two, the source interval, and the offset are all part of the state.

### Theorem 3.1 — Source chart, target chart, and inverse

For a nonempty word \(p\), set

\[
 g=\gcd(d,2^A),\qquad c=(\rho_p-a)/2.
 \tag{3.2}
\]

The compatibility mask is

\[
 \kappa_p(a,d)=\mathbf1_{g\mid c}.
 \tag{3.3}
\]

An incompatible word has empty intersection with this source progression. For a compatible word set

\[
 P=2^A/g,\qquad
 s\equiv(c/g)(d/g)^{-1}\pmod P,\quad 0\le s<P,
 \tag{3.4}
\]

with \(s=0\) for \(P=1\). Then the actual source points with word \(p\) are exactly

\[
 t=s+Pv,
 \tag{3.5}
\]

and their terminal values are exactly

\[
 T^m(n(s+Pv))=u+2d'v,
 \tag{3.6}
\]

where

\[
 u=\frac{L(a+2ds)+C}{2^A}\in2\mathbb Z+1,
 \qquad d'=\frac d g L.
 \tag{3.7}
\]

The source and target parametrizations have inverse parameter maps

\[
 v=(t-s)/P,
 \qquad v=(y-u)/(2d').
 \tag{3.8}
\]

Their common parameter range is exactly

\[
 \left\lceil\frac{b-s}{P}\right\rceil
 \le v\le
 \left\lfloor\frac{b+N-1-s}{P}\right\rfloor.
 \tag{3.9}
\]

**Proof.** The original cylinder equation is
\(a+2dt\equiv\rho_p\pmod {2^{A+1}}\), or \(dt\equiv c\pmod {2^A}\). Elementary divisibility gives (3.3). Division by the recorded common factor \(g\), with that factor retained in the chart, gives the invertible coefficient \(d/g\) modulo \(P\). This proves (3.4) and (3.5). Substitution in the original numerator gives

\[
 \frac{L(a+2d(s+Pv))+C}{2^A}
 =\frac{L(a+2ds)+C}{2^A}+2\frac d g L v.
\]

The base numerator gives an odd integer by Proposition 1.2, even when the chosen section lies outside the sampled interval. Equations (3.8) are literal inverse maps on their stated fibers. Restricting \(b\le t\le b+N-1\) proves (3.9). ∎

### The commuting integral matrix diagram

Define the source and target lattice embeddings

\[
 J_p=\begin{pmatrix}2dP&a+2ds\\0&1\end{pmatrix},
 \qquad K_p=\begin{pmatrix}2d'&u\\0&1\end{pmatrix}.
\]

The exact relation is

\[
 \boxed{\mathcal M_pJ_p=2^A K_p.}
 \tag{3.10}
\]

Both columns are equal as integer vectors. The first column is the identity
\(LdP=2^Ad'\); the second is \(L(a+2ds)+C=2^Au\). Thus the diagram includes the original integral lattices and the denominator map.

### Marked restart, with every factor retained

For any positive integer \(M\) and \(0\le r<M\), write \(v=r+M\ell\). The exact restriction and target are

\[
 t=s+Pr+PM\ell,
 \qquad y=u+2d'r+2Md'\ell.
 \tag{3.11}
\]

The bounds in (3.9) become the corresponding ceiling/floor bounds on \(\ell\). This is an exact restart family with parameters

\[
 (a_{\rm new},d_{\rm new})=(u+2d'r,Md').
 \tag{3.12}
\]

The original full-support index set and the compatibility mask remain recorded even for empty sampled fibers.

### Exactly how dyadic information is consumed

Write \(s_0=\nu_2(d)\). Equation (3.7) gives

\[
 \nu_2(d')=\max\{s_0-A,0\}.
 \tag{3.13}
\]

An additional mark modulus \(M\) adds \(\nu_2(M)\) to this exponent. For odd \(d\), the unmarked target step parameter is \(d'=d3^m\), still odd. For even \(d\), the original fixed dyadic digits are consumed according to (3.13), with every incompatible branch still marked. These are exact relationships between the two source descriptions, not an assumption that conditional branches become unconditioned.

---

## 4. The arithmetic image complex and its exact localizations

The target of (3.6), in the invertible odd-index coordinate

\[
 z=(y-1)/2,\qquad y=2z+1,
 \tag{4.1}
\]

is the affine lattice

\[
 z=z_0+d'v,\qquad z_0=(u-1)/2.
 \tag{4.2}
\]

The division in (4.1) is an explicitly inverted bijection between odd integers and integers. The original value \(y\) and its step \(2d'\) are recoverable by its displayed inverse.

### Theorem 4.1 — Image cohomology with the affine coset retained

The two-term integral complex

\[
 K_{p,a,d}^{\rm image}
 =\left[\mathbb Z\xrightarrow{\;d'\;}\mathbb Z\right]
 \quad\text{in degrees }0,1
 \tag{4.3}
\]

has

\[
 H^0=0,\qquad H^1=\mathbb Z/d'\mathbb Z.
 \tag{4.4}
\]

The image progression is the distinguished affine coset

\[
 [z_0]\in H^1;
 \qquad z\text{ is in that image exactly when }[z]=[z_0].
 \tag{4.5}
\]

The order of this distinguished class is
\(d'/\gcd(d',z_0)\). A zero class still specifies a present image lattice; it does not remove the source word, the ambient group, or the source map.

**Proof.** Multiplication by the positive integer \(d'\) is injective on \(\mathbb Z\). Its cokernel is the indicated quotient. Equation (4.2) is equivalent to \(z-z_0\in d'\mathbb Z\), proving (4.5). The least positive integer \(k\) with \(d'\mid kz_0\) is \(d'/\gcd(d',z_0)\). ∎

This complex records the arithmetic image lattice. It is not declared to equal an unread workbench complex. The exact map to the source dynamics is (3.10), and the affine image condition is (4.5).

Changing the lift section by \(v'=v-h\) changes \(u\) to \(u+2d'h\) and \(z_0\) to \(z_0+d'h\). The class in (4.5) is unchanged by this displayed coordinate transition.

### Theorem 4.2 — Exact coefficient comparison and homotopy

Let \(\ell\) be a prime. Write, retaining both factors,

\[
 d'=\ell^e w,\qquad \ell\nmid w.
\]

The coefficient map \(\mathbb Z\hookrightarrow\mathbb Z_\ell\) gives the commutative square with multiplication by the same original \(d'\) on both rows. Over \(\mathbb Z_\ell\), the complex (4.3) has

\[
 H^0=0,\qquad H^1=\mathbb Z_\ell/d'\mathbb Z_\ell.
 \tag{4.6}
\]

The explicit comparison with \([\mathbb Z_\ell\xrightarrow{\ell^e}\mathbb Z_\ell]\) has degree-zero map multiplication by \(w\) and degree-one map the identity. Its inverse has degree-zero map multiplication by \(w^{-1}\) and degree-one map the identity. Both compositions are identities, and the distinguished degree-one coset is unchanged.

For \(e=0\), the complex is contractible with homotopy

\[
 h^1(x)=(d')^{-1}x.
 \tag{4.7}
\]

**Proof.** A nonzero integer acts injectively on \(\mathbb Z_\ell\), proving degree-zero vanishing. The cokernel is (4.6). The chain-map equation is \(\ell^e w=d'\). The unit inverse \(w^{-1}\) exists in \(\mathbb Z_\ell\), and gives the displayed inverse chain map. When \(e=0\), both \(d'h^1\) and \(h^1d'\) are the identity. ∎

For odd \(d\), the image complex therefore contracts over \(\mathbb Z_2\), while its original integral quotient has order \(d3^m\). At the prime 3 its quotient has order \(3^{m+\nu_3(d)}\). These statements are related by the coefficient embeddings and explicit chain maps above; they are not assertions of unrelated categories.

### Finite coefficients retain both image and kernel

For every \(N\ge1\), put \(g_N=\gcd(d',N)\). The equation

\[
 d'v=z-z_0\pmod N
 \tag{4.8}
\]

has exactly \(g_N\) solutions for \(g_N\mid z-z_0\), and zero otherwise. Its homogeneous kernel has \(g_N\) elements. The explicit connecting isomorphism is

\[
 \beta:H^0(K^{\rm image}\otimes\mathbb Z/N)
 \longrightarrow (\mathbb Z/d'\mathbb Z)[N],
 \qquad [v]\longmapsto\left[\frac{d'v}{N}\right].
 \tag{4.9}
\]

The fraction in (4.9) is an integer on its domain. Changing the lift of \(v\) by \(Nq\) changes it by \(d'q\). Injectivity follows because \(d'v/N\in d'\mathbb Z\) forces \(v\in N\mathbb Z\); both groups have \(g_N\) elements. Thus no finite-coefficient kernel is silently discarded.

### The dyadic and triadic images of a word

For the unrestricted odd cylinder \(n=\rho_p+2^{A+1}k\), write its terminal value as \(y=u+2Lk\). Over the odd 2-adic integers, the branch inverse is

\[
 n=\frac{2^Ay-C}{L}.
 \tag{4.10}
\]

The odd integer \(L\) is a 2-adic unit, so every odd 2-adic \(y\) has this inverse, lying in the original cylinder. On ordinary integers the same inverse is integral precisely when

\[
 2^Ay\equiv C\pmod {3^m};
 \tag{4.11}
\]

with the required positivity and source bound imposed literally. Consequently the square formed by the integer embeddings into \(\mathbb Z_2\), the branch map, and (4.10) commutes. Its integer target is the affine lattice described by (4.11), whose step is \(2\cdot3^m\). This is the exact arithmetic information lost by replacing the integer target with all odd integers.

### Worked image defect

For \(p=(1,1,3,2)\),

\[
 (A,L,C,\rho_p)=(7,81,89,247),
\]
\[
 247+256k\longmapsto157+162k.
 \tag{4.12}
\]

In the target coordinate (4.1), this is

\[
 z=78+81k.
\]

Thus the image complex has differential 81, \(H^1=\mathbb Z/81\mathbb Z\), and distinguished coset \([78]\), of order 27. Over \(\mathbb Z_2\), the homotopy is multiplication by \(81^{-1}\). The original integral lattice and class remain recorded alongside that contraction. The identity (4.12), not the 2-adic contraction alone, is the restart input.

---

## 5. Exact synchronized residues and the genuine first descent

Fix a compatible source chart from Section 3. Let \(n_*=a+2ds\). For a prefix of length \(j\), substitution gives

\[
 T^j(n(s+Pv))
 =F_j(n_*)+2^{A+1-A_j}\frac d g L_jv.
 \tag{5.1}
\]

Every displayed base and coefficient is integral. The coefficient follows from \(2dP/2^{A_j}\), and the base is integral by cylinder legality.

For every modulus \(M\), the mark \(r=v\bmod M\) therefore determines, jointly,

\[
 \left(n\bmod M,T(n)\bmod M,\ldots,T^m(n)\bmod M\right)
 \tag{5.2}
\]

by the explicit readout (5.1). This assertion includes even \(M\), powers of 3, and mixed moduli. No coprimality between \(M\) and the displayed coefficients is needed. Repeated or constant readouts are retained as such.

### The first-descent cells

For \(D_j>0\), define the exact source-index threshold

\[
 \theta_j=\frac{C_j/D_j-a}{2d}.
 \tag{5.3}
\]

The source starts with actual first descent at \(j\) lie in

\[
 E_j(p)=\left(\theta_j,\ \min_{i<j,\,D_i>0}\theta_i\right],
 \tag{5.4}
\]

with upper endpoint \(+\infty\) when there is no preceding positive \(D_i\). Set \(E_j=\varnothing\) for \(D_j\le0\), or when the lower endpoint is at least the upper endpoint. Each declared index \(j=1,\ldots,m\) is retained even for an empty cell.

**Proof.** By (2.1), actual descent at \(j\) is equivalent to \(D_j>0\) and \(t>\theta_j\). Absence of descent at each earlier index with \(D_i>0\) is \(t\le\theta_i\); earlier nonpositive \(D_i\) never produce positive-source descent. Intersecting these exact inequalities gives (5.4). ∎

For \(p\in\mathcal L\), these cells partition every real source value \(t\) with \(n(t)\ge3\), because the terminal certificate guarantees at least one descent. Their boundaries keep the strict/non-strict distinction: equality at a threshold is not strict descent.

### The joint observation and its complete fiber

For a source integer that stops at \(p\), define

\[
 \pi(n)=(p,r,J),\qquad r=v\bmod M,
 \tag{5.5}
\]

where \(J\) is its actual first descent index. The exact fiber is

\[
 \left\{a+2d(s+Pr+PM\ell):\ell\in\mathbb Z,\ 
 b\le s+Pr+PM\ell<b+N,\ 
 s+Pr+PM\ell\in E_J(p)\right\}.
 \tag{5.6}
\]

Equation (5.6) supplies an inverse parametrization of the fiber, not merely its cardinality. Together, (5.1) and (5.6) recover the synchronized residue vector, the genuine first descent, and the target restart lattice. Forgetting \(r\), \(J\), or a selected residue readout is a specified projection with fibers obtained by union over exactly the forgotten labels.

### Example: reference stopping and actual first descent both retained

For the source \(247\), the word \((1,1,3,2)\) gives

\[
 247\to371\to557\to209\to157.
\]

The actual first descent is \(J=3\). The reference values at 3 are

\[
 3\to5\to8\to25/8\to83/32.
\]

The reference certificate first occurs at \(m=4\). At prefix 3, \(D_3=5\) and \(C_3=19\), so the exact actual descent threshold is \(19/5\). The source 247 exceeds it; the reference 3 does not. Both indices and their map (5.4) are retained.

---

## 6. Exact counts, including empty labels and overflow

For each declared label \(\lambda=(p,r,j)\), let \(c_\lambda\) be the number of points in (5.6). This is computed by integer ceiling and floor operations on that original progression and its exact open/closed interval. Explicitly, for a compatible chart let

\[
 o=s+Pr,\qquad h=PM,
\]

and write \(E_j=(\theta_j,\eta_j]\). Put

\[
 l=\max\{b,\lfloor\theta_j\rfloor+1\},\qquad
 u=\min\{b+N-1,\lfloor\eta_j\rfloor\},
\]

where an infinite upper endpoint contributes no extra restriction. For \(l\le u\),

\[
 c_\lambda=
 \max\left\{0,\left\lfloor\frac{u-o}{h}\right\rfloor
             -\left\lceil\frac{l-o}{h}\right\rceil+1\right\}.
 \tag{6.1}
\]

Otherwise the count is zero. An incompatible chart or empty first-descent cell also has count zero, with its reason separately recorded. These labels are not removed from the declared target set.

Define the comparison weight on the **same threshold interval** by

\[
 q_\lambda=
 \frac{|[b,b+N)\cap E_j(p)|}{NMP}
 \tag{6.2}
\]

for compatible charts, and zero for incompatible charts. The length in (6.2) is ordinary interval length in the original source parameter \(t\). This is an explicitly defined lattice-density comparison. It depends on the source interval when the first-descent mark is included. It is not an assumption of independence between residue marks and actual deterministic descent.

### Proposition 6.1 — Exact cell discrepancy

For every declared finite leaf label,

\[
 \left|\frac{c_\lambda}{N}-q_\lambda\right|\le\frac1N.
 \tag{6.3}
\]

For a fixed compatible leaf, \(\sum_{r,j}q_{p,r,j}=1/P\).

**Proof.** Intersecting (5.6) with the source range gives one interval, possibly empty and with its specified endpoint conventions. The number of points of \(o+h\mathbb Z\) in any such bounded interval differs from its length divided by \(h\) by at most one. This follows directly from the two endpoint floor/ceiling formulas, including the cases in which endpoints themselves are lattice points. Division by \(N\) gives (6.3). The first-descent intervals partition the source real interval; their lengths sum to \(N\). Summing over \(M\) marks in (6.2) gives \(1/P\). ∎

The reference mass of a compatible unmarked leaf is therefore

\[
 \mu_{a,d}(p)=\frac1P=\frac{g}{2^A},
 \qquad
 \mu_{a,d}(p)=0\text{ for an incompatible leaf}.
 \tag{6.4}
\]

For odd \(d\), \(g=1\), every leaf is compatible, and this is exactly \(2^{-A}\). For even \(d\), equation (6.4), rather than the unconditioned weight, is retained.

At cutoff \(H\), set

\[
 t_H^{a,d}=1-\sum_{p\in\mathcal L_H}\mu_{a,d}(p).
 \tag{6.5}
\]

The actual overflow count is
\(N-\sum_{p\in\mathcal L_H,r,j}c_{p,r,j}\). Both overflow labels are included, even at value zero. The next two sections prove that (6.5) is nonnegative, tends to zero, and bounds the full countable comparison law.

---

## 7. A retained-translation square-root estimate and the complete-word tail

This section constructs the reference probability space and proves its tail bound. Nothing in this construction assigns independent random exponents to one fixed integer trajectory.

### 7.1 Literal binary factorization and its cylinder law

Define the half-step affine maps

\[
 f_0(x)=x/2,\qquad f_1(x)=(3x+1)/2.
 \tag{7.1}
\]

The original odd branch is exactly

\[
 g_a=f_0^{a-1}\circ f_1.
 \tag{7.2}
\]

A word \((a_1,\ldots,a_m)\) corresponds to the binary input string

\[
 1\,0^{a_1-1}\,1\,0^{a_2-1}\cdots1\,0^{a_m-1},
\]

followed by the next odd input bit 1. It uses \(A\) executed half-steps and \(A+1\) known input bits. Its initial bit is fixed to 1.

For completeness, parity-prefix lifting gives one odd residue modulo \(2^h\) for every prescribed binary input prefix of length \(h\) with initial bit 1. Indeed the affine output after \(h\) half-steps has odd numerator slope \(3^j\) and denominator \(2^h\). The two lifts of a legal input class modulo \(2^{h+1}\) change that output by the odd integer \(3^j\), so they realize the two possible next parities exactly once. Induction proves the assertion.

Consequently uniform odd residues give probability \(2^{-(h-1)}\) to each such length-\(h\) prefix. These consistent finite laws are the fair binary product law after the forced initial odd bit. By (7.2), its exponent-word cylinder probabilities are exactly

\[
 \mu(p)=2^{-A(p)}=\prod_{i=1}^m2^{-a_i}.
 \tag{7.3}
\]

### 7.2 Exact coordinate morphism for the potential

Use the bijection

\[
 \phi:x\longmapsto z=x-1,\qquad\phi^{-1}(z)=z+1.
 \tag{7.4}
\]

The conjugated maps, retaining their translations, are

\[
 \phi f_0\phi^{-1}(z)=\frac{z-1}{2},\qquad
 \phi f_1\phi^{-1}(z)=\frac{3z+2}{2}.
 \tag{7.5}
\]

The potential is \(V(x)=\sqrt{x-1}\) on \(x\ge3\). The source domain becomes \(z\ge2\); it is not changed to a different positivity chamber.

### Theorem 7.1 — Exact square-root contraction

For every real \(x\ge3\),

\[
 \frac{\sqrt{f_0(x)-1}+\sqrt{f_1(x)-1}}2
 \le\frac{\sqrt{15}}4\sqrt{x-1}.
 \tag{7.6}
\]

Equality holds at \(x=7\). In particular, the same bound holds for the killed expectation in which branches with new value below 3 contribute zero.

**Proof.** Put

\[
 A_x=f_0(x)-1=(x-2)/2,\qquad
 B_x=f_1(x)-1=(3x-1)/2.
\]

Both are positive on the stated domain, and the original translations give the exact identity

\[
 2A_x+B_x=\frac52(x-1).
 \tag{7.7}
\]

The Cauchy–Schwarz inequality, with its displayed weights, gives

\[
 (\sqrt{A_x}+\sqrt{B_x})^2
 \le(1/2+1)(2A_x+B_x)=\frac{15}{4}(x-1).
\]

Division by 4 and taking nonnegative square roots gives (7.6). Its equality condition \(B_x=4A_x\) is exactly \(x=7\). An entirely polynomial certificate is

\[
 R=\frac{15}{4}(x-1)-A_x-B_x=\frac{7x-9}{4}>0,
 \qquad R^2-4A_xB_x=\frac{(x-7)^2}{16}.
 \tag{7.8}
\]

Removing positive contributions from branches killed below 3 preserves the bound. ∎

### 7.3 Survival of the binary reference process

Apply (7.1) to the literal reference \(X_0=3\), with the first bit forced odd and subsequent bits fair. Let

\[
 \tau=\inf\{h\ge1:X_h<3\},\qquad S_h=\Pr(\tau>h).
\]

Before killing, \(V(X_h)\ge\sqrt2\). The forced first step gives \(X_1=5\), \(V(X_1)=2\). Iterating the killed estimate gives, for \(h\ge1\),

\[
 S_h\le\sqrt2\left(\frac{\sqrt{15}}4\right)^{h-1}.
 \tag{7.9}
\]

The entirely rational constants used by the checker are

\[
 \rho=\frac{31}{32},\qquad C_0=\frac32.
 \tag{7.10}
\]

They satisfy
\(15/16<\rho^2\) and \(2<(C_0\rho)^2\). Thus, including \(h=0\),

\[
 S_h\le C_0\rho^h.
 \tag{7.11}
\]

This proves \(\Pr(\tau=\infty)=0\) in the specified binary reference probability space.

### 7.4 Completion to the original odd-return word

The first crossing below 3 occurs on an even half-step: \(f_1(x)>x\) for \(x\ge3\). After that crossing, finish the remaining even run before the next odd input. Let \(R\) be the number of additional zero input bits. The completed original exponent word has sum

\[
 A_{\rm stop}=\tau+R.
 \tag{7.12}
\]

For every finite stopping prefix, the unused bits are fair, and

\[
 \Pr(R=r\mid\text{that prefix})=2^{-r-1},\qquad r\ge0.
 \tag{7.13}
\]

This follows by counting the specified next \(r\) zeros and the following 1. It proves independence from the stopping prefix directly on the original binary cylinders. Earlier completed odd returns were at least 3; the completed return in (7.12) is below 3. Thus its leaf is exactly the one in (2.2).

Let

\[
 t_H=\Pr(A_{\rm stop}>H)=1-\sum_{p\in\mathcal L_H}2^{-A(p)}.
\]

Then \(t_0=1\), and

\[
 t_H=\frac{t_{H-1}+S_H}{2}\qquad(H\ge1).
 \tag{7.14}
\]

**Proof.** Decompose by \(\tau\). For a crossing at \(\tau\le H\), equation (7.13) gives
\(\Pr(R>H-\tau)=2^{-(H-\tau+1)}\); crossings after \(H\) have total mass \(S_H\). Subtracting the expressions at \(H\) and \(H-1\), and using \(\Pr(\tau=H)=S_{H-1}-S_H\), gives (7.14). ∎

Since

\[
 K=\frac{31}{20},\qquad K(2\rho-1)=C_0\rho,
\]

induction in (7.14) proves

\[
 \boxed{t_H\le K\rho^H.}
 \tag{7.15}
\]

In particular, the leaf masses sum to one. All complete exponents, rather than a prematurely cut even run, are retained.

### 7.5 Exact leaf count and a quantitative growth bound

The number of binary prefixes first killed at length \(h\) is

\[
 b_h=2^{h-1}(S_{h-1}-S_h).
\]

Each gives exactly one completed odd leaf for each additional even-run length \(R=0,\ldots,H-h\). The decomposition by the first crossing and additional zeros is unique. Therefore

\[
 |\mathcal L_H|=\sum_{h=1}^H b_h(H-h+1).
 \tag{7.16}
\]

Equation (7.11) gives \(b_h\le C_0(2\rho)^{h-1}\). Summing the geometric derivative series yields

\[
 |\mathcal L_H|
 \le C_0\frac{(2\rho)^{H+1}}{(2\rho-1)^2},
 \qquad
 \sum_{p\in\mathcal L_H}m(p)\le H|\mathcal L_H|.
 \tag{7.17}
\]

These are explicit bounds, not fitted decay rates. The checker separately enumerates binary survival and complete odd leaves and verifies the exact identities (7.14) and (7.16) through exponent sum 20.

---

## 8. The full stopped law, with joint arithmetic marks

### 8.1 Reference measure for the original source progression

Uniform residues of \(t\) modulo growing powers of two in (3.1) induce a measure on odd dyadic source classes. Its word-cylinder mass is exactly the congruence count (6.4). This also gives a direct finite-level construction of that measure.

Write \(d=2^{s_0}d_o\) with \(d_o\) odd. The affine map \(t\mapsto a+2dt\) is a bijection from uniform dyadic parameters onto the class \(n\equiv a\pmod {2^{s_0+1}}\), with inverse parameter obtained by division by the retained \(2^{s_0+1}\) and the dyadic unit \(d_o\). That class has mass \(2^{-s_0}\) among all odd dyadic classes. Thus every event \(E\) satisfies the explicit conditional-measure comparison

\[
 \mu_{a,d}(E)=2^{s_0}\mu\bigl(E\cap\{n\equiv a\pmod{2^{s_0+1}}\}\bigr).
 \tag{8.1}
\]

Applied to the event of no completed leaf by exponent sum \(H\), it proves

\[
 0\le t_H^{a,d}\le2^{s_0}t_H\le2^{s_0}K\rho^H.
 \tag{8.2}
\]

For odd \(d\), \(t_H^{a,d}=t_H\). In particular, \(\sum_{p\in\mathcal L}\mu_{a,d}(p)=1\), for every fixed retained progression.

### 8.2 The two countable probability laws

Let \(P_{a,d,b,N,M}\) be the actual pushforward of the uniform law on the \(N\) integer parameters in (3.1) by (5.5), with the additional never-certified symbol \(\infty\).

Let \(Q_{a,d,b,N,M}\) assign every finite label its weight (6.2), and assign \(Q(\infty)=0\). Equations (6.4) and (8.2) prove that its finite-label weights sum to one. Its declared zero labels, including \(\infty\), remain in the target set. This is a precise definition of the comparison law, not an assertion that it equals actual arithmetic data.

### Theorem 8.1 — All-horizon joint-observation bound

For every admissible source progression, every \(N,M\ge1\), and every integer \(H\ge0\),

\[
 \boxed{\Delta(P_{a,d,b,N,M},Q_{a,d,b,N,M})
 \le\min\left\{1,
 t_H^{a,d}+\frac{M}{N}\sum_{p\in\mathcal L_H}m(p)
 \right\}.}
 \tag{8.3}
\]

The left side concerns the full countable stopped observation with no prescribed final return horizon. For odd \(d\), the bound is uniform in the original location \(a,b\) and the retained odd step \(d\).

**Proof.** Let \(S\) be the finite declared labels lying over \(\mathcal L_H\), and let \(e=|S|/N=M\sum m(p)/N\). Equation (6.3) gives
\(\sum_{\lambda\in S}|P(\lambda)-Q(\lambda)|\le e\). Its consequence for total mass is
\(P(S^c)\le Q(S^c)+e=t_H^{a,d}+e\). Therefore

\[
 2\Delta(P,Q)
 \le e+P(S^c)+Q(S^c)
 \le2e+2t_H^{a,d}.
\]

This inequality includes every tail leaf and the actual never-certified atom, so it has not discarded either. The bound by one is the defining maximum of total variation. ∎

For the stopped word alone, the identical proof with one cell per leaf gives

\[
 \Delta(P^{\rm word},\mu_{a,d})
 \le\min\{1,t_H^{a,d}+|\mathcal L_H|/N\}.
 \tag{8.4}
\]

### Explicit convergence rate for odd source step

Set \(\eta=-\log_2(31/32)>0\). For parameters \(N\ge M(1+\log_2N)\), choose the explicit nonnegative integer

\[
 H=\left\lfloor\log_2\frac{N}{M(1+\log_2N)}\right\rfloor.
 \tag{8.5}
\]

Equations (7.15), (7.17), and (8.3) yield

\[
 \Delta(P,Q)
 \le\left(K+C_0\frac{2\rho}{(2\rho-1)^2}\right)\rho^H
 \le\frac{K+C_0(2\rho)/(2\rho-1)^2}{\rho}
 \left(\frac{M(1+\log_2N)}{N}\right)^\eta.
 \tag{8.6}
\]

Indeed \(M H2^H/N\le H/(1+\log_2N)\le1\), and the floor in (8.5) loses at most one factor of \(\rho\). For fixed \(M\), this tends to zero uniformly over the stated odd-step source families. This explicit rate is not optimized.

For general even step, the finite inequality remains (8.3) with the exact conditional tail (6.5), or its bound (8.2). The dyadic factor is not omitted to assert uniformity in an unrestricted growing even step.

### Exact projection to other observations

For any declared readout map \(\psi\) of the retained labels, define the pushforward by summing its literal fibers. Then

\[
 \Delta(\psi_*P,\psi_*Q)
 =\frac12\sum_y\left|\sum_{\lambda:\psi(\lambda)=y}
                  (P(\lambda)-Q(\lambda))\right|
 \le\Delta(P,Q).
 \tag{8.7}
\]

Thus (8.3) applies to the synchronized residue vector, the actual first-descent index, or their joint readout, by their explicit maps in Section 5. The proof shows exactly which fibers are combined.

The observation in (8.3) forgets the post-stop tail by (2.6). It does not recover the predecessor's entire fixed-length history law. No equivalence between those two distributions is asserted; their exact relation is the pushforward (2.5) and its displayed fibers.

---

## 9. Restart composition and the retained dyadic/triadic correspondence

### 9.1 Exact ancestral state

A restart node consists of a current family

\[
 x(t)=a+2dt,\quad b\le t<b+N,
\]

an original source family on the same parameter

\[
 n_0(t)=a_0+2d_0t,
\]

and the complete concatenated history \(w\). They satisfy the coefficient identities

\[
 L(w)a_0+C(w)=2^{A(w)}a,\qquad
 L(w)d_0=2^{A(w)}d.
 \tag{9.1}
\]

For a compatible next leaf \(p\) and mark restriction (3.11), set

\[
 o=s+Pr,\quad h=PM,\quad t=o+h\ell.
\]

The new original coefficients are

\[
 a'_0=a_0+2d_0o,\qquad d'_0=d_0h,
 \tag{9.2}
\]

and the new current coefficients are

\[
 a'=u+2d'r,\qquad d'_{\rm current}=Md'.
 \tag{9.3}
\]

The new history is \(wp\), with composition law (1.4). Direct substitution in (9.1) proves its two new coefficient identities. This is an inductive commuting diagram at every restart, not just endpoint agreement on a sampled orbit.

Within each node, distinct leaf cylinders are disjoint by prefix-freeness. Congruence marks partition each compatible cylinder. Exact first-descent cells further partition by (5.4). Empty fibers, cutoff overflow, and the singleton value 1 are separately retained. The singleton 1 is an absorbing boundary state, because \(T(1)=1\); Theorem 2.1 is used only at current sources at least 3.

### 9.2 The explicit dyadic itinerary map

The infinite regular exponent code has the 2-adic realization

\[
 \Xi(a_1,a_2,\ldots)
 =-\sum_{i=1}^{\infty}\frac{2^{A_{i-1}}}{3^i}.
 \tag{9.4}
\]

The series converges in \(\mathbb Z_2\) because \(A_{i-1}\to\infty\); its first term is odd and later terms are even. Splitting the sum after \(m\) terms gives the exact branch equation

\[
 \Xi(p\omega)=\frac{2^{A(p)}\Xi(\omega)-C(p)}{L(p)}.
 \tag{9.5}
\]

It follows, using (1.7), that its prefix cylinder has the original residue and modulus. Conversely, the finite cylinders of any infinite exponent code are nested and have moduli tending to infinity, so they specify the unique dyadic integer (9.4). The points where a dyadic trajectory reaches \(-1/3\), and hence an infinite valuation at a finite stage, are excluded from the regular exponent domain by their explicit defining equation. They form a countable set of finite-prefix inverse images under (9.5). No positive integer lies in that set: every finite actual iterate of a positive integer is positive. A separate exceptional symbol may be assigned to those dyadic points; its dyadic measure is zero.

This records the exact domain and exceptional set of the coding. Formula (9.5) is the same inverse as (4.10), with its integer integrality criterion (4.11) still retained.

### Theorem 9.1 — Product law of completed blocks in the reference code

Successive words in \(\mathcal L\), obtained by restarting the reference stopping rule on the unused exponent code, have the cylinder law

\[
 \Pr(p_1,\ldots,p_r)=\prod_{i=1}^r2^{-A(p_i)}.
 \tag{9.6}
\]

**Proof.** Prefix-free stopping parses a concatenation of \(r\) leaf words uniquely. Prescribing that stopped tuple is exactly prescribing the concatenated exponent prefix \(p_1\cdots p_r\). Its cylinder mass from (7.3) is \(2^{-\sum_i A(p_i)}\), which is (9.6). Section 7 proves that each unused reference tail completes a leaf with probability one, so these masses have total one for each fixed \(r\). ∎

This is a theorem about the specified reference code. For actual finite integer samples, the corresponding concatenated cylinder is counted by its original floor formula and restricted through the restart charts. No independence of actual finite-sample block outcomes is asserted.

The dyadic branch (9.5) maps onto all regular odd dyadic tail values, while its ordinary integer target is the triadic congruence class (4.11). The two assertions coexist through the explicit embedding and inverse diagram of Section 4. In an integer restart the step \(d3^m\), or its fully retained even-step counterpart (3.7), remains part of the source. Equation (9.6) does not authorize replacing that source with consecutive odd integers.

At the actual integer 1, the infinite code \((2,2,\ldots)\) realizes 1 by (9.4). The unabsorbed reference parser would keep returning \((2)\). The positive-integer engine instead maps that exact source point to the absorbing label 1. This is a specified change on a literal singleton of reference measure zero, not a claim that the singleton is absent from a finite integer sample.

---

## 10. Support-aware chain maps and finite Hurwitz reconstruction

The arithmetic image complex in Section 4 and the actual support-incidence complex are linked by an affine incidence complex carrying both the original mass and the actual terminal odd-index. The comparison chain maps, their cohomology sequence, and a retained-anchor homotopy are given first.

### 10.0 Exact chain-level bridge through the actual terminal moment

The link between support incidence and the arithmetic image complex can be made at chain level, not merely by citing the same source chart. Fix a compatible declared label \(\lambda=(p,r,j)\). In (3.11), let \(F_\lambda\) be the finite set of actual lift parameters \(\ell\) in the fiber (5.6). It is a consecutive integer interval, possibly empty. Retain

\[
 D_\lambda=Md',\qquad
 z_\lambda=\frac{u+2d'r-1}{2},\qquad
 z(\ell)=z_\lambda+D_\lambda\ell.
 \tag{10.0a}
\]

Here \(z(\ell)\) is the **actual terminal odd-index**, not an arbitrary numerical label. Form the affine incidence complex

\[
 \mathcal A_\lambda=
 \left[\mathbb Z[F_\lambda]\xrightarrow{d_{\mathcal A}}\mathbb Z^2\right],
 \qquad d_{\mathcal A}(e_\ell)=(1,z(\ell)).
 \tag{10.0b}
\]

Its first coordinate is the original support incidence. Its second coordinate is the actual terminal moment. Write the one-label support complex and marked image complex as

\[
 \mathcal I_\lambda=[\mathbb Z[F_\lambda]\xrightarrow{\delta}\mathbb Z],
 \quad\delta(e_\ell)=1,
 \qquad
 \mathcal K_\lambda=[\mathbb Z\xrightarrow{D_\lambda}\mathbb Z].
\]

There is the following explicit span of chain maps:

\[
 \mathcal I_\lambda\ \xleftarrow{\ q\ }\ \mathcal A_\lambda
 \ \xrightarrow{\ f\ }\ \mathcal K_\lambda,
 \tag{10.0c}
\]

with

\[
 q^0=\mathrm{id},\quad q^1(a,b)=a,
 \qquad
 f^0(e_\ell)=\ell,\quad f^1(a,b)=b-z_\lambda a.
 \tag{10.0d}
\]

The chain equations are exactly

\[
 q^1d_{\mathcal A}(e_\ell)=1=\delta(e_\ell),
 \qquad
 f^1d_{\mathcal A}(e_\ell)=z(\ell)-z_\lambda
                         =D_\lambda f^0(e_\ell).
 \tag{10.0e}
\]

The coefficient \(z_\lambda\) is retained in the map; it has not been set to zero without its inverse data.

#### The exact sequence exposing the image torsion

The kernel complex of \(q\) has only \(\mathbb Z\) in degree one, embedded by \(b\mapsto(0,b)\). Its resulting exact cohomology sequence is

\[
 0\longrightarrow H^0(\mathcal A_\lambda)
 \longrightarrow H^0(\mathcal I_\lambda)
 \xrightarrow{\ \theta\ }\mathbb Z
 \longrightarrow H^1(\mathcal A_\lambda)
 \longrightarrow H^1(\mathcal I_\lambda)
 \longrightarrow0,
 \tag{10.0f}
\]

where the connecting map, with its sign fixed by the displayed embedding, is

\[
 \theta\!\left(\sum_\ell c_\ell e_\ell\right)
   =\sum_\ell c_\ell z(\ell)
   =D_\lambda\sum_\ell c_\ell\ell,
 \qquad \sum_\ell c_\ell=0.
 \tag{10.0g}
\]

**Direct proof of exactness.** The kernel of \(\theta\) consists exactly of source vectors of both mass zero and terminal moment zero, which is \(H^0(\mathcal A_\lambda)\). The next map sends \(b\) to the class of \((0,b)\). Its kernel consists of moments of mass-zero source vectors, exactly the image of \(\theta\). The next map is induced by the first-coordinate projection, and is surjective. Its kernel is represented by the second-coordinate vectors after subtracting a source lift of the first coordinate whenever that coordinate is in the support image. This proves the remaining exactness, including the empty source case. ∎

Let \(n_\lambda=|F_\lambda|\). For an empty fiber, \(H^1(\mathcal A_\lambda)=\mathbb Z^2\). For a singleton, its sole image vector \((1,z)\) is primitive, so \(H^1(\mathcal A_\lambda)\cong\mathbb Z\). For at least two points, their consecutive parameters give

\[
 \theta(H^0(\mathcal I_\lambda))=D_\lambda\mathbb Z,
 \qquad
 H^1(\mathcal A_\lambda)\cong\mathbb Z/D_\lambda\mathbb Z,
 \qquad \operatorname{rank}H^0(\mathcal A_\lambda)=n_\lambda-2.
 \tag{10.0h}
\]

Indeed the first two columns have determinant \(D_\lambda\), and every column difference is \((0,D_\lambda k)\). Thus the original terminal lattice appears as the cokernel of the **actual terminal-moment map on the support kernel**. Empty and singleton fibers retain their different free cohomology instead of being silently forced into the at-least-two-point calculation.

#### Explicit homotopy retaining the anchor

For \(n_\lambda\ge2\), choose the first two actual parameters \(\ell_0,\ell_0+1\), and retain \(z_*=z(\ell_0)\). The anchored comparison has

\[
 \bar f^0(e_\ell)=\ell-\ell_0,
 \qquad\bar f^1(a,b)=b-z_*a.
\]

Its right inverse from \(\mathcal K_\lambda\) is

\[
 i^0(1)=e_{\ell_0+1}-e_{\ell_0},\qquad i^1(1)=(0,1).
\]

Let

\[
 R_\ell=e_\ell-e_{\ell_0}
             -(\ell-\ell_0)(e_{\ell_0+1}-e_{\ell_0}),
\]

let \(P^0(e_\ell)=R_\ell\), \(P^1=0\), and put \(h^1(a,b)=a e_{\ell_0}\). Direct substitution gives

\[
 \bar f i=1,\qquad
 1-i\bar f-P=d_{\mathcal A}h+h d_{\mathcal A}.
 \tag{10.0i}
\]

Each \(R_\ell\) has both zero mass and zero original terminal moment. The vectors outside the two anchors give a free basis of the kernel. Hence (10.0i) is a complete chain homotopy onto the marked image complex plus the actual affine-relation module in degree zero.

The original and anchored comparison maps themselves differ by the explicit chain homotopy \(s^1(a,b)=\ell_0 a\):
\(f-\bar f=d_{\mathcal K}s+s d_{\mathcal A}\). The original coset is retained because \(z_*-z_\lambda=D_\lambda\ell_0\). Thus neither the anchor nor its translation has been silently discarded.

#### Mark refinement of the image complex

The map from \(\mathcal K_\lambda\) back to the unmarked complex in Section 4 is multiplication by \(M\) in degree zero and the identity in degree one. Its chain equation is \(d'M=D_\lambda\). The cohomology maps fit the exact sequence

\[
 0\longrightarrow\mathbb Z/M\mathbb Z
 \xrightarrow{\ [c]\mapsto[d'c]\ }
 \mathbb Z/(Md')\mathbb Z
 \longrightarrow\mathbb Z/d'\mathbb Z
 \longrightarrow0.
 \tag{10.0j}
\]

Its middle-to-right map is literal reduction. The marked coset \([z_\lambda]\) maps to the original \([(u-1)/2]\), because their difference is \(d'r\). This is the exact lattice data carried by forgetting a mark.

#### Seven-point instance

On the actual points \(247+256\ell\), \(\ell=0,\ldots,6\), use \(p=(1,1,3,2)\), \(M=1\), and actual first descent \(j=3\). The affine incidence matrix has columns

\[
 \begin{pmatrix}
 1&1&1&1&1&1&1\\
 78&159&240&321&402&483&564
 \end{pmatrix}.
 \tag{10.0k}
\]

The support map is its first row. The terminal-moment map on the support kernel has image \(81\mathbb Z\), giving the exact sequence

\[
 0\longrightarrow\mathbb Z^5\longrightarrow\mathbb Z^6
 \xrightarrow{\theta}\mathbb Z
 \longrightarrow\mathbb Z/81\mathbb Z\longrightarrow0.
 \tag{10.0l}
\]

In particular, the image torsion in Section 4 is recovered from these original finite arithmetic values and explicit source maps, not inserted as an unrelated auxiliary group.

### 10.1 Incidence complex of the actual observation

Fix a finite source sample \(I\) and the declared finite label set \(\Lambda_H\) of all \((p,r,j)\) with \(p\in\mathcal L_H\), together with overflow. Incompatible labels and empty first-descent cells remain in \(\Lambda_H\), with their masks recorded. The actual map is \(\pi_H:I\to\Lambda_H\).

Form

\[
 K^\bullet_{\pi_H}=
 \left[\mathbb Z[I]\xrightarrow{\delta}\mathbb Z[\Lambda_H]\right],
 \qquad \delta(e_n)=e_{\pi_H(n)}.
 \tag{10.1}
\]

For each occupied label \(\lambda\), select one actual source point \(n_\lambda\) in its fiber and retain that selection. Define

\[
 h^1(e_\lambda)=
 \begin{cases}e_{n_\lambda},&\lambda\text{ occupied},\\0,&\lambda\text{ empty}.
 \end{cases}
 \tag{10.2}
\]

Let \(P^0=1-h^1\delta\) and \(P^1=1-\delta h^1\). These formulas give

\[
 1-P^0=h^1\delta,\qquad1-P^1=\delta h^1,
 \qquad\delta P^0=0,\qquad P^1\delta=0.
 \tag{10.3}
\]

They are explicit projections and a chain homotopy onto the following zero-differential cohomology representatives:

\[
 H^0\cong\bigoplus_{\lambda\text{ occupied}}
 \left\langle e_n-e_{n_\lambda}:n\in\pi_H^{-1}(\lambda),\ n\ne n_\lambda\right\rangle,
\]
\[
 H^1\cong\mathbb Z[\{\lambda\in\Lambda_H:\pi_H^{-1}(\lambda)=\varnothing\}].
 \tag{10.4}
\]

**Proof.** In a source fiber, \(\delta\) sums its coefficients into its target basis vector. Its kernel is freely generated by the displayed differences. Its image contains exactly the occupied target basis vectors. The other target basis vectors form a free cokernel basis. Equations (10.3) follow on each source and target basis vector from (10.2). ∎

Changing the selected source representative in a fiber changes \(h^1(e_\lambda)\) by the explicitly known kernel vector \(e_{n'_\lambda}-e_{n_\lambda}\). This retains the section-change map as well.

Thus a declared label with zero actual weight remains a basis element; it is not removed because a numerical weight vanishes. The distinct reasons for zero—source congruence incompatibility, empty threshold interval, or no point in this particular finite sample—remain metadata on those exact labels.

### 10.2 Pullback, pushforward, and a retained count vector

The function pullback is

\[
 \pi_H^*f=f\circ\pi_H.
 \tag{10.5}
\]

On formal source measures it is dual to the exact pushforward \(\delta\), and

\[
 \delta\left(\sum_{n\in I}e_n\right)=\sum_{\lambda\in\Lambda_H}c_\lambda e_\lambda.
 \tag{10.6}
\]

For a further declared projection \(\psi:\Lambda_H\to\Gamma\), the chain map from the incidence complex of \(\pi_H\) to that of \(\psi\pi_H\) is the identity in degree zero and \(e_\lambda\mapsto e_{\psi(\lambda)}\) in degree one. Its chain equation is literal composition of the source maps. In degree one its kernel is generated by label contrasts \(e_\lambda-e_{\lambda_0}\) inside the fibers of \(\psi\). This exhibits exactly the information lost by a further observation.

### 10.3 Finite spectral input with its label dictionary retained

Choose and retain a bijective enumeration

\[
 \iota:\Lambda_H\longrightarrow\{1,\ldots,d_\Lambda\}.
\]

The associated diagonal label operator has eigenvalues \(\lambda_i=i\), with an idempotent \(e_i\) for **every** declared label. The dictionary \(\iota^{-1}\) is part of the object; discarding it would discard the connection to (5.6).

Put \(w_i=c_i/N\), including zero weights, and

\[
 M_k=\sum_{i=1}^{d_\Lambda}w_i\lambda_i^k,
 \qquad Z(s)=\sum_{i=1}^{d_\Lambda}w_i\zeta(s,\lambda_i).
 \tag{10.7}
\]

The finite weights are the actual counts (10.6), not an unspecified probability vector. The equality \(M_0=1\) includes overflow.

The standard Hurwitz–Bernoulli identity [R3] is

\[
 \zeta(-k,x)=-\frac{B_{k+1}(x)}{k+1},
 \quad
 B_{k+1}(x)=\sum_{r=0}^{k+1}\binom{k+1}{r}B_{k+1-r}x^r.
 \tag{10.8}
\]

For this finite source, it gives the literal triangular relation

\[
 Z(-k)=-\frac1{k+1}\sum_{r=0}^{k+1}
                   \binom{k+1}{r}B_{k+1-r}M_r.
 \tag{10.9}
\]

Starting from \(M_0=1\), the explicit inverse is

\[
 M_{k+1}=-(k+1)Z(-k)-\sum_{r=0}^{k}
                   \binom{k+1}{r}B_{k+1-r}M_r.
 \tag{10.10}
\]

For each label form the Lagrange polynomial

\[
 L_i(X)=\prod_{j\ne i}\frac{X-\lambda_j}{\lambda_i-\lambda_j}
       =\sum_{k=0}^{d_\Lambda-1}l_{ik}X^k.
\]

Its exact weight reconstruction is

\[
 \boxed{w_i=\sum_{k=0}^{d_\Lambda-1}l_{ik}M_k.}
 \tag{10.11}
\]

**Proof.** Equation (10.9) follows by inserting the finite sum (10.7) into (10.8). The coefficient of \(M_{k+1}\) inside the sum is one, which gives (10.10). Finally
\(\sum_k l_{ik}M_k=\sum_jw_jL_i(\lambda_j)=w_i\). All finite sums and their label maps are explicit. In particular (10.11) reconstructs zero weights without deleting their idempotents. ∎

The checker uses exact Bernoulli fractions and polynomial arithmetic to test (10.9)–(10.11). It does not claim numerical analytic continuation of zeta functions or identification with an inaccessible predecessor implementation.

---

## 11. A complete worked restart family

Start with the compatible family in (4.12). On the target \(157+162t\), the next leaf \((3)\) selects \(t=8u\). The exact two-block diagram is

\[
 247+2048u\longmapsto157+1296u\longmapsto59+486u,
 \qquad u\in\mathbb Z_{\ge0}.
 \tag{11.1}
\]

The first map uses four odd returns; the second uses one. Each displayed block begins at a value at least 3 and strictly descends. The step 486 is \(2\cdot3^5\), not 2.

For the anchor 247 the successive reference-certified blocks are

\[
 (1,1,3,2),\quad(3),\quad(1,2,1,4),\quad(1,3),\quad(1,2,3),\quad(4).
 \tag{11.2}
\]

Their endpoint values are respectively

\[
 157,\quad59,\quad19,\quad11,\quad5,\quad1.
\]

The complete prefix data are:

| Completed block | Total odd returns | Total exponent sum | Original source step | Terminal step | Anchor endpoint |
|---:|---:|---:|---:|---:|---:|
| 1 | 4 | 7 | 256 | 162 | 157 |
| 2 | 5 | 10 | 2,048 | 486 | 59 |
| 3 | 9 | 18 | 524,288 | 39,366 | 19 |
| 4 | 11 | 22 | 8,388,608 | 354,294 | 11 |
| 5 | 14 | 28 | 536,870,912 | 9,565,938 | 5 |
| 6 | 15 | 32 | 8,589,934,592 | 28,697,814 | 1 |

Each row is an infinite-family identity

\[
 247+2^{A+1}t\longmapsto x_{\rm anchor}+2\cdot3^mt,
 \qquad t\ge0,
 \tag{11.3}
\]

with the row's original word, \(A\), and \(m\). In particular,

\[
 T^{15}(247+2^{33}t)=1+28\,697\,814t
 \tag{11.4}
\]

on precisely the concatenated word in (11.2). The assertion that the terminal value equals 1 applies to the anchor \(t=0\); equation (11.4) states the other values exactly and does not assert that the whole infinite family has already reached 1.

---

## 12. Executed verification and precise scope

The accompanying `verify.py` uses only the Python standard library, integers, and exact rational fractions. Every proof check is an explicit exception check rather than an `assert`, so optimization does not disable the checks.

The verified families include 340 original words of lengths 1 through 4 with exponents 1 through 4; independent binary and odd-leaf enumerations through exponent sum 20; 180 marked finite-source laws with odd and even progression steps, large source offsets, and odd/even mark moduli; synchronized residue readouts modulo 3, 4, 9, and 12; integral image complexes and finite coefficient kernels at powers of 2 and 3; enriched-incidence chain maps and homotopies, including empty, singleton, and occupied-fiber cases; exact product-cylinder counts for one, two, and three stopped blocks; the worked infinite-family identities; and a three-round original-source restart replay.

For the 17 source points \(3,5,\ldots,35\), exponent cutoff 4 and mark modulus 3, the finite incidence/Hurwitz fixture has 16 declared labels, 8 occupied labels, \(\operatorname{rank}H^0=9\), and \(\operatorname{rank}H^1=8\). Every zero-weight label is reconstructed exactly.

The three-round finite restart starts with the 1,024 odd integers \(3,5,\ldots,2049\) and uses exponent cutoff 10 at each block:

| Round | Input points | Accepted descent points | Already at 1, absorbed | Explicit cutoff overflow | Output progressions |
|---:|---:|---:|---:|---:|---:|
| 1 | 1,024 | 809 | 0 | 215 | 71 |
| 2 | 809 | 637 | 5 | 167 | 302 |
| 3 | 637 | 502 | 14 | 121 | 423 |

At each round the counts in the three outcome columns sum to the input count. Every accepted point is checked against actual valuations, terminal values, original-source ancestry, and strict descent. Overflow points are retained as unresolved outcomes of that finite cutoff and are not silently sent through the restart. Output points reaching 1 are absorbed at the next input boundary; the table does not count every final output at 1 as already absorbed.

The exact stopped profiles include

| Exponent cutoff | Number of leaves | Sum of leaf lengths | Reference overflow |
|---:|---:|---:|---:|
| 4 | 4 | 5 | 1/2 |
| 8 | 28 | 75 | 69/256 |
| 12 | 212 | 1,102 | 339/2048 |
| 16 | 1,601 | 12,116 | 1901/16384 |
| 20 | 17,396 | 181,297 | 10845/131072 |

These are finite exact checks of the displayed formulas. The infinite-series, coefficient-comparison, and all-horizon statements rest on the proofs above, not on extrapolation from these numbers. Ordinary and optimized execution receipts are supplied separately. No Lean execution, external mathematical audit, current-workbench replay, GitHub CI success, or remote publication is claimed.

### What remains an actual integer question

For a finite source sample, the never-certified symbol has actual weight

\[
 P(\infty)=\frac1N\#\{n\in I:\sigma(\text{actual itinerary of }n)=\infty\}.
 \tag{12.1}
\]

Its reference weight is zero, and the map from source points to that label is still present. A positive actual point contributes \(1/N\), regardless of its zero reference measure. Equations (8.3) and (12.1) state the relationship explicitly. They do not prove the count in (12.1) is zero for every sample, nor that every individual positive start enters an accepted restart branch.

The concrete deterministic continuation object is the restart system (3.10), (4.3)–(4.11), and (9.1)–(9.3), with original source ancestry attached. It supports exact further work on the unresolved integer fibers without substituting a uniform odd source or deleting a zero-reference label. The present contribution constructs that system and executes several levels of it; it does not replace the remaining integer-fiber question by an unproved assumption.

---

## References

**[R1]** Riho Terras, *A stopping time problem on the positive integers*, Acta Arithmetica **30** (1976), 241–252, DOI `10.4064/aa-30-3-241-252`. Publisher bibliographic record inspected on 14 September 2026. The full paper was not used as a proof dependency.

**[R2]** Terence Tao, *Almost all orbits of the Collatz map attain almost bounded values*, arXiv `1909.03562`; Forum of Mathematics, Pi **10** (2022), e12. The current abstract and metadata inspected on 14 September 2026 identify version 7, revised 16 July 2026. The abstract states the logarithmic-density orbit-minimum theorem and the first-passage/3-adic transport method. No assertion of having audited its complete current proof is made here. Source: `https://arxiv.org/abs/1909.03562`.

**[R3]** NIST Digital Library of Mathematical Functions, equations 25.11.14 and 24.2.1–24.2.3, Hurwitz values at nonpositive integers and the Bernoulli generating functions/polynomials. Inspected on 14 September 2026. Sources: `https://dlmf.nist.gov/25.11.E14` and `https://dlmf.nist.gov/24.2`.

**[R4]** Author-supplied conversation and readable historical author workbench records, September 2026 intake: original affine Collatz definitions, exact-morphism methodology, and the claimed predecessor path. Private record locators and the distinction between readable historical material and inaccessible current repository files are preserved in the local source-intake record, outside the repository patch.
