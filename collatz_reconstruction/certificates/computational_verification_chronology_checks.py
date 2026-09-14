"""Finite exact checks for the F031 computational-verification lineage.

The certificate pins the Barina, Oliveira e Silva, Roosendaal, code, sieve,
status, and immutable-route manifestations used by F031.  It checks the exact
map bridges, block and dyadic coordinates, finite sieve generator, elementary
predecessor/coalescence transports, the corrected generalized-map
branch-cylinder affine formula, and the finite maximum-excursion bridge.  It
also gives an exact counterexample to Oliveira e Silva's printed Euclidean
version of Proposition 2 instead of silently normalizing that statement.

It does not reproduce a historical distributed computation, authenticate a
server database, certify hardware or compilers, prove an unbounded recursive
v3 sieve invariant, justify a Markov asymptotic, or prove the Collatz
conjecture.  The v3 check is instead an exact finite reduction for the pinned
implementation domain k <= 34; it makes no claim for arbitrary k.
"""

from __future__ import annotations

import functools
import hashlib
import json
import re
import subprocess
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHELF = Path(
    r"C:\Users\LOCAL_USER\Documents\arxiv_latex\library\collatz_reconstruction"
)
PUBLISHED = SHELF / "published"
SOURCE = SHELF / "source"
BARINA_REPO = SOURCE / "xbarin02-collatz"
SIEVE_REPO = SOURCE / "xbarin02-collatz-sieve"
F031 = (
    ROOT
    / "qa"
    / "BARINA-OLIVEIRA-ROOSENDAAL-F031-computational-verification-audit.md"
)


PDF_PINS = {
    PUBLISHED / "Barina-2021-Convergence-verification-publisher.pdf": (
        630_022,
        "737a225fbc291cc182e940cc7ca31da4d2eb99b64e51a33e380213d8ed6b33a3",
        8,
    ),
    SOURCE / "Barina-2020-Convergence-verification-postprint.pdf": (
        205_829,
        "6df53d8f2a41d032f215209f06a021d35e447f6bdf222f1d557be730b64409dc",
        8,
    ),
    PUBLISHED / "Barina-2025-Improved-verification-limit-publisher.pdf": (
        862_781,
        "764fd732ad79545e71440f74bf738bf315b479eb404f68bae2c3b109785a5d06",
        14,
    ),
}

WEB_AND_STATUS_PINS = {
    SOURCE / "Barina-FIT-result-c168171-20260828.html": (
        86_108,
        "4552fef8ff8e4df696128fc9acf92e52a26bacb57f754cce13b9271f36d1ad16",
    ),
    SOURCE / "Barina-FIT-result-c197809-20260828.html": (
        86_250,
        "f568ef3f8d675493c4993458e94f912abf6f3386ecc397f815433615f5270161",
    ),
    SOURCE / "Oliveira-e-Silva-3x-plus-1-20260828.html": (
        11_526,
        "46aba9a800d4fd9e0c08419e02ad4ec7ea2141b68ed0b9781987f7a309c8eeff",
    ),
    SOURCE / "Oliveira-e-Silva-bibliography-3.5-20260828.html": (
        3_303,
        "ad4e9677811b3d3a82822f4938e924d199c5d34bd2ff42bac02c10746fe756c9",
    ),
    SOURCE / "Roosendaal-wondrous-20260828.html": (
        35_449,
        "e3ff21c62b1fe108ecaa9086a2c8679207339b3e086289a159b56099515f157d",
    ),
    SOURCE / "Barina-project-status-20260828.json": (
        198,
        "daf454223878d578dc7a87dc0677aa1925eba602ae295f8547ce25927ce5c5ab",
    ),
}

BUNDLE_PINS = {
    SOURCE / "xbarin02-collatz-all-20260828.bundle": (
        1_083_308,
        "e7b655972c628f060ecbc7aaffaa381eeebe6868567d14c4f4524c18559cc3dd",
    ),
    SOURCE / "xbarin02-collatz-sieve-all-20260828.bundle": (
        787_146_017,
        "687f00faba696d2a3dc8b0a6f556c9cc6da56756bdb36535ac8f3ed49575983f",
    ),
}

SIEVE_ARTIFACT_PINS = {
    SIEVE_REPO / "esieve-34.lut50.gz": (
        87_843_031,
        "450596d8222a30724b732238de69b7fc13779795a52a93528941076a59e200ef",
    ),
    SIEVE_REPO / "h2esieve-24.gz": (
        150_110,
        "b0222a680a7f65a59efd413829cc56668dd5734c099bfc32c356b285a1867fa4",
    ),
    SIEVE_REPO / "h2esieve-34.lut50.gz": (
        67_560_328,
        "4096350cf6b04fcf0fae38d07c50fb18c9a9825354772cbe05e0f55264178161",
    ),
    SIEVE_REPO / "esieve-16.map": (
        8_192,
        "f819daf6fbbdcb7ebe3da376ead93255d927e630d4df8876e830fc8fd1ba392e",
    ),
}

ROUTE_PINS = {
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

# Frozen admission copy of the completed F031 audit.
F031_AUDIT_PIN: tuple[int, str] | None = (
    46971,
    "835b4a4a760a80dbee2af4c4c13ae2e44f6f86686b2d04ea5ea87e0a3df5c891",
)

BARINA_HEAD = "326638d25c11f5849e9a7dc029f68fcf65afef79"
BARINA_HEAD_TREE = "21f47c3cec5b3afa1a05816495f6eb0b7bd5e3b4"
BARINA_2020_COMMIT = "0fabf721434b20f00af820564e3b3781dcabe768"
BARINA_2020_TREE = "f8597ec3867e5734cd6a9fb57379aef2c670f857"
BARINA_2025_COMMIT = "53c2a0608075d6fe3f10cc6eeeaf50e400c86338"
BARINA_2025_TREE = "82b9731dcd5108298a2fb2085ba1d76c837de6f5"
SIEVE_HEAD = "e5f0c264ba1f5f9c0a7d32a10c3aa61b225c70d1"
SIEVE_HEAD_TREE = "4b5a3b5afdf35596409c91da7f226e338c7c763a"
SIEVE_BAD_ARGUMENT_COMMIT = "49c5524d8d42867c866e863030a8e5d86237bf17"
SIEVE_ARGUMENT_FIX_COMMIT = "b3d2f61d89eec55008d61c32577a9e8c8b3874ab"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_pin(path: Path, expected_bytes: int, expected_hash: str) -> None:
    assert path.is_file(), path
    assert path.stat().st_size == expected_bytes, (
        path,
        path.stat().st_size,
        expected_bytes,
    )
    assert sha256(path) == expected_hash, path


def pdf_pages(path: Path) -> int:
    info = subprocess.run(
        ["pdfinfo", str(path)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    ).stdout
    match = re.search(r"(?m)^Pages:\s+(\d+)\s*$", info)
    assert match is not None, path
    return int(match.group(1))


def git(repo: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *arguments],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
    ).stdout.strip()


def source_and_repository_checks() -> dict[str, int | bool | str]:
    for path, (expected_bytes, expected_hash, pages) in PDF_PINS.items():
        check_pin(path, expected_bytes, expected_hash)
        assert pdf_pages(path) == pages
    for pins in (
        WEB_AND_STATUS_PINS,
        BUNDLE_PINS,
        SIEVE_ARTIFACT_PINS,
        ROUTE_PINS,
    ):
        for path, (expected_bytes, expected_hash) in pins.items():
            check_pin(path, expected_bytes, expected_hash)

    assert git(BARINA_REPO, "rev-parse", "HEAD") == BARINA_HEAD
    assert git(BARINA_REPO, "rev-parse", "HEAD^{tree}") == BARINA_HEAD_TREE
    assert (
        git(BARINA_REPO, "rev-parse", f"{BARINA_2020_COMMIT}^{{tree}}")
        == BARINA_2020_TREE
    )
    assert (
        git(BARINA_REPO, "rev-parse", f"{BARINA_2025_COMMIT}^{{tree}}")
        == BARINA_2025_TREE
    )
    assert git(SIEVE_REPO, "rev-parse", "HEAD") == SIEVE_HEAD
    assert git(SIEVE_REPO, "rev-parse", "HEAD^{tree}") == SIEVE_HEAD_TREE
    assert (
        git(SIEVE_REPO, "rev-parse", SIEVE_BAD_ARGUMENT_COMMIT)
        == SIEVE_BAD_ARGUMENT_COMMIT
    )
    assert (
        git(SIEVE_REPO, "rev-parse", SIEVE_ARGUMENT_FIX_COMMIT)
        == SIEVE_ARGUMENT_FIX_COMMIT
    )

    bootstrap = git(BARINA_REPO, "show", f"{BARINA_2025_COMMIT}:scripts/bootstrap.sh")
    assert "git clone git@github.com:xbarin02/collatz-sieve.git" in bootstrap
    assert "git pull || echo \"cannot sync repo\"" in bootstrap
    assert "SIEVE_LOGSIZE=34" in bootstrap
    assert "USE_LIBGMP=1" in bootstrap
    assert "h2esieve-24" in bootstrap
    assert "mv gpuworker/h2esieve-24.map gpuworker/esieve-24.map" in bootstrap

    server = git(BARINA_REPO, "show", f"{BARINA_2025_COMMIT}:src/server/server.c")
    assert server.index("if (g_clientids[n] != clid)") < server.index(
        "if (set_complete(n) < 0)"
    )
    assert server.index("if (set_complete(n) < 0)") < server.index(
        'message(ERR "checksums do not match!'
    )
    assert server.index('message(ERR "checksums do not match!') < server.index(
        "g_checksums[n] = checksum;"
    )
    assert server.index('message(ERR "mxoffsets do not match!') < server.index(
        "g_mxoffsets[n] = mxoffset;"
    )

    mclient = git(BARINA_REPO, "show", f"{BARINA_2025_COMMIT}:src/mclient/mclient.c")
    assert "trying to run on the CPU" in mclient
    assert "ABORTED_DUE_TO_OVERFLOW" in mclient
    assert "(void)checksum_beta;" in mclient

    gpuworker = git(
        BARINA_REPO, "show", f"{BARINA_2025_COMMIT}:src/gpuworker/gpuworker.c"
    )
    assert "checksum_alpha[i] == 0" in gpuworker
    assert 'printf("ABORTED_DUE_TO_OVERFLOW' in gpuworker

    worker = git(BARINA_REPO, "show", f"{BARINA_2025_COMMIT}:src/worker/worker.c")
    assert "mpz_check2" in worker
    assert "#ifdef _USE_GMP" in worker
    assert "n of the form 4n+3" in worker
    assert "for (n = n_min; n < n_sup; n += 4)" in worker

    lumi_gpu = git(
        BARINA_REPO, "show", f"{BARINA_2025_COMMIT}:scripts/lumi_submit_gpu.sh"
    )
    meta_gpu = git(
        BARINA_REPO, "show", f"{BARINA_2025_COMMIT}:scripts/meta_submit_gpu.sh"
    )
    for gpu_only_script in (lumi_gpu, meta_gpu):
        assert "make -C gpuworker" in gpu_only_script
        assert "make -C mclient" in gpu_only_script
        assert "make -C worker" not in gpu_only_script

    kernel_tree = git(
        BARINA_REPO,
        "ls-tree",
        BARINA_2025_COMMIT,
        "src/gpuworker/kernel.cl",
    )
    assert kernel_tree.startswith("120000 blob ")
    assert git(
        BARINA_REPO,
        "show",
        f"{BARINA_2025_COMMIT}:src/gpuworker/kernel.cl",
    ) == "kernel32.cl"
    precalc_kernel = git(
        BARINA_REPO,
        "show",
        f"{BARINA_2025_COMMIT}:src/gpuworker/kernel32-precalc.cl",
    )
    divergent_barrier_fragment = re.compile(
        r"if \(!IS_LIVE\(n0\)\) \{\s*continue;\s*\}"
        r"\s*barrier\(CLK_LOCAL_MEM_FENCE\);"
    )
    assert divergent_barrier_fragment.search(precalc_kernel) is not None

    fsieve = git(SIEVE_REPO, "show", f"{SIEVE_HEAD}:src/fsieve.c")
    assert "return lhs < rhs && lhs < 0;" in fsieve
    assert "is_live_in_sieve_2_34v2" in fsieve
    assert "smallest_predecessor" in fsieve
    assert "is_live_in_sieve_2_34v3" in fsieve
    assert "smallest_predecessor((L_last - 1) / 2" in fsieve
    assert "assert(b < ((size_t)1 << 34));" in fsieve
    assert "e.bc = ((uint64_t)b << 30) | (uint64_t)c;" in fsieve
    sieve_compat = git(SIEVE_REPO, "show", f"{SIEVE_HEAD}:src/compat.h")
    assert "case sizeof(unsigned long): return __builtin_ctzl" in sieve_compat
    assert "default: __builtin_trap();" in sieve_compat
    buggy_fsieve = git(
        SIEVE_REPO,
        "show",
        f"{SIEVE_BAD_ARGUMENT_COMMIT}:src/fsieve.c",
    )
    fixed_fsieve = git(
        SIEVE_REPO,
        "show",
        f"{SIEVE_ARGUMENT_FIX_COMMIT}:src/fsieve.c",
    )
    assert "is_convergent(k, b, c_, c_)" in buggy_fsieve
    assert "is_convergent(k, b, c_, /*c_*/d_)" in fixed_fsieve

    status = json.loads(
        (SOURCE / "Barina-project-status-20260828.json").read_text(encoding="utf-8")
    )
    assert status == {
        "verified_up_to_times_2_60": 2075,
        "work_unit_exp": 40,
        "lowest_incomplete_work_unit": 2175975546,
        "lowest_unassigned_work_unit": 2175975546,
        "generated": "Fri, 28 Aug 2026 19:24:59 +0200",
    }

    audit_pin = "DEFERRED"
    if F031_AUDIT_PIN is not None:
        check_pin(F031, *F031_AUDIT_PIN)
        audit_pin = "ENFORCED"
    else:
        assert F031.is_file()

    return {
        "pinned_primary_pdfs": len(PDF_PINS),
        "pinned_web_and_status_snapshots": len(WEB_AND_STATUS_PINS),
        "pinned_complete_git_bundles": len(BUNDLE_PINS),
        "pinned_sieve_artifacts": len(SIEVE_ARTIFACT_PINS),
        "pinned_frozen_route_artifacts": len(ROUTE_PINS),
        "repository_commit_and_tree_checks": 8,
        "pinned_bootstrap_dependency_and_unpinned_pull_checked": True,
        "server_client_id_gate_and_overwrite_order_checked": True,
        "checksum_beta_discard_checked": True,
        "conditional_gpu_cpu_gmp_chain_components_checked": True,
        "gpu_only_scripts_lack_cpu_worker_checked": True,
        "default_gpu_kernel_symlink_checked": True,
        "optional_precalc_divergent_barrier_order_checked": True,
        "historical_generator_argument_defect_and_fix_checked": True,
        "recursive_zero_unsigned_predecessor_expression_checked": True,
        "packed_34_bit_residue_assertion_and_alias_expression_checked": True,
        "ctzu64_LP64_assumption_checked": True,
        "f031_audit_pin": audit_pin,
    }


def nu2(value: int) -> int:
    assert value > 0
    return (value & -value).bit_length() - 1


def ctz64(value: int) -> int:
    assert 0 <= value < 2**64
    return 64 if value == 0 else nu2(value)


def shortened(value: int) -> int:
    assert value >= 0
    return value // 2 if value % 2 == 0 else (3 * value + 1) // 2


def unshortened(value: int) -> int:
    assert value > 0
    return value // 2 if value % 2 == 0 else 3 * value + 1


def t1(value: int) -> int:
    assert value > 0
    return (value + 1) // 2 if value % 2 else 3 * value // 2


def iterate(function, value: int, steps: int) -> int:
    for _ in range(steps):
        value = function(value)
    return value


def block_data(value: int) -> tuple[int, int, int]:
    assert value > 0
    alpha = nu2(value + 1)
    quotient = (value + 1) // 2**alpha
    intermediate = 3**alpha * quotient - 1
    beta = nu2(intermediate)
    return alpha, beta, intermediate // 2**beta


def map_and_block_checks() -> dict[str, int | bool]:
    bridge_checks = 0
    block_checks = 0
    fibre_checks = 0
    for value in range(1, 200_001):
        if value % 2:
            assert shortened(value) == t1(value + 1) - 1
        else:
            assert shortened(value) == value // 2
        if value % 2:
            assert t1(value) == shortened(value - 1) + 1
        else:
            assert t1(value) == 3 * value // 2
        bridge_checks += 2

        alpha, beta, target = block_data(value)
        assert beta >= 1
        assert target % 2 == 1
        assert iterate(shortened, value, alpha + beta) == target
        quotient = (value + 1) // 2**alpha
        for j in range(alpha + 1):
            assert iterate(shortened, value, j) == 3**j * (value + 1) // 2**j - 1
        block_checks += alpha + 2

        reconstructed = 2**alpha * (2**beta * target + 1) // 3**alpha - 1
        assert (2**beta * target + 1) % 3**alpha == 0
        assert reconstructed == value
        fibre_checks += 1

    assert block_data(1) == (1, 1, 1)
    for target in range(1, 256, 2):
        assert block_data(2 * target)[2] == target
        for alpha in range(9):
            for beta in range(1, 9):
                numerator = 2**beta * target + 1
                if numerator % 3**alpha:
                    continue
                value = 2**alpha * (numerator // 3**alpha) - 1
                assert value > 0
                assert block_data(value) == (alpha, beta, target)
                fibre_checks += 1

    return {
        "T_T1_branch_bridge_checks": bridge_checks,
        "block_clock_and_formula_checks": block_checks,
        "block_fibre_and_section_checks": fibre_checks,
        "block_map_surjective_section_checked": True,
        "block_map_noninjective_fibres_checked": True,
        "block_map_n0_equals_1_fixed_point_checked": block_data(1)[2] == 1,
    }


def dyadic_affine_checks() -> dict[str, int | bool]:
    affine_checks = 0
    endpoint_checks = 0
    uniform_criterion_checks = 0
    coordinate_groups: dict[tuple[int, int, int], list[int]] = {}

    for k in range(13):
        modulus = 2**k
        for residue in range(modulus):
            low = residue
            odd_count = 0
            lows = [low]
            odd_counts = [0]
            for _ in range(k):
                odd_count += low % 2
                low = shortened(low)
                lows.append(low)
                odd_counts.append(odd_count)

            for high in range(8):
                value = modulus * high + residue
                for j in range(k + 1):
                    expected = (
                        3 ** odd_counts[j] * 2 ** (k - j) * high + lows[j]
                    )
                    assert iterate(shortened, value, j) == expected
                    affine_checks += 1

            a = odd_counts[k]
            d = lows[k]
            lhs = 3**a - modulus
            rhs = residue - d
            criterion = (lhs < 0 and lhs < rhs) or (lhs == 0 and rhs > 0)
            code_criterion = lhs < rhs and lhs < 0
            assert not code_criterion or criterion

            if criterion:
                for high in range(1, 80):
                    assert high * 3**a + d < high * modulus + residue
            else:
                if lhs > 0:
                    witness = max(1, (rhs + lhs - 1) // lhs)
                    while witness * lhs < rhs:
                        witness += 1
                else:
                    witness = 1
                assert not (
                    witness * 3**a + d < witness * modulus + residue
                )
            uniform_criterion_checks += 1
            coordinate_groups.setdefault((k, a, d), []).append(residue)

    for (k, a, d), residues in coordinate_groups.items():
        if len(residues) < 2:
            continue
        lower = min(residues)
        for upper in residues:
            if upper == lower:
                continue
            for high in range(1, 10):
                assert iterate(shortened, 2**k * high + lower, k) == (
                    iterate(shortened, 2**k * high + upper, k)
                )
                assert 2**k * high + lower < 2**k * high + upper
                endpoint_checks += 1

    return {
        "dyadic_affine_prefix_checks": affine_checks,
        "uniform_descent_exact_criterion_checks": uniform_criterion_checks,
        "endpoint_coordinate_coalescence_checks": endpoint_checks,
        "code_uniform_test_is_conservative_checked": True,
    }


TRANSPORTS = (
    # modulus, target offset, source coefficient, source offset, odd steps,
    # total shortened steps
    (3, 2, 2, 1, 1, 1),
    (9, 4, 8, 3, 2, 3),
    (81, 10, 64, 7, 4, 6),
    (243, 182, 128, 95, 5, 7),
)


def transport_and_coalescence_checks() -> dict[str, int | bool]:
    transport_checks = 0
    for q in range(100_001):
        for modulus, target_offset, source_coefficient, source_offset, odd, total in (
            TRANSPORTS
        ):
            source = source_coefficient * q + source_offset
            target = modulus * q + target_offset
            assert source < target
            assert iterate(shortened, source, total) == target
            trajectory = source
            counted = 0
            for _ in range(total):
                counted += trajectory % 2
                trajectory = shortened(trajectory)
            assert counted == odd
            transport_checks += 1

    oliveira_coalescence_checks = 0
    for q in range(100_001):
        target = 81 * q + 20
        assert iterate(shortened, 64 * q + 15, 6) == target
        assert iterate(shortened, 64 * q + 14, 6) == target
        assert iterate(shortened, 32 * q + 7, 5) == target
        oliveira_coalescence_checks += 3

    hercher_checks = 0
    for value in range(3, 500_001, 2):
        alpha, beta, target = block_data(value)
        if beta < 2:
            continue
        lower = (value - 1) // 2
        assert iterate(shortened, lower, alpha + beta - 1) == target
        assert iterate(shortened, value, alpha + beta) == target
        hercher_checks += 1

    omitted_mod9 = {n for n in range(9) if n % 3 == 2 or n % 9 == 4}
    assert omitted_mod9 == {2, 4, 5, 8}
    omitted_mod27 = {n for n in range(27) if n % 3 == 2 or n % 9 == 4}
    assert omitted_mod27 == {2, 4, 5, 8, 11, 13, 14, 17, 20, 22, 23, 26}
    omitted_mod81 = {
        n
        for n in range(81)
        if n % 3 == 2 or n % 9 == 4 or n % 81 == 10
    }
    assert len(omitted_mod81) == 37

    return {
        "primitive_lower_predecessor_transport_checks": transport_checks,
        "Oliveira_Roosendaal_coalescence_checks": oliveira_coalescence_checks,
        "Hercher_local_coalescence_checks": hercher_checks,
        "mod9_omitted_residue_count": len(omitted_mod9),
        "mod27_omitted_residue_count": len(omitted_mod27),
        "mod81_omitted_residue_count": len(omitted_mod81),
    }


@functools.lru_cache(maxsize=None)
def predecessor_paths(value: int, odd_budget: int) -> frozenset[tuple[int, int, int]]:
    """Return (predecessor, odd steps, total steps) recursion paths."""

    result: set[tuple[int, int, int]] = {(value, 0, 0)}
    if odd_budget == 0:
        return frozenset(result)
    for modulus, offset, coefficient, source_offset, odd, total in TRANSPORTS:
        if odd > odd_budget or value % modulus != offset:
            continue
        source = (value - offset) // modulus * coefficient + source_offset
        for predecessor, used_odd, used_total in predecessor_paths(
            source, odd_budget - odd
        ):
            result.add((predecessor, used_odd + odd, used_total + total))
    return frozenset(result)


@functools.lru_cache(maxsize=None)
def restricted_forward_states(
    predecessor: int, maximum_odd: int
) -> frozenset[tuple[int, int, int]]:
    """Return every restricted (target, odd steps, total steps) witness.

    This is the forward closure dual to ``predecessor_paths``.  Enumerating it
    from the proposed lower predecessor is what makes the k <= 34 reduction
    small: a putative unsafe witness must have a very small predecessor, even
    though its target residue need not be small.
    """

    pending = [(predecessor, 0, 0)]
    result: set[tuple[int, int, int]] = set()
    while pending:
        target, used_odd, used_total = pending.pop()
        state = (target, used_odd, used_total)
        if state in result:
            continue
        result.add(state)
        for (
            modulus,
            target_offset,
            source_coefficient,
            source_offset,
            odd,
            total,
        ) in TRANSPORTS:
            if used_odd + odd > maximum_odd:
                continue
            if target < source_offset:
                continue
            source_remainder = target - source_offset
            if source_remainder % source_coefficient:
                continue
            quotient = source_remainder // source_coefficient
            next_target = modulus * quotient + target_offset
            assert next_target > target
            pending.append((next_target, used_odd + odd, used_total + total))
    return frozenset(result)


def nearby_prefix_records(
    predecessor: int, gaps: range, maximum_steps: int, *, coalescence: bool
) -> dict[int, list[tuple[int, int, int]]]:
    """Index nearby starts by a prefix endpoint or by (endpoint-1)/2."""

    result: dict[int, list[tuple[int, int, int]]] = {}
    for gap in gaps:
        initial = predecessor + gap
        value = initial
        odd_count = 0
        for step in range(maximum_steps + 1):
            if not coalescence:
                result.setdefault(value, []).append((initial, step, odd_count))
            elif value % 2:
                result.setdefault((value - 1) // 2, []).append(
                    (initial, step, odd_count)
                )
            odd_count += value % 2
            value = shortened(value)
    return result


def recursive_predecessor_finite_checks() -> dict[str, int | bool]:
    """Check the recursive v3 coefficient condition for the finite code domain.

    If ``T^s(n) = L`` has ``c`` odd steps and a restricted predecessor word
    has ``T^t(P) = L`` with ``d <= c`` odd steps, then its lift over
    ``N = A 2^k + n`` is

        Q = A 2^(k-s+t) 3^(c-d) + P.

    Thus ``P < n`` is a uniform lower-start certificate only when

        2^t 3^(c-d) <= 2^s.                                  (current)

    In the beta >= 2 coalescence branch, with ``m = (T^s(n)-1)/2``, the
    corresponding required inequality is

        2^t 3^(c-d) <= 2^(s+1).                              (coalescence)

    The C source does not store ``d`` or ``t`` and does not test either
    inequality.  This function checks them without enumerating 2^34 residues.

    Every elementary inverse is an exact floor map

        phi(L) = (2^t L-H)/3^d = floor(2^t L/3^d),

    with H in {1,5,73,211}.  A nonempty composition has normalized rounding
    loss h < word_length <= d.  If the current coefficient C were > 1 while
    P < n, then P(C-1) < h < 34.  In the coalescence branch the extra division
    contributes at most 1/2, so P(C-1) < 34+1/2.  Over c,d,s <= 34 (and
    s+1 <= 35), the exact smallest possible C > 1 is

        3^12/2^19 = 531441/524288,

    giving P <= 2492 and P <= 2528 respectively.  Moreover n-P <= 33 in the
    current branch and n-P <= 34 in the coalescence branch.  If the power
    difference is negative then C >= 2; otherwise that difference lies in
    0..35, which is the exact exponent box enumerated below.  Identity words
    are checked separately with zero rounding loss.  The loops enumerate
    supersets of precisely those finite candidate sets.  This is a finite
    k <= 34 result only, not an unbounded invariant.
    """

    maximum_k = 34
    coefficient_candidates = [
        Fraction(3**odd_difference, 2**power_difference)
        for odd_difference in range(maximum_k + 1)
        for power_difference in range(maximum_k + 2)
        if Fraction(3**odd_difference, 2**power_difference) > 1
    ]
    minimum_unsafe_coefficient = min(coefficient_candidates)
    assert minimum_unsafe_coefficient == Fraction(531_441, 524_288)
    minimum_excess = minimum_unsafe_coefficient - 1
    assert minimum_excess == Fraction(7_153, 524_288)

    current_predecessor_bound = Fraction(maximum_k, 1) / minimum_excess
    coalescence_predecessor_bound = (
        Fraction(2 * maximum_k + 1, 2) / minimum_excess
    )
    assert 2_492 < current_predecessor_bound < 2_493
    assert 2_528 < coalescence_predecessor_bound < 2_529

    current_state_count = 0
    current_common_endpoint_pairs = 0
    current_identity_endpoint_pairs = 0
    current_identity_coefficient_safe_pairs = 0
    current_budget_admissible_pairs = 0
    current_coefficient_safe_pairs = 0
    path_identity_checks = 0
    rounding_loss_checks = 0

    # The proved gap is at most 33.  This is the exact required range.
    for predecessor in range(1, 2_492 + 1):
        records = nearby_prefix_records(
            predecessor, range(1, 34), maximum_k, coalescence=False
        )
        for target, used_odd, used_total in restricted_forward_states(
            predecessor, maximum_k
        ):
            current_state_count += 1
            assert iterate(shortened, predecessor, used_total) == target
            path_identity_checks += 1
            if used_odd:
                rounding_numerator = (
                    2**used_total * target - 3**used_odd * predecessor
                )
                assert 0 < rounding_numerator < used_odd * 3**used_odd
                rounding_loss_checks += 1
            else:
                assert (target, used_total) == (predecessor, 0)

            for initial, step, odd_count in records.get(target, []):
                assert predecessor < initial
                if not used_odd:
                    current_identity_endpoint_pairs += 1
                    assert 3**odd_count <= 2**step
                    current_identity_coefficient_safe_pairs += 1
                    continue
                current_common_endpoint_pairs += 1
                if used_odd > odd_count:
                    continue
                current_budget_admissible_pairs += 1
                assert (
                    2**used_total * 3 ** (odd_count - used_odd) <= 2**step
                )
                current_coefficient_safe_pairs += 1

    assert current_state_count == 7_105
    assert current_identity_endpoint_pairs == 1_557
    assert (
        current_identity_coefficient_safe_pairs
        == current_identity_endpoint_pairs
    )
    assert current_common_endpoint_pairs == 2_983
    assert current_budget_admissible_pairs == 2_585
    assert current_coefficient_safe_pairs == current_budget_admissible_pairs

    coalescence_state_count = 0
    coalescence_common_endpoint_pairs = 0
    coalescence_identity_pairs = 0
    coalescence_identity_coefficient_safe_pairs = 0
    coalescence_nonidentity_pairs = 0
    coalescence_budget_admissible_pairs = 0
    coalescence_coefficient_safe_pairs = 0

    # The proved gap is at most 34; gap 35 is intentionally included as an
    # adversarial one-step superset guard.
    for predecessor in range(1, 2_528 + 1):
        records = nearby_prefix_records(
            predecessor, range(1, 36), maximum_k, coalescence=True
        )
        for target, used_odd, used_total in restricted_forward_states(
            predecessor, maximum_k
        ):
            coalescence_state_count += 1
            assert iterate(shortened, predecessor, used_total) == target
            path_identity_checks += 1
            if used_odd:
                rounding_numerator = (
                    2**used_total * target - 3**used_odd * predecessor
                )
                assert 0 < rounding_numerator < used_odd * 3**used_odd
                rounding_loss_checks += 1
            else:
                assert (target, used_total) == (predecessor, 0)

            for initial, step, odd_count in records.get(target, []):
                assert predecessor < initial
                coalescence_common_endpoint_pairs += 1
                if not used_odd:
                    coalescence_identity_pairs += 1
                    assert 3**odd_count <= 2 ** (step + 1)
                    coalescence_identity_coefficient_safe_pairs += 1
                    continue
                coalescence_nonidentity_pairs += 1
                if used_odd > odd_count:
                    continue
                coalescence_budget_admissible_pairs += 1
                assert (
                    2**used_total * 3 ** (odd_count - used_odd)
                    <= 2 ** (step + 1)
                )
                coalescence_coefficient_safe_pairs += 1

    assert coalescence_state_count == 7_216
    assert coalescence_common_endpoint_pairs == 1_003
    assert coalescence_identity_pairs == 480
    assert (
        coalescence_identity_coefficient_safe_pairs
        == coalescence_identity_pairs
    )
    assert coalescence_nonidentity_pairs == 523
    assert coalescence_budget_admissible_pairs == 487
    assert (
        coalescence_coefficient_safe_pairs
        == coalescence_budget_admissible_pairs
    )

    return {
        "recursive_predecessor_path_identity_checks": path_identity_checks,
        "recursive_predecessor_rounding_loss_checks": rounding_loss_checks,
        "finite_recursive_implementation_maximum_k": maximum_k,
        "minimum_unsafe_coefficient_numerator": minimum_unsafe_coefficient.numerator,
        "minimum_unsafe_coefficient_denominator": minimum_unsafe_coefficient.denominator,
        "current_predecessor_bound_superset": 2_492,
        "current_restricted_word_states": current_state_count,
        "current_identity_endpoint_pairs": current_identity_endpoint_pairs,
        "current_identity_coefficient_safe_pairs": (
            current_identity_coefficient_safe_pairs
        ),
        "current_common_endpoint_pairs": current_common_endpoint_pairs,
        "current_budget_admissible_pairs": current_budget_admissible_pairs,
        "current_coefficient_safe_pairs": current_coefficient_safe_pairs,
        "coalescence_predecessor_bound_superset": 2_528,
        "coalescence_restricted_word_states": coalescence_state_count,
        "coalescence_common_endpoint_pairs": coalescence_common_endpoint_pairs,
        "coalescence_identity_pairs": coalescence_identity_pairs,
        "coalescence_identity_coefficient_safe_pairs": (
            coalescence_identity_coefficient_safe_pairs
        ),
        "coalescence_nonidentity_pairs": coalescence_nonidentity_pairs,
        "coalescence_budget_admissible_pairs": (
            coalescence_budget_admissible_pairs
        ),
        "coalescence_coefficient_safe_pairs": coalescence_coefficient_safe_pairs,
        "finite_k_le_34_recursive_coefficient_domain_checked": True,
        "unbounded_recursive_coefficient_invariant_certified": False,
    }


def v2_live(k: int, residue: int) -> bool:
    remaining = k
    value = residue
    previous = residue
    mask64 = 2**64 - 1
    while remaining > 0:
        value += 1
        alpha = min(ctz64(value), remaining)
        remaining -= alpha
        value = value // 2**alpha * 3**alpha
        value -= 1
        beta = min(ctz64(value), remaining)
        remaining -= beta
        value //= 2**beta
        if value < residue:
            return False
        previous_minus_one = (previous - 1) & mask64
        if beta >= 2 and previous_minus_one // 2 < residue:
            return False
        previous = value
    return True


def smallest_predecessor_value(value: int, odd_budget: int) -> int:
    return min(path[0] for path in predecessor_paths(value, odd_budget))


def v3_live(k: int, residue: int) -> bool:
    remaining = k
    odd_count = 0
    value = residue
    previous = residue
    while remaining > 0:
        value += 1
        alpha = min(ctz64(value), remaining)
        odd_count += alpha
        remaining -= alpha
        value = value // 2**alpha * 3**alpha
        value -= 1
        beta = min(ctz64(value), remaining)
        remaining -= beta
        value //= 2**beta
        predecessor = smallest_predecessor_value(value, odd_count)
        if beta >= 2:
            previous_lower = ((previous - 1) & (2**64 - 1)) // 2
            predecessor = min(
                predecessor,
                smallest_predecessor_value(previous_lower, odd_count - alpha),
            )
        if predecessor < residue:
            return False
        previous = value
    return True


def endpoint(value: int, steps: int) -> tuple[int, int]:
    odd = 0
    for _ in range(steps):
        odd += value % 2
        value = shortened(value)
    return odd, value


def basic_uniform_dead(k: int, residue: int) -> bool:
    odd, target = endpoint(residue, k)
    lhs = 3**odd - 2**k
    rhs = residue - target
    return lhs < rhs and lhs < 0


def generate_sieve(
    maximum_k: int, *, use_v2: bool, use_v3: bool
) -> list[bytes]:
    maps: list[list[bool]] = []
    packed: list[bytes] = []
    for k in range(maximum_k + 1):
        size = 2**k
        live = [True] * size
        coordinates: list[tuple[int, int]] = []
        for residue in range(size):
            if use_v2 and not v2_live(k, residue):
                live[residue] = False
            if use_v3 and not v3_live(k, residue):
                live[residue] = False
            odd, target = endpoint(residue, k)
            coordinates.append((odd, target))
            if basic_uniform_dead(k, residue):
                live[residue] = False
            if k > 0 and not maps[k - 1][residue & (2 ** (k - 1) - 1)]:
                live[residue] = False

        least: dict[tuple[int, int], int] = {}
        for residue, coordinate in enumerate(coordinates):
            least.setdefault(coordinate, residue)
        for residue, coordinate in enumerate(coordinates):
            if live[residue] and least[coordinate] < residue:
                live[residue] = False

        maps.append(live)
        data = bytearray((size + 7) // 8)
        for residue, is_live in enumerate(live):
            if is_live:
                data[residue >> 3] |= 1 << (residue & 7)
        packed.append(bytes(data))
    return packed


def small_sieve_reproduction_checks() -> dict[str, int | bool | str]:
    generated = generate_sieve(16, use_v2=False, use_v3=False)[16]
    pinned = (SIEVE_REPO / "esieve-16.map").read_bytes()
    assert generated == pinned
    live = sum(byte.bit_count() for byte in generated)
    assert live == 1720
    enhanced = generate_sieve(16, use_v2=True, use_v3=True)[16]
    enhanced_live = sum(byte.bit_count() for byte in enhanced)
    assert enhanced_live <= live
    return {
        "basic_esieve_reproduced_through_k": 16,
        "esieve_16_map_exact_byte_match": True,
        "esieve_16_live_bits": live,
        "esieve_16_sha256": hashlib.sha256(generated).hexdigest(),
        "finite_h2_generator_smoke_depth": 16,
        "finite_h2_generator_live_bits": enhanced_live,
        "full_h2_map_independently_reproduced": False,
    }


def generalized_5(value: int) -> int:
    if value % 2 == 0:
        return value // 2
    if value % 3 == 0:
        return value // 3
    return 5 * value + 1


def generalized_counts(value: int, steps: int) -> tuple[int, int, int, int]:
    k2 = k3 = k5 = 0
    for _ in range(steps):
        if value % 2 == 0:
            k2 += 1
        elif value % 3 == 0:
            k3 += 1
        else:
            k5 += 1
        value = generalized_5(value)
    return k2, k3, k5, value


def generalized_coordinate_checks() -> dict[str, int | bool]:
    affine_checks = 0
    branch_stability_checks = 0

    # Oliveira e Silva's printed Proposition 2 is circular.  For i = 1 and
    # n_0 = 1, none of the only possible values r in {1, 2, 3} is a fixed
    # point of "take m = n_0 mod r, then recompute r from m's branch".
    printed_fixed_points = []
    for candidate_r in (1, 2, 3):
        candidate_m = 1 % candidate_r
        ck2, ck3, _ck5, _target = generalized_counts(candidate_m, 1)
        induced_r = 2**ck2 * 3**ck3
        if induced_r == candidate_r:
            printed_fixed_points.append((candidate_r, candidate_m))
    assert printed_fixed_points == []

    # Taking the branch of n_0 first does not repair the printed statement:
    # n_0 = 1 selects 5n+1, hence r = 1, m = 0, n_i = 1, but 6 != 5.
    nk2, nk3, nk5, n_target = generalized_counts(1, 1)
    naive_r = 2**nk2 * 3**nk3
    naive_quotient, naive_remainder = divmod(1, naive_r)
    _mk2, _mk3, _mk5, naive_remainder_target = generalized_counts(
        naive_remainder, 1
    )
    assert n_target == 6
    assert 5**nk5 * naive_quotient + naive_remainder_target == 5

    # The exact repair uses the branch cylinder modulo 6^i.  If
    # a_i = n_0 mod 6^i and R_i is the product of the divisors selected by
    # a_i's first i branches, then n_0 and a_i have the same branch word,
    # R_i divides 6^i, and
    #   C^i(n_0) = 5^k5 ((n_0-a_i)/R_i) + C^i(a_i).
    for steps in range(9):
        cylinder_modulus = 6**steps
        for initial in range(1, 30_001):
            cylinder_quotient, branch_representative = divmod(
                initial, cylinder_modulus
            )
            k2, k3, k5, representative_target = generalized_counts(
                branch_representative, steps
            )
            ik2, ik3, ik5, target = generalized_counts(initial, steps)
            assert (ik2, ik3, ik5) == (k2, k3, k5)

            branch_denominator = 2**k2 * 3**k3
            assert cylinder_modulus % branch_denominator == 0
            assert (initial - branch_representative) % branch_denominator == 0
            high_coordinate = (
                initial - branch_representative
            ) // branch_denominator
            assert high_coordinate == (
                cylinder_modulus // branch_denominator
            ) * cylinder_quotient
            assert target == (
                5**k5 * high_coordinate + representative_target
            )
            affine_checks += 1
            branch_stability_checks += steps

    matrix = (
        (3, 0, 0, 3, 0, 0),
        (6, 0, 0, 0, 0, 0),
        (0, 3, 0, 0, 3, 0),
        (0, 2, 0, 2, 0, 2),
        (0, 0, 3, 0, 0, 3),
        (0, 0, 6, 0, 0, 0),
    )
    transition = tuple(
        tuple(Fraction(entry, 6) for entry in row) for row in matrix
    )
    stationary = tuple(Fraction(entry, 27) for entry in (8, 4, 4, 6, 2, 3))
    assert all(sum(row) == 1 for row in transition)
    assert all(
        sum(stationary[i] * transition[i][j] for i in range(6))
        == stationary[j]
        for j in range(6)
    )

    example = 17
    expected = (
        48 * 0 + 17,
        240 * 0 + 86,
        120 * 0 + 43,
        600 * 0 + 216,
        300 * 0 + 108,
        150 * 0 + 54,
        75 * 0 + 27,
        25 * 0 + 9,
    )
    observed = tuple(iterate(generalized_5, example, i) for i in range(8))
    assert observed == expected

    return {
        "printed_Proposition_2_i1_n1_fixed_points": len(printed_fixed_points),
        "printed_Proposition_2_branch_first_counterexample_checked": True,
        "corrected_generalized_5_branch_cylinder_affine_checks": affine_checks,
        "corrected_generalized_5_branch_stability_step_checks": (
            branch_stability_checks
        ),
        "printed_markov_matrix_row_stochastic_checked": True,
        "printed_stationary_distribution_checked": True,
        "Markov_asymptotic_equality_certified": False,
    }


def orbit_until_one(function, start: int, cap: int = 100_000) -> list[int]:
    value = start
    result = [value]
    for _ in range(cap):
        if value == 1:
            return result
        value = function(value)
        result.append(value)
    raise AssertionError(("orbit cap", function.__name__, start))


def maximum_and_roosendaal_checks() -> dict[str, int | bool]:
    maximum_bridge_checks = 0
    roosendaal_checks = 0
    shortened_records: list[int] = []
    unshortened_records: list[int] = []
    best_t = -1
    best_u = -1

    for start in range(1, 200_001):
        t_maximum = max(orbit_until_one(shortened, start))
        u_maximum = max(orbit_until_one(unshortened, start))
        if start > 1 and start % 2:
            assert u_maximum == 2 * t_maximum
            maximum_bridge_checks += 1
        if t_maximum > best_t:
            shortened_records.append(start)
            best_t = t_maximum
        if u_maximum > best_u:
            unshortened_records.append(start)
            best_u = u_maximum
        if start > 2 and start % 2 and u_maximum > 3 * start + 1:
            assert u_maximum % 36 == 16
            roosendaal_checks += 1

    assert shortened_records[1:] == unshortened_records[1:]
    assert all(record == 2 or record % 2 for record in unshortened_records)
    return {
        "odd_shortened_unshortened_maximum_factor_two_checks": maximum_bridge_checks,
        "finite_record_start_sequence_agreement": True,
        "Roosendaal_mod36_maximum_checks": roosendaal_checks,
        "Roosendaal_statement_applies_to_maxima_not_starts_checked": True,
    }


def exact_bound_arithmetic_checks() -> dict[str, int | bool]:
    assert 20 * 2**58 == 5_764_607_523_034_234_880
    assert 87 * 2**60 == 100_304_170_900_795_686_912
    assert 2075 * 2**60 == 2_392_312_122_059_207_475_200
    assert 2175975546 * 2**40 == 2_392_510_414_583_230_365_696
    assert 2**32 * 2**40 == 2**72
    for task_id in (0, 1, 1_000_000_000, 2_175_975_546):
        lower = task_id * 2**40
        upper = (task_id + 1) * 2**40
        assert upper - lower == 2**40
        assert lower <= lower + 3 < upper
        assert (upper - 1 - (lower + 3)) % 4 == 0
    assert shortened(20 * 2**58) == 10 * 2**58
    assert iterate(shortened, 2**71, 71) == 1
    return {
        "Oliveira_bound_exact": 20 * 2**58,
        "yoyo_bound_exact": 87 * 2**60,
        "dynamic_status_bound_exact": 2075 * 2**60,
        "dynamic_first_incomplete_start_exact": 2175975546 * 2**40,
        "server_representable_endpoint_exact": 2**72,
        "half_open_work_unit_checks": 4,
        "inclusive_Oliveira_endpoint_reduction_checked": True,
        "Barina_boundary_power_of_two_reduction_checked": True,
    }


def main() -> None:
    report = {
        "status": "PASS",
        "scope": "finite exact F031 computational-verification chronology kernels",
        **source_and_repository_checks(),
        **map_and_block_checks(),
        **dyadic_affine_checks(),
        **transport_and_coalescence_checks(),
        **recursive_predecessor_finite_checks(),
        **small_sieve_reproduction_checks(),
        **generalized_coordinate_checks(),
        **maximum_and_roosendaal_checks(),
        **exact_bound_arithmetic_checks(),
        "explicitly_not_certified": [
            "any historical distributed run or completed-work database",
            "hardware, compiler, network, or server correctness",
            "the full 2^24 or 2^34 sieve independently of pinned artifacts",
            "an unbounded recursive v3 coefficient invariant beyond k <= 34",
            "the Oliveira 3x+1, 5x+1, or 7x+1 exhaustive computations",
            "the Barina 2^68, 2^71, or later dynamic exhaustive computation",
            "the non-rigorous Markov growth exponents",
            "the Collatz conjecture",
        ],
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
