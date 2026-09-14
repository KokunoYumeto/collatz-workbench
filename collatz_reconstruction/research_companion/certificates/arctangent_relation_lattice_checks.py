"""Exact portable certificate for a finite arctangent-relation lattice.

For

    z_{k,A} = 2^A + i 3^(k-1),
    theta_{k,A} = arctan(3^(k-1) / 2^A),

this script treats every pair 1 <= k <= 15 and k <= A <= 60.  It proves
that the lattice of integer vectors m for which

    sum m_{k,A} theta_{k,A} belongs to pi Q

has rank two on this finite grid.  Its displayed generators are R1 and R2
below.  The proof is not a floating-point search: it is an exact collection
of cubic-character rows over finite fields, followed by exact row reduction
over F_3 and an elementary saturated-lattice lift.

Why the finite-field test applies
---------------------------------
Put alpha_{k,A} = z_{k,A} / conjugate(z_{k,A}) in Q(i)^x.  A rational-pi
relation makes the corresponding product of the alphas a root of unity in
Q(i), hence an element of mu_4.  For q == 1 (mod 12), every good reduction
admits a cubic character and that character kills mu_4.  Consequently the
reduction modulo 3 of every genuine relation lies in every character row's
kernel.

Why the mod-3 result gives the exact integer lattice
----------------------------------------------------
Let L be the genuine relation lattice and R = Z R1 + Z R2.  Exact Gaussian
products below prove R is contained in L.  The character matrix has nullity
two, and R1,R2 are independent kernel vectors, so its kernel is R modulo 3.
For l in L write l = r + 3z with r in R.  In Q(i)^x / mu_4 this says
3 f(z) = 0.  That group is torsion-free: the complete torsion subgroup of
Q(i)^x is mu_4.  Thus z is in L and L = R + 3L.  Finally, the coordinates
(2,2) and (1,2) give an identity minor for R1,R2, so R is a direct summand
of Z^795.  Hence L/R is finitely generated free.  The equality L/R = 3(L/R)
forces L/R = 0, proving L = R.

The final chain check is also exact.  A Collatz valuation prefix contains at
most one (k,A) for each k.  All nine combinations of R1,R2 modulo 3 are
enumerated; only the two nonzero multiples of R1 have chain-compatible
support.  That support occurs precisely for the prefix (a_1,a_2) = (1,1).

The program uses only the Python standard library and refuses optimized
Python so that its fail-closed assertions cannot be disabled.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from math import isqrt
from typing import Iterable


if not __debug__:
    raise RuntimeError(
        "arctangent_relation_lattice_checks.py refuses optimized Python: "
        "fail-closed checks require __debug__"
    )


MAX_K = 15
MAX_A = 60
PRIME_BOUND = 38_821
FIELD = 3

R1_TERMS = ((1, 1, 2), (2, 2, 1))
R2_TERMS = ((1, 1, 2), (1, 2, 1), (1, 3, 1), (3, 5, 1))

EXPECTED_METRICS: dict[str, object] = {
    "candidate_primes": 1008,
    "good_rows": 794,
    "bad_rows": 214,
    "columns": 795,
    "rank_F3": 793,
    "nullity_F3": 2,
    "rank_before_38821": 792,
    "first_full_rank_prime": 38821,
    "independent_rows": 793,
    "dependent_good_primes": [38749],
    "grid_sha256": (
        "44a20a0e9275cf53c7270cbf8bf8bf8ec0650fd66cf562ba3b5c56933ff70e80"
    ),
    "candidate_primes_sha256": (
        "2f908102d0ceb0ce76dbec035f0c5144904cc61b4c962b572f09cefdf4c2a784"
    ),
    "good_primes_sha256": (
        "b9d5651f3a798be55f0db4f7bf0bcc4c150d3df03ac612928fecfe3ba96c1ca4"
    ),
    "bad_primes_sha256": (
        "e93aa2993a88d8d6fa3626b52bc43eb21e500281207cad0546422f2c6916b385"
    ),
    "character_matrix_trits_sha256": (
        "15071896fda6f1d4e75b42c91db02a2155777baa4a7eb7bdb79c6959959e1ab6"
    ),
    "independent_primes_sha256": (
        "b6741708e4657d844cebb7c339beedd08e3cb8f3dbd48550ce04728265935369"
    ),
    "pivot_columns_sha256": (
        "8895d50418089aefded51fa863c04474fc77c71cab2b04a38238160a5a9e766e"
    ),
}


def require(condition: bool, message: str) -> None:
    """Fail closed with a useful diagnostic instead of returning partial data."""
    if not condition:
        raise AssertionError(message)


def compact_json_bytes(value: object) -> bytes:
    return json.dumps(value, separators=(",", ":"), sort_keys=True).encode("utf-8")


def json_sha256(value: object) -> str:
    return hashlib.sha256(compact_json_bytes(value)).hexdigest()


def primes_through(limit: int) -> list[int]:
    """Return the primes <= limit by an exact Eratosthenes sieve."""
    require(limit >= 2, "prime limit must be at least two")
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for prime in range(2, isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            count = (limit - start) // prime + 1
            sieve[start : limit + 1 : prime] = b"\x00" * count
    return [value for value in range(2, limit + 1) if sieve[value]]


def least_quadratic_nonresidue(prime: int) -> int:
    for value in range(2, prime):
        if pow(value, (prime - 1) // 2, prime) == prime - 1:
            return value
    raise AssertionError(f"no quadratic nonresidue found modulo {prime}")


def canonical_square_root_minus_one(prime: int) -> int:
    """Deterministically select the smaller of the two square roots of -1."""
    nonresidue = least_quadratic_nonresidue(prime)
    root = pow(nonresidue, (prime - 1) // 4, prime)
    require(root * root % prime == prime - 1, "invalid square root of minus one")
    return min(root, prime - root)


def deterministic_cube_root(prime: int) -> int:
    """Select an order-three element using the least successful base."""
    exponent = (prime - 1) // 3
    for base in range(2, prime):
        root = pow(base, exponent, prime)
        if root != 1:
            require(pow(root, 3, prime) == 1, "invalid cube root of unity")
            return root
    raise AssertionError(f"no nontrivial cube root found modulo {prime}")


def character_row(
    prime: int,
    grid: tuple[tuple[int, int], ...],
) -> list[int] | None:
    """Return one cubic-character row, or None at a bad reduction prime."""
    imaginary_unit = canonical_square_root_minus_one(prime)
    omega = deterministic_cube_root(prime)
    omega_squared = omega * omega % prime
    exponent = (prime - 1) // 3
    require(exponent % 4 == 0, "the cubic character must kill mu_4")

    row: list[int] = []
    for k, total_exponent in grid:
        real_part = pow(2, total_exponent, prime)
        imaginary_part = imaginary_unit * pow(3, k - 1, prime) % prime
        numerator = (real_part + imaginary_part) % prime
        denominator = (real_part - imaginary_part) % prime
        if numerator == 0 or denominator == 0:
            return None
        alpha = numerator * pow(denominator, -1, prime) % prime
        character = pow(alpha, exponent, prime)
        if character == 1:
            row.append(0)
        elif character == omega:
            row.append(1)
        elif character == omega_squared:
            row.append(2)
        else:
            raise AssertionError(
                f"cubic character escaped mu_3 modulo {prime}: {character}"
            )
    return row


def add_row_to_basis(
    row: list[int],
    basis: dict[int, dict[int, int]],
) -> tuple[bool, int | None]:
    """Deterministic sparse row insertion over F_3."""
    work = {column: value for column, value in enumerate(row) if value}
    while work:
        pivot = min(work)
        if pivot not in basis:
            inverse = pow(work[pivot], -1, FIELD)
            if inverse != 1:
                work = {
                    column: value * inverse % FIELD
                    for column, value in work.items()
                }
            require(work[pivot] == 1, "new pivot was not normalized")
            basis[pivot] = work
            return True, pivot

        factor = work[pivot]
        prior = basis[pivot]
        for column, value in prior.items():
            reduced = (work.get(column, 0) - factor * value) % FIELD
            if reduced:
                work[column] = reduced
            else:
                work.pop(column, None)
    return False, None


def relation_vector(
    terms: tuple[tuple[int, int, int], ...],
    column_of: dict[tuple[int, int], int],
    column_count: int,
) -> list[int]:
    vector = [0] * column_count
    for k, total_exponent, coefficient in terms:
        vector[column_of[(k, total_exponent)]] = coefficient % FIELD
    return vector


def dot_mod_three(left: Iterable[int], right: Iterable[int]) -> int:
    return sum(a * b for a, b in zip(left, right)) % FIELD


def gaussian_multiply(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c


def gaussian_power(value: tuple[int, int], exponent: int) -> tuple[int, int]:
    require(exponent >= 0, "Gaussian exponent must be nonnegative")
    result = (1, 0)
    base = value
    remaining = exponent
    while remaining:
        if remaining % 2:
            result = gaussian_multiply(result, base)
        base = gaussian_multiply(base, base)
        remaining //= 2
    return result


def gaussian_relation_product(
    terms: tuple[tuple[int, int, int], ...],
) -> tuple[int, int]:
    product = (1, 0)
    for k, total_exponent, coefficient in terms:
        gaussian_integer = (2**total_exponent, 3 ** (k - 1))
        product = gaussian_multiply(
            product,
            gaussian_power(gaussian_integer, coefficient),
        )
    return product


def combine_mod_three(
    coefficient_r1: int,
    coefficient_r2: int,
    r1: list[int],
    r2: list[int],
) -> list[int]:
    return [
        (coefficient_r1 * first + coefficient_r2 * second) % FIELD
        for first, second in zip(r1, r2)
    ]


def support_can_lie_on_prefix_chain(
    vector: list[int],
    grid: tuple[tuple[int, int], ...],
) -> bool:
    """Whether the support can be contained in one positive-exponent prefix."""
    support = [point for point, coefficient in zip(grid, vector) if coefficient]
    by_k: dict[int, int] = {}
    for k, total_exponent in support:
        if k in by_k:
            return False
        by_k[k] = total_exponent

    selected = sorted(by_k.items())
    for (left_k, left_total), (right_k, right_total) in zip(
        selected, selected[1:]
    ):
        if right_total - left_total < right_k - left_k:
            return False
    return True


def run() -> dict[str, object]:
    checks = Counter()
    grid = tuple(
        (k, total_exponent)
        for k in range(1, MAX_K + 1)
        for total_exponent in range(k, MAX_A + 1)
    )
    column_of = {point: index for index, point in enumerate(grid)}
    require(len(grid) == 795, "unexpected grid cardinality")
    require(len(column_of) == len(grid), "grid contains duplicate columns")

    all_primes = primes_through(PRIME_BOUND)
    candidate_primes = [prime for prime in all_primes if prime % 12 == 1]
    for prime in candidate_primes:
        require(prime % 12 == 1, "candidate prime has the wrong congruence")
        checks["prime_sieve_checks"] += 1

    good_primes: list[int] = []
    bad_primes: list[int] = []
    rows: list[list[int]] = []
    basis: dict[int, dict[int, int]] = {}
    independent_primes: list[int] = []
    dependent_good_primes: list[int] = []
    rank_before_bound: int | None = None
    first_full_rank_prime: int | None = None

    for prime in candidate_primes:
        if prime == PRIME_BOUND:
            rank_before_bound = len(basis)
        row = character_row(prime, grid)
        if row is None:
            bad_primes.append(prime)
            checks["bad_reduction_primes"] += 1
            continue

        require(len(row) == len(grid), "character row has the wrong width")
        require(all(value in (0, 1, 2) for value in row), "non-trit matrix entry")
        good_primes.append(prime)
        rows.append(row)
        checks["good_reduction_character_rows"] += 1
        checks["character_entry_checks"] += len(row)

        independent, _pivot = add_row_to_basis(row, basis)
        if independent:
            independent_primes.append(prime)
            if len(basis) == 793 and first_full_rank_prime is None:
                first_full_rank_prime = prime
        else:
            dependent_good_primes.append(prime)

    rank = len(basis)
    nullity = len(grid) - rank
    require(rank == 793, "character matrix does not have the pinned rank")
    require(nullity == 2, "character matrix does not have the pinned nullity")
    checks["rank_checks"] += 1

    r1 = relation_vector(R1_TERMS, column_of, len(grid))
    r2 = relation_vector(R2_TERMS, column_of, len(grid))
    for row in rows:
        require(dot_mod_three(row, r1) == 0, "R1 left the character kernel")
        checks["kernel_vector_checks"] += 1
        require(dot_mod_three(row, r2) == 0, "R2 left the character kernel")
        checks["kernel_vector_checks"] += 1

    # The coordinate projection to ((2,2),(1,2)) maps (R1,R2) to the
    # standard basis.  This simultaneously proves independence and gives a
    # unit maximal minor, hence a direct-summand (saturated) sublattice.
    saturation_minor = (
        r1[column_of[(2, 2)]] * r2[column_of[(1, 2)]]
        - r1[column_of[(1, 2)]] * r2[column_of[(2, 2)]]
    )
    require(saturation_minor == 1, "the saturation minor is not a unit")
    require(nullity == 2, "two kernel witnesses do not exhaust the kernel")
    checks["saturation_minor_checks"] += 1

    first_product = gaussian_relation_product(R1_TERMS)
    second_product = gaussian_relation_product(R2_TERMS)
    require(first_product == (0, 25), "R1 Gaussian product identity failed")
    checks["exact_gaussian_product_relations"] += 1
    require(second_product == (0, 5525), "R2 Gaussian product identity failed")
    checks["exact_gaussian_product_relations"] += 1

    chain_compatible_nonzero: list[list[int]] = []
    chain_supports: dict[str, list[list[int]]] = {}
    for coefficient_r1 in range(FIELD):
        for coefficient_r2 in range(FIELD):
            combination = combine_mod_three(
                coefficient_r1,
                coefficient_r2,
                r1,
                r2,
            )
            compatible = support_can_lie_on_prefix_chain(combination, grid)
            support = [
                [k, total_exponent]
                for (k, total_exponent), coefficient in zip(grid, combination)
                if coefficient
            ]
            chain_supports[f"{coefficient_r1},{coefficient_r2}"] = support
            if compatible and any(combination):
                chain_compatible_nonzero.append([coefficient_r1, coefficient_r2])
            checks["chain_kernel_combination_checks"] += 1

    require(
        chain_compatible_nonzero == [[1, 0], [2, 0]],
        "unexpected chain-compatible kernel combination",
    )
    require(
        chain_supports["1,0"] == [[1, 1], [2, 2]],
        "R1 does not have the pinned chain support",
    )
    for coefficient_r1 in range(FIELD):
        for coefficient_r2 in (1, 2):
            support = chain_supports[f"{coefficient_r1},{coefficient_r2}"]
            k_one_totals = [total for k, total in support if k == 1]
            require(
                2 in k_one_totals and 3 in k_one_totals,
                "a nonzero R2 coefficient lost its two incompatible k=1 columns",
            )

    matrix_hash = hashlib.sha256(
        b"".join(bytes(row) for row in rows)
    ).hexdigest()
    metrics: dict[str, object] = {
        "candidate_primes": len(candidate_primes),
        "good_rows": len(good_primes),
        "bad_rows": len(bad_primes),
        "columns": len(grid),
        "rank_F3": rank,
        "nullity_F3": nullity,
        "rank_before_38821": rank_before_bound,
        "first_full_rank_prime": first_full_rank_prime,
        "independent_rows": len(independent_primes),
        "dependent_good_primes": dependent_good_primes,
        "grid_sha256": json_sha256([list(point) for point in grid]),
        "candidate_primes_sha256": json_sha256(candidate_primes),
        "good_primes_sha256": json_sha256(good_primes),
        "bad_primes_sha256": json_sha256(bad_primes),
        "character_matrix_trits_sha256": matrix_hash,
        "independent_primes_sha256": json_sha256(independent_primes),
        "pivot_columns_sha256": json_sha256(sorted(basis)),
    }
    require(metrics == EXPECTED_METRICS, "pinned metric/hash audit failed")

    require(
        checks
        == Counter(
            {
                "prime_sieve_checks": 1008,
                "good_reduction_character_rows": 794,
                "bad_reduction_primes": 214,
                "character_entry_checks": 631230,
                "exact_gaussian_product_relations": 2,
                "kernel_vector_checks": 1588,
                "rank_checks": 1,
                "saturation_minor_checks": 1,
                "chain_kernel_combination_checks": 9,
            }
        ),
        "check-family cardinalities changed",
    )

    return {
        "schema_version": "1.0",
        "status": "PASS",
        "scope": (
            "exact finite-field character certificate for the full (k,A) "
            "arctangent grid 1<=k<=15, k<=A<=60"
        ),
        "source_pins": 0,
        "checks": dict(sorted(checks.items())),
        "metrics": metrics,
        "relations": {
            "R1": [list(term) for term in R1_TERMS],
            "R2": [list(term) for term in R2_TERMS],
            "R1_gaussian_product": [0, 25],
            "R2_gaussian_product": [0, 5525],
            "chain_compatible_nonzero_F3_combinations": chain_compatible_nonzero,
        },
        "integer_lattice_lift": {
            "relation_target": "Q(i)^x / mu_4",
            "target_torsion": "zero",
            "character_kernel_mod_3": "span_F3(R1,R2)",
            "saturation_projection_coordinates": [[2, 2], [1, 2]],
            "saturation_minor_determinant": saturation_minor,
            "lift_steps": [
                "for l in L, the character kernel gives l=r+3z with r in R",
                "3f(z)=0 in torsion-free Q(i)^x/mu_4, so z is in L",
                "therefore L/R=3(L/R)",
                "R is a direct summand, so L/R is finitely generated free",
                "a finitely generated free group equal to three times itself is zero",
            ],
            "conclusion": "L=Z R1 direct-sum Z R2 on the certified grid",
        },
        "chain_restriction": {
            "criterion": (
                "the integer relation lattice on a prefix chain is Z R1 "
                "exactly when (a_1,a_2)=(1,1), and is zero otherwise"
            ),
            "reason": (
                "every nonzero R2 coefficient retains both (1,2) and (1,3), "
                "whereas a prefix chain contains at most one column at k=1"
            ),
        },
        "explicitly_not_certified": [
            "any analogous relation-lattice assertion outside the finite grid",
            "the Collatz conjecture, universal termination, or any endpoint assertion",
            "priority or novelty of the two exact identities or the lattice theorem",
            "absence of the identities or theorem from the published literature",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
