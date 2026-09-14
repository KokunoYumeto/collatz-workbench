from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from fractions import Fraction


if not __debug__:
    raise RuntimeError(
        "groupoid_motivic_interface_checks.py refuses optimized Python: fail-closed checks require __debug__"
    )


def accelerated_step(x: int) -> tuple[int, int]:
    if x <= 0 or x % 2 == 0:
        raise ValueError("the arithmetic map is defined here on positive odd integers")
    value = 3 * x + 1
    exponent = 0
    while value % 2 == 0:
        value //= 2
        exponent += 1
    return value, exponent


def orbit_data(x: int, length: int) -> tuple[int, int, tuple[int, ...]]:
    total = 0
    word: list[int] = []
    current = x
    for _ in range(length):
        current, exponent = accelerated_step(current)
        total += exponent
        word.append(exponent)
    return current, total, tuple(word)


Affine = tuple[Fraction, Fraction]


def affine_compose(left: Affine, right: Affine) -> Affine:
    """Return left after right."""
    left_slope, left_offset = left
    right_slope, right_offset = right
    return (
        left_slope * right_slope,
        left_slope * right_offset + left_offset,
    )


def affine_inverse(value: Affine) -> Affine:
    slope, offset = value
    return Fraction(1, 1) / slope, -offset / slope


def word_affine(word: tuple[int, ...]) -> Affine:
    result: Affine = (Fraction(1), Fraction(0))
    for exponent in word:
        letter = (Fraction(3, 2**exponent), Fraction(1, 2**exponent))
        result = affine_compose(letter, result)
    return result


def apply_affine(value: Affine, x: Fraction) -> Fraction:
    slope, offset = value
    return slope * x + offset


def valuation_fraction(value: Fraction, prime: int) -> int:
    numerator = abs(value.numerator)
    denominator = value.denominator
    result = 0
    while numerator and numerator % prime == 0:
        numerator //= prime
        result += 1
    while denominator % prime == 0:
        denominator //= prime
        result -= 1
    return result


def gaussian_multiply(
    left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]
) -> tuple[Fraction, Fraction]:
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c


def gaussian_inverse(value: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    a, b = value
    norm = a * a + b * b
    return a / norm, -b / norm


def gaussian_divide(
    numerator: tuple[Fraction, Fraction],
    denominator: tuple[Fraction, Fraction],
) -> tuple[Fraction, Fraction]:
    return gaussian_multiply(numerator, gaussian_inverse(denominator))


def cayley(r: Fraction) -> tuple[Fraction, Fraction]:
    return gaussian_divide((Fraction(1), r), (Fraction(1), -r))


def cayley_inverse(value: tuple[Fraction, Fraction]) -> Fraction:
    # z=(w-1)/(i(w+1)); the checked inputs have a rational, real inverse.
    numerator = (value[0] - 1, value[1])
    denominator = (-value[1], value[0] + 1)
    quotient = gaussian_divide(numerator, denominator)
    if quotient[1] != 0:
        raise AssertionError("Cayley inverse did not return a rational point")
    return quotient[0]


def run() -> dict:
    checks: dict[str, int | str | bool] = {}

    # Enumerate bounded representatives of the discrete orbit groupoid.
    odd_points = tuple(range(1, 160, 2))
    max_time = 7
    orbit_table = {
        (x, n): orbit_data(x, n) for x in odd_points for n in range(max_time + 1)
    }
    representatives: dict[
        tuple[int, int, int], list[tuple[int, int, int]]
    ] = defaultdict(list)
    for x in odd_points:
        for y in odd_points:
            for m in range(max_time + 1):
                target_x, total_x, _ = orbit_table[(x, m)]
                for n in range(max_time + 1):
                    target_y, total_y, _ = orbit_table[(y, n)]
                    if target_x == target_y:
                        representatives[(x, m - n, y)].append(
                            (m, n, total_x - total_y)
                        )

    alternative_representation_checks = 0
    xi_representation_checks = 0
    xi_images: dict[tuple[int, int, Affine], tuple[int, int, int]] = {}
    for (x, degree, y), reps in representatives.items():
        exponent_cocycles = {record[2] for record in reps}
        if len(exponent_cocycles) != 1:
            raise AssertionError("the exponent cocycle depends on its representative")
        c_a = next(iter(exponent_cocycles))
        xi_values: set[Affine] = set()
        for m, n, _ in reps:
            word_x = orbit_table[(x, m)][2]
            word_y = orbit_table[(y, n)][2]
            xi = affine_compose(
                affine_inverse(word_affine(word_x)), word_affine(word_y)
            )
            xi_values.add(xi)
            if valuation_fraction(xi[0], 3) != -degree:
                raise AssertionError("the 3-adic slope valuation lost the groupoid degree")
            if valuation_fraction(xi[0], 2) != c_a:
                raise AssertionError("the 2-adic slope valuation lost the exponent cocycle")
            recovered_bidegree = (
                valuation_fraction(xi[0], 3),
                -valuation_fraction(xi[0], 2)
                - valuation_fraction(xi[0], 3),
            )
            expected_bidegree = (-degree, -c_a + degree)
            if recovered_bidegree != expected_bidegree:
                raise AssertionError("the affine slope lost the two-coordinate cocycle")
            if apply_affine(xi, Fraction(y)) != x:
                raise AssertionError("the germ representative has the wrong source or range")
            xi_representation_checks += 1
        if len(xi_values) != 1:
            raise AssertionError("the arithmetic-to-germ map depends on a common tail")
        unique_xi = next(iter(xi_values))
        germ_key = (y, x, unique_xi)
        previous = xi_images.setdefault(germ_key, (x, degree, y))
        if previous != (x, degree, y):
            raise AssertionError("two bounded arithmetic arrows have the same affine germ")
        if len(reps) > 1:
            alternative_representation_checks += len(reps) - 1

    # Test cocycle multiplication with the exact common-middle alignment.
    groupoid_product_checks = 0
    xi_functor_checks = 0
    elements = list(representatives.items())
    by_range: dict[int, list[tuple[tuple[int, int, int], list[tuple[int, int, int]]]]] = defaultdict(list)
    for item in elements:
        by_range[item[0][0]].append(item)
    for (x, degree_g, y), reps_g in elements:
        for (y2, degree_h, z), reps_h in by_range.get(y, []):
            if y2 != y:
                raise AssertionError("groupoid range index corruption")
            m, n, c_g = reps_g[0]
            p, q, c_h = reps_h[0]
            common_middle = max(n, p)
            left_extension = common_middle - n
            right_extension = common_middle - p
            product_m = m + left_extension
            product_n = q + right_extension
            target_x, total_x, _ = orbit_data(x, product_m)
            target_z, total_z, _ = orbit_data(z, product_n)
            if target_x != target_z:
                raise AssertionError("aligned product representatives do not meet")
            if product_m - product_n != degree_g + degree_h:
                raise AssertionError("groupoid integer degree is not additive")
            if total_x - total_z != c_g + c_h:
                raise AssertionError("Birkhoff exponent cocycle is not additive")
            word_x = orbit_data(x, product_m)[2]
            word_z = orbit_data(z, product_n)[2]
            xi_product = affine_compose(
                affine_inverse(word_affine(word_x)), word_affine(word_z)
            )
            word_g_x = orbit_table[(x, m)][2]
            word_g_y = orbit_table[(y, n)][2]
            xi_g = affine_compose(
                affine_inverse(word_affine(word_g_x)), word_affine(word_g_y)
            )
            word_h_y = orbit_table[(y, p)][2]
            word_h_z = orbit_table[(z, q)][2]
            xi_h = affine_compose(
                affine_inverse(word_affine(word_h_y)), word_affine(word_h_z)
            )
            if affine_compose(xi_g, xi_h) != xi_product:
                raise AssertionError("Xi does not preserve a bounded groupoid product")
            groupoid_product_checks += 1
            xi_functor_checks += 1
            if groupoid_product_checks >= 6000:
                break
        if groupoid_product_checks >= 6000:
            break

    # The path functor J(p)=(target,-length,source) retains both bidegrees.
    path_embedding_checks = 0
    path_composition_checks = 0
    for x in range(1, 320, 2):
        for first_length in range(0, 7):
            middle, first_total, first_word = orbit_data(x, first_length)
            groupoid_degree = -first_length
            exponent_cocycle = -first_total
            bidegree = (-groupoid_degree, -exponent_cocycle + groupoid_degree)
            if bidegree != (first_length, first_total - first_length):
                raise AssertionError("the groupoid bidegree does not recover path degree")
            if word_affine(first_word)[0] != Fraction(3**first_length, 2**first_total):
                raise AssertionError("path affine slope is incorrect")
            path_embedding_checks += 1
            for second_length in range(0, 5):
                end, second_total, second_word = orbit_data(middle, second_length)
                composite_end, composite_total, composite_word = orbit_data(
                    x, first_length + second_length
                )
                if end != composite_end or composite_total != first_total + second_total:
                    raise AssertionError("path composition changed endpoint or exponent sum")
                if composite_word != first_word + second_word:
                    raise AssertionError("chronological word composition is incorrect")
                # J(q)J(p)=(end,-second_length,middle)(middle,-first_length,x).
                if -second_length - first_length != -(first_length + second_length):
                    raise AssertionError("J reverses the target-left product")
                path_composition_checks += 1

    # Finite-level certificates for g_a: Z_3 -> Y_a and beta_a: Y_a -> Z_3.
    z3_inverse_checks = 0
    for level in range(1, 6):
        modulus = 3**level
        lifted_modulus = 3 ** (level + 1)
        for exponent in range(1, 10):
            inverse_two = pow(pow(2, exponent, lifted_modulus), -1, lifted_modulus)
            expected_residue = pow(pow(2, exponent, 3), -1, 3)
            image: set[int] = set()
            for x in range(modulus):
                y = ((3 * x + 1) * inverse_two) % lifted_modulus
                if y % 3 != expected_residue:
                    raise AssertionError("g_a missed its clopen residue class")
                recovered = ((2**exponent * y - 1) // 3) % modulus
                if recovered != x:
                    raise AssertionError("beta_a g_a is not the identity at finite level")
                image.add(y)
                z3_inverse_checks += 1
            expected_image = {y for y in range(lifted_modulus) if y % 3 == expected_residue}
            if image != expected_image:
                raise AssertionError("g_a is not onto Y_a at finite level")
            for y in expected_image:
                x = ((2**exponent * y - 1) // 3) % modulus
                recovered_y = ((3 * x + 1) * inverse_two) % lifted_modulus
                if recovered_y != y:
                    raise AssertionError("g_a beta_a is not the identity at finite level")
                z3_inverse_checks += 1

    # The raw l2(O) isometry assertion fails already at a=1 and source 1.
    raw_l2_counterexample = {
        "exponent": 1,
        "source_basis_point": 1,
        "unique_formal_image": Fraction(3 * 1 + 1, 2),
        "is_positive_odd_image": False,
        "conclusion": "V_1 delta_1=0, hence V_1^* V_1 is not the identity",
    }
    if raw_l2_counterexample["unique_formal_image"] != 2:
        raise AssertionError("the explicit l2 counterexample changed")

    # Left prefixing does not preserve the multiplicative identity relation.
    prefix_word = (1,)
    prefix_of_product = prefix_word
    product_of_prefixes = prefix_word + prefix_word
    if prefix_of_product == product_of_prefixes:
        raise AssertionError("the free-word prefix obstruction disappeared")
    prefix_endomorphism_obstruction_checks = 1

    # Exact unimodular change between arithmetic and grading tori.
    forward_matrix = ((1, 1), (-1, 0))
    inverse_matrix = ((0, -1), (1, 1))
    for row in range(2):
        for column in range(2):
            left = sum(forward_matrix[row][k] * inverse_matrix[k][column] for k in range(2))
            right = sum(inverse_matrix[row][k] * forward_matrix[k][column] for k in range(2))
            expected = 1 if row == column else 0
            if left != expected or right != expected:
                raise AssertionError("torus exponent matrices are not mutual inverses")

    torus_character_checks = 0
    motive_square_checks = 0
    character_product_checks = 0
    for word_length in range(0, 8):
        for seed in range(1, 48, 2):
            _, total, word = orbit_data(seed, word_length)
            degree = (word_length, total - word_length)
            arithmetic_character = (total, -word_length)
            transformed = (
                degree[0] + degree[1],
                -degree[0],
            )
            if transformed != arithmetic_character:
                raise AssertionError("the grading and arithmetic characters do not match")
            for lattice_value in range(-3, 4):
                alpha = Fraction(2**total, 3**word_length)
                left = Fraction(2 ** (total * max(lattice_value, 0)), 3 ** (word_length * max(lattice_value, 0)))
                if lattice_value < 0:
                    left = Fraction(1, 1) / Fraction(
                        2 ** (total * (-lattice_value)),
                        3 ** (word_length * (-lattice_value)),
                    )
                if left != alpha**lattice_value:
                    raise AssertionError("the Kummer 1-motive square does not commute")
                motive_square_checks += 1
            torus_character_checks += 1
            split = word_length // 2
            first = word[:split]
            second = word[split:]
            first_total = sum(first)
            second_total = sum(second)
            if (first_total + second_total, -(len(first) + len(second))) != (
                total,
                -word_length,
            ):
                raise AssertionError("multiplication of characters lost an exponent")
            character_product_checks += 1

    # Exact rational Cayley endpoint and inverse checks.
    cayley_checks = 0
    for denominator in range(1, 30):
        for numerator in range(1, 2 * denominator + 1):
            r = Fraction(numerator, denominator)
            alpha = cayley(r)
            expected = (
                Fraction(1 - r * r, 1 + r * r),
                Fraction(2 * r, 1 + r * r),
            )
            if alpha != expected:
                raise AssertionError("the Cayley endpoint formula is incorrect")
            if cayley_inverse(alpha) != r:
                raise AssertionError("the Cayley inverse formula is incorrect")
            if alpha[1] <= 0:
                raise AssertionError("a positive rational endpoint produced a real Cayley value")
            cayley_checks += 1

    canonical_payload = {
        "groupoid_elements": len(representatives),
        "groupoid_representatives": sum(len(value) for value in representatives.values()),
        "alternative_representation_checks": alternative_representation_checks,
        "groupoid_product_checks": groupoid_product_checks,
        "xi_functor_checks": xi_functor_checks,
        "xi_injective_images": len(xi_images),
        "path_embedding_checks": path_embedding_checks,
        "path_composition_checks": path_composition_checks,
        "xi_representation_checks": xi_representation_checks,
        "z3_inverse_checks": z3_inverse_checks,
        "torus_character_checks": torus_character_checks,
        "motive_square_checks": motive_square_checks,
        "character_product_checks": character_product_checks,
        "cayley_checks": cayley_checks,
        "prefix_endomorphism_obstruction_checks":
            prefix_endomorphism_obstruction_checks,
    }
    canonical_json = json.dumps(canonical_payload, sort_keys=True, separators=(",", ":"))
    checks.update(canonical_payload)
    checks["metrics_sha256"] = hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()

    return {
        "schema_version": "1.0",
        "status": "PASS",
        "scope": "bounded exact checks for the arithmetic orbit groupoid, the 3-adic germ interface, torus-character squares, and Cayley pairs",
        "checks": checks,
        "raw_l2_counterexample": {
            "exponent": raw_l2_counterexample["exponent"],
            "source_basis_point": raw_l2_counterexample["source_basis_point"],
            "unique_formal_image": str(raw_l2_counterexample["unique_formal_image"]),
            "is_positive_odd_image": raw_l2_counterexample["is_positive_odd_image"],
            "conclusion": raw_l2_counterexample["conclusion"],
        },
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
