#!/usr/bin/env python3
"""Exact, bounded certificate for the single affine packet (m,A)=(10,16).

Python standard library only. Run without -O, optionally with --receipt PATH.
No literature files or other certificate implementations are imported.
The complete joint table is stored with row C mod 13, column C mod 499.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
from itertools import combinations
import json
from math import comb, gcd
from pathlib import Path
import platform
import sys
from time import perf_counter_ns


if not __debug__ or sys.flags.optimize:
    raise SystemExit("Optimized Python is rejected: assertions must remain active.")

M, A = 10, 16
P, Q = 13, 499
D = 2**A - 3**M
assert D == P * Q == 6487
STRATA = (1, P, Q, D)


def compositions_by_cuts():
    for cuts in combinations(range(1, A), M - 1):
        boundaries = (0,) + cuts + (A,)
        yield tuple(boundaries[i + 1] - boundaries[i] for i in range(M))


def compositions_by_recursion(m, total):
    if m == 1:
        if total >= 1:
            yield (total,)
        return
    for first in range(1, total - m + 2):
        for tail in compositions_by_recursion(m - 1, total - first):
            yield (first,) + tail


def numerator_formula(word):
    prefix = [sum(word[:j]) for j in range(len(word))]
    return sum(3 ** (len(word) - 1 - j) * 2**prefix[j] for j in range(len(word)))


def numerator_growing(word):
    value, total = 0, 0
    for letter in word:
        value = 3 * value + 2**total
        total += letter
    return value


def numerator_first_letter(word):
    if not word:
        return 0
    return 3 ** (len(word) - 1) + 2 ** word[0] * numerator_first_letter(word[1:])


def rotate(word, j):
    return word[j:] + word[:j]


def period(word):
    return next(j for j in range(1, len(word) + 1) if rotate(word, j) == word)


@lru_cache(None)
def joint_dp(m, total):
    if total < m:
        return Counter()
    if m == 1:
        return Counter({(1 % P, 1 % Q): 1})
    result = Counter()
    shift = 3 ** (m - 1)
    for first in range(1, total - m + 2):
        multiplier = 2**first
        for (u, v), count in joint_dp(m - 1, total - first).items():
            result[((shift + multiplier * u) % P, (shift + multiplier * v) % Q)] += count
    assert sum(result.values()) == comb(total - 1, m - 1)
    return result


@lru_cache(None)
def single_dp(modulus, m, total):
    if total < m:
        return Counter()
    if m == 1:
        return Counter({1 % modulus: 1})
    result = Counter()
    for first in range(1, total - m + 2):
        for residue, count in single_dp(modulus, m - 1, total - first).items():
            result[(3 ** (m - 1) + 2**first * residue) % modulus] += count
    assert sum(result.values()) == comb(total - 1, m - 1)
    return result


CRT_P = Q * pow(Q, -1, P)
CRT_Q = P * pow(P, -1, Q)


def crt(u, v):
    return (CRT_P * u + CRT_Q * v) % D


def witness(word):
    value = numerator_formula(word)
    return {
        "word": list(word), "numerator": value,
        "residue_mod_13": value % P, "residue_mod_499": value % Q,
        "gcd_with_D": gcd(value, D), "least_packet_rotation_period": period(word),
    }


def full_strata(counter):
    return {str(divisor): counter[divisor] for divisor in STRATA}


def peak_working_set_bytes():
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes

        class ProcessMemoryCounters(ctypes.Structure):
            _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD)] + [
                (field, ctypes.c_size_t) for field in (
                    "PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage",
                    "QuotaPagedPoolUsage", "QuotaPeakNonPagedPoolUsage", "QuotaNonPagedPoolUsage",
                    "PagefileUsage", "PeakPagefileUsage",
                )
            ]

        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        psapi = ctypes.WinDLL("psapi", use_last_error=True)
        kernel.GetCurrentProcess.restype = wintypes.HANDLE
        psapi.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(ProcessMemoryCounters), wintypes.DWORD]
        counters = ProcessMemoryCounters()
        counters.cb = ctypes.sizeof(counters)
        if not psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(), ctypes.byref(counters), counters.cb):
            raise ctypes.WinError(ctypes.get_last_error())
        return counters.PeakWorkingSetSize
    import resource
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return peak if sys.platform == "darwin" else 1024 * peak


def check():
    started = perf_counter_ns()
    words = list(compositions_by_cuts())
    assert words == list(compositions_by_recursion(M, A))
    assert len(words) == len(set(words)) == comb(A - 1, M - 1) == 5005
    strata_all, strata_primitive, strata_classes = Counter(), Counter(), Counter()
    periods = Counter()
    classes = defaultdict(list)
    direct_joint = Counter()
    direct_D = Counter()
    numerators = {}
    cyclic_transport_checks = 0
    repeated_root_checks = 0
    for word in words:
        assert len(word) == M and sum(word) == A and min(word) >= 1
        value = numerator_formula(word)
        assert value == numerator_growing(word) == numerator_first_letter(word)
        numerators[word] = value
        divisor = gcd(value, D)
        assert divisor in STRATA
        strata_all[divisor] += 1
        direct_joint[(value % P, value % Q)] += 1
        direct_D[value % D] += 1
        least_period = period(word)
        periods[least_period] += 1
        if least_period == M:
            strata_primitive[divisor] += 1
        else:
            assert least_period == 5 and word == word[:5] * 2
            assert sum(word[:5]) == 8
            assert value == (2**8 + 3**5) * numerator_formula(word[:5])
            assert divisor == Q
            repeated_root_checks += 1
        representative = min(rotate(word, j) for j in range(M))
        classes[representative].append(word)
        rotated_value = numerator_formula(rotate(word, 1))
        assert 3 * value + D == 2 ** word[0] * rotated_value
        assert gcd(rotated_value, D) == divisor
        cyclic_transport_checks += 1
    primitive_class_count = 0
    for representative, members in classes.items():
        least_period = period(representative)
        assert len(members) == least_period
        divisor = gcd(numerators[representative], D)
        assert all(gcd(numerators[word], D) == divisor for word in members)
        if least_period == M:
            primitive_class_count += 1
            strata_classes[divisor] += 1
    assert all(strata_primitive[d] == M * strata_classes[d] for d in STRATA)
    assert full_strata(strata_all) == {"1": 4560, "13": 410, "499": 35, "6487": 0}
    assert full_strata(strata_primitive) == {"1": 4560, "13": 410, "499": 0, "6487": 0}
    assert full_strata(strata_classes) == {"1": 456, "13": 41, "499": 0, "6487": 0}
    assert repeated_root_checks == 35

    joint = joint_dp(M, A)
    assert joint == direct_joint
    marginal_P, marginal_Q = Counter(), Counter()
    for (u, v), count in joint.items():
        marginal_P[u] += count
        marginal_Q[v] += count
    assert marginal_P == single_dp(P, M, A)
    assert marginal_Q == single_dp(Q, M, A)
    assert direct_D == single_dp(D, M, A)
    assert Counter({crt(u, v): count for (u, v), count in joint.items()}) == direct_D
    dense = [[joint[(u, v)] for v in range(Q)] for u in range(P)]
    assert sum(map(sum, dense)) == 5005
    assert len(joint) == 3473 and len(marginal_P) == P and len(marginal_Q) == Q

    pairs = set()
    for residue in range(D):
        pair = (residue % P, residue % Q)
        assert crt(*pair) == residue
        pairs.add(pair)
    assert pairs == {(u, v) for u in range(P) for v in range(Q)}
    for u, v in pairs:
        residue = crt(u, v)
        assert residue % P == u and residue % Q == v
    synchronization_checks = 0
    for m in range(2, M + 1):
        shift = 3 ** (m - 1)
        for first in range(1, A - M + 2):
            multiplier = 2**first
            inverse_D = pow(multiplier, -1, D)
            inverse_P = pow(multiplier, -1, P)
            inverse_Q = pow(multiplier, -1, Q)
            for residue in range(D):
                image = (shift + multiplier * residue) % D
                u = (shift + multiplier * (residue % P)) % P
                v = (shift + multiplier * (residue % Q)) % Q
                assert crt(u, v) == image
                assert inverse_D * (image - shift) % D == residue
                assert inverse_P * (u - shift) % P == residue % P
                assert inverse_Q * (v - shift) % Q == residue % Q
                preimage = inverse_D * (residue - shift) % D
                assert (shift + multiplier * preimage) % D == residue
                synchronization_checks += 1
    assert synchronization_checks == 9 * 7 * D == 408681

    witnesses = {}
    for modulus in (P, Q):
        divisible = [word for word in words if numerators[word] % modulus == 0]
        primitive_divisible = [word for word in divisible if period(word) == M]
        witnesses[str(modulus)] = {
            "lexicographically_least_all_words": witness(min(divisible)),
            "least_numerator_all_words_tie_break_lex": witness(min(divisible, key=lambda word: (numerators[word], word))),
            "lexicographically_least_primitive_word": witness(min(primitive_divisible)) if primitive_divisible else None,
        }
    assert marginal_P[0] == strata_all[P] + strata_all[D]
    assert marginal_Q[0] == strata_all[Q] + strata_all[D]
    assert joint[(0, 0)] == strata_all[D]
    assert marginal_P[0] > 0 and marginal_Q[0] > 0 and joint[(0, 0)] == 0
    peak = peak_working_set_bytes()
    assert peak < 5_000_000_000
    return {
        "status": "pass", "scope": {"m": M, "A": A, "D": D, "factorization": [P, Q]},
        "word_count": len(words),
        "primitive_word_count": sum(strata_primitive.values()),
        "imprimitive_word_count": len(words) - sum(strata_primitive.values()),
        "all_cyclic_class_count": len(classes),
        "primitive_cyclic_class_count": primitive_class_count,
        "imprimitive_cyclic_class_count": len(classes) - primitive_class_count,
        "word_counts_by_least_packet_period": dict(sorted(periods.items())),
        "gcd_strata_all_words": full_strata(strata_all),
        "gcd_strata_primitive_words": full_strata(strata_primitive),
        "gcd_strata_primitive_cyclic_classes": full_strata(strata_classes),
        "least_witnesses": witnesses,
        "joint_support_size": len(joint),
        "joint_zero_cell_count": P * Q - len(joint),
        "joint_origin_count": joint[(0, 0)],
        "marginal_support_sizes": {"13": len(marginal_P), "499": len(marginal_Q)},
        "marginal_zero_counts": {"13": marginal_P[0], "499": marginal_Q[0]},
        "full_joint_table_rows_mod_13_columns_mod_499": dense,
        "full_marginal_mod_13": [marginal_P[u] for u in range(P)],
        "full_marginal_mod_499": [marginal_Q[v] for v in range(Q)],
        "joint_dense_table_sha256_compact_json": hashlib.sha256(json.dumps(dense, separators=(",", ":")).encode()).hexdigest(),
        "checks": {
            "independent_enumerators_equal": True,
            "numerator_formula_growing_and_first_letter_equal": 5005,
            "cyclic_transport_and_gcd_invariance": cyclic_transport_checks,
            "imprimitive_squares_and_exact_499_numerator_multiplier": repeated_root_checks,
            "joint_dp_equals_complete_direct_joint_count": True,
            "marginals_equal_independent_single_modulus_dp": [P, Q],
            "joint_CRT_pushforward_equals_independent_mod_D_dp": True,
            "CRT_both_inverse_identities_each_domain_size": D,
            "synchronized_transition_and_inverse_tests": synchronization_checks,
            "transition_indices": {"m_inclusive": [2, 10], "first_letter_inclusive": [1, 7], "residue_inclusive": [0, D - 1]},
            "joint_dp_cached_states": joint_dp.cache_info().currsize,
            "single_modulus_dp_cached_states": single_dp.cache_info().currsize,
        },
        "CRT_inverse": {"formula": "(3992*u + 2496*v) mod 6487", "coefficient_u": CRT_P, "coefficient_v": CRT_Q},
        "execution": {"python": sys.version, "platform": platform.platform(), "optimized": sys.flags.optimize,
                      "elapsed_ns": perf_counter_ns() - started, "peak_working_set_bytes": peak,
                      "peak_working_set_below_5000000000_bytes": True},
        "nonclaims": ["Only the (10,16) packet is enumerated; no extended cycle search was run.",
                      "Finite checks do not replace a general proof or establish a novelty claim."],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    result = check()
    result["recorded_utc"] = datetime.now(timezone.utc).isoformat()
    result["certificate_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result["command_argv"] = sys.argv
    if args.receipt:
        with args.receipt.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(result, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
    summary = {key: value for key, value in result.items() if not key.startswith("full_")}
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
