# LAARHOVEN-DEWEGER-1209-F006 — finite and adic De Bruijn audit

## Status and controlling witnesses

This is a content-level audit of Thijs Laarhoven and Benne de Weger,
*The Collatz conjecture and De Bruijn graphs*, arXiv:1209.3495v1.  It covers
the complete mathematical source, not merely the title, abstract, routing
record, or earlier F013 orientation check.  It is a working-edition
checkpoint, not a completion claim for the Collatz corpus.

- frozen document route: `DOCROUTE-COL-031AE8C7B4763CF5E8D2`
- frozen index routes:
  `ROUTE-COL-091F8EFB870FD5F78876`,
  `ROUTE-COL-A921D0C73A9CC8377315`, and
  `ROUTE-COL-32B2942DB3BF022A116E`
- arXiv identity: `1209.3495v1`, submitted 2012-09-16 15:37:48 UTC
- version-pinned source archive:
  `C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/source/1209.3495v1.eprint`
- archive bytes: 14903
- archive SHA-256:
  `1d9a27d86565f52dd7bd4cae32eb3fc724fbd7abe725229dacca8efcbfc692a8`
- extracted controlling TeX:
  `C:/Users/LOCAL_USER/Documents/arxiv_latex/library/collatz_reconstruction/latex/1209.3495v1/main.tex`
- TeX bytes: 52459
- TeX SHA-256:
  `51b2c072646d33fc7f37fcd23e966f4435dc3e2026cd3fe83b6717829c31e0eb`
- official arXiv-served v1 PDF:
  `C:/Users/LOCAL_USER/Documents/Papors/OS/1209.3495v1 The Collatz conjecture and De Bruijn graphs.pdf`
- PDF pages: 9
- PDF bytes: 241098
- PDF SHA-256:
  `ffc518643cd06f71d8f13892d08c5f643d2e8f30f0e0dd987c9682394eb75327`

The routed PDF is byte-identical to the official arXiv-served v1 PDF checked
at this checkpoint.  Its metadata creation and modification time, and its
visible title date, are 27 November 2024.  This is not evidence of a second
mathematical version.  The PDF retains the banner
`arXiv:1209.3495v1 [math.NT] 16 Sep 2012`; the official history contains only
v1; the pinned source archive is the current official v1 archive; and its
single TeX file is byte-identical to the extracted controlling TeX.  Source
line 36 is `\date{\today}`, so a later rendering necessarily prints its render
date.  The evidence establishes a later official rendering of unchanged v1
source.  It does not establish why that rendering was produced.

The complete 509-line source was read.  The main exact locators are:

- lines 47–57: map convention, conjecture, and introduction;
- lines 65–199: modular graphs, finite De Bruijn graphs, finite parity map,
  path counts, and the proposed natural-number recovery;
- lines 205–230: infinite binary graph, 2-adic Collatz graph, and conjugacy;
- lines 239–345: component assertions, periodicity conjecture, cycle counts,
  Lyndon words, and the rational-cycle / `3n+b` discussion;
- lines 357–386: odd `an+b` maps;
- lines 390–441: general `p`-branch maps and the ternary example.

All four active theorem environments—lines 139–152, 218–224, 367–380, and
402–415—lack active proof environments.  Lines 160–166 contain a commented,
inactive proof attempt.  Every theorem used below is therefore either proved
in the edition or crosswalked to an already proved result; no theorem is
admitted merely because it is printed.

## Exact finite objects: relations, not self-maps

Let

\[
 V_k=\mathbb Z/2^k\mathbb Z,\qquad k\geq1.
\]

Source lines 67 and 81–84 define an edge from \([a]_k\) to \([b]_k\) when
some integer lifts satisfy \(T(a_1)=b_1\).  For the shortened Collatz map this
is exactly the set-valued relation

\[
 T_k([a]_k)
 =\{[T(a)]_k,[T(a)+2^{k-1}]_k\}.
\]

Indeed, all lifts have the same parity.  Replacing a lift by one plus
\(2^k\) changes its branch value by an odd multiple of \(2^{k-1}\), hence by
exactly \(2^{k-1}\) modulo \(2^k\).  Thus each vertex has two distinct
successors.  The finite graph does not define a deterministic quotient of
\(T\); division by two loses one input bit.

The source identifies a word \(b_0\cdots b_{k-1}\) with
\(\sum_{i<k}b_i2^i\), least significant digit first.  Its De Bruijn forward
relation is

\[
 \sigma_{2,k}(b_0\cdots b_{k-1})
 =\{b_1\cdots b_{k-1}c:c\in\{0,1\}\}.
\]

In numeric coordinates this is the two-element set consisting of the right
shift and that value plus \(2^{k-1}\).  This, too, is a relation
\(V_k\to\mathcal P(V_k)\), not a point map.  By contrast, source lines
205–229 define deterministic maps on \(\mathbb Z_2\): the complete input has
no missing next bit.

## Finite parity isomorphism and orientation

For \([a]_k\in V_k\), define

\[
 q_k([a]_k)=\sum_{i=0}^{k-1}
       (T^i(a)\bmod2)2^i.
\]

This is source \(\Phi_k\), not an editorial normalization.  The first \(k\)
parities depend exactly on the input modulo \(2^k\), so the formula is
well-defined.  Bernstein–Lagarias's isometry, already reconstructed in
`CLM-COL-000009`, gives

\[
 q_k([a]_k)=Q_3(a)\pmod{2^k}
\]

and proves that \(q_k\) is a permutation.  For a subset \(A\subseteq V_k\),
write \(q_k[A]=\{q_k(a):a\in A\}\).  The exact source relation is

\[
 q_k[T_k(a)]=\sigma_{2,k}(q_k(a)).
\]

The first \(k-1\) output digits are the input itinerary digits 1 through
\(k-1\).  The two lift classes modulo \(2^{k+1}\) give the two possible next
digits.  This proves both inclusions and every fibre is a singleton.  The
inverse is the reduction modulo \(2^k\) of Bernstein–Lagarias's
\(\Phi_3=Q_3^{-1}\).

The notation boundary is consequential:

- Laarhoven–de Weger \(\Phi_k\) and \(\Phi\) map a state to its chronological
  itinerary;
- Bernstein–Lagarias \(Q_3\) has that orientation;
- Bernstein–Lagarias \(\Phi_3\) has the inverse orientation.

Thus source line 156 is a conjugacy of finite relations, with the inverse
applied elementwise to subsets.  It is not a deterministic finite-dynamical
conjugacy.  The infinite relation in lines 218–229 is the already recorded
deterministic conjugacy \(Q_3T=SQ_3\).

## Exact path counts and the probability boundary

Let \(A_k\) be the adjacency matrix, with entries counting directed edges.
After \(k\) De Bruijn steps all \(k\) original digits have been discarded.
For each chosen terminal word there is exactly one sequence of \(k\) appended
digits.  Therefore

\[
 A_k^k=J,
 \qquad
 A_k^\ell=2^{\ell-k}J\quad(\ell\geq k),
\]

where \(J\) is the all-ones matrix.  The same holds for \(C(k)\) by \(q_k\).
This verifies the exact count in source line 191.

Uniformity is a conditional probability statement: if at each finite-graph
step one chooses each outgoing edge with probability \(1/2\), the endpoint
modulo \(2^k\) is uniform after \(k\) steps.  Equivalently, it describes a
uniform unresolved higher-bit model.  The source phrase that the low bits
tell us “absolutely nothing” about the deterministic integer \(T^k(n)\) is
not admitted without such a probability model.  The path count neither makes
an integer iterate random nor proves statistical independence for positive
integer orbits.

## Projective compatibility and the actual inverse limit

Let \(\rho_{k+1,k}:V_{k+1}\to V_k\) be reduction.  The encoders satisfy

\[
 \rho_{k+1,k}q_{k+1}=q_k\rho_{k+1,k}.
\]

For an edge \(([a]_k,[b]_k)\in E_k\), the exact lower-precision condition is

\[
 b\equiv T(a)\pmod{2^{k-1}}.
\]

Thus edge reduction sends \(E_{k+1}\) onto \(E_k\), although the two
successors of one fixed level-\((k+1)\) vertex reduce to only one of the two
successors of its level-\(k\) image.  Equality of pointwise successor sets
under reduction would be false.

The inverse limit of the vertex systems is \(\mathbb Z_2\).  If compatible
vertices \(x,y\in\mathbb Z_2\) form an edge at every finite level, then
\(y\equiv T(x)\pmod{2^{k-1}}\) for all \(k\), hence \(y=T(x)\).  Conversely,
an actual 2-adic edge reduces to an edge at every level.  Therefore the
inverse limit of the edge relations is exactly the graph of deterministic
\(T:\mathbb Z_2\to\mathbb Z_2\); the corresponding De Bruijn limit is the
graph of the digit shift.  The compatible family \((q_k)_k\) has inverse
limit \(Q_3\).

Source line 199 says informally that edges occurring in infinitely many
finite graphs recover the natural-number graph.  Across changing vertex sets
that phrase needs a common ambient set.  The exact repair is: for fixed
\(a,b\in\mathbb N_0\), represented literally once \(a,b<2^k\),

\[
 b=T(a)
 \quad\Longleftrightarrow\quad
 ([a]_k,[b]_k)\in E_k\text{ for all sufficiently large }k
 \quad\Longleftrightarrow\quad
 ([a]_k,[b]_k)\in E_k\text{ for infinitely many }k.
\]

The reverse implication follows because every such finite edge gives
\(b\equiv T(a)\pmod{2^{k-1}}\); one occurrence with
\(2^{k-1}>|b-T(a)|\) forces equality.  No untyped “limit graph” is used.

## Periodic components and the corrected necklace count

Under the conjugacy, exact \(k\)-cycles correspond to binary purely periodic
words of least period \(k\), modulo cyclic rotation.  If \(M_k\) denotes the
number of components containing a cycle of exact length \(k\), then

\[
 2^k=\sum_{d\mid k}dM_d,
 \qquad
 M_k=\frac1k\sum_{d\mid k}\mu(d)2^{k/d}
     =\frac{2^k}{k}+O(2^{k/2}).
\]

Every exact \(d\)-cycle contributes its \(d\) distinct phases to the
\(2^k\) words whose periods divide \(k\); Möbius inversion proves the second
formula.  The first values are

\[
 (M_k)_{k\geq1}=(2,1,2,3,6,9,\ldots).
\]

Source lines 303–309 print the correct divisor identity and Möbius formula,
but the asymptotic switches to an unbound variable \(n\).  Line 311 prints
`(1,2,1,2,3,6,...)`, contradicting both the formula and line 275's two
fixed-point components.  These are forced source corrections, not a change
of convention.  A cyclic De Bruijn sequence corresponds to a Hamiltonian
cycle; lines 129 and 315 call it a path while their wrap-around digits supply
the closing edge.

## Exact predecessor fibres and the failed automorphism sentence

Every \(y\in\mathbb Z_2\) has exactly two predecessors under the shortened
map:

\[
 x_0=2y,
 \qquad
 x_1=\frac{2y-1}{3}.
\]

The first is even, the second is odd, both map to \(y\), and the two branch
equations show that there are no others.  They are distinct because their
equality would give \(4y=-1\), impossible in \(\mathbb Z_2\).  Both
predecessors lie in the same weak component as \(y\).  Consequently the
forward map is two-to-one on every component and is not a function
automorphism.  Source line 241's “forward mapping is an automorphism” is
false under the ordinary meaning of automorphism.  The separate assertion
that the aperiodic components are pairwise isomorphic is not needed for any
downstream result here.

## Generalized maps: the exact coefficient gate

For odd \(a,b\), source lines 360–380 define

\[
 T^{(a,b)}(n)=
 \begin{cases}
  n/2,&n\equiv0\pmod2,\\
  (an+b)/2,&n\equiv1\pmod2.
 \end{cases}
\]

This is the retained-\(d=2\) Matthews presentation
\((m_0,r_0)=(1,0)\), \((m_1,r_1)=(a,-b)\).  Oddness gives both the branch
congruence and the unit condition.  The source's finite and infinite parity
encoders are therefore exact specializations of the constructive generalized
itinerary theorem `CLM-COL-000016`; their orientation is
\(\operatorname{It}_{T^{(a,b)}}\), not its inverse.  This encoder is \(Q_3\)
only at \((a,b)=(3,1)\).  No new infinite conjugacy is needed.

For the broader source formula

\[
 f(n)=\frac{a_i n+b_i}{p}\qquad(n\equiv i\pmod p),
\]

the required hypotheses are not “appropriately chosen” in an unspecified
sense.  The exact gates are

\[
 a_i i+b_i\equiv0\pmod p
 \quad\text{and}\quad
 \gcd(a_i,p)=1
 \qquad(0\leq i<p).
\]

The first makes the branch integer-valued.  Writing \(n=i+pt\), its next
digit is

\[
 \frac{a_i i+b_i}{p}+a_it\pmod p.
\]

The second condition makes this affine map a permutation of the \(p\) next
digits, with singleton fibres.  It is exactly the retained Matthews unit
condition with \(m_i=a_i,r_i=-b_i\).  If a multiplier is not a unit, the
range and fibre sizes are those in `CLM-COL-000017`, so the full De Bruijn
claim fails.  For example, taking \(a_i=p,b_i=0\) on every branch gives the
integer-valued identity map, whose modular graph is not \(B(p,k)\).

Source lines 393–415 do not state these gates, do not explicitly define
\(x_i^{(f)}\), and do not say that \(p\) is prime even though
\(\mathbb Z_p\) is invoked.  The edition admits the theorem only at the exact
unit-gated scope already proved for any retained base \(d\geq2\); for prime
\(p\) this is the usual \(p\)-adic specialization.  The displayed ternary
example has multipliers \(2,4,4\), all units modulo 3, so it lies within the
repaired scope.

## Rational cycles and the scaling quotient

Source lines 317–321 use the correct identity

\[
 T(n/b)=T^{(3,b)}(n)/b
\]

for odd \(b\).  The source's first unqualified one-to-one sentence requires
the primitive reduced-denominator condition or the explicit common-scaling
quotient.  If \((x_j)\) is a rational \(T\)-cycle and
\(b>0\) is its least common odd denominator, then \(n_j=bx_j\) is an integer
\(T^{(3,b)}\)-cycle.  Conversely such a pair scales back to a rational
\(T\)-cycle.  Replacing
\((b,(n_j))\) by \((cb,(cn_j))\) for an odd positive \(c\) leaves the
rational cycle unchanged.  Thus the exact bijection is with equivalence
classes generated by common odd scaling,
or with the unique primitive representative satisfying
\(\gcd(b,n_0,\ldots,n_{k-1})=1\).  If the cycle has length \(k\) and \(m\)
odd phases, that primitive denominator divides \(2^k-3^m\).  When
\(m\geq1\), this integer is coprime to 3.  When \(m=0\), every phase is
division by 2, periodicity forces the zero cycle, and the primitive denominator
is 1.  Thus the primitive denominator is coprime to 3 in both cases.  Without
the quotient, the cycles \(\{b,2b\}\)
of \(T^{(3,b)}\) all scale to the same rational cycle \(\{1,2\}\).  The
source's later phrase “having denominator \(b\)” can naturally mean the exact
reduced common denominator; that reading already chooses the primitive
representative and is correct.  Lagarias 1990, now read from the official
publisher scan, explicitly states the raw gcd strata and the primitive
condition; it does not omit that distinction.

## Remaining source defects, conjectures, and nonclaims

The following statements are retained as source issues or context and are not
used as theorems.

1. Line 51 glosses “no divergent paths” by
   \(\lim_kT^k(n)<\infty\).  Even the \(1\leftrightarrow2\) orbit has no
   limit.  The exact boundedness condition is
   \(\sup_kT^k(n)<\infty\); bounded integer orbits are eventually periodic,
   after which exclusion of nontrivial cycles gives the conjecture.
2. Line 79 quantifies `for all n` inside a statement about one starting
   value; the argument requires `for all k`.
3. Line 131's first omitted itinerary digit is \(x_k\), not \(x_{k+1}\).
   The commented proof at lines 160–166 is inactive and its opening sentence
   reverses the graph arrow before its following equivalence states the
   correct orientation.
4. Line 212 defines the function named \(\sigma_2\) using the display symbol
   \(\sigma\); this is notation, not a second map.
5. The rational-periodicity statement at lines 273 and 325 is explicitly a
   conjecture.  It is not used to classify rational components.
6. The average-multiplier discussion at line 364 and the component forecasts
   at line 384 are heuristics and conjectural context, not conditional
   theorems or endpoint evidence.
7. Source line 230's positive-integer reformulation through
   \(\frac13\mathbb Z\setminus\mathbb Z\) depends on earlier cited
   literature.  It was deferred at this checkpoint and was subsequently
   registered at exact conjectural scope after the primary dependency audit.

Nothing in the finite graph isomorphism, path count, inverse-limit
construction, cycle count, or generalized unit-gated conjugacy proves that a
positive integer reaches 1.  The unresolved problem is the exact image of the
embedded positive integers under the itinerary conjugacy, not the existence
of the conjugacy itself.

## Independent mathematical recheck and dependency-gate resolution

An independent fresh-agent audit checked `CLM-COL-000043` through
`CLM-COL-000050` and `MOR-COL-000013` through `MOR-COL-000014`.  It found no
theorem- or morphism-level failure.  It separately verified finite relation
typing, edge-projection surjectivity, the deterministic inverse limit, exact
path multiplicities, component-versus-necklace counting, the generalized
unit gate, predecessor fibres, and the common-scaling/primitive-representative
bijection.  It did find the local false identification of the general
\(T^{(a,b)}\) encoder with \(Q_3\), together with the residue-edge notation,
periodic-block wording, and source-criticism precision points repaired above.

Before following the consequential citations, the frozen ledgers
`state/index_routes.jsonl` and `state/document_routes.jsonl` were checked,
without a filesystem rescan or ledger mutation, for the exact bibliographic
keys of Bernstein's *A Non-Iterative 2-adic Statement of the 3n+1
Conjecture* (1994), Lagarias's *The Set of Rational Cycles for the 3x+1
Problem* (1990), and Lagarias's *The 3x+1 Problem and its Generalizations*
(1985), including `Periodicity Conjecture`, `bernstein94`, `lagarias85b`, and
`lagarias90`.  No exact route record was found.  These sources must therefore
be acquired from primary official, publisher, or author witnesses and pinned
before any dependent claim is enlarged.  The frozen index remains unchanged.

That dependency gate was subsequently resolved by the controlling primary
witnesses recorded in `qa/BERNSTEIN-1994-F007-noniterative-adic-audit.md`,
`qa/LAGARIAS-1985-F008-parity-periodicity-audit.md`, and
`qa/LAGARIAS-1990-F009-rational-cycles-audit.md`.  The exact results and new
source defects are propagated in
`tex/chapters/01d_primary_parity_dependencies.tex`; the frozen route ledgers
were not mutated or rescanned.
