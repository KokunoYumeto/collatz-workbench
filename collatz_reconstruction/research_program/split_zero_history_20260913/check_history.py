"""Exact finite certificates for the Split Zero / Collatz history application.

Standard library only. Writes JSON to stdout and creates no output files.
The Hurwitz analytic theorem is audited in AUDIT.md, not numerically tested here.
Run: python -B check_history.py
"""

from fractions import Fraction as F
from itertools import product
from math import comb, prod
import json


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def trim(poly):
    poly = list(poly)
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return tuple(poly)


def evaluate(poly, x):
    result = F(0)
    for coefficient in reversed(poly):
        result = result * x + coefficient
    return result


def multiply_root(poly, root):
    result = [0] * (len(poly) + 1)
    for j, coefficient in enumerate(poly):
        result[j] -= root * coefficient
        result[j + 1] += coefficient
    return result


def forward_numerator(word):
    """P_w(q) for T_last ... T_first(x)=(q^m*x+P_w(q))/2^N."""
    m = sum(word)
    coefficients = [0] * max(1, m)
    s = 0
    for j, digit in enumerate(word):
        if digit:
            coefficients[m - 1 - s] += 2**j
            s += 1
    return trim(coefficients)


def recover_word(n, polynomial):
    result = [0] * n
    last_position = -1
    for coefficient in reversed(polynomial):
        if coefficient == 0:
            continue
        require(coefficient > 0 and coefficient & (coefficient - 1) == 0,
                "nonzero formal coefficients must be powers of two")
        position = coefficient.bit_length() - 1
        require(last_position < position < n, "coefficient order or word length")
        result[position] = 1
        last_position = position
    return tuple(result)


def shortcut(n):
    return (3 * n + 1) // 2 if n % 2 else n // 2


def parity_prefix(n, length):
    digits = []
    for _ in range(length):
        digits.append(n % 2)
        n = shortcut(n)
    return tuple(digits), n


def check_forward(max_n=10):
    word_count = residue_count = lift_count = 0
    for n in range(max_n + 1):
        modulus = 2**n
        residues = {}
        for word in product((0, 1), repeat=n):
            polynomial = forward_numerator(word)
            require(recover_word(n, polynomial) == word, "formal word inverse")
            # Independent affine composition, retaining every polynomial term.
            intercept = (F(0),)
            slope = (F(1),)
            for digit in word:
                intercept = ((F(0),) + intercept) if digit else intercept
                intercept = [value / 2 for value in intercept]
                intercept[0] += F(digit, 2)
                intercept = trim(intercept)
                slope = ((F(0),) + slope) if digit else slope
                slope = tuple(value / 2 for value in slope)
            require(intercept == trim(F(c, modulus) for c in polynomial),
                    "forward affine numerator formula")
            require(slope == tuple([F(0)] * sum(word) + [F(1, modulus)]),
                    "forward affine slope")
            b = int(evaluate(polynomial, 3))
            residue = (-b * pow(3**sum(word), -1, modulus)) % modulus
            require(residue not in residues, "parity cylinder injectivity")
            residues[residue] = word
            for k in range(3):
                start = residue + k * modulus
                actual, end = parity_prefix(start, n)
                require(actual == word, "cylinder lift parity")
                require(modulus * end == 3**sum(word) * start + b,
                        "specialized affine endpoint")
                lift_count += 1
            word_count += 1
        # Independent exhaustive scan of every residue, without prescribed bits.
        for residue in range(modulus):
            actual, _ = parity_prefix(residue, n)
            require(residues[residue] == actual, "complete residue partition")
            residue_count += 1
    return {"maximum_length": max_n, "words": word_count,
            "residues_exhausted": residue_count, "integer_lifts": lift_count}


def f_series(binary_integer):
    coefficients = []
    j = 0
    while binary_integer:
        if binary_integer & 1:
            coefficients.append(F(1, 2**(j + 1)))
        j += 1
        binary_integer >>= 1
    return tuple(coefficients or [F(0)])


def check_information_loss():
    first, second = f_series(17), f_series(28)
    require(first == (F(1, 2), F(1, 32)), "17 formal series")
    require(second == (F(1, 8), F(1, 16), F(1, 32)), "28 formal series")
    require(first != second and evaluate(first, 3) == evaluate(second, 3) == F(19, 32),
            "specialization endpoint collision")
    difference = tuple((second[j] if j < len(second) else 0)
                       - (first[j] if j < len(first) else 0) for j in range(3))
    require(difference == tuple(F(c, 32) for c in (-12, 1, 1)),
            "difference is (q-3)(q+4)/32")
    # Both matrices have diagonal (q/4,1); their off-diagonal terms differ.
    require(forward_numerator((0, 1)) == (2,), "01 intercept numerator")
    require(forward_numerator((1, 0)) == (1,), "10 intercept numerator")
    return {"f_series_indices": [17, 28], "specialized_value": "19/32",
            "difference_numerator_ascending": [-12, 1, 1],
            "same_spectrum_words": [[0, 1], [1, 0]],
            "different_forward_translations": ["1/2", "1/4"]}


def compositions(total, length):
    if length == 1:
        if total >= 1:
            yield (total,)
        return
    for first in range(1, total - length + 2):
        for tail in compositions(total - first, length - 1):
            yield (first,) + tail


def odd_b(word):
    result, prefix_sum = 0, 0
    for a in word:
        result = 3 * result + 2**prefix_sum
        prefix_sum += a
    return result


def odd_path(start, word):
    current = start
    require(current % 2 == 1, "odd starting value")
    for a in word:
        value = 3 * current + 1
        require(value % 2**a == 0 and (value // 2**a) % 2 == 1,
                "exact odd-return valuation")
        current = value // 2**a
    return current


def moments(nodes, weights, count):
    result = []
    for degree in range(count):
        result.append(sum((weight * node**degree
                           for node, weight in zip(nodes, weights)), F(0)))
    return result


def lagrange_basis(nodes):
    """Ascending exact coefficient vectors, using synthetic division."""
    full = [1]
    for node in nodes:
        full = multiply_root(full, node)
    result = []
    k = len(nodes)
    for node in nodes:
        quotient = [0] * k
        quotient[-1] = full[-1]
        for degree in range(k - 1, 0, -1):
            quotient[degree - 1] = full[degree] + node * quotient[degree]
        require(full[0] + node * quotient[0] == 0, "synthetic division remainder")
        denominator = evaluate(quotient, node)
        require(denominator != 0, "distinct interpolation nodes")
        result.append(tuple(F(coefficient) / denominator for coefficient in quotient))
    return result


def check_odd_return(max_a=9):
    packet_count = word_count = interpolation_count = ambiguity_count = 0
    max_k = 0
    example = None
    for a in range(1, max_a + 1):
        for m in range(1, a + 1):
            words = list(compositions(a, m))
            k = len(words)
            require(k == comb(a - 1, m - 1), "composition count")
            modulus = 2**(a + 1)
            b_values = [odd_b(word) for word in words]
            nodes = [((2**a - b) * pow(3**m, -1, modulus)) % modulus
                     for b in b_values]
            require(len(set(nodes)) == k, "odd-return cylinder injectivity")
            for word, b, node in zip(words, b_values, nodes):
                require(0 < node < modulus and node % 2 == 1, "canonical odd node")
                for start in (node, node + modulus):
                    end = odd_path(start, word)
                    require(2**a * end == 3**m * start + b, "odd affine formula")
            basis = lagrange_basis(nodes)
            for i, polynomial in enumerate(basis):
                for j, node in enumerate(nodes):
                    require(evaluate(polynomial, node) == int(i == j),
                            "Lagrange evaluation delta")
            denominator = 2**a - 3**m
            require(denominator != 0, "nonzero return denominator")
            qualifies = [b % abs(denominator) == 0 for b in b_values]
            for word, b, flag in zip(words, b_values, qualifies):
                if flag:
                    start = b // denominator
                    require(odd_path(start, word) == start, "integer return predicate")
                    require((start > 0) == (denominator > 0), "return sign")
            indicator = [sum((basis[i][j] for i in range(k) if qualifies[i]), F(0))
                         for j in range(k)]
            for weights in ([F(1, k)] * k,
                            [F(i + 1, k * (k + 1) // 2) for i in range(k)]):
                moment = moments(nodes, weights, k)
                recovered = [sum((c * moment[j] for j, c in enumerate(poly)), F(0))
                             for poly in basis]
                require(recovered == weights, "moment recovery of all probabilities")
                recovered_mass = sum((c * moment[j] for j, c in enumerate(indicator)), F(0))
                actual_mass = sum((weight for weight, flag in zip(weights, qualifies) if flag), F(0))
                require(recovered_mass == actual_mass, "arithmetic predicate mass")
                interpolation_count += 1
            if k >= 2:
                null = [F(1, prod(node - other for j, other in enumerate(nodes) if i != j))
                        for i, node in enumerate(nodes)]
                null_moments = moments(nodes, null, k)
                require(null_moments[:-1] == [0] * (k - 1) and null_moments[-1] == 1,
                        "Vandermonde null vector and first surviving moment")
                epsilon = F(1, 2 * k) / max(abs(v) for v in null)
                plus = [F(1, k) + epsilon * v for v in null]
                minus = [F(1, k) - epsilon * v for v in null]
                require(min(plus + minus) > 0 and sum(plus) == sum(minus) == 1,
                        "positive probability perturbations")
                require(plus != minus and moments(nodes, plus, k - 1) == moments(nodes, minus, k - 1),
                        "lower-jet ambiguity")
                require(moments(nodes, plus, k)[-1] != moments(nodes, minus, k)[-1],
                        "sharp last required moment")
                ambiguity_count += 1
            if (m, a) == (2, 4):
                require(words == [(1, 3), (2, 2), (3, 1)] and nodes == [19, 1, 29],
                        "explicit (2,4) nodes")
                require(qualifies == [False, True, False], "explicit integer return subset")
                expected = [F(551, 504), F(-48, 504), F(1, 504)]
                require(indicator == expected, "explicit mass polynomial")
                example = {"words": words, "nodes": nodes, "B_values": b_values,
                           "D": denominator, "indicator_coefficients_ascending": [str(c) for c in expected],
                           "mass_formula": "(m2 - 48*m1 + 551)/504"}
            packet_count += 1
            word_count += k
            max_k = max(max_k, k)
    return {"maximum_total_exponent": max_a, "packets": packet_count,
            "words": word_count, "maximum_packet_size": max_k,
            "probability_reconstructions": interpolation_count,
            "lower_jet_ambiguities": ambiguity_count, "example_m2_A4": example}


def main():
    report = {"status": "pass", "arithmetic": "exact standard-library Fraction",
              "analytic_scope": "Hurwitz H1-H13 proof reviewed in AUDIT.md; no numerical zeta computation",
              "forward": check_forward(), "information_loss": check_information_loss(),
              "odd_return": check_odd_return(),
              "limits": ["finite enumeration is not a universal Collatz convergence proof",
                         "K-1 jet sharpness concerns all weights on known distinct nodes",
                         "positive return additionally requires D > 0"]}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
