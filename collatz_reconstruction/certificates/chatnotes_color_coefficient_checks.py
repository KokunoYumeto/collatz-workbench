"""Exact finite checks for the Chatnotes color-coefficient construction.

The certificate separates four structures that the raw transcript conflates:

* the label group V = F_2^2;
* the injective set map from V to four affine rational branches;
* the pointwise function algebra C^V with its primitive idempotents; and
* the V-graded group algebra C[V] with its group-element basis.

It also checks the Fourier passage between the last two presentations, the
state-dependent parity evaluator required to recover the shortened Collatz
map, and the distinction between coordinate swap and the independently chosen
exchange on the diagonal coefficient plane.  It is not a Collatz-conjecture
certificate and does not construct a color-superalgebra action on Collatz
states or paths.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from itertools import product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_CHAT = Path(
    r"C:\Users\LOCAL_USER\Documents\Obsidian notes\ChatGPT-Branch · Z_n Symmetries of Collatz.md"
)
ARXIV_ARCHIVE = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction\source\1808.09112v1.eprint"
)
ARXIV_TEX = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction\latex\1808.09112v1\Z2-N1-ellv5.tex"
)

PINNED = {
    RAW_CHAT: "9a80f53764a9da42c0f8e0b6d19ce61f978980a448a683b9c45f04038716160d",
    ARXIV_ARCHIVE: "d5361e762a6f8f0983aabe62fa9256c9a9adf0531dc3cefccd2f187324dd76b0",
    ARXIV_TEX: "168e9e0b3c524c0813c795b357c87fbacabf9d4d013f430330b63fc4a46562ab",
    ROOT / "state" / "index_routes.jsonl": "b05028694bf133b9b19f2b0c0a771323b7a47ae872c0712769267aaf1f1eff38",
    ROOT / "state" / "document_routes.jsonl": "e439a5f9a70253b00824df5be791415e1c068d574c23f6f7f61851c19a88b2a5",
    ROOT / "state" / "index_snapshot.json": "7d5a17440a3cb039f2bfbb4814567b5805117002136cc65687de738ee99af62f",
}

V = tuple(product((0, 1), repeat=2))
ZERO = (0, 0)
DIAGONAL = {(0, 0), (1, 1)}
OFF_DIAGONAL = {(0, 1), (1, 0)}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add(v: tuple[int, int], w: tuple[int, int]) -> tuple[int, int]:
    return ((v[0] + w[0]) % 2, (v[1] + w[1]) % 2)


def dot(v: tuple[int, int], w: tuple[int, int]) -> int:
    return (v[0] * w[0] + v[1] * w[1]) % 2


def branch(v: tuple[int, int]) -> tuple[Fraction, Fraction]:
    """Slope and intercept of F_(a,b)(x)=((1+2a)x+b)/2."""

    a, b = v
    return Fraction(1 + 2 * a, 2), Fraction(b, 2)


def affine_compose(
    f: tuple[Fraction, Fraction], g: tuple[Fraction, Fraction]
) -> tuple[Fraction, Fraction]:
    """Return f composed with g in slope/intercept coordinates."""

    fm, fc = f
    gm, gc = g
    return fm * gm, fm * gc + fc


def shortened_collatz(n: int) -> int:
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def evaluate_affine(f: tuple[Fraction, Fraction], n: int) -> Fraction:
    return f[0] * n + f[1]


def delta(u: tuple[int, int]) -> dict[tuple[int, int], Fraction]:
    return {v: Fraction(v == u) for v in V}


def function_product(
    f: dict[tuple[int, int], Fraction], g: dict[tuple[int, int], Fraction]
) -> dict[tuple[int, int], Fraction]:
    return {v: f[v] * g[v] for v in V}


def group_convolution(
    f: dict[tuple[int, int], Fraction], g: dict[tuple[int, int], Fraction]
) -> dict[tuple[int, int], Fraction]:
    result = {v: Fraction(0) for v in V}
    for v in V:
        for w in V:
            result[add(v, w)] += f[v] * g[w]
    return result


def primitive_idempotent(u: tuple[int, int]) -> dict[tuple[int, int], Fraction]:
    """Fourier idempotent p_u in C[V] for chi_u(v)=(-1)^(u dot v)."""

    return {v: Fraction((-1) ** dot(u, v), 4) for v in V}


def vector_add(
    f: dict[tuple[int, int], Fraction], g: dict[tuple[int, int], Fraction]
) -> dict[tuple[int, int], Fraction]:
    return {v: f[v] + g[v] for v in V}


def vector_scale(
    scalar: Fraction, f: dict[tuple[int, int], Fraction]
) -> dict[tuple[int, int], Fraction]:
    return {v: scalar * f[v] for v in V}


def matrix_multiply(a: tuple[tuple[int, int], tuple[int, int]], b):
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2))
        for i in range(2)
    )


def matrix_scale(c: int, a):
    return tuple(tuple(c * entry for entry in row) for row in a)


def determinant(a) -> int:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def main() -> None:
    for path, expected in PINNED.items():
        assert path.is_file(), path
        assert sha256(path) == expected, path

    route_text = (
        (ROOT / "state" / "index_routes.jsonl").read_text(encoding="utf-8")
        + (ROOT / "state" / "document_routes.jsonl").read_text(encoding="utf-8")
    ).lower()
    for signature in ("aizawa", "isaac", "segar", "1808.09112"):
        assert signature not in route_text

    tex = ARXIV_TEX.read_text(encoding="utf-8", errors="strict")
    source_signatures = (
        r"\bm{a}\cdot \bm{b} = a_1 b_1 + a_2 b_2",
        r"P _{nm} \equiv \{ P_n, P_m \}",
        r"\Lambda_{nm}\equiv\{P_n,X_m\}",
        r"X_{nm} \equiv [X_n,X_m]",
        r"(0,0) & : & H, \ D, \ K, \ P_{nm}, \ X_{nm}",
        r"(0,1) & : & P_n",
        r"(1,0) & : & Q, \ S,  \ \Lambda_{nm}",
        r"(1,1) & : & X_n",
        r"[X_n , X_m] = X_{nm}",
    )
    for signature in source_signatures:
        assert signature in tex, signature

    # The four coefficient labels give four distinct affine maps, but not a
    # representation of the additive group V under affine composition.
    assert len({branch(v) for v in V}) == 4
    assert branch(ZERO) != (Fraction(1), Fraction(0))
    homomorphism_equalities = sum(
        affine_compose(branch(v), branch(w)) == branch(add(v, w))
        for v in V
        for w in V
    )
    assert homomorphism_equalities == 0

    # Delta is exactly the kernel of a+b and is totally isotropic for the
    # dot-product bicharacter used by the cited color-superalgebra paper.
    assert {v for v in V if (v[0] + v[1]) % 2 == 0} == DIAGONAL
    assert OFF_DIAGONAL == set(V) - DIAGONAL
    assert all(dot(v, w) == 0 for v in DIAGONAL for w in DIAGONAL)

    # In the function algebra C^V the delta functions are orthogonal
    # idempotents.  They cannot simultaneously be nonzero homogeneous elements
    # of degrees v != 0 in a V-graded algebra, since deg(delta_v^2)=0.
    function_basis_checks = 0
    grading_obstructions = 0
    for u in V:
        for w in V:
            expected = delta(u) if u == w else {v: Fraction(0) for v in V}
            assert function_product(delta(u), delta(w)) == expected
            function_basis_checks += 1
        if u != ZERO:
            assert function_product(delta(u), delta(u)) == delta(u)
            assert add(u, u) == ZERO
            grading_obstructions += 1
    assert grading_obstructions == 3

    # In C[V] the group basis multiplies by addition.  The orthogonal
    # idempotents arise only after Fourier transform using the chosen pairing.
    group_basis_checks = 0
    fourier_checks = 0
    for u in V:
        for w in V:
            gu = delta(u)
            gw = delta(w)
            assert group_convolution(gu, gw) == delta(add(u, w))
            group_basis_checks += 1

            pu = primitive_idempotent(u)
            pw = primitive_idempotent(w)
            expected = pu if u == w else {v: Fraction(0) for v in V}
            assert group_convolution(pu, pw) == expected
            fourier_checks += 1
    sum_idempotents = {v: Fraction(0) for v in V}
    for u in V:
        sum_idempotents = vector_add(sum_idempotents, primitive_idempotent(u))
    assert sum_idempotents == delta(ZERO)

    # Check the displayed inverse on every group-basis vector:
    # g_v = sum_u (-1)^(u dot v) p_u.
    fourier_inverse_checks = 0
    for v in V:
        reconstructed = {w: Fraction(0) for w in V}
        for u in V:
            reconstructed = vector_add(
                reconstructed,
                vector_scale(Fraction((-1) ** dot(u, v)), primitive_idempotent(u)),
            )
        assert reconstructed == delta(v)
        fourier_inverse_checks += 1

    p_diagonal = vector_add(
        primitive_idempotent((0, 0)), primitive_idempotent((1, 1))
    )
    assert p_diagonal == {
        (0, 0): Fraction(1, 2),
        (0, 1): Fraction(0),
        (1, 0): Fraction(0),
        (1, 1): Fraction(1, 2),
    }
    assert group_convolution(p_diagonal, p_diagonal) == p_diagonal

    # Diagonal projection retains two labelled affine maps.  Recovering the
    # scalar Collatz value additionally requires evaluation at the
    # state-dependent label iota(n)=(n mod 2,n mod 2).
    projected_family = {v: branch(v) if v in DIAGONAL else None for v in V}
    assert sum(value is not None for value in projected_family.values()) == 2
    parity_evaluation_checks = 0
    integrality_checks = 0
    for n in range(-1000, 1001):
        for v in V:
            value = evaluate_affine(branch(v), n)
            assert (value.denominator == 1) == (n % 2 == v[1])
            integrality_checks += 1
        label = (n % 2, n % 2)
        assert evaluate_affine(projected_family[label], n) == shortened_collatz(n)
        parity_evaluation_checks += 1

    # Coordinate swap fixes Delta pointwise.  The exchange S used later in the
    # transcript swaps its two points and is instead translation by (1,1) on
    # Delta; that translation is not a group homomorphism because it moves 0.
    swap = lambda v: (v[1], v[0])
    translate = lambda v: add(v, (1, 1))
    assert all(swap(v) == v for v in DIAGONAL)
    assert translate((0, 0)) == (1, 1)
    assert translate((1, 1)) == (0, 0)
    assert translate(ZERO) != ZERO

    # The independently chosen matrices satisfy the standard O(2) block
    # relations.  These identities alone do not make the choice intrinsic to
    # the Collatz map.
    identity = ((1, 0), (0, 1))
    s_matrix = ((0, 1), (1, 0))
    j_matrix = ((0, -1), (1, 0))
    assert matrix_multiply(s_matrix, s_matrix) == identity
    assert matrix_multiply(j_matrix, j_matrix) == matrix_scale(-1, identity)
    assert matrix_multiply(matrix_multiply(s_matrix, j_matrix), s_matrix) == matrix_scale(
        -1, j_matrix
    )
    assert determinant(s_matrix) == -1
    assert determinant(j_matrix) == 1

    print(
        json.dumps(
            {
                "status": "PASS",
                "pinned_hashes": len(PINNED),
                "primary_source_signatures": len(source_signatures),
                "affine_labels": 4,
                "affine_composition_equalities_out_of_16": homomorphism_equalities,
                "function_basis_product_checks": function_basis_checks,
                "naive_homogeneous_idempotent_obstructions": grading_obstructions,
                "group_basis_product_checks": group_basis_checks,
                "fourier_idempotent_product_checks": fourier_checks,
                "fourier_inverse_basis_checks": fourier_inverse_checks,
                "integrality_checks": integrality_checks,
                "parity_evaluation_checks": parity_evaluation_checks,
                "explicitly_not_certified": [
                    "a V-graded color-superalgebra action on Collatz states or paths",
                    "canonicity or universality of the coefficient completion",
                    "an intrinsic O(2) action or determinant obstruction for Collatz",
                    "the SpinSU(2)(4) analogy",
                    "the Collatz conjecture",
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
