"""Exact finite regressions for cut concentration and actual passage coverage.
The analytic proof is in audit.tex. This script does not certify it or run Lean.
"""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
from math import comb, ceil, floor
from pathlib import Path
import json
import re

from check_mazur_descent import compositions, exp_interval

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SOURCE = ROOT / "external_literature/mazur_2026_v2/source/Erdos1135"
COUNT = Counter()

def require(ok, message):
    if not ok:
        raise AssertionError(message)

def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0

def exp_negative_lower(x):
    """Rational lower bound for exp(-x), x>=0, by a positive Taylor upper bound."""
    require(x >= 0, "nonnegative exponent magnitude")
    power = 1
    while x > 1:
        x /= 2
        power *= 2
    return 1 / exp_interval(x, 24)[1]**power

def cuts_and_moments():
    for ell in range(1, 13):
        for n in range(1, min(ell, 6)+1):
            words = compositions(n, ell)
            images = set()
            for word in words:
                cuts = tuple(sum(word[:j]) for j in range(1, n))
                borders = (0,) + cuts + (ell,)
                inverse = tuple(borders[j+1]-borders[j] for j in range(n))
                require(inverse == word, "cut map inverse")
                images.add(cuts)
                for q in range(ell):
                    require(sum(s <= q for s in cuts) == sum(s-1 < q for s in cuts),
                            "physical inclusive / source zero-based strict convention")
                COUNT["composition_cut_bijections"] += 1
            require(images == set(combinations(range(1, ell), n-1)),
                    "surjectivity onto every cut set")
            require(len(words) == choose(ell-1, n-1), "composition cardinality")
    for N in range(1, 9):
        for K in range(N+1):
            subsets = tuple(combinations(range(1, N+1), K))
            rho = Q(K, N)
            for q in range(N+1):
                hist = Counter(sum(s <= q for s in subset) for subset in subsets)
                for j in range(N+1):
                    actual = Q(sum(count*choose(h, j) for h, count in hist.items()), len(subsets))
                    exact = Q(choose(q, j)*choose(K, j), choose(N, j))
                    require(actual == exact <= choose(q, j)*rho**j, "factorial moment")
                    COUNT["factorial_moment_identities"] += 1
                for x in (Q(1), Q(3, 2), Q(2)):
                    pgf = sum((Q(count, len(subsets))*x**h for h, count in hist.items()), Q(0))
                    require(pgf <= (1+rho*(x-1))**q, "without-replacement PGF")
                    COUNT["positive_pgf_comparisons"] += 1
                if q:
                    for v in (Q(0), Q(1, 2), Q(1), Q(2)):
                        upper = Q(sum(count for h, count in hist.items() if h-q*rho >= v), len(subsets))
                        lower = Q(sum(count for h, count in hist.items() if q*rho-h >= v), len(subsets))
                        bound = exp_negative_lower(2*v*v/q)
                        require(upper <= bound and lower <= bound, "directed inclusive cut-count tails")
                        COUNT["directed_cut_tail_checks"] += 2

def order_statistic_checks():
    for n in range(3, 7):
        for ell in range(n, min(3*n, 15)+1):
            words = compositions(n, ell)
            for j in range(1, n):
                hist = Counter(sum(a[:j]) for a in words)
                center = Q(j*ell, n)
                for u in (Q(0), Q(1, 2), Q(1), Q(8), Q(17, 2), Q(3*j)):
                    q = floor(center-u)
                    v = ceil(center+u)
                    for a in words:
                        cuts = tuple(sum(a[:k]) for k in range(1, n))
                        require((sum(a[:j]) <= q) == (sum(s <= q for s in cuts) >= j),
                                "lower event with floor")
                        require((sum(a[:j]) >= v) == (sum(s <= v-1 for s in cuts) <= j-1),
                                "upper event with ceiling minus one")
                        COUNT["order_statistic_event_identities"] += 2
                    if 8 <= u <= 3*j:
                        mass = Q(sum(c for h, c in hist.items() if abs(h-center) >= u), len(words))
                        require(mass <= 2*exp_negative_lower(u*u/(63*j)), "directed T3 regression")
                        require(63*(u-1)**2-48*u*u == 15*(u-8)**2+114*(u-8)+15 >= 0,
                                "upper-tail endpoint polynomial")
                        COUNT["directed_T3_checks"] += 1
    for x in (Q(3, 4), Q(1), Q(5, 4), Q(4, 3)):
        require(2*x/(2-x)**2 <= 6, "geometric log MGF second derivative")
        COUNT["geometric_mgf_guard_checks"] += 1
    require(Q(225, 63) == Q(25, 7) and Q(16**2, 32) == 8, "exact tail powers")
    require(3**29 < 2**46, "integer certificate for clock padding")
    COUNT["exact_exponent_and_clock_constants"] += 1

def orbit(N, steps):
    xs, aa = [N], []
    for _ in range(steps):
        value = 3*xs[-1]+1
        a = (value & -value).bit_length()-1
        aa.append(a)
        xs.append(value >> a)
    return xs, aa

def affine(a, N):
    value = Q(N)
    for v in a:
        value = (3*value+1)/2**v
    return value

def block_offset(a):
    return sum((Q(3**(len(a)-i-1), 2**sum(a[i:])) for i in range(len(a))), Q(0))

def orbit_checks():
    for N in range(1, 1500, 2):
        xs, aa = orbit(N, 12)
        for j in range(4):
            for r in (0, 1, 3, 7):
                a = aa[j:j+r]
                offset = block_offset(a)
                require(xs[j+r] == Q(3**r, 2**sum(a))*xs[j]+offset == affine(a, xs[j]),
                        "actual consecutive block identity")
                require(0 <= offset <= 3**r, "offset guard including zero length")
                COUNT["actual_affine_block_identities"] += 1
    for N in range(100001, 100402, 2):
        xs, aa = orbit(N, 10)
        for r in range(1, 9):
            H = max(abs(sum(aa[:k])-2*k) for k in range(r+1))
            for B in (3, 10, 50):
                budget = 2**(2*H)*B+3**r
                if xs[r] > budget:
                    require(all(value > B for value in xs[:r]), "reverse-prefix exclusion")
                    COUNT["nonvacuous_reverse_prefix_exclusions"] += 1
    for N in range(51, 1600, 2):
        xs, aa = orbit(N, 100)
        for B in (20, 50, 200):
            if N <= B:
                continue
            t = next((j for j, x in enumerate(xs) if x <= B), None)
            if t is None:
                continue
            H = max(abs(sum(aa[:k])-2*k) for k in range(t+1))
            for h in range(1, min(t, 4)+1):
                if 2*3**(h-1) > B:
                    continue
                M = xs[t-h]
                require(Q(3, 8)*Q(4, 3)**h*Q(1, 2**(2*H))*B < M
                        <= Q(4, 3)**h*2**(2*H)*B, "lost-window exact bounds")
                require(next(j for j, x in enumerate(xs[t-h:]) if x <= B) == h, "first-hit shift")
                COUNT["forward_stepback_and_first_hit_checks"] += 1
    n, h, r = 90, 80, 10
    N, B = 2*4**n+1, 2*3**n+1
    xs, aa = orbit(N, n)
    M = 2*4**h*3**r+1
    require(aa == [2]*n and xs[r] == M and xs[-1] == B, "exact all-two witness")
    require(all(x > B for x in xs[:-1]) and M > B+3**r, "nonvacuous first-hit endpoint budget")
    require(affine(aa[:r], N) == M, "witness affine record")
    COUNT["large_exact_first_passage_witnesses"] += 1

def exceptional_event_checks():
    # Exhaust all pairs of subsets of a five-element probability space.
    weights = [Q(i, 15) for i in range(1, 6)]
    for A in range(32):
        for U in range(32):
            bad = [i for i in range(5) if ((A >> i) & 1) != ((U >> i) & 1)]
            difference = sum((weights[i]*(((A >> i) & 1)-((U >> i) & 1)) for i in range(5)), Q(0))
            require(abs(difference) <= sum((weights[i] for i in bad), Q(0)), "one complement charge")
            COUNT["coefficient_one_event_mass_checks"] += 1

def main():
    audit = (HERE/"audit.tex").read_text(encoding="utf-8")
    start = audit.index(r"\section{Concentration from cuts and the actual passage event}")
    end = audit.index("\n"+chr(92)+"section{", start+10)
    section = audit[start:end].strip()
    expected = section.replace("mazur-", "Mazur-").replace(r"\section{", r"\subsection{", 1)
    cumulative = (ROOT/"tex/chapters/01m_mazur_terminal_rates.tex").read_text(encoding="utf-8")
    require(expected in cumulative, "complete concentration and coverage proof propagation")
    labels = re.findall(r"\\label\{([^}]+)\}", audit)
    require(len(labels) == len(set(labels)), "duplicate labels")
    require(set(re.findall(r"\\(?:ref|eqref)\{([^}]+)\}", audit)) <= set(labels), "unresolved references")
    require("For the original A5 sub-bands, with the band-mass and assembled-test" in section,
            "terminal bound must retain its stronger band-mass guards")
    COUNT["written_proof_propagation_checks"] += 1
    cuts_and_moments()
    order_statistic_checks()
    orbit_checks()
    exceptional_event_checks()
    files = ["ND/Fourier/FixedTotalBars.lean", "ND/Fourier/FixedTotalConcentration.lean",
             "ND/Fourier/FixedTotalPGF.lean", "ND/Fourier/FixedTotalMGF.lean",
             "ND/Fourier/FixedTotalTail.lean", "ND/Fourier/FixedTotalT3.lean",
             "ND/Fourier/FixedTotalRatioTails.lean",
             "ND/Band/A5TerminalAtomCoverage.lean", "ND/Band/A5TerminalAtomCoverageProbability.lean",
             "ND/Band/A5GoodTimeLocalization.lean", "ND/Band/A5GoodEPrimeIngress.lean",
             "Tao/Section5/ReversePrefix.lean", "Tao/Section5/ReversePrefixScalar.lean",
             "Tao/Section5/PassLostWindow.lean"]
    report = {"status": "passed", "counts": dict(COUNT),
              "scope": "Exact finite regressions, directed rational exponential tests and proof-text propagation; not an analytic proof, global Collatz verification or Lean replay.",
              "source_package_commit": "ca3dd0d63920411213403092aecc6946619eb082",
              "source_hashes": {p: sha256((SOURCE/p).read_bytes()).hexdigest() for p in files},
              "artifact_hashes": {p: sha256((HERE/p).read_bytes()).hexdigest()
                                 for p in ("audit.tex", "CLAIMS.json", "check_mazur_coverage.py")},
              "large_witness_scope": "An exact finite orbit with all valuations two; not the asymptotic schedule of the coverage theorem.",
              "lean_started": False, "public_mutations": False}
    (HERE/"mazur_coverage_checks.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
