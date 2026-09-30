"""Exact regressions for the written finite Mazur reconstruction.
One standard-library process. No Lean or imported source proof code.
Finite tests do not prove the all-parameter statements or analytic inputs.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
from math import comb
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SRC = ROOT / "external_literature/mazur_2026_v2/source/Erdos1135"


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def step(n):
    x = 3*n+1
    a = (x & -x).bit_length()-1
    return x >> a, a


def first_hit(n, B, bound=128):
    for h in range(bound+1):
        if n <= B:
            return h
        n, _ = step(n)
    return None


def main():
    counts = Counter()
    records = []
    for nu in range(1, 5):
        for word in product(range(1, 5), repeat=nu):
            ell, c = 0, 0
            for a in word:
                c = 3*c + 2**ell
                ell += a
            for M in range(1, 100, 2):
                numerator = 2**ell*M-c
                if numerator <= 0 or numerator % 3**nu:
                    continue
                N = numerator//3**nu
                require(N > 0 and N % 2 == 1, "compatible positive odd inverse")
                x, observed = N, []
                for _ in word:
                    x, a = step(x)
                    observed.append(a)
                require(tuple(observed) == word and x == M, "actual valuation decoding")
                N0 = Q(2**ell*M, 3**nu)
                alpha = Q(c, 2**ell*M)
                require(N == (1-alpha)*N0 and Q(1, 1)/N0 == (1-alpha)/N,
                        "exact nominal/actual identities")
                records.append((nu, word, ell, c, M, N, N0, alpha))
                counts["affine_inverse_and_actual_word"] += 1
    for B in (1, 5, 20, 50):
        groups = defaultdict(list)
        for rec in records:
            nu, word, ell, c, M, N, N0, alpha = rec
            h = first_hit(M, B)
            if h is not None and 1 <= h <= 6 and nu <= h+1:
                groups[h].append(rec)
        for h, group in groups.items():
            sources = [rec[5] for rec in group]
            require(len(sources) == len(set(sources)), "short-window injectivity")
            counts["injective_time_windows"] += 1
            counts["injective_terminal_records"] += len(sources)
            # delta <= log(2) is exactly alpha <= 1/2; no float logs.
            group = [rec for rec in group if rec[7] <= Q(1, 2)]
            if not group:
                continue
            rho = max(rec[7] for rec in group)
            endpoint = min(rec[6] for rec in group)
            bands = (Q(1), Q(3), Q(7), Q(13), Q(40), Q(80),
                     endpoint, Q(2,5)*endpoint)
            for z in bands:
                U = Q(5, 2)*z
                band = [n for n in range(1, int(U)+2, 2) if z <= n < U]
                D = len(band)
                H = sum((Q(1,n) for n in band), Q(0))
                require(D > 0 and H > 0, "nonempty exact sampling band")
                lower = {n for n in range(1, int(z)+2, 2) if z/2 <= n < z}
                upper = {n for n in range(1, int(U)+2, 2) if U/2 <= n < U}
                UH = UF = IH = IF = Q(0)
                seen_mismatch = set()
                for nu, word, ell, c, M, N, N0, alpha in group:
                    P, R = z <= N < U, z < N0 < U
                    UH += Q(int(P), N)/H
                    UF += Q(int(P), D)
                    IH += int(R)/(N0*H)
                    IF += Q(int(R), D)
                    if P != R:
                        require(N not in seen_mismatch, "boundary counted once")
                        seen_mismatch.add(N)
                        require(N in (lower if R else upper), "oriented boundary shell")
                        counts["nominal_only" if R else "actual_only"] += 1
                    if N0 == z or N0 == U:
                        counts["strict_nominal_endpoint_fixtures"] += 1
                shellH = sum((Q(1,n) for n in lower | upper), Q(0))/H
                require(0 <= UH <= 1 and 0 <= UF <= 1, "actual union probability")
                require(abs(UF-IF) <= Q(len(lower | upper), D), "flat shell bound")
                require(abs(UH-IH) <= rho*UH+shellH, "harmonic shell bound")
                require(IF <= UF+Q(len(lower), D), "one-sided flat cap")
                require(IH <= UH+sum((Q(1,n) for n in lower), Q(0))/H,
                        "one-sided harmonic cap")
                counts["paired_shell_and_mass_caps"] += 1
    for nu, frac, shift, width_div, beta_ratio in product(
            range(1, 25), (Q(0),Q(1,4),Q(1,2),Q(3,4)),
            (-2,-1,0,1,2), (8,9,16), (Q(1,2),Q(1),Q(7,5),Q(199,100))):
        b = 2*nu + shift + frac
        W = Q(nu, width_div)
        left = [ell for ell in range(nu,3*nu+1)
                if abs(ell-2*nu) < W and 0 < ell-b < beta_ratio]
        right = [b.__floor__()+1+r for r in (0,1)
                 if abs(b.__floor__()+1+r-2*nu) < W
                 and 0 < b.__floor__()+1+r-b < beta_ratio]
        require(left == right, "literal +1 two-row bijection")
        def mass(ell):
            return Q(comb(ell-1, nu-1), 2**ell)
        for f in (lambda ell: Q(1), lambda ell: Q(ell-2*nu),
                  lambda ell: Q(2)**ell):
            require(sum((mass(ell)*f(ell) for ell in left), Q(0)) ==
                    sum((mass(ell)*f(ell) for ell in right), Q(0)),
                    "signed and flat-weight finite sums")
            counts["two_row_sum_identities"] += 1
    for lam,Y,E in product((Q(0),Q(1,10),Q(1,2),Q(9,10),Q(99,100)),
                           (Q(0),Q(1,7),Q(1),Q(10)),
                           (Q(0),Q(2,9),Q(2))):
        low, high = max(Q(0),(Y-E)/(1+lam)), (Y+E)/(1-lam)
        for theta in (Q(0),Q(1,4),Q(1,2),Q(1)):
            Z = low+(high-low)*theta
            require(abs(Y-Z) <= E+lam*Z, "local comparison premise")
            require(abs(Y-Z) <= (lam*Y+E)/(1-lam), "sharp denominator")
            counts["sharp_absorption_cells"] += 1
        require(abs(Y-high) == (lam*Y+E)/(1-lam), "sharp equality witness")
        counts["sharp_equality_witnesses"] += 1
        Ys, Zs, Es = [], [], []
        for a in (Q(0),lam/2,lam):
            Yi,Ei = Y+1, E+Q(1,3)
            Zi = (Yi+Ei)/(1-a)
            require(abs(Yi-Zi) == Ei+a*Zi, "variable coefficient premise")
            Ys.append(Yi); Zs.append(Zi); Es.append(Ei)
        lhs = sum(abs(y-z) for y,z in zip(Ys,Zs))
        require(lhs <= (lam*sum(Ys)+sum(Es))/(1-lam), "all-cell aggregation")
        counts["variable_coefficient_aggregates"] += 1
        cap, W, p = Q(13,10), Q(17,3), Q(2,19)
        original = 2*lam*cap+14*W*p
        sharpened = (lam*cap+7*W*p)/(1-lam)
        require(sharpened == original/(2*(1-lam)), "exact refinement quotient")
        if lam <= Q(1,2):
            require(sharpened <= original, "finite monotonic improvement")
        counts["terminal_quotient_identities"] += 1
    xs = [63]
    for _ in range(38):
        xs.append(step(xs[-1])[0])
    require(first_hit(63,50) == 35 and xs[34:39] == [61,23,35,53,5],
            "terminal versus first-passage example")
    require(first_hit(61,50) == first_hit(53,50) == 1, "wide-window collision example")
    require(counts["nominal_only"] > 0 and counts["actual_only"] > 0,
            "both mismatch orientations exercised")
    require(counts["strict_nominal_endpoint_fixtures"] > 0, "endpoint fixture absent")
    source_names = [
        "ND/Band/A5TerminalAtoms.lean",
        "ND/Band/A5TerminalAtomDenominatorComparison.lean",
        "ND/Band/A5TerminalAtomNominalization.lean",
        "ND/Band/A5TerminalBoundaryShell.lean",
        "ND/Band/A5NominalTotalCap.lean",
        "ND/Band/A5TerminalAtomReconstruction.lean",
        "ND/Band/A5ReferenceFixedTimeAbsorption.lean",
        "ND/Band/A5ReferenceTerminalAggregate.lean",
        "ND/Band/A5ReferenceTerminalPacket.lean",
        "ND/Probability/TrueAbsorption.lean",
    ]
    report = {
        "status":"passed", "counts":dict(counts),
        "source_commit":"ca3dd0d63920411213403092aecc6946619eb082",
        "source_hashes":{p:sha256((SRC/p).read_bytes()).hexdigest() for p in source_names},
        "artifact_hashes":{p:sha256((HERE/p).read_bytes()).hexdigest()
                           for p in ("check_mazur_finite.py","audit.tex","CLAIMS.json")},
        "wide_window_example":{"start":63,"B":50,"first_hit":35,
                               "times_34_through_38":xs[34:39]},
        "scope":"Finite exact rational regressions, not analytic mixing, coverage, source-package certification or Lean replay.",
        "lean_started":False,"public_mutations":False
    }
    (HERE/"mazur_finite_checks.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))


if __name__ == "__main__":
    main()
