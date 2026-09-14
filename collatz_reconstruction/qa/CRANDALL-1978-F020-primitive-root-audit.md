# Crandall 1978 primitive-root implication: exact constructive audit

## Controlling source and locator

- Source: Richard E. Crandall, “On the ‘3x + 1’ Problem,” *Mathematics of
  Computation* **32** (1978), 1281–1292, `SRC-COL-000001`.
- Controlling manifestation:
  `C:/Users/LOCAL_USER/Documents/Papors/OS/on-the-3x-1-problem-5cygpgqcjg.pdf`.
- SHA-256: `acafa9070e7c5e4b167d70d7cace81da39489710804c510ff8db4369133217f4`.
- Exact locator: printed p. 1288, the paragraph immediately after the
  fixed-difference reports and immediately before the separate sufficient
  divisibility obstruction.

Crandall states that, assuming Conjecture (2.1), if $2$ is a primitive root
of a prime $p$, every integer solution of

\[
2^x-3^y=p
\]

must satisfy $y<p/(t-1)$, where $t=\log_2 3$.  The paper gives no proof in
that paragraph.  The following construction supplies it without identifying
it with the adjacent special case $A_j=j$.

## Frozen-index routing result

The immutable ledgers were queried before the reconstruction for
`primitive root`, `primitive-root`, `Artin`, `2^x-3^y=p`, the displayed bound,
and Crandall.  They return only the already admitted Crandall work:

- `DOCROUTE-COL-EC8037330D561573C31E`;
- `ROUTE-COL-591DD74C83DB96290076`;
- `ROUTE-COL-F9379F3657AAC3711D2B`.

No separate indexed paper supplies the omitted proof.  The argument below
uses only the definition of a primitive root and the already proved exact
return equation.  The frozen route files were neither rescanned nor mutated.

## Domain and exact slack

Let $p$ be an odd prime with
$\operatorname{ord}_p(2)=p-1$, and suppose

\[
(x,y)\in\mathbb Z^2,\qquad 2^x-3^y=p,
\qquad y\geq\frac{p}{t-1}.
\]

The existing denominator obstruction for an integer value of
$2^x-3^y$ forces $x,y\geq0$.  The lower bound makes $y>0$.  If $p=3$,
reduction of the equation modulo $3$ would give $2^x\equiv0\pmod3$, so
in this branch $p\geq5$.  Because $0<t-1<1$, the lower bound also gives
$y>p\geq5$, so every index range in the selector construction is
nonempty.

Since $2^x>3^y$, $x>ty$.  Therefore the integer $L=x-y$ satisfies

\[
L>(t-1)y\geq p,
\qquad L\geq p+1.
\]

The logarithmic lower bound has the exact integer form

\[
y\geq\frac{p}{t-1}
\quad\Longleftrightarrow\quad
3^y\geq2^{p+y};
\]

no floating-point comparison is needed.

## Deterministic construction of the monotone word

Set the return length $k=y$ and endpoint $A_y=x$.  Initially put
$A_j=j$ for $0\leq j\leq y-2$, and define

\[
R_0=\sum_{j=0}^{y-2}2^j3^{y-1-j}.
\]

There are two exhaustive cases.

1. If $R_0\not\equiv0\pmod p$, choose the least
   $A_{y-1}\in[y-1,x-1]\cap\mathbb Z$ such that
   $2^{A_{y-1}}\equiv-R_0\pmod p$.
2. If $R_0\equiv0\pmod p$, retain $A_j=j$ through $j=y-3$, set
   $A_{y-2}=y-1$, and put
   \[
   R_1=\sum_{j=0}^{y-3}2^j3^{y-1-j}+2^{y-1}3.
   \]
   Then
   $R_1-R_0=3\cdot2^{y-2}\not\equiv0\pmod p$.  Choose the least
   $A_{y-1}\in[y,x-1]\cap\mathbb Z$ such that
   $2^{A_{y-1}}\equiv-R_1\pmod p$.

The first selection interval has $L+1$ elements and the second has $L$
elements.  Each therefore contains a complete residue system of exponents
modulo $p-1$.  Because $\operatorname{ord}_p(2)=p-1$, the corresponding
powers of $2$ run through every element of
$(\mathbb Z/p\mathbb Z)^\times$.  Both least-exponent selectors exist, and
in both branches

\[
0=A_0<A_1<\cdots<A_y=x.
\]

## Exact return and contradiction

Define

\[
S=\sum_{j=0}^{y-1}2^{A_j}3^{y-1-j},
\qquad m=S/p.
\]

The selector gives $p\mid S$, so $m$ is integral.  Exactly the $j=0$
summand is odd; hence $S$, and therefore $m$, is odd.  Since
$0<t-1<1$, one has $y>p$, and

\[
S\geq3^{y-1}\geq3^p>p.
\]
Here $3^p>p$ is the elementary induction $3^n>n$ for $n\geq1$.

Thus $m>1$.  Finally,

\[
m(2^{A_y}-3^y)=mp=S
=\sum_{j=0}^{y-1}2^{A_j}3^{y-1-j}.
\]

This is exactly Crandall’s equation (7.3).  Its already proved converse gives
$C_{\mathrm{Cr}}^y(m)=m$.  Hence a solution at or beyond the bound
constructs a nontrivial accelerated return and falsifies Conjecture (2.1).
The printed conditional strict bound follows by contraposition.

## Typed boundaries and nonclaims

- No solution at or beyond the bound is asserted to exist.
- The proof constructs a general monotone cumulative-exponent word.  It does
  not prove the adjacent stronger-looking condition
  $0<2^a-3^b\mid2^{a-b}-1$, which is the special word $A_j=j$.
- The constructed exponent $y$ is a return time; the least period may be a
  proper divisor.
- Primitive-root status is used only as the exact surjectivity of
  $a\mapsto2^a\pmod p$ on nonzero residues.  No Artin-density statement is
  imported.
- The unconditional result is the explicit solution-to-return construction.
  The numerical upper bound is conditional on the Collatz conjecture.
- The proof does not use Herschfeld’s eventual uniqueness theorem, Siegel’s
  inaccessible 1929 theorem, or any unpublished computation.

## Certificate

`certificates/primitive_root_return_checks.py` pins the source and frozen
route hashes, checks both residue branches over every prime below 300 for
which (2) is primitive and over a deterministic range of slack parameters,
checks strict monotonicity, divisibility, parity, and least-selector status,
and separately enumerates bounded genuine equations $2^x-3^y=p$.  These
finite checks are subordinate to the arbitrary-parameter proof in TeX.
