# V7 baseline and first-entry-law extension

Controlling user messages: `raw/USR-0017-tao-v7-baseline.txt` in the corpus root.
Date: 2026-09-04. This record is local audit history, not reader exposition.

The preceding manuscript compared Tao V5's half-reserve with V7's 0.99
reserve. That comparison established attribution: the change was Tao's own.
It is not a contribution of this preprint. The historical calculation and
source hashes remain in the earlier review records and receipts. The live
paper now uses V7 alone for its mathematical baseline and retains only the
explicit sufficient bound for the reserve actually used there.

The old text's numerical comparison was rho*=log(2)/(4log(4/3))=0.602355...,
with (log2)^2/(4log(4/3))=0.417520..., half log2=0.346573..., and
0.99 log2=0.686215.... V5's displayed estimate also omitted a log2 factor.
None of that historical observation proves an improvement of V7.

The mathematical extension being checked is exact compatibility at all
thresholds for a common sequence of input measures. The old corollary fixed
the threshold u as the base of its sequence, and related only thresholds
v=u^(alpha^k). Instead fix one b>=s*, put t_j=b^(alpha^j), and for each x>=1
consider K_x mu_(t_(j+1)). Once t_j>=x, adjacent differences are bounded by
e(t_j) through K_x K_(t_j)=K_x. Their geometric tail gives convergence with
an explicit rate; the same finite input sequence gives compatibility for
every x<=y. A tuple of thresholds is the deterministic image of its largest
threshold, giving simultaneous distributional convergence with the same
bound, without a factor for the number of thresholds.

This extends the present draft's distributional corollary. Tao's V7
Proposition1.11 remains its analytic input. V7 Section3 already proves the
uniform fixed-threshold orbit-minimum bound. No improvement to that bound,
independent full analytic proof, phase independence, or priority claim follows.

Separate unfinished source-audit findings preserved for the next corpus
propagation: the affine antecedent's Theorem10.1 already explicitly proves
affine cyclic transport; its Theorem10.3 misstates equality of pointed
periodic words; the H1 locator is A55/C56 and its exact domain is weighted
ell2. See research_companion/audit/affine_antecedent_version_comparison_20260904.md.
Do not infer these changes are already in the live critical reader.
