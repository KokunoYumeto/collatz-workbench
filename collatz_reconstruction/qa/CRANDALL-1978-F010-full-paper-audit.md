# CRANDALL-1978-F010 — complete accelerated-map, counting, cycle, and \(qx+r\) audit

## Status and controlling witness

This is a complete content-level audit of Richard E. Crandall, *On the
"3x+1" Problem*, *Mathematics of Computation* **32** (1978), no. 144,
1281--1292.  The audit uses the article itself rather than either frozen
routing description.  In particular, a routing description's phrase
"positive-density result" is rejected: Theorem 6.1 is a power-law lower
bound and is compatible with density zero.

- controlling local witness:
  `C:/Users/LOCAL_USER/Documents/Papors/OS/on-the-3x-1-problem-5cygpgqcjg.pdf`
- byte-identical indexed manifestation:
  `C:/Users/LOCAL_USER/Documents/arxiv_latex/library/other/on-the-3x-1-problem-5cygpgqcjg.pdf`
- PDF pages: `12`, containing printed pp. 1281--1292
- PDF bytes: `964602`
- PDF SHA-256:
  `acafa9070e7c5e4b167d70d7cace81da39489710804c510ff8db4369133217f4`
- received: 28 March 1977; revised: 20 March 1978; issue date: October 1978
- frozen exact routes:
  `DOCROUTE-COL-EC8037330D561573C31E`,
  `ROUTE-COL-591DD74C83DB96290076`, and
  `ROUTE-COL-F9379F3657AAC3711D2B`

All twelve printed pages were rendered at 300 dpi and read visually.  OCR was
used only as a search aid.  It corrupts several formulas and, in particular,
misreads the printed \(q=181\) starting value \(27\) as \(21\).

## Exact clock, trajectory, and height convention

The paper works on the positive odd integers \(D^+\) with the fully
accelerated odd-to-odd map

\[
 C(x)=\frac{3x+1}{2^{e(x)}},
 \qquad e(x)=v_2(3x+1).
\]

The trajectory is the indexed sequence
\(T_m=(C^j(m))_{j\geq1}\), stopped after the least positive index at which
the value is 1, and left infinite if there is no such index.  Its height is
that least index, or infinity if it does not exist.  The braces in the
source's display denote this ordered sequence rather than its underlying
set: repetitions in a nonterminating periodic trajectory do not make the
height finite.  Thus the source convention has \(T_1=(1)\) and \(h(1)=1\);
it does not use the zero-step hitting time.
Every height and period in this paper is accelerated \(C\)-time.

If \(e_i=e(C^i(x))\) and
\(A_k=e_0+\cdots+e_{k-1}\), then \(k\) accelerated steps are exactly
\(A_k\) steps of the shortened whole-integer map and \(A_k+k\) steps of the
unshortened map.  Consequently the historical statement \(k>17985\) is
measured in accelerated time.  Since every \(e_i\geq1\), it transfers to the
weaker numerical bounds \(A_k\geq k>17985\) and \(A_k+k>k>17985\) for the
corresponding shortened and unshortened return lengths, but those clocks are
not equal to \(k\).

## Preliminary theorem and heuristic boundary

Printed p. 1282, Theorem 2.2, takes \(m_k=2^k-1\) and proves

\[
 C^j(m_k)=3^j2^{k-j}-1\quad(0\leq j<k),
 \qquad
 \frac{\sup T_{m_k}}{m_k}>
 \left(\frac32\right)^{k-1}.
\]

The construction proves that \((\sup T_m)/m^\alpha\) is unbounded only for
\(\alpha<\log_2 3\).  It does not prove an analogous assertion at or above
that exponent.

Crandall reports Everett's result that for "almost all" positive odd \(m\),
\(\inf T_m<m\), but gives no proof.  Everett's paper is not present in the
completed frozen route ledger and this edition does not use the reported
theorem before its primary dependency is read.

Section 3 is expressly heuristic.  It assigns the model probability
\(\Pr(e(m)=k)=2^{-k}\), obtains model drift

\[
 \sum_{k\geq1}2^{-k}\log(3/2^k)=-\log(4/3),
\]

and proposes
\(h(m)\sim\log m/\log(4/3)\).  With

\[
 H(x)=\frac2x\sum_{\substack{m\leq x\\m\in D^+}}h(m),
\]

Conjecture 3.1 is
\(H(x)\sim2\log x/\log(16/9)\).  None of these random-walk statements is a
theorem.  The sentence after Conjecture 3.1 calls it "(3.1)", colliding with
the earlier individual-height heuristic; this is a source cross-reference
defect.

## Backward coordinates and the corrected finite-height address space

Printed p. 1284 defines, for \(a\in\mathbb Z_{>0}\) and rational \(n\),

\[
 B_a(n)=\frac{2^a n-1}{3},
 \qquad
 B_{a_j\cdots a_1}=B_{a_j}\circ\cdots\circ B_{a_1}.
\]

If \(n\) is a positive odd integer and the full composition is integral,
Lemma 4.1 proves that every prefix is an odd integer and that \(C\) removes
one \(B\)-letter at a time.  Lemma 4.2 proves that, when \(a_1>2\), the
listed prefixes followed by 1 are the exact terminated trajectory.

For an address \((a_1,\ldots,a_j)\), put \(n_0=1\) and
\(n_i=B_{a_i}(n_{i-1})\).  The exact repaired gate for an integer
\(n_j>1\) of height \(j\) is

\[
 a_1>2,
 \qquad
 2^{a_i}n_{i-1}\equiv1\pmod3\quad(1\leq i\leq j),
 \qquad
 2^{a_i}n_{i-1}\not\equiv1\pmod9\quad(1\leq i<j).
\]

The mod-9 condition says precisely that an intermediate \(n_i\), which must
admit another predecessor, is not divisible by 3.  There is no mod-9 gate at
the terminal letter.  With this repair, Theorem 4.1 is the bijection between
finite-height odd integers \(m>1\) and the admitted finite addresses, with
inverse

\[
 a_i=e(C^{h(m)-i}(m))\quad(1\leq i\leq h(m)).
\]

### Two endpoint defects in the printed address theorem

1. The displayed definition of \(G\) places a non-\(1\pmod9\) condition on
   \(a_1\) and a terminal mod-3 condition on \(a_j\).  At length \(j=1\)
   these are both conditions on the same letter.  This excludes the valid
   height-one address \(a_1=6\):
   \(B_6(1)=21\), \(C(21)=1\), but \(2^6\equiv1\pmod9\).
2. Lemma 4.3 is false if its phrase "an integer of height \(j\)" includes the
   source's own \(m=1\) convention.  The address \(a_1=2\) gives
   \(B_2(1)=1\) and \(h(1)=1\), but \(G\) requires \(a_1>2\).  The repaired
   lemma is restricted to the \(m>1\) set used by Theorem 4.1.

Section 5's sentence that height-one values are
\((4^s-1)/3\) includes \(s=1\), namely \(m=1\).  Inside the paper's set
\(M=\{m\in D^+:m>1,\ h(m)<\infty\}\), the exact parameter range is
\(s\geq2\).

## Given-height and total counting bounds

Let \(\pi_h(x)\) count \(m\in M\) with \(h(m)=h\) and \(m\leq x\).
Lemma 5.1 proves

\[
 B_{a_j\cdots a_1}(1)<\frac{2^{a_1+\cdots+a_j}}{3^j}.
\]

For sufficiently large \(z\), Lemma 5.2 counts addresses of length \(j\)
and sum at most \(z\) from below by

\[
 \left(2\left\lfloor\frac{z-2}{6j}\right\rfloor\right)^j.
\]

The printed hypothesis "\(z>0\)" is false when the floor is negative and
\(j\) is even: at \(z=1,j=2\), the right side is 4 while no positive address
has sum at most 1.  Requiring \(z\geq2\), or replacing the base by its
nonnegative part, repairs the lemma.  Its application in Theorem 5.1 has
large \(z\), so the theorem survives.

Printed p. 1286, Theorem 5.1, states exactly that there are positive real
constants \(r,x_0\), independent of \(h\), such that

\[
 x>\max\{x_0,2^{h/r}\}
 \quad\Longrightarrow\quad
 \pi_h(x)>\frac{(\log_2(x^r))^h}{h!}.
\]

The proof chooses \(0<r<1\) satisfying

\[
 r\log_2(3/64)+\frac12>3\mathrm e r>0
\]

and uses the address count plus \(h!\mathrm e^h>h^h\).  It proves, in
particular, infinitely many positive odd starting values of every positive
accelerated height.

Let \(\pi(x)=\#\{m\in M:m\leq x\}\).  Lemma 6.1 is the Poisson half-mass
limit

\[
 \lim_{t\to\infty}e^{-t}
 \sum_{\substack{u\in\mathbb Z_{>0}\\u<\lfloor t\rfloor}}
 \frac{t^u}{u!}=\frac12.
\]

The relation sign is controlled by the high-resolution source raster: it is
strict \(<\), not \(\leq\).  Crandall supplies only a remark pointing to
error-function asymptotics and to Abramowitz--Stegun reference 4; he gives no
handbook section, page, or formula number.  The relevant formulas can now be
identified independently.  In the NBS first-printing facsimile, formula
26.4.21 gives

\[
 Q(\chi^2\mid\nu)
 =\sum_{j=0}^{c-1}e^{-m}\frac{m^j}{j!},
 \qquad c=\frac\nu2,\quad m=\frac{\chi^2}{2},\quad \nu\text{ even}.
\]

With \(n=\lfloor t\rfloor\), \(\nu=2n\), and \(\chi^2=2t\), this is
exactly the sum through \(u=n-1\), including \(u=0\).  Formula 26.4.11 gives
the associated normal coordinate

\[
 \frac{\chi^2-\nu}{\sqrt{2\nu}}
 =\frac{t-n}{\sqrt n}\longrightarrow0,
\]

while 26.2.2--26.2.6 give \(P(0)=Q(0)=1/2\).  This is an edition-level
identification of the relevant formula path, not a locator printed by
Crandall.  The complete witness is the June 1964 NBS first printing, not the
ninth Dover printing cited by Crandall; that manifestation difference is
retained explicitly.

Formula 26.4.11 prints no quantified remainder or uniformity statement on
that page.  The controlling all-real completion therefore takes
\(X_t\sim\mathrm{Poisson}(t)\): the characteristic function of
\((X_t-t)/\sqrt t\) is

\[
 \exp\!\left(t\left(e^{is/\sqrt t}-1-is/\sqrt t\right)\right)
 \longrightarrow e^{-s^2/2}.
\]

The L\'evy continuity theorem and an explicit fixed-\(\delta\) squeeze apply
to every integer cutoff \(k(t)\) satisfying
\((k(t)-t)/\sqrt t\to0\).  In particular they cover the printed cutoff
\(k(t)=\lfloor t\rfloor-1\), the adjacent cutoff \(\lfloor t\rfloor\), and
the repaired theorem cutoff \(\lceil t\rceil-1\).  Omitting the \(u=0\) mass
changes the expression by exactly \(e^{-t}\).  This proof explicitly depends
on L\'evy's theorem; it is not called elementary or dependency-free.

Printed p. 1287, Theorem 6.1, is

\[
 \exists c>0\ \exists X_0\ \forall x>X_0:
 \qquad \pi(x)>x^c.
\]

There is a strict-endpoint slip in the printed summation: Theorem 5.1 needs
\(h<r\log_2x\), whereas the proof sums through
\(\lfloor r\log_2x\rfloor\), which can include equality.  Summing through
\(\lceil r\log_2x\rceil-1\) repairs the application and has the same Poisson
half-mass limit.  The proof then gives

\[
 \pi(x)>(1/2-d)e^{r\log_2x}
       =(1/2-d)x^{r/\log 2}
\]

for every fixed \(d\in(0,1/2)\) and sufficiently large \(x\).  Hence every
\(c<r/\log2\) is admissible after increasing the threshold.  The explicit
choice \(r=1/100\) satisfies the source inequality (use
\(\log_2(3/64)>-5\) and \(\mathrm e<3\)), so the proof can be made to yield
the concrete edition witness \(c=1/100\).

This is not positive density.  It does not imply that a positive proportion,
let alone almost every odd integer, reaches 1.

## Membership equation, returns, and an explicit cycle obstruction

For \(m=B_{b_k\cdots b_1}(n)\), Crandall sets

\[
 A_0=0,
 \qquad
 A_i=\sum_{j=k-i+1}^{k}b_j\quad(1\leq i\leq k)
\]

and expands the affine composition to

\[
 2^{A_k}n-3^km
 =\sum_{j=0}^{k-1}2^{A_j}3^{k-1-j}.
\]

Theorem 7.1 proves both directions: for positive odd \(m,n\), one has
\(n\in T_m\) exactly when there are an integer \(k\geq1\) and integers
\(0=A_0<A_1<\cdots<A_k\) satisfying this equation.  The reverse differences
\(d_i=A_{k-i+1}-A_{k-i}\) recover the exact \(B\)-word, and Lemma 4.1 proves
branch correctness.  When \(n\ne1\), it is the \(k\)-th displayed trajectory
element; \(n=1\) is the termination case.

The printed converse instead writes
\(d_i=A_{k-i+1}-A_{k-1}\).  This is an index defect: it can give
\(d_2=0\) and cannot recover successive coordinate gaps.  Replacing the
second subscript by \(k-i\) is forced by the displayed strictly increasing
\(A\)-sequence and makes the claimed identity
\(m=B_{d_k\cdots d_1}(n)\) valid.

Corollary 7.1 specializes to a return:

\[
 m(2^{A_k}-3^k)
 =\sum_{j=0}^{k-1}2^{A_j}3^{k-1-j}.
\]

Its printed forward clause assumes a trajectory of period \(k\), while its
converse establishes a return at the \(k\)-th trajectory element.  Combining
the converse with the repaired Theorem 7.1 gives the edition's more general
equivalence for arbitrary return exponent \(k\); that formulation is a
deduction, not the verbatim scope of the printed forward clause.  A return
after \(k\) accelerated steps need not have least period \(k\).  Positivity
of the right side forces \(2^{A_k}>3^k\).

Crandall's explicit sufficient obstruction is exact.  If integers \(a,b\)
satisfy

\[
 b>1,
 \qquad
 0<2^a-3^b\mid 2^{a-b}-1,
\]

put

\[
 d=\frac{2^{a-b}-1}{2^a-3^b},
 \qquad m=2^bd-1.
\]

Then \(a>b\), \(d\) is positive, and \(m\) is an odd integer greater than
1.  With \(k=b\) and \(A_j=j\), the return equation reduces to

\[
 m(2^a-3^b)=3^b-2^b
 =\sum_{j=0}^{b-1}2^j3^{b-1-j}.
\]

Thus \(C^b(m)=m\) and the main conjecture fails; the least period may divide
\(b\).

Crandall also reports two external results about
\(2^x-3^y=z\): citing Pillai [9], finiteness of the integer solution set for
each fixed \(z\); citing Herschfeld [10], at most one integer solution for
all sufficiently large \(z\).  Crandall's bibliography misspells the second
author “Herschefeld”; the primary title and byline give Aaron Herschfeld.
Pillai's eleven-page primary article has now been read.  Its printed
Corollary 1 gives the positive-exponent,
positive-difference statement, but its quantitative proof misstates
Siegel's positive real constant as an integer, falsely infers that
\((a/b)^{1/r}\) has degree \(r\), omits a lower-ratio case, and applies its
lemma to residue classes which can violate the printed “not both powers”
hypothesis.  The literal derivation is therefore not imported.

The fixed-difference conclusion itself is certified independently through
the Pólya theorem which Pillai identifies on printed p. 2.  The official
1918 primary scan states that the adjacent gaps between the increasingly
ordered integers supported on any fixed set of at least two primes tend to
infinity.  Hence only finitely many pairs of \(\{2,3\}\)-smooth integers can
have any fixed nonzero difference.  A separate denominator argument proves
that an integer value of \(2^x-3^y\) forces \(x,y\geq0\), and unique
factorization leaves only \((0,0)\) when \(z=0\).  Thus Crandall's literal
all-integer-exponent wording is now proved, but the proof is not attributed
to Crandall.  Siegel's 1921 primary theorem was also read; applying it at the
actual algebraic degree and treating degree one by rational separation
repairs Pillai's quantitative lemma and residue argument.  Exact records are
`qa/PILLAI-1931-F014-fixed-difference-audit.md`,
`qa/POLYA-1918-F015-smooth-gap-audit.md`, and
`qa/SIEGEL-1921-F016-approximation-audit.md`.  Pólya's explicit Thue
dependency has also been read.  The exact residue-cell cubic need not be
irreducible, so Thue III alone is insufficient; Thue II's exceptional-form
classification applies after coefficient comparison excludes a scalar linear
cube.  Thue I supplies the cited modulo-three template.  The full primary
boundary and the missing Thue II pp. 2--3 raster are recorded in
`qa/THUE-1908-1909-F017-binary-form-audit.md`.

Herschfeld's complete four-page official AMS article has also been read.
Its exact theorem is

\[
 \exists D>0\ \forall d\in\mathbb Z,
 \qquad |d|>D\Longrightarrow
 \#\{(x,y)\in\mathbb N_{>0}^2:2^x-3^y=d\}\leq1.
\]

Thus Herschfeld's parameter is the stronger two-sided \(|d|\), whereas his
printed exponent domain is positive rather than Crandall's integers.  For a
chosen \(0<\delta<1/2\), the proof permits

\[
 D=\max\{2^{x_1+5},3^{y_1+2}\},
\]

where \(x_1\) and \(y_1\) are the ineffective Pillai thresholds for bases
\((2,3)\) and \((3,2)\).  The edition uses its already proved actual-degree
repair of Pillai's theorem rather than importing Pillai's defective literal
derivation.

If two solutions are ordered by \(X>x\), monotonicity forces \(Y>y\), and

\[
 2^x(2^{X-x}-1)=3^y(3^{Y-y}-1).
\]

The exact order identities

\[
 \operatorname{ord}_{3^y}(2)=2\cdot3^{y-1},
 \qquad
 \operatorname{ord}_{2^x}(3)=2^{x-2}\quad(x\geq3)
\]

then force the exponent separations used in both sign contradictions.  The
same proof includes \(y=0\) on the positive-\(d\) branch and \(x=0\) on the
negative-\(d\) branch.  Composing with the separately proved obstruction to
negative integer exponents therefore yields, as an edition consequence,

\[
 |d|>D\Longrightarrow
 \#\{(x,y)\in\mathbb Z^2:2^x-3^y=d\}\leq1.
\]

This closes Crandall's reported scope without attributing the all-integer
extension to Herschfeld.  Fixed-difference finiteness and eventual uniqueness
remain distinct theorems.  Herschfeld's printed report of unpublished
\(|d|\leq100\) calculations is unused.  His final general
\(a^x-b^y=d\) at-most-nine paragraph has a distinct Siegel-1929 dependency
and remains unadmitted pending that primary audit.  Exact details are in
`qa/HERSCHFELD-1936-F018-eventual-uniqueness-audit.md`.

The following paragraph's primitive-root bound for solutions of
\(2^x-3^y=p\) is conditional on the Collatz conjecture and is printed without
derivation.  The omitted construction is now supplied exactly in
`qa/CRANDALL-1978-F020-primitive-root-audit.md`.  An integer-valued
difference first forces \(x,y\geq0\).  If
\(y\geq p/(\log_2 3-1)\), then \(x-y\geq p+1\).  This exponent slack and
\(\operatorname{ord}_p(2)=p-1\) permit a deterministic two-branch choice of
one penultimate cumulative exponent, producing

\[
 0=A_0<\cdots<A_y=x,
 \qquad
 p\mid\sum_{j=0}^{y-1}2^{A_j}3^{y-1-j}.
\]

The quotient by \(p\) is proved to be a positive odd integer greater than
one, so the full converse of Eq. (7.3) gives a nontrivial self-return.  Thus
the printed strict upper bound follows by contraposition under the main
conjecture.  The unconditional content is the explicit
solution-to-monotone-return construction; the numerical bound remains
conditional.  This is not the adjacent special-word divisibility condition
with every \(A_j=j\), and the constructed return time need not be least.

## Continued-fraction cycle bound and its repairs

Let \(t=\log_2 3\) and \(p_n/q_n\) be the continued-fraction convergents,
with \(p_{-1}=1,q_{-1}=0,p_0=a_0,q_0=1\) and

\[
 p_n=a_np_{n-1}+p_{n-2},
 \qquad q_n=a_nq_{n-1}+q_{n-2}.
\]

The continued-fraction list printed in Eq. (7.5) is

\[
 [1,1,1,2,2,3,1,5,2,23,2,2,1,1,55,1,4,3,1,1,15,1,9,2,5,
  7,1,1,4,8,1,11,1,20,2,1,10,1,4,1,1,1,1,1,37,4,55,1,1,49,\ldots].
\]

For a cycle with least member \(m>1\), period \(k\), and cumulative
exponents \(A_j\), Lemmas 7.4--7.5 prove

\[
 2^{A_j}\leq(3+1/m)^j,
 \qquad
 m<\frac{k(3+1/m)^{k-1}}{2^{A_k}-3^k}.
\]

The printed rational-approximation chain needs four exact repairs.

1. Lemma 7.1 omits \(0<y\); as written, \((x,y)=(0,0)\) contradicts its
   strict inequality.  The exact used form has \(0<y<q_n\) and is derived
   from Steuding's published Theorem 3.8 in
   `qa/STEUDING-2005-F021-crandall-continued-fraction-audit.md`.
2. Lemma 7.3 switches from \(n\) to \(m\), leaves \(x\) unquantified, and
   proves its bound using \(|e^u-1|>|u|\).  That analytic inequality holds
   for \(u>0\), not for \(u<0\).  The cycle application has the missing sign:
   \(u=(A_k-k t)\log2>0\), because the return equation gives
   \(2^{A_k}-3^k>0\).  Thus the required repaired form is
   \[
    0<y<q_n,\quad x-y t>0
    \quad\Longrightarrow\quad
    |2^x-3^y|>3^y\log2\,|p_n-q_nt|.
   \]
   The literal statement is already false at the omitted zero endpoint.  No
   positive-\(y\), negative-gap counterexample is asserted here; the printed
   proof simply does not cover that case.
3. Theorem 7.2 explicitly assumes \(k\le q_n\), but then invokes Lemma 7.3,
   whose repaired denominator hypothesis is strict: \(y<q_n\).  The exact
   convergent estimate gives
   \(|p_n-q_nt|<1/q_{n+1}<1/2\) for \(n\geq4\).  If \(A_k\ne p_n\),
   integrality gives a strict lower bound; if \(A_k=p_n\), the positive-gap
   exponential inequality itself is strict.  This supplies the missing
   equality boundary.
4. The printed proof of Corollary 7.2 says the minimum in Theorem 7.2 becomes
   unbounded "as \(n\) increases" for an infinite family.  For fixed \(m\)
   its second term instead tends to zero.  The correct quantifier order is:
   for a proposed fixed period \(L\), first choose an integer \(n\ge4\) with
   \(q_n>L\) (the denominators are unbounded), then choose from a supposed
   infinite family a cycle minimum
   \(m>L(q_n+q_{n+1})/2\).  Both terms then exceed \(L\), a contradiction.

With the first three repairs, Crandall's printed Theorem 7.2 remains

\[
 k>\min\left\{q_n,\frac{2m}{q_n+q_{n+1}}\right\}
 \qquad(n\geq4).
\]

The source's split \(k\ge m/10\) versus \(k<m/10\) correctly yields,
respectively, the trivial second-member bound and the strict factor
\(1-k/(3m)>29/30\); no equality repair is needed there.  Corollary 7.2 still
proves that only finitely many cyclic trajectories can have a fixed
accelerated period.

Printed p. 1282 says that Conjecture (2.1) had been verified for
\(m<10^9\), citing references [1] and [5].  Content and metadata inspection
shows that these are not two witnesses.  Reference [1] is Conway's 1972
conference paper, whose correct pages are 49--52 rather than Crandall's
45--52.  Reference [5], printed as *Zentralblatt für Mathematik*, Bd. 233,
p. 10041, is a miscitation of Zbl 0337.10041, the record for that same Conway
paper; 10041 is an accession suffix, not a printed page.  The duplicated
route therefore supplies no independent corroboration.

Conway's first page defines the ordinary unshortened map and reports the
inclusive range \(n\le10^9\), attributing the computation to D. H. Lehmer,
Emma Lehmer, and J. L. Selfridge.  It supplies no citation, code, algorithm,
machine, range partition, stopping criterion, independent check, checksum,
log, or preserved output.  Its proved generalized-map undecidability theorem
is explicitly said to say nothing about the particular Collatz game.  The
published historical assertion and attribution are content-verified; the
underlying computation is not authenticated or reproducible here.

The exact clock bridge is not assumed.  For an odd starting value, the
successive odd states of the ordinary orbit are precisely the accelerated
orbit, with unshortened time \(A_j+j\).  Since 1 is odd, an ordinary orbit
that reaches 1 reaches it at an accelerated return; conversely an accelerated
self-return from \(m>1\) is periodic and cannot enter the fixed point 1.
Thus Conway's inclusive ordinary-map report implies Crandall's strict
accelerated self-return exclusion without identifying the two clocks.

The least cycle member \(m_0\) is odd.  Conway's inclusive report and the
proved bridge directly give \(m_0>10^9\).  Independently, Crandall's strict
range first gives \(m_0\ge10^9\), while parity excludes equality with the
even endpoint.  Hence both routes give
\(m_0>10^9\), equivalently \(m_0\ge1{,}000{,}000{,}001\), exactly as
Crandall writes.  With \(q_{10}=31867\), \(q_{11}=79335\), Theorem 7.2 gives
its least accelerated period \(\ell\) the bound

\[
 \ell>\min\left\{31867,\frac{2\cdot10^9}{111202}\right\}>17985.
\]

Every positive self-return exponent \(k\) is a multiple of \(\ell\), so the
printed Theorem 7.3 conclusion \(C^k(m)=m\Rightarrow k>17985\) follows.  This
is conditional on the published 1972 report reused in 1978, not on a located
or reproducible computational record.  The variable is accelerated time; the
corresponding whole-integer return lengths satisfy
\(A_k\geq k>17985\) and \(A_k+k>k>17985\), but are not equal to \(k\).

The Section 7 opening also says bounded iterates are strictly less than
\(\sup T_m\); the correct relation is \(\leq\).  Its finite-state argument
still proves that boundedness plus absence of nontrivial returns would imply
the conjecture.

## The generalized \(qx+r\) programme

Printed p. 1291 defines, for positive odd \(q,r\) with \(q>1\),

\[
 C_{q,r}(m)=\frac{qm+r}{2^{e_{q,r}(m)}},
 \qquad e_{q,r}(m)=v_2(qm+r),
 \qquad m\in D^+.
\]

Conjecture 8.1 says that, except for \((q,r)=(3,1)\), some positive odd
starting value fails to reach 1.  The exception is not a proof of the Collatz
conjecture.

For \(r>1\), every odd \(m\equiv0\pmod r\) remains divisible by the odd
integer \(r\) under every iterate, so it cannot reach 1.  For \(r=1\), the
paper gives the exact cycles

\[
 q=5:\quad13\longmapsto33\longmapsto83\longmapsto13,
 \qquad (e_0,e_1,e_2)=(1,1,5),
\]

and

\[
 q=181:\quad27\longmapsto611\longmapsto27,
 \qquad (e_0,e_1)=(3,12).
\]

They correspond respectively to \(2^7-5^3=3\) and
\(2^{15}-181^2=7\).

For \(q=1093\), the source states

\[
 h(m)=1
 \quad\Longleftrightarrow\quad
 m=\frac{2^{364p}-1}{1093},
 \qquad p\in\mathbb Z_{>0},
\]

and says that no height-two value exists.  The omitted finite certificate is

\[
 \operatorname{ord}_{1093}(2)=364,
 \qquad 2^{364}\equiv1\pmod{1093^2}.
\]

Exact witnesses for the order are

\[
 2^{182}\equiv1092,
 \qquad 2^{52}\equiv27,
 \qquad 2^{28}\equiv121\pmod{1093}.
\]

Every height-one predecessor is therefore divisible by 1093.  If it had a
predecessor \(u\), the equation \(1093u+1=2^a m\) would be congruent to
\(1=0\pmod{1093}\), impossible.  Thus no height-two value exists; any finite
height greater than one would contain a height-two tail, so all other values
have infinite height.  The height-one family has counting function
\(O(\log x)\), so the infinite-height set has natural density one among
positive odd integers.

Infinite height is not the same as an unbounded orbit.  The paper explicitly
states that no unbounded \(qx+1\) trajectory was then known.  Its \(7x+1\)
orbit from 3 exceeding \(10^{2000}\) is empirical evidence only.

## Consequence boundary

The complete paper supplies exact accelerated coordinates, a finite-height
address bijection after the two endpoint repairs, fixed-height and total
power-law counting bounds, a return Diophantine equation, a repaired
continued-fraction cycle bound, and three rigorous generalized-map failure
examples.  It supplies no positive-density convergence theorem, no unbounded
orbit, no exclusion of nontrivial \(3x+1\) cycles, and no proof of the Collatz
conjecture.  The article-wide finite computations are independently checked
by `certificates/crandall_1978_checks.py`; the continued-fraction endpoint,
closest-competitor, parity, and historical-bound arithmetic are separately
checked by `certificates/continued_fraction_dependency_checks.py`.  Neither
finite certificate replaces an infinite proof or authenticates the 1978
computation report.
