"""Exact finite checks accompanying the preprint; not a proof of Tao's theorem."""
from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
import json

if not __debug__:
    raise RuntimeError("Run without -O: disabled assertions must not yield a PASS.")


def v2(n):
    assert n > 0
    return (n & -n).bit_length() - 1


def full(n):
    return 3 * n + 1 if n % 2 else n // 2


def short(n):
    return (3 * n + 1) // 2 if n % 2 else n // 2


def odd(n):
    return n >> v2(n)


def advance(fn, n, steps):
    for _ in range(steps):
        n = fn(n)
    return n


def clocks():
    checked = 0
    for n in range(1, 1025):
        a = v2(n)
        m = odd(n)
        accumulated = 0
        for j in range(17):
            assert advance(full, n, a + j + accumulated) == m
            assert advance(short, n, a + accumulated) == m
            q = v2(3 * m + 1)
            nxt = (3 * m + 1) >> q
            for r in range(1, q + 2):
                assert advance(full, m, r) == (1 << (q - r + 1)) * nxt
                checked += 1
            for r in range(1, q + 1):
                assert advance(short, m, r) == (1 << (q - r)) * nxt
                checked += 1
            accumulated += q
            m = nxt
    return checked


def sampling():
    for x in range(1, 257):
        h = sum((Q(1, n) for n in range(1, x + 1)), Q(0))
        ho = sum((Q(1, n) for n in range(1, x + 1, 2)), Q(0))
        hh = sum((Q(1, n) for n in range(1, x // 2 + 1)), Q(0))
        pushes = {m: Q(0) for m in range(1, x + 1, 2)}
        for n in range(1, x + 1):
            pushes[odd(n)] += Q(1, n) / h
        deficiency = Q(0)
        for m in pushes:
            r = (x // m).bit_length() - 1
            assert pushes[m] == (2 - Q(1, 2 ** r)) / (m * h)
            deficiency += Q(1, 2 ** r * m)
        assert deficiency == 2 * ho - h == h - hh
        l1 = sum(abs(pushes[m] - Q(1, m) / ho) for m in pushes)
        assert l1 <= 2 * deficiency / h
        for a in range(10):
            left = sum((Q(1, n) for n in range(1, x + 1) if v2(n) == a), Q(0))
            right = Q(1, 2 ** a) * sum(
                (Q(1, m) for m in range(1, x // 2 ** a + 1, 2)), Q(0)
            )
            assert left == right
    return 256


def passage(mapping, start, threshold):
    # 0 is the separate failure state for this finite model, never an integer orbit state.
    if start == 0:
        return 0
    seen = set()
    current = start
    while current > threshold:
        if current in seen:
            return 0
        seen.add(current)
        current = mapping[current - 1]
    return current


def push(mapping, threshold, measure):
    result = [Q(0)] * 5
    for state, mass in enumerate(measure):
        result[passage(mapping, state, threshold)] += mass
    return result


def distance(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))


def kernels():
    checked = 0
    bases = [[Q((state + k) % 5 + 1, 15) for state in range(5)] for k in range(3)]
    for mapping in product(range(1, 5), repeat=4):
        for lower in range(1, 5):
            for upper in range(lower, 5):
                for state in range(5):
                    target = passage(mapping, state, lower)
                    assert passage(mapping, passage(mapping, state, upper), lower) == target
                    assert passage(mapping, target, upper) == target
                    checked += 1
        scales = [1, 2, 4]
        measures = [push(mapping, threshold, base) for threshold, base in zip(scales, bases)]
        errors = [distance(measures[i], push(mapping, scales[i], measures[i + 1])) for i in range(2)]
        assert distance(measures[0], push(mapping, 1, measures[2])) <= sum(errors)
        for a, b in product(measures, repeat=2):
            qa, qb = list(a), list(b)
            qa[1] += qa[0]
            qb[1] += qb[0]
            qa[0] = qb[0] = Q(0)
            assert distance(a, b) <= distance(qa, qb) + 2 * abs(a[0] - b[0])
    return checked


def push_atoms(images, masses):
    """Push a finitely supported signed measure, retaining exact fibre sums."""
    result = {}
    for image, mass in zip(images, masses):
        if mass:
            result[image] = result.get(image, 0) + mass
    return result


def joint_entries():
    """Check finite algebra of cor:joint-entry, not its limiting conclusion.

    The finite orbit state space is {1,...,n}; 0 denotes the separate dagger.
    Thresholds are arbitrary half-integers, unrelated to any starting scales.
    """
    counts = {
        "maps": 0,
        "maps_with_failed_positive_start_passage": 0,
        "threshold_state_passages": 0,
        "failed_positive_start_passages": 0,
        "chains_by_length": {"1": 0, "2": 0, "3": 0},
        "chains_with_repeated_thresholds": 0,
        "chains_with_noninteger_thresholds": 0,
        "chains_with_largest_threshold_above_domain": 0,
        "independently_enumerated_product_tuples": 0,
        "compatible_tuples_and_inverse_checks": 0,
        "bijections": 0,
        "signed_l1_isometry_checks": 0,
        "rational_signed_l1_isometry_checks": 0,
        "common_input_dirac_columns_including_dagger": 0,
        "common_input_probability_laws": 0,
        "common_input_marginal_laws": 0,
        "positive_starts_with_mixed_success_failure_coordinates": 0,
    }
    # Every integer signed measure with coefficients in {-1,0,1} is tested
    # on each largest-threshold state space, together with a rational probe.
    signed_probes = {
        size: [(weights, sum(abs(w) for w in weights))
               for weights in product((-1, 0, 1), repeat=size)]
        for size in range(2, 6)
    }
    for n in range(1, 5):
        states = tuple(range(n + 1))
        thresholds = tuple(Q(k, 2) for k in range(2, 2 * n + 3))
        harmonic_mass = sum((Q(1, state) for state in range(1, n + 1)), Q(0))
        common_inputs = (
            (Q(0),) + (Q(1, n),) * n,
            (Q(0),) + tuple(Q(1, state) / harmonic_mass for state in range(1, n + 1)),
        )
        assert all(sum(weights) == 1 for weights in common_inputs)
        for mapping in product(range(1, n + 1), repeat=n):
            counts["maps"] += 1
            passages = {
                threshold: tuple(passage(mapping, state, threshold) for state in states)
                for threshold in thresholds
            }
            failed_for_map = False
            for threshold in thresholds:
                assert passages[threshold][0] == 0
                for state in range(1, n + 1):
                    counts["threshold_state_passages"] += 1
                    if passages[threshold][state] == 0:
                        counts["failed_positive_start_passages"] += 1
                        failed_for_map = True
            counts["maps_with_failed_positive_start_passage"] += int(failed_for_map)
            for length in range(1, 4):
                for chain in combinations_with_replacement(thresholds, length):
                    counts["chains_by_length"][str(length)] += 1
                    counts["chains_with_repeated_thresholds"] += int(len(set(chain)) < length)
                    counts["chains_with_noninteger_thresholds"] += int(any(x.denominator != 1 for x in chain))
                    counts["chains_with_largest_threshold_above_domain"] += int(chain[-1] > n)
                    domains = [tuple(state for state in states if state == 0 or state <= x) for x in chain]
                    largest_domain = domains[-1]
                    # Construct C from its compatibility equations, independently
                    # of the proposed image of J.
                    compatible = set()
                    for candidate in product(*domains):
                        counts["independently_enumerated_product_tuples"] += 1
                        if all(passages[chain[i]][candidate[i + 1]] == candidate[i]
                               for i in range(length - 1)):
                            compatible.add(candidate)
                    images = {
                        state: tuple(passages[x][state] for x in chain)
                        for state in largest_domain
                    }
                    assert set(images.values()) == compatible
                    assert len(images) == len(set(images.values())) == len(compatible)
                    for state, image in images.items():
                        assert image[-1] == state
                    for candidate in compatible:
                        assert images[candidate[-1]] == candidate
                        counts["compatible_tuples_and_inverse_checks"] += 1
                    counts["bijections"] += 1

                    image_atoms = tuple(images[state] for state in largest_domain)
                    for signed, original_norm in signed_probes[len(largest_domain)]:
                        lifted = push_atoms(image_atoms, signed)
                        assert sum(abs(mass) for mass in lifted.values()) == original_norm
                        counts["signed_l1_isometry_checks"] += 1
                    signed_rational = tuple(Q(3 * i - 4, 2 * i + 1) for i in range(len(largest_domain)))
                    lifted = push_atoms(image_atoms, signed_rational)
                    assert sum(abs(mass) for mass in lifted.values()) == sum(abs(mass) for mass in signed_rational)
                    counts["rational_signed_l1_isometry_checks"] += 1

                    joint_atoms = tuple(tuple(passages[x][state] for x in chain) for state in states)
                    for state, joint_atom in enumerate(joint_atoms):
                        assert joint_atom == images[passages[chain[-1]][state]]
                        counts["common_input_dirac_columns_including_dagger"] += 1
                        if state and 0 in joint_atom and any(value != 0 for value in joint_atom):
                            counts["positive_starts_with_mixed_success_failure_coordinates"] += 1
                    for common_input in common_inputs:
                        direct_joint = push_atoms(joint_atoms, common_input)
                        largest_law = push_atoms(passages[chain[-1]], common_input)
                        lifted_joint = push_atoms(
                            tuple(images[state] for state in largest_law),
                            tuple(largest_law.values()),
                        )
                        assert direct_joint == lifted_joint
                        assert sum(direct_joint.values()) == 1
                        assert set(direct_joint) <= compatible
                        counts["common_input_probability_laws"] += 1
                        for i, threshold in enumerate(chain):
                            marginal = push_atoms(tuple(atom[i] for atom in direct_joint), tuple(direct_joint.values()))
                            direct_marginal = push_atoms(passages[threshold], common_input)
                            assert marginal == direct_marginal
                            counts["common_input_marginal_laws"] += 1
    assert counts["maps"] == 1 + 4 + 27 + 256 == 288
    assert counts["failed_positive_start_passages"] > 0
    assert counts["positive_starts_with_mixed_success_failure_coordinates"] > 0
    return {
        "scope": {
            "finite_domain": "D={1,...,n}, 1<=n<=4; all maps D->D",
            "failure_state": "0 represents dagger and is not in D",
            "thresholds": "all half-integers 1,3/2,...,n+1; all nondecreasing chains of lengths 1,2,3",
            "signed_measure_probes": "all coefficients in {-1,0,1} on E_largest, plus one mixed-sign rational probe",
            "common_inputs": "uniform and harmonic probabilities on D, plus every Dirac column including dagger",
        },
        **counts,
    }


def log_interval(x, terms=80):
    # log(x) = 2 sum z^(2j+1)/(2j+1), z=(x-1)/(x+1), with a positive tail bound.
    assert x >= 1
    z = (x - 1) / (x + 1)
    lower = 2 * sum((z ** (2 * j + 1) / (2 * j + 1) for j in range(terms)), Q(0))
    upper = lower + 2 * z ** (2 * terms + 1) / ((2 * terms + 1) * (1 - z * z))
    return lower, upper


def constants_and_words():
    a0, a1 = log_interval(Q(4, 3))
    b0, b1 = log_interval(Q(2))
    assert Q(6023552, 10 ** 7) < b0 / (4 * a1)
    assert b1 / (4 * a0) < Q(6023553, 10 ** 7)
    assert b0 * b0 / (4 * a1) - b1 / 2 > 0
    assert Q(99, 100) * b0 - b1 * b1 / (4 * a0) > 0
    assert Q(4, 25) - Q(1, 4) + Q(1, 100000) == -Q(8999, 100000)
    assert 3 ** 5 < 2 ** 8
    assert Q(1001, 1000) ** 3 - 1 < Q(1, 300)
    assert a0 / (10 * b1) > Q(1, 40)
    checked = 0
    cap = 6
    one_mass = sum((Q(1, 2 ** a) for a in range(1, cap + 1)), Q(0))
    one_moment = sum((Q(a, 2 ** a) for a in range(1, cap + 1)), Q(0))
    assert one_mass == 1 - Q(1, 2 ** cap)
    assert one_moment == 2 - Q(cap + 2, 2 ** cap)
    for m in range(1, 5):
        total = Q(0)
        for word in product(range(1, cap + 1), repeat=m):
            A = sum(word)
            offset = sum((Q(3 ** (m - i - 1), 2 ** sum(word[i:])) for i in range(m)), Q(0))
            numerator = offset * 2 ** A
            assert numerator.denominator == 1 and numerator.numerator % 2 == 1
            value = Q(5)
            for a in word:
                value = (3 * value + 1) / 2 ** a
            assert value == Q(3 ** m, 2 ** A) * 5 + offset
            total += Q(word[-1], 2 ** A)
            checked += 1
        assert total == one_mass ** (m - 1) * one_moment
    return checked


def main():
    result = {
        "status": "PASS",
        "clock_segment_checks": clocks(),
        "sampling_cutoffs": sampling(),
        "finite_map_nested_passage_checks": kernels(),
        "positive_valuation_words_checked": constants_and_words(),
        "joint_first_entry_checks": joint_entries(),
        "arithmetic": "integers_and_exact_rationals_only",
        "exclusions": [
            "No proof of Tao's analytic first-passage or Fourier-renewal estimates",
            "No finite experiment is used as proof of the limiting entrance law",
            "No Collatz convergence assertion and no Lean formalization claim",
        ],
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
