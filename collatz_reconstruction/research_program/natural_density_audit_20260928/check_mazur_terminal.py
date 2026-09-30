"""Exact bounded checks for the retained Mazur terminal scales.

Rational intervals enclose all logarithms and roots used in the tests.
These are finite regressions, not proofs of the asymptotic propositions.
No Lean invocation, subprocess, network operation or third-party package.
"""
from fractions import Fraction as Q
from hashlib import sha256
from math import isqrt
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "external_literature/mazur_2026_v2"


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def log_unit_interval(x, terms=96):
    require(Q(1) <= x <= Q(2), "log interval domain")
    z = (x - 1) / (x + 1)
    z2, power, partial = z * z, z, Q(0)
    for j in range(terms):
        partial += 2 * power / (2 * j + 1)
        power *= z2
    tail = 2 * power / ((2 * terms + 1) * (1 - z2))
    return partial, partial + tail


LN2 = log_unit_interval(Q(2))


def log_integer(n):
    require(n >= 1, "positive logarithm argument")
    k = n.bit_length() - 1
    low, high = log_unit_interval(Q(n, 2**k))
    return low + k * LN2[0], high + k * LN2[1]


def sqrt_interval(x, digits=30):
    require(x >= 0, "nonnegative square root")
    scale = 10**digits
    floor_root = isqrt(x.numerator * scale**2 // x.denominator)
    low, high = Q(floor_root, scale), Q(floor_root + 1, scale)
    require(low * low <= x < high * high, "directed root enclosure")
    return low, high


def main():
    a, b, f = Q(1, 200000), Q(1, 50000), Q(340, 100000)
    qlo, qhi = 1 / (10 * LN2[1]), 1 / (10 * LN2[0])
    counts = {"exact_schedule_cases": 0, "directed_eta_enclosures": 0,
              "terminal_coefficient_identities": 0, "power_identities": 0}
    for t in (100, 101, 127, 199, 200, 251, 333, 500, 999, 1000,
              1777, 2000, 10000, 99991, 100000):
        L = t**5  # Then all fractional powers of L below are rational.
        m0 = L // 100000
        m = (m0 + t*t - 1) // (t*t)
        nlo, nhi = (L * qlo).__floor__(), (L * qhi).__floor__()
        require(nlo == nhi, "exact horizon unresolved by log interval")
        n = nlo
        require(a*t**3 <= m <= b*t**3 <= L and 1 <= n <= L,
                "unchanged floor/ceiling schedule bounds")
        logL, logm, logn = log_integer(L), log_integer(m), log_integer(n)
        S2lo, S2hi = m*logm[0], m*logm[1]
        counts["exact_schedule_cases"] += 1
        for C in (Q(1, 2), Q(40), Q(100)):
            W2lo, W2hi = C*C*n*logn[0], C*C*n*logn[1]
            SWlo = sqrt_interval(S2lo * W2lo)[0]
            SWhi = sqrt_interval(S2hi * W2hi)[1]
            etalo = 57*SWlo/(f*L) + 1021*S2lo/(f*L) + Q(8, m**3)
            etahi = 57*SWhi/(f*L) + 1021*S2hi/(f*L) + Q(8, m**3)
            coefflo = 57*C*sqrt_interval(b*qlo)[0]/f
            envelope_lo = (coefflo*logL[0]/t +
                           1021*b*logL[0]/(f*t**2) + 8*a**-3/t**9)
            require(0 <= etalo <= etahi <= envelope_lo,
                    "finite directed eta bound")
            counts["directed_eta_enclosures"] += 1
            Wlo, Whi = sqrt_interval(W2lo)[0], sqrt_interval(W2hi)[1]
            for K in (Q(0), Q(1), Q(7, 3)):
                pH = 20*K/m**11 + Q(80, m**3)
                pF = 80*K/m**11 + Q(320, m**3)
                require(pF == 4*pH and 0 <= pH <= pF,
                        "harmonic/flat coefficient identity")
                require(14*pF == 1120*K/m**11 + Q(4480, m**3),
                        "all nonproportional coefficients retained")
                require(Q(2)*Q(43, 25) == Q(86, 25), "absorption factor")
                require(Wlo <= Whi, "width enclosure order")
                counts["terminal_coefficient_identities"] += 1
    identities = (
        (Q(3, 10)+Q(1, 2)-1, -Q(1, 5)),
        (Q(7, 20)+Q(3, 5)-1, -Q(1, 20)),
        (Q(3, 5)-1, -Q(2, 5)),
        (-3*Q(3, 5), -Q(9, 5)),
        (Q(1, 2)-11*Q(3, 5), -Q(61, 10)),
        (Q(1, 2)-3*Q(3, 5), -Q(13, 10)),
        (Q(1, 4)+Q(1, 2)+Q(1, 4)+6, Q(7)),
        (1/(2*Q(143, 10)), Q(5, 143)),
        (1/(2*Q(8616, 1000)), Q(125, 2154)),
    )
    for left, right in identities:
        require(left == right, "exact exponent/coefficient identity")
        counts["power_identities"] += 1
    require(Q(5, 143) < Q(1, 20) < Q(1, 18) < Q(125, 2154) < Q(1, 5),
            "old/new phase and terminal ceilings")
    manifest = json.loads((SOURCE / "source/proofatlas-source-manifest.json").read_text())
    for entry in manifest["files"]:
        data = (SOURCE / "source" / entry["path"]).read_bytes()
        require(len(data) == entry["bytes"], "package length mismatch")
        require(sha256(data).hexdigest() == entry["sha256"].removeprefix("sha256:"),
                "package hash mismatch")
    inventory = [p.relative_to(SOURCE / "source").as_posix()
                 for p in (SOURCE / "source").rglob("*") if p.is_file()]
    missing_build_files = [p for p in ("lakefile.lean", "lakefile.toml",
                          "lake-manifest.json", "lean-toolchain")
                          if not (SOURCE / "source" / p).exists()]
    report = {
        "status": "passed", "counts": counts,
        "source_manifest_files_verified": len(manifest["files"]),
        "lean_files_present": sum(p.endswith(".lean") for p in inventory),
        "source_package_commit": manifest["packageCommit"],
        "build_files_not_bundled": missing_build_files,
        "finite_test_domain": "L=t^5, t in a fixed 15-point set; C=1/2,40,100; K=0,1,7/3",
        "analytic_scope": "Finite rational interval regressions; written proofs, not these samples, establish the limits.",
        "formal_status": "No Lean worker launched and no new Lean theorem compiled.",
        "source_hashes": {p: sha256((SOURCE/p).read_bytes()).hexdigest()
                          for p in ("paper.pdf", "checked_source.zip",
                                    "source/Erdos1135/ND/LogTime/Paper.lean")},
        "artifact_hashes": {p: sha256((HERE/p).read_bytes()).hexdigest()
                            for p in ("check_mazur_terminal.py", "audit.tex", "CLAIMS.json")}
    }
    (HERE / "mazur_terminal_checks.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
