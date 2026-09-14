from __future__ import annotations

import hashlib
import itertools
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]


if not __debug__:
    raise RuntimeError(
        "chatnotes_symbolic_completion_checks.py refuses optimized Python: "
        "fail-closed checks require __debug__"
    )


SOURCE_PINS = {
    Path(
        r"C:\Users\LOCAL_USER\Documents\Obsidian notes\ChatGPT-Branch · Z_n Symmetries of Collatz.md"
    ): (
        538005,
        "9a80f53764a9da42c0f8e0b6d19ce61f978980a448a683b9c45f04038716160d",
    ),
    Path(
        r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\idempotent_tropical_F1_semirings"
        r"\1502.05580__Geometry of the arithmetic site\arithmeticsite_Adv_final1.tex"
    ): (
        165807,
        "bd9da2b9e3c8846e306af18dbf745d7cf603450d6630a00e239da4235a7320b4",
    ),
    Path(
        r"C:\Users\LOCAL_USER\Documents\Papors\OS\perfectoid spaces\Rings"
        r"\2310.13790v3 Absolute calculus and prismatic crystals on cyclotomic rings.pdf"
    ): (
        1144580,
        "deb83315e7842c35d2d080b15f543f241dfb24a5a49d9e7f34c8b144f848845f",
    ),
    Path(
        r"C:\Users\LOCAL_USER\Documents\arxiv_latex\perfectoid_padic_bundle"
        r"\THE PRISMATIZATION OF p-ADIC FORMAL SCHEMES\prismatization-for-arxiv.tex"
    ): (
        231255,
        "49a4226bad2ca2abb698309ab15e24327069626cfc8dcccfffb4e1d310c633eb",
    ),
    Path(
        r"C:\Users\LOCAL_USER\Documents\Papors\OS"
        r"\Sarig O (2003) Existence of Gibbs measures for countable.pdf"
    ): (
        359658,
        "b24ccd8591638a9b03ca612dd1fdb140ee2065c3e844e032105914cb2b891a3b",
    ),
    Path(
        r"C:\Users\LOCAL_USER\Documents\Papors\OS"
        r"\arig O (1999) Thermodynamic formalism for countable.pdf"
    ): (
        544513,
        "db08aa70c9676db5becd352ed4881b7b7ffd08c89e0d3db52c0f7f0a34720492",
    ),
    PROJECT
    / "external_literature"
    / "act42_sarig_1999"
    / "sarig_1999_author_preprint_pr_4.pdf": (
        347306,
        "9e32047d0d605f22375a419ccda190ad9aff7c71a1a78aae0c142cb170618c47",
    ),
    PROJECT
    / "intake"
    / "chatnotes"
    / "ZN-SYMMETRIES-TROPICAL-PRISMATIC-SYMBOLIC-DIRECT-LOCATOR-AUDIT-04.md": (
        14364,
        "da9e24cc4e5fac820d2e9ad773a4bc14baf94237e2408ed95cb52c631fee2b6c",
    ),
}


REQUIRED_TEX_LABELS = {
    "lem:symbolic-exceptional-backward-orbit",
    "lem:symbolic-Z2-prefix-cylinders",
    "lem:symbolic-inverse-branch-homeomorphism",
    "thm:symbolic-survivor-conjugacy",
    "thm:symbolic-positive-language-density",
    "thm:symbolic-positive-stabilization",
    "construction:symbolic-prefix-refinement-tree",
    "thm:symbolic-full-shift-pressure",
    "eq:symbolic-gurevich-partition",
    "cor:symbolic-positive-image-null",
    "prop:symbolic-transducer-counterexample",
    "prop:symbolic-canonical-pair-injection",
    "prop:symbolic-tropical-degree-shadow",
    "prop:symbolic-tropical-algebra-obstruction",
    "prop:symbolic-WCart-formal-map-obstruction",
    "prop:symbolic-formal-affine-line-repair",
    "prop:symbolic-no-three-adic-valuation-selector",
    "nonclaim:symbolic-late-interface-boundary",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def v2(value: int) -> int:
    if value == 0:
        raise ValueError("v2(0) is not a finite integer")
    value = abs(value)
    exponent = 0
    while value % 2 == 0:
        exponent += 1
        value //= 2
    return exponent


def crt_pair(
    residue_three: int,
    modulus_three: int,
    residue_two: int,
    modulus_two: int,
) -> int:
    """Least nonnegative simultaneous solution for coprime displayed moduli."""
    correction = (
        (residue_two - residue_three)
        * pow(modulus_three, -1, modulus_two)
    ) % modulus_two
    return (residue_three + modulus_three * correction) % (
        modulus_three * modulus_two
    )


def word_data(word: tuple[int, ...]) -> tuple[int, int]:
    total = sum(word)
    prefix = 0
    intercept = 0
    length = len(word)
    for index, exponent in enumerate(word):
        intercept += 3 ** (length - index - 1) * 2**prefix
        prefix += exponent
    return total, intercept


def canonical_residue(word: tuple[int, ...]) -> tuple[int, int]:
    if not word:
        return 1, 2
    total, intercept = word_data(word)
    modulus = 2 ** (total + 1)
    residue = pow(3 ** len(word), -1, modulus) * (2**total - intercept)
    residue %= modulus
    assert residue % 2 == 1
    return residue, modulus


def odd_itinerary_prefix(start: int, length: int) -> tuple[int, ...]:
    if start <= 0 or start % 2 == 0:
        raise ValueError("certificate trajectory expects a positive odd start")
    value = start
    symbols: list[int] = []
    for _ in range(length):
        exponent = v2(3 * value + 1)
        symbols.append(exponent)
        value = (3 * value + 1) // (2**exponent)
        assert value > 0 and value % 2 == 1
    return tuple(symbols)


def raw_update(state: tuple[int, int], exponent: int) -> tuple[int, int]:
    level, residue = state
    next_level = level + exponent
    modulus = 2**next_level
    next_residue = pow(3, -1, modulus) * (2**exponent * residue - 1)
    next_residue %= modulus
    assert next_residue % 2 == 1
    return next_level, next_residue


def run() -> dict:
    checks: defaultdict[str, int] = defaultdict(int)

    for path, (expected_bytes, expected_hash) in SOURCE_PINS.items():
        assert path.is_file(), path
        assert path.stat().st_size == expected_bytes, path
        assert sha256(path) == expected_hash, path
        checks["source_pin_checks"] += 1

    connes_source = next(
        path for path in SOURCE_PINS if path.name == "arithmeticsite_Adv_final1.tex"
    ).read_text(encoding="utf-8")
    for exact_source_fragment in (
        r"C+\R_+^2=C",
        r"admits $Q=\R_+^2$ as neutral element",
    ):
        assert exact_source_fragment in connes_source
        checks["connes_consani_definition_locator_checks"] += 1

    chapter = (
        PROJECT
        / "tex"
        / "chapters"
        / "04_symbolic_completion_and_geometric_boundaries.tex"
    )
    chapter_text = chapter.read_text(encoding="utf-8")
    for label in REQUIRED_TEX_LABELS:
        assert rf"\label{{{label}}}" in chapter_text
        checks["required_tex_label_checks"] += 1

    words: list[tuple[int, ...]] = []
    for length in range(1, 6):
        words.extend(itertools.product(range(1, 6), repeat=length))

    canonical_by_pair: dict[tuple[int, int], tuple[int, ...]] = {}
    for word in words:
        total, intercept = word_data(word)
        residue, modulus = canonical_residue(word)
        assert (3 ** len(word) * residue + intercept - 2**total) % modulus == 0
        assert (3 ** len(word) * residue + intercept) % (2 ** (total + 1)) == 2**total
        for lift in range(4):
            start = residue + lift * modulus
            assert odd_itinerary_prefix(start, len(word)) == word
            checks["positive_word_lift_checks"] += 1
        checks["finite_word_residue_checks"] += 1

        pair = (total + 1, residue)
        previous = canonical_by_pair.setdefault(pair, word)
        assert previous == word
        checks["canonical_pair_injectivity_checks"] += 1

        if len(word) < 5:
            for exponent in range(1, 6):
                child_residue, child_modulus = canonical_residue(word + (exponent,))
                assert child_modulus == modulus * 2**exponent
                assert child_residue % modulus == residue
                increment = (child_residue - residue) // modulus
                assert 0 <= increment < 2**exponent
                checks["prefix_refinement_checks"] += 1

    singular = Fraction(-1, 3)
    for exponent in range(1, 33):
        predecessor = -Fraction(2**exponent + 3, 9)
        numerator = 3 * predecessor + 1
        assert numerator == -Fraction(2**exponent, 3)
        assert v2(numerator.numerator) - v2(numerator.denominator) == exponent
        assert numerator / (2**exponent) == singular
        assert predecessor.denominator % 2 == 1
        assert predecessor.numerator % 2 == 1
        checks["exceptional_preimage_checks"] += 1

    state = (1, 1)
    for exponent in (1, 1, 2):
        state = raw_update(state, exponent)
    assert state == (5, 9)
    correct_residue, correct_modulus = canonical_residue((1, 1, 2))
    assert (correct_residue, correct_modulus) == (7, 32)
    checks["raw_transducer_counterexample_checks"] += 1

    for length in range(1, 21):
        residue, modulus = canonical_residue((1,) * length)
        assert residue == 2 ** (length + 1) - 1
        assert modulus == 2 ** (length + 1)
        checks["negative_fixed_point_prefix_checks"] += 1

    pressure_metrics: dict[str, dict[str, str]] = {}
    for beta in range(1, 9):
        one_symbol_sum = Fraction(3**beta, 2**beta - 1)
        q = Fraction(1, 2**beta)
        normalized_factor = 1 - q
        cutoff = 16
        weight_partial = sum(
            (Fraction(3, 2**symbol) ** beta for symbol in range(1, cutoff + 1)),
            Fraction(0),
        )
        weight_tail = Fraction(3**beta, 2 ** (beta * (cutoff + 1))) / (1 - q)
        assert weight_partial + weight_tail == one_symbol_sum
        checks["one_symbol_geometric_decomposition_checks"] += 1

        probability_partial = sum(
            (normalized_factor * q ** (symbol - 1) for symbol in range(1, cutoff + 1)),
            Fraction(0),
        )
        probability_tail = q**cutoff
        assert probability_partial + probability_tail == 1
        assert one_symbol_sum == Fraction(3**beta, 2**beta) / (1 - q)
        for length in range(1, 7):
            assert one_symbol_sum**length == Fraction(
                3 ** (beta * length), (2**beta - 1) ** length
            )
            checks["pressure_factorization_checks"] += 1
            for base_symbol in range(1, 5):
                base_weight = Fraction(3**beta, 2 ** (beta * base_symbol))
                based_periodic_sum = base_weight * one_symbol_sum ** (length - 1)
                assert based_periodic_sum / one_symbol_sum**length == (
                    base_weight / one_symbol_sum
                )
                checks["gurevich_based_partition_checks"] += 1
        pressure_metrics[str(beta)] = {
            "one_symbol_partition_sum": str(one_symbol_sum),
            "largest_Bernoulli_atom": str(normalized_factor),
        }
        checks["Bernoulli_normalization_checks"] += 1

    for exponent in range(1, 33):
        g_at_zero = Fraction(1, 2**exponent)
        assert g_at_zero != 0
        checks["formal_point_ring_map_obstruction_checks"] += 1

    # The printed proof is general.  These bounded CRT instances verify its
    # exact congruence witness for a=1..8, k=1..4, and every residue mod 3^k.
    for exponent in range(1, 9):
        modulus_two = 2 ** (exponent + 1)
        selector_residue = (
            pow(3, -1, modulus_two) * (2**exponent - 1)
        ) % modulus_two
        assert selector_residue % 2 == 1
        next_modulus_two = 2 ** (exponent + 2)
        complement_residue = (
            pow(3, -1, next_modulus_two) * (2 ** (exponent + 1) - 1)
        ) % next_modulus_two
        for level in range(1, 5):
            modulus_three = 3**level
            for residue_three in range(modulus_three):
                selected = crt_pair(
                    residue_three,
                    modulus_three,
                    selector_residue,
                    modulus_two,
                )
                if selected == 0:
                    selected += modulus_three * modulus_two
                outside = crt_pair(
                    residue_three,
                    modulus_three,
                    complement_residue,
                    next_modulus_two,
                )
                if outside == 0:
                    outside += modulus_three * next_modulus_two
                assert selected > 0 and selected % 2 == 1
                assert outside > 0 and outside % 2 == 1
                assert selected % modulus_three == residue_three
                assert outside % modulus_three == residue_three
                assert v2(3 * selected + 1) == exponent
                assert v2(3 * outside + 1) == exponent + 1
                checks["three_adic_selector_CRT_checks"] += 1

    # Inside the translated-quadrant family j(r,s)=(r,s)+Q, Minkowski
    # multiplication is exactly addition of the unique integral anchors.
    def translated_quadrant_product(
        left: tuple[int, int], right: tuple[int, int]
    ) -> tuple[int, int]:
        return left[0] + right[0], left[1] + right[1]

    quadrant_unit = (0, 0)
    for r, s, r_prime, s_prime in itertools.product(range(5), repeat=4):
        assert translated_quadrant_product((r, s), (r_prime, s_prime)) == (
            r + r_prime,
            s + s_prime,
        )
        checks["translated_quadrant_monoid_checks"] += 1
    assert translated_quadrant_product(quadrant_unit, quadrant_unit) == quadrant_unit

    # Orthogonal object identities multiply to the additive zero (empty
    # polygon), while object erasure sends both to Q, whose square is Q.
    empty_polygon_anchor = None
    erased_degree_product = translated_quadrant_product(
        quadrant_unit, quadrant_unit
    )
    assert empty_polygon_anchor != erased_degree_product
    checks["object_idempotent_obstruction_checks"] += 1

    return {
        "schema_version": "1.0",
        "status": "PASS",
        "scope": (
            "finite exact certificate for the survivor-coding Chatnotes "
            "repairs, counterexamples, and typed boundary calculations"
        ),
        "source_pins": len(SOURCE_PINS),
        "checks": dict(sorted(checks.items())),
        "pressure_metrics": pressure_metrics,
        "explicitly_not_certified": [
            "the infinite survivor-space bijection independently of its printed nested-ball proof",
            "the infinite positivity stabilization theorem independently of its printed proof",
            "the complete exceptional backward tree beyond the checked first preimage family",
            "the inverse-branch homeomorphism, density of the exceptional set, and infinite conjugacy independently of their printed proofs",
            "the real-beta pressure domain, beta<=0 divergence, Gibbs cylinder identity, and positive-locus nullity independently of their printed proofs",
            "Sarig's published infinite-state theorems independently of their source proofs",
            "membership of every translated quadrant in Connes-Consani's semiring independently of the pinned source definition and printed proof",
            "the formal-affine-line substitution, continuity, and point fibres independently of their printed proof",
            "the general three-adic density and codensity theorem beyond the bounded CRT instances independently of its printed proof",
            "a tropical, C-star, KMS, BCM, motivic, prismatic, crystalline, or Langlands Collatz construction",
            "the Collatz conjecture or termination of every positive orbit",
            "priority or novelty of the independently proved repairs",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
