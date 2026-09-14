"""Finite exact checks for Crandall's primitive-root return construction.

The certificate pins the controlling source and frozen route artifacts,
checks both deterministic selector branches, and enumerates a bounded family
of genuine equations.  The arbitrary-prime proof remains the TeX proof.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(
    r"C:\Users\LOCAL_USER\Documents\Papors\OS\on-the-3x-1-problem-5cygpgqcjg.pdf"
)
PINNED = {
    SOURCE: (964_602, "acafa9070e7c5e4b167d70d7cace81da39489710804c510ff8db4369133217f4"),
    ROOT / "state" / "index_routes.jsonl": (
        274_170,
        "b05028694bf133b9b19f2b0c0a771323b7a47ae872c0712769267aaf1f1eff38",
    ),
    ROOT / "state" / "document_routes.jsonl": (
        324_776,
        "e439a5f9a70253b00824df5be791415e1c068d574c23f6f7f61851c19a88b2a5",
    ),
    ROOT / "state" / "index_snapshot.json": (
        799,
        "7d5a17440a3cb039f2bfbb4814567b5805117002136cc65687de738ee99af62f",
    ),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    for d in range(3, math.isqrt(n) + 1, 2):
        if n % d == 0:
            return False
    return True


def order_mod_odd_prime(base: int, prime: int) -> int:
    assert is_prime(prime) and prime % 2 == 1 and base % prime
    value = 1
    for exponent in range(1, prime):
        value = value * base % prime
        if value == 1:
            return exponent
    raise AssertionError("Fermat range exhausted")


def prime_divisors(n: int) -> list[int]:
    result: list[int] = []
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            result.append(divisor)
            while n % divisor == 0:
                n //= divisor
        divisor += 1 if divisor == 2 else 2
    if n > 1:
        result.append(n)
    return result


def two_is_primitive(prime: int) -> bool:
    assert is_prime(prime) and prime % 2 == 1
    return all(pow(2, (prime - 1) // q, prime) != 1 for q in prime_divisors(prime - 1))


def selector(p: int, x: int, y: int) -> tuple[list[int], int, str]:
    """Return the deterministic cumulative word, numerator, and branch.

    This finite kernel assumes only ord_p(2)=p-1, p>=5, y>=3, and
    x-y>=p+1.  The Diophantine equality is used separately in the theorem to
    identify the denominator 2^x-3^y with p.
    """

    assert p >= 5 and is_prime(p)
    assert order_mod_odd_prime(2, p) == p - 1
    assert y >= 3 and x - y >= p + 1

    cumulative = list(range(y + 1))
    cumulative[y] = x
    r0 = sum(pow(2, j, p) * pow(3, y - 1 - j, p) for j in range(y - 1)) % p

    if r0:
        candidates = range(y - 1, x)
        target = -r0 % p
        branch = "nonzero_R0"
    else:
        cumulative[y - 2] = y - 1
        r1 = (
            sum(pow(2, j, p) * pow(3, y - 1 - j, p) for j in range(y - 2))
            + pow(2, y - 1, p) * 3
        ) % p
        assert r1 == 3 * pow(2, y - 2, p) % p
        assert r1
        candidates = range(y, x)
        target = -r1 % p
        branch = "zero_R0_shift"

    selected = next(a for a in candidates if pow(2, a, p) == target)
    cumulative[y - 1] = selected
    assert all(a < b for a, b in zip(cumulative, cumulative[1:]))

    numerator = sum(
        2**cumulative[j] * 3 ** (y - 1 - j) for j in range(y)
    )
    assert numerator % p == 0
    assert numerator % 2 == 1
    assert selected == min(a for a in candidates if pow(2, a, p) == target)
    return cumulative, numerator, branch


def main() -> int:
    for path, (size, digest) in PINNED.items():
        assert path.is_file()
        assert path.stat().st_size == size
        assert sha256(path) == digest

    primitive_primes = [
        p for p in range(5, 300) if is_prime(p) and order_mod_odd_prime(2, p) == p - 1
    ]
    selector_checks = 0
    nonzero_checks = 0
    shifted_checks = 0
    for p in primitive_primes:
        for y in range(p + 1, p + 14):
            for extra in (p + 1, p + 2, 2 * p + 3):
                cumulative, numerator, branch = selector(p, y + extra, y)
                assert cumulative[0] == 0 and cumulative[-1] == y + extra
                assert numerator // p > 0 and (numerator // p) % 2 == 1
                selector_checks += 1
                nonzero_checks += branch == "nonzero_R0"
                shifted_checks += branch == "zero_R0_shift"

    assert primitive_primes
    assert nonzero_checks > 0 and shifted_checks > 0

    # Bounded genuine solutions are evidence only; the exact threshold test is
    # 3^y >= 2^(p+y), equivalent to y >= p/(log_2(3)-1).
    genuine_solutions = 0
    violating_solutions = 0
    for y in range(0, 14):
        three_power = 3**y
        for x in range(0, 20):
            p = 2**x - three_power
            if p < 3 or not is_prime(p) or p == 2:
                continue
            if not two_is_primitive(p):
                continue
            genuine_solutions += 1
            if 3**y >= 2 ** (p + y):
                violating_solutions += 1
                cumulative, numerator, _ = selector(p, x, y)
                m = numerator // p
                assert m > 1 and m % 2 == 1
                assert m * (2 ** cumulative[-1] - 3**y) == numerator

    measurements = {
        "status": "pass",
        "pinned_hashes": len(PINNED),
        "primitive_primes_below_300": len(primitive_primes),
        "selector_checks": selector_checks,
        "nonzero_R0_checks": nonzero_checks,
        "zero_R0_shift_checks": shifted_checks,
        "bounded_genuine_solutions": genuine_solutions,
        "bounded_violating_solutions": violating_solutions,
    }
    print(json.dumps(measurements, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
