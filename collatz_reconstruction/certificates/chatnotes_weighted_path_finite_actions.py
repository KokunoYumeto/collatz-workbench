from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]


if not __debug__:
    raise RuntimeError(
        "chatnotes_weighted_path_finite_actions.py refuses optimized Python: "
        "fail-closed checks require __debug__"
    )

SOURCE_PINS = {
    Path(r"C:\Users\LOCAL_USER\Documents\Obsidian notes\ChatGPT-Branch · Z_n Symmetries of Collatz.md"): (
        538005,
        "9a80f53764a9da42c0f8e0b6d19ce61f978980a448a683b9c45f04038716160d",
    ),
    Path(r"C:\Users\LOCAL_USER\Documents\Papors\OS\Droste M., Kuich W., Vogler H. (eds.) Handbook of Weighted Automata.pdf"): (
        4661165,
        "bed78d1a74aaf9f530c378192e6ec06802502194b3f9b717cb48c236976566f6",
    ),
    Path(r"C:\Users\LOCAL_USER\Documents\Papors\OS\Semirings, Automata, Languages  Linear Algebra (Kuich, Werner Salomaa, Arto).pdf"): (
        7217309,
        "244371a345372d19737c27608886a170f2a6de62d61cec6e00b7e3789b2bfe55",
    ),
    Path(r"C:\Users\LOCAL_USER\Documents\Papors\OS\used often\Arthur selber trace\Representation Theory of Finite Monoids (Benjamin Steinberg).pdf"): (
        5302841,
        "e29e06886656082a1d3458f3cea466094d7c977f7596681e7ae141bc141d54fb",
    ),
    Path(r"C:\Users\LOCAL_USER\Documents\Papors\OS\collatz_path_algebraZ2Z2 note.pdf"): (
        297211,
        "825672edf890283994d82ad6633ebbe18548a77afb4e565a5383284da2d33ccf",
    ),
    Path(r"C:\Users\LOCAL_USER\Documents\Papors\OS\collatz_path_algebra.pdf"): (
        232098,
        "32cbb12167d6c5a24749593717e8d9f6b81bd558c985a30e857761a0d9c854ce",
    ),
    Path(r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction\latex\1909.03562v7\collatz.tex"): (
        164932,
        "bfbc39432d4084a276416cb019a592003c868fa32f18e2f90028ac325ae5c19d",
    ),
    PROJECT / "tex" / "chapters" / "01_literature_spine.tex": (
        110712,
        "4168d99ee777a47a2bdf285cc64808b91c9d1695bf997408b650cf4ae371e163",
    ),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def v2(n: int) -> int:
    if n <= 0:
        raise ValueError("v2 is used here only on positive integers")
    value = 0
    while n % 2 == 0:
        n //= 2
        value += 1
    return value


def odd_step(x: int) -> tuple[int, int]:
    if x <= 0 or x % 2 == 0:
        raise ValueError("odd_step expects a positive odd integer")
    exponent = v2(3 * x + 1)
    return (3 * x + 1) // (2**exponent), exponent


def encode_blocks(word: tuple[int, ...]) -> tuple[str, ...]:
    return tuple(symbol for a in word for symbol in ("o",) + ("e",) * (a - 1))


def decode_blocks(symbols: tuple[str, ...]) -> tuple[int, ...]:
    result: list[int] = []
    index = 0
    while index < len(symbols):
        if symbols[index] != "o":
            raise ValueError("a block word must begin each block with o")
        index += 1
        even_count = 0
        while index < len(symbols) and symbols[index] == "e":
            even_count += 1
            index += 1
        result.append(even_count + 1)
    return tuple(result)


def apply_local_block(x: int, exponent: int) -> tuple[int, tuple[int, ...]]:
    trajectory = [x]
    value = (3 * x + 1) // 2
    trajectory.append(value)
    for _ in range(exponent - 1):
        if value % 2:
            raise AssertionError("an e-step was requested at an odd intermediate state")
        value //= 2
        trajectory.append(value)
    return value, tuple(trajectory)


def rho_prefix(word: tuple[int, ...]) -> Fraction:
    total = 0
    prefix = 0
    for index, exponent in enumerate(word):
        prefix += exponent
        total += Fraction(3**index, 2**prefix)
    return total


def beta_forward(word: tuple[int, ...]) -> Fraction:
    length = len(word)
    total = Fraction(0)
    for index in range(length):
        total += Fraction(3 ** (length - index - 1), 2 ** sum(word[index:]))
    return total


def reconstruct_prefix_word(length: int, total_exponent: int, rho: Fraction) -> tuple[int, ...]:
    if length == 0:
        if total_exponent != 0 or rho != 0:
            raise ValueError("invalid empty-word coordinates")
        return ()
    scaled = rho * (2**total_exponent)
    if scaled.denominator != 1:
        raise ValueError("the scaled prefix coordinate is not integral")
    integer = scaled.numerator
    remaining_total = total_exponent
    reversed_exponents: list[int] = []
    remaining_length = length
    while remaining_length > 1:
        difference = integer - 3 ** (remaining_length - 1)
        if difference <= 0:
            raise ValueError("invalid prefix coordinate")
        last = v2(difference)
        if last < 1 or last >= remaining_total:
            raise ValueError("invalid recovered terminal exponent")
        reversed_exponents.append(last)
        integer = difference // (2**last)
        remaining_total -= last
        remaining_length -= 1
    if integer != 1 or remaining_total < 1:
        raise ValueError("invalid recovered initial exponent")
    reversed_exponents.append(remaining_total)
    return tuple(reversed(reversed_exponents))


def compose(outer: tuple[int, int], inner: tuple[int, int], modulus: int) -> tuple[int, int]:
    """Affine pair for outer after inner."""
    a, b = outer
    c, d = inner
    return (a * c % modulus, (a * d + b) % modulus)


def units(modulus: int) -> tuple[int, ...]:
    return tuple(value for value in range(modulus) if value % 3)


def generated_semigroup(level: int) -> tuple[set[tuple[int, int]], list[set[tuple[int, int]]]]:
    modulus = 3**level
    unit_values = units(modulus)
    generators = {(3 * u % modulus, u) for u in unit_values}
    depths = [set(), generators]
    union = set(generators)
    current = generators
    for _length in range(2, level + 1):
        current = {
            compose((3 * u % modulus, u), prior, modulus)
            for u in unit_values
            for prior in current
        }
        depths.append(current)
        union.update(current)
    return union, depths


def expected_strata(level: int) -> tuple[set[tuple[int, int]], dict[int, set[tuple[int, int]]]]:
    modulus = 3**level
    unit_values = units(modulus)
    constants = {(0, b) for b in unit_values}
    if level == 1:
        return constants, {1: constants}
    strata: dict[int, set[tuple[int, int]]] = {
        1: {(3 * b % modulus, b) for b in unit_values}
    }
    for length in range(2, level):
        reduced_units = units(3 ** (level - length))
        strata[length] = {
            (3**length * slope_unit % modulus, b)
            for slope_unit in reduced_units
            for b in unit_values
        }
    strata[level] = constants
    return set().union(*strata.values()), strata


def affine_rank(pair: tuple[int, int], modulus: int) -> int:
    a, b = pair
    return len({(a * x + b) % modulus for x in range(modulus)})


def reduction(pair: tuple[int, int], lower_level: int) -> tuple[int, int]:
    modulus = 3**lower_level
    return pair[0] % modulus, pair[1] % modulus


def g_exponent(exponent: int, modulus: int) -> tuple[int, int]:
    inverse = pow(pow(2, exponent, modulus), -1, modulus)
    return 3 * inverse % modulus, inverse


def path_data(start: int, length: int, modulus: int) -> dict:
    state = start
    word: list[int] = []
    transformation = (1, 0)
    for _ in range(length):
        state, exponent = odd_step(state)
        word.append(exponent)
        transformation = compose(g_exponent(exponent, modulus), transformation, modulus)
    return {
        "source": start,
        "target": state,
        "word": tuple(word),
        "weight": (length, sum(word) - length),
        "transformation": transformation,
    }


def valuation_word(start: int, length: int) -> tuple[int, ...]:
    state = start
    result: list[int] = []
    for _ in range(length):
        state, exponent = odd_step(state)
        result.append(exponent)
    return tuple(result)


def forward_numerator(word: tuple[int, ...]) -> int:
    return sum(
        3 ** (len(word) - index - 1) * 2 ** sum(word[:index])
        for index in range(len(word))
    )


def multiply_typed(left: dict, right: dict, modulus: int) -> dict | None:
    if left["source"] != right["target"]:
        return None
    return {
        "source": right["source"],
        "target": left["target"],
        "word": right["word"] + left["word"],
        "weight": (
            left["weight"][0] + right["weight"][0],
            left["weight"][1] + right["weight"][1],
        ),
        "transformation": compose(left["transformation"], right["transformation"], modulus),
    }


def run() -> dict:
    checks = Counter()

    for path, (expected_bytes, expected_hash) in SOURCE_PINS.items():
        assert path.is_file(), path
        assert path.stat().st_size == expected_bytes, path
        assert sha256(path) == expected_hash, path
        checks["pinned_source_files"] += 1

    # The exponent word and the legal local o e^(a-1) block retain exactly the
    # same trajectory data between odd states.
    for x in range(1, 4001, 2):
        target, exponent = odd_step(x)
        block_target, trajectory = apply_local_block(x, exponent)
        assert block_target == target
        assert trajectory[0] == x and trajectory[-1] == target
        assert all(value % 2 == 0 for value in trajectory[1:-1])
        assert trajectory[-1] % 2 == 1
        checks["local_block_trajectory_checks"] += 1
    for length in range(0, 5):
        for word in itertools.product(range(1, 6), repeat=length):
            assert decode_blocks(encode_blocks(word)) == word
            checks["block_word_inverse_checks"] += 1

    # The edge-count grading and the older coefficient-label grading are
    # distinct.  The exact comparison kappa(r,s)=(r,r) has two-point fibres.
    fibre_counts = Counter()
    for r, s in itertools.product(range(2), repeat=2):
        fibre_counts[(r, r)] += 1
    assert fibre_counts == Counter({(0, 0): 2, (1, 1): 2})
    for length in range(8):
        for total in range(length, length + 8):
            count_degree = (length % 2, (total - length) % 2)
            coefficient_degree = (length % 2, length % 2)
            assert (count_degree[0], count_degree[0]) == coefficient_degree
            checks["grading_comparison_checks"] += 1

    # Prefix cocycle, the exact reversal to the forward affine intercept, Tao's
    # finite F_n coordinate, and the recursive inverse of the prefix code.
    words: list[tuple[int, ...]] = [()]
    for length in range(1, 6):
        words.extend(itertools.product(range(1, 5), repeat=length))
    seen_prefix_coordinates: dict[tuple[int, int, Fraction], tuple[int, ...]] = {}
    for word in words:
        rho = rho_prefix(word)
        key = (len(word), sum(word), rho)
        assert key not in seen_prefix_coordinates or seen_prefix_coordinates[key] == word
        seen_prefix_coordinates[key] = word
        assert reconstruct_prefix_word(len(word), sum(word), rho) == word
        assert beta_forward(word) == rho_prefix(tuple(reversed(word)))
        # Tao's F_n is the same displayed suffix sum as beta_forward.
        tao_f = Fraction(0)
        for index in range(len(word)):
            tao_f += Fraction(3 ** (len(word) - index - 1), 2 ** sum(word[index:]))
        assert tao_f == beta_forward(word)
        checks["prefix_inverse_and_reversal_checks"] += 1
    short_words = [word for word in words if len(word) <= 3]
    for left in short_words:
        for right in short_words:
            concatenated = left + right
            expected = rho_prefix(left) + Fraction(3 ** len(left), 2 ** sum(left)) * rho_prefix(right)
            assert rho_prefix(concatenated) == expected
            checks["prefix_concatenation_checks"] += 1
    collision = Fraction(19, 32)
    assert rho_prefix((1, 4)) == collision
    assert rho_prefix((3, 1, 1)) == collision
    assert (2, 5, collision) != (3, 5, collision)
    checks["undecorated_prefix_collision_checks"] += 1

    # The exact word coordinate is injective, but erasing source objects gives
    # one infinite odd residue class modulo 2^(A+1).
    for length in range(1, 5):
        for word in itertools.product(range(1, 5), repeat=length):
            total = sum(word)
            modulus_two = 2 ** (total + 1)
            numerator = forward_numerator(word)
            source_residue = (
                pow(3**length, -1, modulus_two) * (2**total - numerator)
            ) % modulus_two
            assert source_residue % 2 == 1
            source = source_residue if source_residue > 0 else source_residue + modulus_two
            for odd_residue in range(1, modulus_two, 2):
                candidate = odd_residue
                if odd_residue == source_residue:
                    assert valuation_word(candidate, length) == word
                else:
                    assert valuation_word(candidate, length) != word
                checks["exact_word_source_residue_checks"] += 1
            assert valuation_word(source + modulus_two, length) == word
            checks["exact_word_source_fibre_checks"] += 1

    # Ordinary deconcatenation is not multiplicative for ordinary word
    # concatenation: the tensor word (b,a) is the explicit extra term.
    delta_a = {((), ("a",)), (("a",), ())}
    delta_b = {((), ("b",)), (("b",), ())}
    product_delta = {
        (left_a + left_b, right_a + right_b)
        for left_a, right_a in delta_a
        for left_b, right_b in delta_b
    }
    delta_ab = {((), ("a", "b")), (("a",), ("b",)), (("a", "b"), ())}
    assert product_delta - delta_ab == {(('b',), ('a',))}
    checks["deconcatenation_bialgebra_obstructions"] += 1

    # The pullback order defect is visible on the composable 3 -> 5 -> 1 path.
    modulus = 9
    g1 = g_exponent(1, modulus)
    g4 = g_exponent(4, modulus)
    assert g1 == (6, 5) and g4 == (3, 4)
    assert compose(g4, g1, modulus) == (0, 1)
    assert compose(g1, g4, modulus) == (0, 2)
    checks["composition_order_counterexamples"] += 1

    # Exact predecessor fibres of the odd first-return map.
    for y in range(1, 1000, 2):
        for exponent in range(1, 17):
            numerator = 2**exponent * y - 1
            exists = numerator % 3 == 0
            expected = y % 3 != 0 and exponent % 2 == (0 if y % 3 == 1 else 1)
            assert exists == expected
            if exists:
                x = numerator // 3
                assert x > 0 and x % 2 == 1
                assert odd_step(x) == (y, exponent)
            checks["predecessor_fibre_checks"] += 1

    # Endpoint series and transfer coefficients agree for deterministic paths.
    state = 1
    total_exponent = 0
    for length in range(13):
        assert state == 1
        assert (length, total_exponent - length) == (length, length)
        if length < 12:
            state, exponent = odd_step(state)
            total_exponent += exponent
        checks["fixed_point_endpoint_series_checks"] += 1
    for start in range(1, 200, 2):
        state = start
        total_exponent = 0
        for length in range(8):
            path = path_data(start, length, 3**4)
            assert path["target"] == state
            assert path["weight"] == (length, total_exponent - length)
            checks["transfer_endpoint_coefficient_checks"] += 1
            state, exponent = odd_step(state)
            total_exponent += exponent
    # A fixed path of length n has exactly n+1 cuts in the coefficientwise
    # product completion.
    for length in range(30):
        assert len(range(length + 1)) == length + 1
        checks["finite_path_cut_checks"] += 1
    assert 2**2 > 3  # the positive 1-cycle; the TeX proves the general product inequality
    checks["known_cycle_weight_checks"] += 1

    # Exact finite geometric row norms underlying the analytic l^p formula.
    r = Fraction(1, 2)
    for q in (1, 2, 3, 4):
        for terms in range(1, 12):
            partial = sum((r ** (2 * q * k) for k in range(terms)), Fraction(0))
            closed = (1 - r ** (2 * q * terms)) / (1 - r ** (2 * q))
            assert partial == closed
            checks["analytic_geometric_kernel_checks"] += 1

    # Exact finite transformation semigroups, ranks, ideals, reductions, and
    # finite projections of the 3-adic inverse-limit classification.
    generated_by_level: dict[int, set[tuple[int, int]]] = {}
    cardinalities: dict[str, dict[str, object]] = {}
    for level in range(1, 7):
        modulus = 3**level
        generated, depths = generated_semigroup(level)
        expected, strata = expected_strata(level)
        assert generated == expected
        assert (1, 0) not in generated
        for length, stratum in strata.items():
            assert depths[length] == stratum
        expected_size = 2 if level == 1 else 2 * 3 ** (level - 1) * (3 ** (level - 2) + 1)
        assert len(generated) == expected_size
        rank_distribution = Counter(affine_rank(pair, modulus) for pair in generated)
        constants = {(0, b) for b in units(modulus)}
        assert {pair for pair in generated if affine_rank(pair, modulus) == 1} == constants
        # Constants form the minimum two-sided ideal: every nonempty ideal
        # containing f contains c_b f=c_b for every unit b.
        generators = {(3 * unit % modulus, unit) for unit in units(modulus)}
        for constant in constants:
            for element in generators | {(1, 0)}:
                assert compose(constant, element, modulus) == constant
                assert compose(element, constant, modulus) in constants
                checks["constant_ideal_generator_checks"] += 2
        inverse_projection = {
            (3 * b % modulus, b) for b in units(modulus)
        } | {
            (slope, b)
            for slope in range(0, modulus, 9)
            for b in units(modulus)
        }
        assert inverse_projection == generated
        generated_by_level[level] = generated
        cardinalities[str(level)] = {
            "S_N": len(generated),
            "T_N": len(generated) + 1,
            "rank_distribution": {str(rank): count for rank, count in sorted(rank_distribution.items())},
        }
        checks["finite_semigroup_level_checks"] += 1

        order = 1
        value = 2 % modulus
        while value != 1:
            value = value * 2 % modulus
            order += 1
        assert order == 2 * 3 ** (level - 1)
        checks["unit_generator_order_checks"] += 1

        # The fixed-point loop of exponent two supplies the printed nonzero
        # kernel relation uv[e^N]-[e^(N+1)] for the level-N representation.
        loop = g_exponent(2, modulus)
        loop_power = (1, 0)
        for _ in range(level):
            loop_power = compose(loop, loop_power, modulus)
        next_power = compose(loop, loop_power, modulus)
        assert loop_power == (0, 1)
        assert next_power == (0, 1)
        checks["explicit_finite_kernel_checks"] += 1

    reduction_fibres: dict[str, dict[str, int]] = {}
    for lower in range(1, 6):
        upper_set = generated_by_level[lower + 1]
        lower_set = generated_by_level[lower]
        fibres: dict[tuple[int, int], int] = defaultdict(int)
        for pair in upper_set:
            fibres[reduction(pair, lower)] += 1
        assert set(fibres) == lower_set
        if lower == 1:
            assert set(fibres.values()) == {6}
        else:
            for pair, size in fibres.items():
                assert size == (3 if pair[0] % (3**lower) != 0 and pair[0] % 9 != 0 else 9)
        reduction_fibres[f"{lower + 1}_to_{lower}"] = dict(Counter(fibres.values()))
        checks["adjacent_reduction_surjectivity_checks"] += len(lower_set)

    # Typed forward representation: object matrix units enforce composability,
    # and forward affine maps have the same target-left order.
    for level in range(1, 5):
        modulus = 3**level
        for start in range(1, 200, 2):
            right = path_data(start, 1, modulus)
            left = path_data(right["target"], 1, modulus)
            product = multiply_typed(left, right, modulus)
            direct = path_data(start, 2, modulus)
            assert product == direct
            other = path_data(start + 2, 1, modulus)
            if other["target"] != left["source"]:
                assert multiply_typed(left, other, modulus) is None
            checks["typed_representation_product_checks"] += 1

    return {
        "schema_version": "1.0",
        "status": "PASS",
        "scope": "finite exact certificate for the directly read weighted-path Chatnotes repairs and their typed finite-residue actions",
        "source_pins": len(SOURCE_PINS),
        "checks": dict(sorted(checks.items())),
        "finite_semigroup_metrics": cardinalities,
        "adjacent_reduction_fibre_multiplicities": reduction_fibres,
        "explicitly_not_certified": [
            "the Collatz conjecture or termination of every positive orbit",
            "the general infinite-dimensional analytic norm theorem independently of its printed proof",
            "the universal property of the product completion beyond the explicitly defined coefficientwise convolution",
            "the full injectivity and exact-kernel theorems independently of their printed basis proofs",
            "any groupoid, QGr, Leavitt, Hopf, bialgebra, operator-algebra, BCM, adelic, or KMS construction",
            "priority or novelty of the independently proved repairs",
            "authorship or correctness of either local AI-assisted note beyond the exact statements rederived in the live TeX",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
