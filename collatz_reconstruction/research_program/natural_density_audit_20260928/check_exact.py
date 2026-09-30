"""Small, exact checks of formulas in audit.tex; no asymptotic certification.

No network, subprocesses, numerical libraries or Lean workers. JSON output is
a generated receipt, never a replacement for the mathematical proofs.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from math import comb
from itertools import product
from pathlib import Path
import argparse
import json
import platform
import re

if not __debug__:
    raise RuntimeError("Run without -O: disabled assertions must not report a pass.")


def compositions(total, length):
    if length == 1:
        if total >= 1:
            yield (total,)
        return
    for first in range(1, total - length + 2):
        for rest in compositions(total - first, length - 1):
            yield (first,) + rest


def syr(n):
    value = 3 * n + 1
    valuation = (value & -value).bit_length() - 1
    return value >> valuation, valuation


def prefix(n, length):
    word = []
    for _ in range(length):
        n, a = syr(n)
        word.append(a)
    return tuple(word), n


def coefficients(word):
    a, b = 0, 0
    for part in word:
        b = 3 * b + (1 << a)
        a += part
    return a, b


def x_residue(word):
    modulus = 3 ** len(word)
    total, result = 0, 0
    for j, part in enumerate(word):
        total += part
        result += 3 ** j * pow(1 << total, -1, modulus)
    return result % modulus


def first_passage(n, x, m):
    for j in range(m + 1):
        if n <= x:
            return j
        n, _ = syr(n)
    return None


def check_cylinders():
    words = examples = inequalities = 0
    for r in range(1, 6):
        for total in range(r, 13):
            for word in compositions(total, r):
                words += 1
                a, b = coefficients(word)
                modulus = 1 << (a + 1)
                residue = (pow(3 ** r, -1, modulus) * ((1 << a) - b)) % modulus
                assert residue % 2 == 1
                for j in range(3):
                    n = residue + j * modulus
                    actual, terminal = prefix(n, r)
                    assert actual == word
                    assert terminal * (1 << a) == 3 ** r * n + b
                    assert (terminal * (1 << a) - b) // 3 ** r == n
                    assert terminal % 3 ** r == (b * pow(1 << a, -1, 3 ** r)) % 3 ** r
                    # Reversal is the exact coordinate map between F and X.
                    assert x_residue(word[::-1]) == (b * pow(1 << a, -1, 3 ** r)) % 3 ** r
                    examples += 1
                    for x in (1, 10, n // 2, n, terminal):
                        lower = Fraction(x)
                        for k in range(1, r):
                            ak, bk = coefficients(word[:k])
                            lower = max(lower, Fraction((1 << ak) * x - bk, 3 ** k))
                        upper = Fraction((1 << a) * x - b, 3 ** r)
                        assert (lower < n <= upper) == (first_passage(n, x, r) == r)
                        inequalities += 1
    # The small diagram in the note must describe actual labelled trajectories.
    for j in range(100):
        n = 11 + 16 * j
        assert syr(n) == (17 + 24 * j, 1)
        assert syr(17 + 24 * j) == (13 + 18 * j, 2)
    return {"words": words, "cylinder_examples": examples,
            "first_passage_interval_equivalences": inequalities,
            "ranges": "1<=r<=5, r<=sum<=12; three representatives per cylinder",
            "diagram_examples": 100}


def pair_key(word):
    pairs = tuple(word[i] + word[i + 1] for i in range(0, len(word) - 1, 2))
    return pairs, (word[-1] if len(word) % 2 else None)


def pair_histogram(n, pairs, tail):
    modulus = 3 ** n
    result = Counter({0: 1})
    running = 0
    for j, b in enumerate(pairs):
        running += b
        coefficient = 3 ** (2 * j) * pow(1 << running, -1, modulus) % modulus
        factor = Counter(coefficient * ((1 << r) + 3) % modulus for r in range(1, b))
        next_hist = Counter()
        for x, count_x in result.items():
            for y, count_y in factor.items():
                next_hist[(x + y) % modulus] += count_x * count_y
        result = next_hist
    if tail is not None:
        offset = 3 ** (n - 1) * pow(1 << (running + tail), -1, modulus) % modulus
        result = Counter({(x + offset) % modulus: c for x, c in result.items()})
    return result


def check_pair_factorization():
    groups_checked = tuples_checked = sum_cases = 0
    for n in range(1, 8):
        for s in range(n, min(14, 2 * n + 4) + 1):
            groups = defaultdict(Counter)
            total = 0
            for word in compositions(s, n):
                groups[pair_key(word)][x_residue(word)] += 1
                total += 1
            assert total == comb(s - 1, n - 1)
            for (pairs, tail), histogram in groups.items():
                predicted = pair_histogram(n, pairs, tail)
                assert histogram == predicted
                count = 1
                for b in pairs:
                    count *= b - 1
                assert sum(histogram.values()) == count
                groups_checked += 1
            sum_cases += 1
            tuples_checked += total
    return {"pair_fibres": groups_checked, "tuples": tuples_checked,
            "sum_cases": sum_cases,
            "ranges": "1<=n<=7, n<=s<=min(14,2n+4)",
            "arithmetic": "exact integer histograms modulo 3^n, including odd n"}


def check_residue_discrepancy():
    comparisons = pieces = 0
    moduli = (1, 3, 5, 9, 15, 27)
    for x in (10, 50, 200):
        for m in range(1, 5):
            groups = defaultdict(list)
            for n in range(x + 1, 12 * x + 1):
                if n % 2 and first_passage(n, x, m) == m:
                    groups[prefix(n, m)[0]].append(n)
            pieces += len(groups)
            for values in groups.values():
                word, _ = prefix(values[0], m)
                a, _ = coefficients(word)
                assert all(v - u == 1 << (a + 1) for u, v in zip(values, values[1:]))
            for lo, hi in ((x + 1, 12 * x), (2 * x, 3 * x), (5 * x, 5 * x + 7)):
                active = [[n for n in ns if lo <= n <= hi] for ns in groups.values()]
                active = [ns for ns in active if ns]
                all_values = [n for ns in active for n in ns]
                for q in moduli:
                    counts = Counter(n % q for n in all_values)
                    for z in range(q):
                        assert abs(q * counts[z] - len(all_values)) <= q * len(active)
                        comparisons += 1
    return {"comparisons": comparisons, "nonempty_prefix_parts": pieces,
            "thresholds": [10, 50, 200], "lengths": [1, 2, 3, 4],
            "odd_moduli": list(moduli), "arithmetic": "integer discrepancy after multiplication by q"}


def check_binomial_identity():
    checked = 0
    for n in range(1, 13):
        for s in range(n, 41):
            lhs = sum(Fraction(comb(s - j - 1, n - 1), 1 << s)
                      for j in range(s - n + 1))
            rhs = Fraction(s, n) * Fraction(comb(s - 1, n - 1), 1 << s)
            assert lhs == rhs
            assert Fraction(comb(s - 1, n - 1), 3 ** n) == (
                Fraction(1 << s, 3 ** n) * Fraction(comb(s - 1, n - 1), 1 << s))
            checked += 1
    return {"cases": checked, "ranges": "1<=n<=12, n<=s<=40", "arithmetic": "Fraction"}


def count_compositions(total, length):
    if length == 0:
        return int(total == 0)
    return comb(total - 1, length - 1) if total >= length else 0


def joint_histogram(n, total):
    return Counter(x_residue(word) for word in compositions(total, n))


def check_joint_maps():
    """Compare exact histograms before taking any Fourier transform.

    Each length-n word of total s has mass 2^-s. The independent block
    product has exactly the same mass, 2^-u * 2^-(s-u), term by term.
    No assertion about asymptotic rates follows from these finite cases.
    """
    projections = splits = words_checked = 0
    for n in range(1, 7):
        modulus = 3 ** n
        for total in range(n, min(12, 2 * n + 3) + 1):
            words = list(compositions(total, n))
            words_checked += len(words)
            for nu in range(1, n + 1):
                direct = Counter(x_residue(word) % 3 ** nu for word in words)
                projected = Counter()
                for sigma in range(nu, total + 1):
                    multiplicity = count_compositions(total - sigma, n - nu)
                    for residue, count in joint_histogram(nu, sigma).items():
                        projected[residue] += count * multiplicity
                assert +direct == +projected
                projections += 1
            for length in range(1, n):
                for prefix_total in range(length, total - (n - length) + 1):
                    # A prefix-measurable restriction as in the stopping split;
                    # not an assertion that these small words meet its large-n event.
                    direct = Counter(x_residue(word) for word in words
                                     if sum(word[:length]) == prefix_total
                                     and word[0] % 2 == 1)
                    predicted = Counter()
                    for prefix_word in compositions(prefix_total, length):
                        if prefix_word[0] % 2 == 0:
                            continue
                        # Evaluate the prefix in G_n, not G_length.
                        running = bottom = 0
                        for j, part in enumerate(prefix_word):
                            running += part
                            bottom += 3 ** j * pow(1 << running, -1, modulus)
                        multiplier = 3 ** length * pow(1 << prefix_total, -1, modulus)
                        for tail, count in joint_histogram(n - length, total - prefix_total).items():
                            predicted[(bottom + multiplier * tail) % modulus] += count
                    assert direct == predicted
                    assert Fraction(1, 1 << prefix_total) * Fraction(1, 1 << (total - prefix_total)) == Fraction(1, 1 << total)
                    splits += 1
    isometries = compositions_checked = 0
    for n in range(1, 6):
        for m in range(1, n + 1):
            signed = [Fraction((r % 5) - 2, r + 1) for r in range(3 ** m)]
            lifted = [signed[y % 3 ** m] / 3 ** (n - m) for y in range(3 ** n)]
            assert sum(map(abs, lifted)) == sum(map(abs, signed))
            recovered = [sum(lifted[z::3 ** m]) for z in range(3 ** m)]
            assert recovered == signed
            isometries += 1
            for k in range(1, m + 1):
                projected = [sum(signed[z::3 ** k]) for z in range(3 ** k)]
                via_mid = [projected[y % 3 ** k] / 3 ** (m - k) for y in range(3 ** m)]
                via_mid = [via_mid[y % 3 ** m] / 3 ** (n - m) for y in range(3 ** n)]
                direct = [projected[y % 3 ** k] / 3 ** (n - k) for y in range(3 ** n)]
                assert via_mid == direct
                compositions_checked += 1
    return {"words": words_checked, "joint_projection_histograms": projections,
            "restricted_prefix_split_histograms": splits,
            "signed_lift_isometries_and_left_inverses": isometries,
            "lift_compositions": compositions_checked,
            "ranges": "1<=n<=6, n<=total<=min(12,2n+3); lifts 1<=k<=m<=n<=5",
            "arithmetic": "exact integer histograms and Fraction, including zero-length tail sums"}


def check_local_state(folder, root, local_state=False):
    claims = json.loads((folder / "CLAIMS.json").read_text(encoding="utf-8"))
    tex = (folder / "audit.tex").read_text(encoding="utf-8")
    labels = re.findall(r"\\label\{([^}]+)\}", tex)
    assert len(labels) == len(set(labels))
    assert set(re.findall(r"\\(?:ref|eqref)\{([^}]+)\}", tex)) <= set(labels)
    assert all(c["tex_label"] in labels for c in claims["claims"])
    bibliography = set(re.findall(r"\\bibitem\{([^}]+)\}", tex))
    cited = set()
    for group in re.findall(r"\\cite(?:\[[^]]*\])?\{([^}]+)\}", tex):
        cited.update(group.split(","))
    assert cited <= bibliography
    result = {"audit_labels": len(labels), "claim_locators": len(claims["claims"]),
              "bibliography_keys": len(bibliography),
              "written_endpoint_reconstruction": claims["natural_density_written_reconstruction_complete"],
              "formal_certificate": claims["formal_verification_complete"]}
    assert claims["natural_density_written_reconstruction_complete"] is True
    assert claims["formal_verification_complete"] is False
    assert {"ND-023", "ND-024", "ND-025", "ND-026", "ND-027"} <= {c["id"] for c in claims["claims"]}
    assert {"prop:untimed-ladder", "lem:timed-step", "prop:timed-block", "lem:power-cover", "cor:timed-count", "cor:universal-clock"} <= set(labels)
    if not local_state:
        result["private_workbench_checks"] = "not requested; use --local-state inside the original corpus"
        return result
    preprint = root / "preprints/tao_clock_audit"
    manifest = json.loads((preprint / "MANIFEST.json").read_text(encoding="utf-8"))
    for entry in manifest["files"]:
        data = (preprint / entry["path"]).read_bytes()
        assert len(data) == entry["bytes"], entry["path"]
        assert sha256(data).hexdigest() == entry["sha256"], entry["path"]
    records = [json.loads(line) for line in (root / "state/source_registry.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    source = [r for r in records if r.get("source_id") == "SRC-COL-000053"]
    assert len(source) == 1
    local_source = [s for s in claims["sources"] if s.get("canonical_source_id") == "SRC-COL-000053"]
    assert len(local_source) == 1
    assert source[0]["manifestations"][0]["sha256"] == local_source[0]["sha256"]
    execution = json.loads((root / "state/polyclank_execution_20260928.json").read_text(encoding="utf-8"))
    assert claims["publication_authorized"] is (not execution["no_public_mutations"])
    assert claims["formal_verification_complete"] is False
    return {"audit_labels": len(labels), "claim_locators": len(claims["claims"]),
            "bibliography_keys": len(bibliography), "preprint_manifest_files": len(manifest["files"]),
            "new_canonical_source_records": len(source),
            "older_preprint_finite_suite": "not rerun; this check verifies its source manifest only"}


def check_endpoint_intervals():
    intervals_checked = adjacency_checks = probes_checked = localization_checks = 0
    for cap in range(1, 10):
        qmax = 3 ** cap
        for terminal in (4 * qmax * qmax + 1, 5 * qmax * qmax + 7):
            intervals = []
            for length in range(1, cap + 1):
                for total in range(-3, 2 * cap + 6):
                    scale = Fraction(2 ** total, 3 ** length) if total >= 0 else Fraction(1, (1 << (-total)) * 3 ** length)
                    intervals.append(((terminal - 3 ** length) * scale,
                                      terminal * scale, length, total))
            intervals.sort()
            for left, right in zip(intervals, intervals[1:]):
                assert left[1] < right[0]
                adjacency_checks += 1
            for lower, upper, _, _ in intervals:
                for endpoint in (lower, upper, (lower + upper) / 2):
                    assert sum(lo <= endpoint <= hi for lo, hi, _, _ in intervals) == 1
                    probes_checked += 1
            intervals_checked += len(intervals)
    words = 0
    for length in range(1, 5):
        modulus = 3 ** length
        for total in range(length, 11):
            for word in compositions(total, length):
                words += 1
                a, b = coefficients(word)
                residue = (b * pow(1 << a, -1, modulus)) % modulus
                terminal = residue + ((4 * 9 ** length + 1 - residue + modulus - 1) // modulus) * modulus
                if terminal % 2 == 0:
                    terminal += modulus
                actual = Fraction((1 << a) * terminal - b, modulus)
                zero_offset = Fraction((1 << a) * terminal, modulus)
                assert actual.denominator == 1 and actual.numerator % 2 == 1
                assert prefix(int(actual), length) == (word, terminal)
                candidates = sorted({actual - 1, actual, actual + 1,
                                     zero_offset - 1, zero_offset, zero_offset + 1})
                for low in candidates:
                    for high in candidates:
                        if low > high:
                            continue
                        discrepancy = (low <= actual <= high) != (low < zero_offset <= high)
                        if discrepancy:
                            assert any(Fraction(modulus, 1 << a) * v <= terminal <=
                                       Fraction(modulus, 1 << a) * v + modulus
                                       for v in (low, high))
                        localization_checks += 1
    return {"separated_intervals": intervals_checked, "strict_adjacent_separations": adjacency_checks,
            "closed_endpoint_and_midpoint_probes": probes_checked,
            "actual_valuation_words": words, "window_localizations": localization_checks,
            "arithmetic": "Fraction and integer arithmetic, including negative total-index tests for the abstract interval lemma",
            "ranges": "1<=R<=9, two M>4*9^R each; actual words 1<=r<=4, r<=sum<=10"}


def check_abel_and_envelope_coordinates():
    abel_cases = change_of_variable_cases = cutoff_cases = 0
    for n in range(1, 7):
        sequences = ([Fraction((j * j + 2 * j) % 7 - 3, 7) for j in range(n)],
                     [Fraction((-1) ** j, j + 1) for j in range(n)])
        for weights in product((-1, 0, 1), repeat=n):
            variation = abs(weights[0]) + abs(weights[-1])
            variation += sum(abs(weights[j + 1] - weights[j]) for j in range(n - 1))
            for values in sequences:
                prefixes = []
                total = Fraction(0)
                for value in values:
                    total += value
                    prefixes.append(total)
                direct = sum(w * a for w, a in zip(weights, values))
                abel = weights[-1] * prefixes[-1]
                abel += sum((weights[j] - weights[j + 1]) * prefixes[j] for j in range(n - 1))
                assert direct == abel
                assert abs(direct) <= variation * max(abs(s) for s in prefixes)
                abel_cases += 1
    for z in (Fraction(1, 3), Fraction(1), Fraction(7), Fraction(10000)):
        for p in range(1, 25):
            for q in range(1, 8):
                s = Fraction(p, q)
                v = s - z / s
                positive_sqrt = s + z / s
                assert positive_sqrt > 0 and positive_sqrt ** 2 == v ** 2 + 4 * z
                assert (v + positive_sqrt) / 2 == s
                assert (1 + v / positive_sqrt) / 2 == 1 / (1 + z / s ** 2)
                assert (s ** 2 - z) ** 2 / s ** 2 == v ** 2
                change_of_variable_cases += 1
    for r in range(1, 8):
        for low in range(0, 18):
            for high in range(low, 23):
                direct = sum(comb(s - 1, r - 1) for s in range(max(r, low + 1), high + 1))
                assert direct == (comb(high, r) if high >= r else 0) - (comb(low, r) if low >= r else 0)
                cutoff_cases += 1
    mu = Fraction(1077, 125)
    assert 1 / (2 * (mu + 1)) < Fraction(1, 18) < 1 / (2 * mu)
    return {"signed_Abel_identities_and_endpoint_bounds": abel_cases,
            "exact_change_of_variable_and_Jacobian_checks": change_of_variable_cases,
            "strict_lower_closed_upper_binomial_sums": cutoff_cases,
            "rate_comparison": "1/(2*(8.616+1)) < 1/18 < 1/(2*8.616), exact Fraction",
            "scope": "Finite identities only; does not certify Rhin, discrepancy or asymptotic estimates."}


def check_actual_input_and_measure_mass():
    residues = low_words = tail_cases = measure_cases = 0
    for n in range(1, 6):
        q = 3 * n
        histogram = Counter()
        tail = 0
        for value in range(1, 1 << q, 2):
            word, _ = prefix(value, n)
            if sum(word) < q:
                histogram[word] += 1
            else:
                tail += 1
            residues += 1
        for word, count in histogram.items():
            assert count == 1 << (q - 1 - sum(word))
            low_words += 1
        assert len(histogram) == comb(q - 1, n)
        geometric_tail_count = sum(comb(q - 1, k) for k in range(n))
        assert tail == geometric_tail_count
        assert sum(histogram.values()) + tail == 1 << (q - 1)
        tail_cases += 1
    for masses in product((0, 1, 2), repeat=4):
        mass = sum(masses)
        if mass == 0:
            continue
        p = [Fraction(x, 3) for x in masses]
        total = sum(p)
        pushed = [p[0] + p[2], p[1] + p[3]]
        probability = [x / total for x in pushed]
        assert sum(probability) == 1
        assert sum(abs(x - y) for x, y in zip(probability, pushed)) == abs(total - 1)
        for other in product((0, 1), repeat=4):
            v = [Fraction(x, 3) for x in other]
            pv = [v[0] + v[2], v[1] + v[3]]
            assert sum(abs(x - y) for x, y in zip(pushed, pv)) <= sum(abs(x - y) for x, y in zip(p, v))
            measure_cases += 1
    return {"odd_residues": residues, "exact_low_total_word_masses": low_words,
            "binomial_tail_equalities": tail_cases,
            "pushforward_and_positive_mass_identities": measure_cases,
            "scope": "Finite cylinder and measure identities only, not asymptotic first-passage certification."}



def check_scale_iteration_and_clocks():
    """Finite identities supporting the written iteration; no asymptotic test."""
    maps_checked = passage_checks = failure_checks = 0
    vertices = (1, 3, 5, 7)

    def graph_passage(mapping, start, threshold):
        seen = set()
        time = 0
        current = start
        while current > threshold:
            if current in seen:
                return None, 1
            seen.add(current)
            current = mapping[current]
            time += 1
        return time, current

    for images in product(vertices, repeat=len(vertices)):
        mapping = dict(zip(vertices, images))
        maps_checked += 1
        for start in vertices:
            for low in vertices:
                t_low, v_low = graph_passage(mapping, start, low)
                for subset_bits in range(16):
                    subset = {v for i, v in enumerate(vertices) if subset_bits & (1 << i)}
                    assert (int(v_low in subset) -
                            int(t_low is not None and v_low in subset)) == (
                                int(1 in subset) * int(t_low is None))
                    failure_checks += 1
                for high in vertices:
                    if high < low or t_low is None:
                        continue
                    t_high, middle = graph_passage(mapping, start, high)
                    remainder, endpoint = graph_passage(mapping, middle, low)
                    assert t_high is not None and remainder is not None
                    assert t_low == t_high + remainder and endpoint == v_low
                    passage_checks += 1

    cover_cases = endpoint_cases = 0
    for bottom in (Fraction(5, 2), Fraction(3), Fraction(7, 2)):
        for length in range(1, 4):
            boundaries = [bottom ** (2 ** j) for j in range(length + 1)]
            cutoff = boundaries[-1]
            target = bottom + Fraction(1, 7)
            assert bottom <= target < boundaries[1]
            odds = list(range(1, cutoff.numerator // cutoff.denominator + 1, 2))
            parts = []
            for lo, hi in zip(boundaries, boundaries[1:]):
                assert hi - lo > 2
                halfopen = {n for n in odds if lo < n <= hi}
                closed = {n for n in odds if lo <= n <= hi}
                assert len(halfopen) > 0
                assert len(closed - halfopen) <= 1
                assert len(closed) <= 2 * len(halfopen)
                parts.append((closed, halfopen))
                endpoint_cases += 1
            assert sum(len(h) for _, h in parts) == len(set().union(*(h for _, h in parts)))
            for modulus in (3, 5, 7):
                for residue in range(modulus):
                    bad = {n for n in odds if n > target and n % modulus == residue}
                    epsilon = max(Fraction(len(bad & closed), len(closed)) for closed, _ in parts)
                    assert len(bad) <= 2 * epsilon * len(odds)
                    cover_cases += 1

    geometric_cases = 0
    for ratio in (Fraction(1, 2), Fraction(9, 10), Fraction(999, 1000)):
        for length in range(1, 33):
            total = sum(ratio ** j for j in range(length))
            assert total == (1 - ratio ** length) / (1 - ratio)
            assert total <= 1 / (1 - ratio)
            geometric_cases += 1

    raw_clocks = telescope_cases = 0
    def raw_step(n):
        return 3 * n + 1 if n % 2 else n // 2
    for initial in range(1, 502, 2):
        value, total = initial, 0
        for k in range(13):
            assert (1 << total) * value <= (4 ** k) * initial
            assert (1 << total) <= (4 ** k) * initial
            telescope_cases += 1
            for a in range(5):
                original = (1 << a) * initial
                m = a + k + total
                final = original
                for _ in range(m):
                    final = raw_step(final)
                assert final == value
                assert (1 << m) <= (1 << (3 * k)) * original
                raw_clocks += 1
            value, valuation = syr(value)
            total += valuation
    partition_cases = 0
    for cutoff in range(2, 151):
        for target in (2, 5, 11):
            # An arbitrary odd failure set, not a claim about Collatz failure.
            bad_odds = {m for m in range(1, cutoff + 1, 2) if m > target and m % 7 == 3}
            actual = {n for n in range(1, cutoff + 1)
                      if (n >> ((n & -n).bit_length() - 1)) in bad_odds}
            by_valuation = []
            for a in range(cutoff.bit_length()):
                by_valuation += [(1 << a) * m for m in bad_odds if (1 << a) * m <= cutoff]
            assert len(by_valuation) == len(set(by_valuation))
            assert actual == set(by_valuation)
            partition_cases += 1
    return {
        "finite_functional_graphs": maps_checked,
        "nested_first_passage_identities": passage_checks,
        "failure_convention_indicator_identities": failure_checks,
        "exact_rational_cover_tests": cover_cases,
        "halfopen_closed_endpoint_tests": endpoint_cases,
        "finite_geometric_sum_identities": geometric_cases,
        "valuation_telescopes": telescope_cases,
        "actual_raw_clock_identities": raw_clocks,
        "odd_valuation_partition_identities": partition_cases,
        "scope": "Exact finite identities only. No check of the analytic mixing input or an infinite density theorem."
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--tao-source", type=Path, help="Optional original v7 TeX to verify against its pinned hash")
    parser.add_argument("--allikvere-source", type=Path, help="Optional original v2 TeX to verify against its pinned hash")
    parser.add_argument("--local-state", action="store_true", help="Also verify original private corpus registry and preprint manifest")
    args = parser.parse_args()
    folder = Path(__file__).resolve().parent
    root = folder.parents[1]
    source_files = {
        "ALLIKVERE-2026-V2": args.allikvere_source,
        "TAO-V7": args.tao_source,
    }
    pinned = {
        "ALLIKVERE-2026-V2": "23d9cb265a4fccd4e60827b584f92e7d192ac643fe577657f515a3d54f4ad28a",
        "TAO-V7": "bfbc39432d4084a276416cb019a592003c868fa32f18e2f90028ac325ae5c19d",
    }
    input_hashes = {name: sha256(path.read_bytes()).hexdigest() for name, path in source_files.items() if path is not None}
    assert all(digest == pinned[name] for name, digest in input_hashes.items())
    report = {
        "schema_version": 1,
        "status": "passed",
        "python": platform.python_version(),
        "source_hashes": input_hashes,
        "source_hash_check_not_requested": [name for name, path in source_files.items() if path is None],
        "checks": {
            "valuation_cylinders_and_first_passage": check_cylinders(),
            "conditional_pair_factorization": check_pair_factorization(),
            "first_passage_CRT_discrepancy": check_residue_discrepancy(),
            "hockey_stick_and_fibre_weight": check_binomial_identity(),
            "joint_offset_total_maps": check_joint_maps(),
            "separated_endpoint_intervals": check_endpoint_intervals(),
            "Abel_envelope_and_cutoffs": check_abel_and_envelope_coordinates(),
            "actual_input_and_measure_mass": check_actual_input_and_measure_mass(),
            "scale_iteration_and_clocks": check_scale_iteration_and_clocks(),
            "local_state_and_source_manifest": check_local_state(folder, root, args.local_state),
        },
        "artifact_hashes": {
            name: sha256((folder / name).read_bytes()).hexdigest()
            for name in ("check_exact.py", "audit.tex", "CLAIMS.json")
        },
        "scope": "Finite exact formula checks; not a proof of asymptotic mixing or natural-density almost-boundedness.",
        "lean_started": False,
        "remote_writes": False,
    }
    result = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(result, encoding="utf-8")
    print(result)


if __name__ == "__main__":
    main()
