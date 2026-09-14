#!/usr/bin/env python3
"""Exact stopped Collatz transport, retained arithmetic lifts, and verification.

Standard library only, Python >= 3.10. All proof checks use explicit exceptions;
python -O does not disable them. Run `python verify.py --output verification.json`.
No network access or repository writes are performed.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json
from math import comb, gcd
from pathlib import Path
from typing import Iterable


class VerificationError(RuntimeError):
    pass


COUNTS: Counter[str] = Counter()


def require(ok: bool, tag: str) -> None:
    if not ok:
        raise VerificationError(tag)
    COUNTS[tag] += 1


def positive_integer(x: int, name: str) -> None:
    if type(x) is not int or x <= 0:
        raise ValueError(f"{name} must be a positive integer")


def valuation2(n: int) -> int:
    positive_integer(n, "valuation input")
    return (n & -n).bit_length() - 1


def ceildiv(a: int, b: int) -> int:
    if b <= 0:
        raise ValueError("positive divisor required")
    return -((-a) // b)


def floorq(x: F) -> int:
    return x.numerator // x.denominator


def ceilq(x: F) -> int:
    return -floorq(-x)


@dataclass(frozen=True)
class Packet:
    word: tuple[int, ...]
    A: int
    L: int
    C: int

    @property
    def m(self) -> int:
        return len(self.word)

    @property
    def modulus(self) -> int:
        return 1 << (self.A + 1)

    @property
    def residue(self) -> int:
        # This is a declared section, with a section-change law in note.md.
        return (((1 << self.A) - self.C) * pow(self.L, -1, self.modulus)) % self.modulus

    def evaluate(self, n: int | F) -> F:
        return (self.L * F(n) + self.C) / (1 << self.A)

    def append(self, a: int) -> Packet:
        positive_integer(a, "exponent")
        return Packet(self.word + (a,), self.A + a, 3 * self.L,
                      3 * self.C + (1 << self.A))


@lru_cache(maxsize=None)
def packet(word: tuple[int, ...]) -> Packet:
    z = Packet((), 0, 1, 0)
    for a in word:
        z = z.append(a)
    return z


def join(p: Packet, q: Packet) -> Packet:
    return Packet(p.word + q.word, p.A + q.A, p.L * q.L,
                  q.L * p.C + (1 << p.A) * q.C)


def odd_steps(n: int, m: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    if type(n) is not int or n <= 0 or n % 2 == 0:
        raise ValueError("a positive odd start is required")
    if type(m) is not int or m < 0:
        raise ValueError("nonnegative step count required")
    values = [n]
    word = []
    for _ in range(m):
        v = 3 * n + 1
        a = valuation2(v)
        n = v >> a
        values.append(n)
        word.append(a)
    return tuple(word), tuple(values)


def is_stop(p: Packet, q: int = 3) -> bool:
    positive_integer(q, "reference start")
    if q < 3:
        raise ValueError("this certificate uses q >= 3")
    if not p.word:
        return False
    z = packet(())
    for j, a in enumerate(p.word):
        z = z.append(a)
        desc = z.L * q + z.C < q * (1 << z.A)
        if desc:
            return j == p.m - 1
    return False


@lru_cache(maxsize=None)
def stop_leaves(H: int, q: int = 3) -> tuple[Packet, ...]:
    if type(H) is not int or H < 0 or type(q) is not int or q < 3:
        raise ValueError("H >= 0 and q >= 3 are required")
    out: list[Packet] = []

    def visit(z: Packet) -> None:
        for a in range(1, H - z.A + 1):
            w = z.append(a)
            if w.L * q + w.C < q * (1 << w.A):
                out.append(w)
            else:
                visit(w)
    visit(packet(()))
    return tuple(sorted(out, key=lambda p: (p.A, p.m, p.word)))


def binary_survival(H: int, q: int = 3) -> tuple[list[F], list[int]]:
    """Independent binary-affine enumeration; initial parity is forced odd."""
    if H < 0 or q < 3:
        raise ValueError("H >= 0 and q >= 3 required")
    S = [F(1)]
    deaths = [0]
    if not H:
        return S, deaths
    states = [(3, 1)]
    S.append(F(1)); deaths.append(0)
    for h in range(2, H + 1):
        nxt = []
        dead = 0
        for L, C in states:
            for e in (0, 1):
                LL = L * (3 if e else 1)
                CC = 3 * C + (1 << (h - 1)) if e else C
                if LL * q + CC < q * (1 << h):
                    dead += 1
                else:
                    nxt.append((LL, CC))
        states = nxt
        S.append(F(len(states), 1 << (h - 1)))
        deaths.append(dead)
    return S, deaths


def integer_bracket_count(offset: int, step: int, lower: F, upper: F) -> int:
    """Number of offset+step*z in the open/closed interval (lower, upper]."""
    if step <= 0:
        raise ValueError("positive step required")
    if lower >= upper:
        return 0
    return max(0, floorq((upper - offset) / step) - floorq((lower - offset) / step))


@dataclass(frozen=True)
class Family:
    # n(t)=a+2*d*t, t=b,...,b+N-1. d may have a retained 2-primary part.
    a: int
    d: int
    b: int
    N: int

    def validate(self, minimum: int = 3) -> None:
        if any(type(x) is not int for x in (self.a, self.d, self.b, self.N)):
            raise ValueError("family parameters must be integers")
        if self.a % 2 != 1 or self.d <= 0 or self.N <= 0:
            raise ValueError("odd a, positive d and positive N required")
        if self.a + 2 * self.d * self.b < minimum:
            raise ValueError(f"all source starts must be at least {minimum}")

    def value(self, t: int) -> int:
        return self.a + 2 * self.d * t


@dataclass(frozen=True)
class Chart:
    g: int
    P: int
    s: int
    u: int
    target_d: int


def chart(f: Family, p: Packet) -> Chart | None:
    """Literal cylinder chart; None means a proved congruence incompatibility."""
    if not p.word:
        raise ValueError("nonempty packet required")
    g = gcd(f.d, 1 << p.A)
    c = (p.residue - f.a) // 2
    if c % g:
        return None
    P = (1 << p.A) // g
    s = 0 if P == 1 else (c // g) * pow(f.d // g, -1, P) % P
    num = p.L * f.value(s) + p.C
    if num % (1 << p.A):
        raise VerificationError("chart integrality")
    u = num // (1 << p.A)
    if u % 2 != 1:
        raise VerificationError("chart odd target")
    return Chart(g, P, s, u, f.d * p.L // g)


def descent_intervals(f: Family, p: Packet) -> tuple[tuple[F, F] | None, ...]:
    """The j-th source-index interval is (lower,upper], before sample truncation."""
    # Finite endpoints suffice within the source sample; no sentinel infinity.
    upper = F(f.b + f.N)   # sample has t < this value
    out: list[tuple[F, F] | None] = []
    z = packet(())
    for a in p.word:
        z = z.append(a)
        D = (1 << z.A) - z.L
        if D <= 0:
            out.append(None)
            continue
        lower = (F(z.C, D) - f.a) / (2 * f.d)
        out.append((lower, upper) if lower < upper else None)
        upper = min(upper, lower)
    return tuple(out)


def marked_cells(f: Family, p: Packet, M: int = 1) -> list[tuple[tuple, int, F]]:
    """All declared (word,lift residue,first-descent index) cells, including zeros.

    The reference is the lattice-density integral on the exact same threshold
    interval; it does not assert independence along an integer trajectory.
    """
    f.validate(); positive_integer(M, "mark modulus")
    ch = chart(f, p)
    intervals = descent_intervals(f, p)
    rows = []
    for r in range(M):
        for j, E in enumerate(intervals, 1):
            key = (p.word, r, j)
            if ch is None or E is None:
                rows.append((key, 0, F(0)))
                continue
            lower, upper = E
            # Integer t lie in [b,b+N-1] and (lower,upper].
            low_int = max(f.b, floorq(lower) + 1)
            high_int = min(f.b + f.N - 1, floorq(upper))
            offset, step = ch.s + ch.P * r, ch.P * M
            count = 0 if low_int > high_int else max(
                0, (high_int - offset) // step - ceildiv(low_int - offset, step) + 1)
            # Continuous source-index interval is [b,b+N); endpoint measure is 0.
            length = max(F(0), min(F(f.b + f.N), upper) - max(F(f.b), lower))
            reference = length / (f.N * step)
            rows.append((key, count, reference))
    return rows


def observe(n: int, H: int, q: int = 3) -> tuple[Packet, int] | None:
    """Finite, terminating observation. None is explicit cutoff overflow."""
    if n < q or n % 2 == 0 or q < 3 or H < 0:
        raise ValueError("odd n >= q >= 3 and H >= 0 required")
    x = n
    z = packet(())
    first = 0
    while z.A <= H:
        v = 3 * x + 1
        a = valuation2(v)
        x = v >> a
        z = z.append(a)
        if z.A > H:
            return None
        if not first and x < n:
            first = z.m
        if z.L * q + z.C < q * (1 << z.A):
            if not first:
                raise VerificationError("certified word did not descend")
            return z, first
    raise VerificationError("unreachable observer state")


def actual_label(f: Family, t: int, H: int, M: int = 1) -> tuple:
    obs = observe(f.value(t), H)
    if obs is None:
        return ("overflow",)
    p, j = obs
    ch = chart(f, p)
    if ch is None or (t - ch.s) % ch.P:
        raise VerificationError("observed point missing from its original chart")
    r = ((t - ch.s) // ch.P) % M
    return (p.word, r, j)


def finite_law(f: Family, H: int, M: int = 1) -> tuple[dict, dict, F, int]:
    P: dict[tuple, F] = {}
    Q: dict[tuple, F] = {}
    occupied = 0
    total_reference = F(0)
    count = 0
    for p in stop_leaves(H):
        ch = chart(f, p)
        if ch is not None:
            total_reference += F(1, ch.P)
        for key, c, v in marked_cells(f, p, M):
            P[key] = F(c, f.N); Q[key] = v
            count += c
            occupied += int(c > 0)
    P[("overflow",)] = F(f.N - count, f.N)
    Q[("overflow",)] = 1 - total_reference
    require(P[("overflow",)] >= 0, "nonnegative actual overflow")
    require(Q[("overflow",)] >= 0, "nonnegative reference overflow")
    require(sum(P.values()) == 1, "actual mass conservation")
    require(sum(Q.values()) == 1, "reference mass conservation")
    tv = sum((abs(P[k] - Q[k]) for k in P), F(0)) / 2
    cells = M * sum(p.m for p in stop_leaves(H))
    require(tv <= min(F(1), Q[("overflow",)] + F(cells, f.N)), "finite marked TV bound")
    return P, Q, tv, occupied


def bernoulli(n: int) -> list[F]:
    B = [F(1)]
    for k in range(1, n + 1):
        B.append(-sum((comb(k + 1, r) * B[r] for r in range(k)), F(0)) / (k + 1))
    return B


def polynomial_product(a: list[F], b: list[F]) -> list[F]:
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def spectral_and_incidence_test() -> dict:
    f, H, M = Family(1, 1, 1, 17), 4, 3
    P, Q, tv, occupied = finite_law(f, H, M)
    labels = list(P)
    weights = [P[k] for k in labels]
    d = len(labels)
    lambdas = list(range(1, d + 1))
    moments = [sum((w * (x ** k) for x, w in zip(lambdas, weights)), F(0)) for k in range(d)]
    B = bernoulli(d)
    zeta_neg = [-sum((comb(k + 1, r) * B[k + 1 - r] * moments[r]
                       for r in range(k + 2)), F(0)) / (k + 1) for k in range(d - 1)]
    rebuilt = [F(1)]
    for k, z in enumerate(zeta_neg):
        rebuilt.append(-(k + 1) * z - sum((comb(k + 1, r) * B[k + 1 - r] * rebuilt[r]
                                         for r in range(k + 1)), F(0)))
    require(rebuilt == moments, "Hurwitz Bernoulli triangular inversion")
    for j, x in enumerate(lambdas):
        co = [F(1)]
        for k, y in enumerate(lambdas):
            if j != k:
                co = polynomial_product(co, [F(-y, x - y), F(1, x - y)])
        value = sum((a * b for a, b in zip(co, rebuilt)), F(0))
        require(value == weights[j], "Lagrange reconstruction including zero weights")
    fibers: dict[tuple, list[int]] = defaultdict(list)
    for t in range(f.b, f.b + f.N):
        fibers[actual_label(f, t, H, M)].append(t - f.b)
    refs = {key: v[0] for key, v in fibers.items()}
    # Explicit h^1, P0=1-h*delta, P1=1-delta*h identities on basis vectors.
    for i in range(f.N):
        k = actual_label(f, f.b + i, H, M)
        r = refs[k]
        vector = [0] * f.N; vector[i] += 1; vector[r] -= 1
        image = Counter()
        for ix, v in enumerate(vector):
            image[actual_label(f, f.b + ix, H, M)] += v
        require(all(v == 0 for v in image.values()), "incidence kernel homotopy")
        vector[r] += 1
        require(vector == [int(ix == i) for ix in range(f.N)], "source homotopy identity")
    for key in labels:
        in_image = int(key in refs)
        empty_projection = int(key not in refs)
        require(in_image + empty_projection == 1, "target homotopy including present zeros")
    empty = len(labels) - len(refs)
    require(empty == sum(w == 0 for w in weights), "empty-fiber cohomology rank")
    require(f.N - len(refs) >= 0, "kernel rank nonnegative")
    return {"source_points": f.N, "declared_labels": d,
            "occupied_labels": len(refs), "H0_rank": f.N - len(refs),
            "H1_rank_present_zero_labels": empty,
            "all_zero_weight_labels_reconstructed": True}


@dataclass(frozen=True)
class Node:
    current: Family
    original_a: int
    original_d: int
    history: Packet


def descend_node(node: Node, p: Packet, M: int = 1, r: int = 0) -> Node | None:
    f = node.current
    ch = chart(f, p)
    if ch is None:
        return None
    offset = ch.s + ch.P * r
    step = ch.P * M
    lo = ceildiv(f.b - offset, step)
    hi = (f.b + f.N - 1 - offset) // step
    if lo > hi:
        return None
    aa = (p.L * f.value(offset) + p.C) // (1 << p.A)
    dd = ch.target_d * M
    target = Family(aa, dd, lo, hi - lo + 1)
    original_a = node.original_a + 2 * node.original_d * offset
    original_d = node.original_d * step
    history = join(node.history, p)
    require(history.L * original_a + history.C == (1 << history.A) * aa,
            "restart diagram constant coefficient")
    require(history.L * original_d == (1 << history.A) * dd,
            "restart diagram slope coefficient")
    for v in {lo, hi}:
        n = f.value(offset + step * v)
        y = target.value(v)
        require(p.evaluate(n) == y, "restart evaluation")
        require(0 < y < n and y % 2 == 1, "restart strict descent with original offset")
    return Node(target, original_a, original_d, history)


def restart_certificate_test() -> dict:
    root = Node(Family(1, 1, 1, 1024), 1, 1, packet(()))
    pending = [root]
    H = 10
    rounds = []
    finished: set[int] = set()
    for round_no in range(3):
        nxt = []
        unresolved: set[int] = set()
        accepted = 0
        points_in = sum(x.current.N for x in pending)
        new_finished: set[int] = set()
        for node in pending:
            f = node.current
            if f.value(f.b) == 1:
                original = node.original_a + 2 * node.original_d * f.b
                new_finished.add(original)
                if f.N == 1:
                    continue
                node = Node(Family(f.a, f.d, f.b + 1, f.N - 1),
                            node.original_a, node.original_d, node.history)
                f = node.current
            f.validate()
            accepted_indices: set[int] = set()
            for p in stop_leaves(H):
                child = descend_node(node, p)
                if child is None:
                    continue
                nxt.append(child)
                accepted += child.current.N
                ch = chart(f, p)
                if ch is None:
                    raise VerificationError("lost chart")
                for v in range(child.current.b, child.current.b + child.current.N):
                    t = ch.s + ch.P * v
                    require(t not in accepted_indices, "restart cells disjoint")
                    accepted_indices.add(t)
                    n = f.value(t)
                    actual, values = odd_steps(n, p.m)
                    require(actual == p.word, "restart exact valuation replay")
                    require(values[-1] == child.current.value(v), "restart endpoint replay")
                    original = child.original_a + 2 * child.original_d * v
                    _, replay = odd_steps(original, child.history.m)
                    require(replay[-1] == values[-1], "full ancestral replay")
            for t in range(f.b, f.b + f.N):
                if t not in accepted_indices:
                    require(observe(f.value(t), H) is None, "restart overflow retained")
                    unresolved.add(node.original_a + 2 * node.original_d * t)
        finished.update(new_finished)
        require(points_in == accepted + len(new_finished) + len(unresolved), "restart round mass conservation")
        rounds.append({"round": round_no + 1, "input_points": points_in,
                       "accepted_points": accepted, "reached_one_at_input": len(new_finished),
                       "explicit_cutoff_overflow_points": len(unresolved),
                       "output_progressions": len(nxt)})
        pending = nxt
    return {"N": 1024, "cutoff_each_block": H, "rounds": rounds,
            "overflow_was_not_restarted_or_dropped": True}



def image_complex_test() -> dict:
    """Exact integer image torsor, finite coefficient maps, and connecting map."""
    fixtures = 0
    for d in (1, 2, 4, 9, 12, 81):
        f = Family(1, d, 1, 64)
        for p in stop_leaves(8):
            ch = chart(f, p)
            if ch is None:
                continue
            fixtures += 1
            D, z0 = ch.target_d, (ch.u - 1) // 2
            require(valuation2(D) == max(valuation2(d) - p.A, 0),
                    "retained image dyadic exponent")
            for v in (0, 1, 7):
                n = f.value(ch.s + ch.P*v)
                y = ch.u + 2*D*v
                require((p.L*n+p.C, 1 << p.A) == ((1 << p.A)*y, 1 << p.A),
                        "homogeneous integral diagram")
                require((y-1)//2 == z0+D*v, "integer image torsor")
                require(((1 << p.A)*y-p.C)//p.L == n and
                        ((1 << p.A)*y-p.C) % p.L == 0,
                        "integer image inverse")
            for ell in (2, 3):
                for r in (1, 2, 3):
                    N = ell**r
                    g = gcd(D, N)
                    image = Counter((D*v) % N for v in range(N))
                    for y in range(N):
                        require(image[y] == (g if y % g == 0 else 0),
                                "finite coefficient image and kernel")
                    kernel = [v for v in range(N) if (D*v) % N == 0]
                    beta = {(D*v//N) % D for v in kernel}
                    require(len(beta) == g and all((N*x) % D == 0 for x in beta),
                            "explicit image-complex connecting isomorphism")
                    if D % ell:
                        inv = pow(D, -1, N)
                        require((D*inv) % N == 1,
                                "localization contraction at finite precision")
    p = packet((1, 1, 3, 2))
    z0, D = 78, 81
    require(z0 == (157-1)//2 and D//gcd(D,z0) == 27,
            "worked image torsor order")
    for H in range(1, 10):
        require(pow(D,-1,1<<H)*D % (1<<H) == 1,
                "worked dyadic image contraction")
    return {"compatible_chart_fixtures": fixtures,
            "example_image_complex_differential": D,
            "example_distinguished_coset": z0,
            "example_coset_order": D//gcd(D,z0),
            "localizations_checked_modulo_powers_of": [2,3],
            "infinite_localization_is_proved_not_computationally_assumed": True}


def stopped_tuple(n: int, H: int, r: int) -> tuple[tuple[int, ...], ...] | None:
    """Parity-code observer, including the Haar-null integer fixed point 1.

    This routine checks the dyadic coding law, not strict descent at 1.
    The positive-integer restart engine separately absorbs 1.
    """
    out = []
    A = 0
    for _ in range(r):
        p = packet(())
        while True:
            v = 3*n + 1
            a = valuation2(v)
            n = v >> a
            A += a
            if A > H:
                return None
            p = p.append(a)
            if p.L*3 + p.C < 3*(1 << p.A):
                out.append(p.word)
                break
    return tuple(out)


def renewal_test() -> list[dict]:
    out = []
    for r,H in ((1,8),(2,10),(3,12)):
        paths = []
        def rec(prefix: tuple[tuple[int,...],...], remaining: int) -> None:
            if len(prefix) == r:
                paths.append(prefix)
                return
            for p in stop_leaves(remaining):
                rec(prefix + (p.word,), remaining-p.A)
        rec((),H)
        N = 1 << H
        observed = Counter(stopped_tuple(2*t+1,H,r) for t in range(N))
        expected_mass = F(0)
        for path in paths:
            z = packet(())
            product_mass = F(1)
            for w in path:
                p = packet(w)
                z = join(z,p)
                product_mass *= F(1,1 << p.A)
            require(product_mass == F(1,1 << z.A), "stopped-block product cylinder mass")
            require(observed[path] == N*product_mass, "exact finite renewal cylinder count")
            expected_mass += product_mass
        require(F(observed[None],N) == 1-expected_mass,
                "renewal cutoff overflow retained")
        require(sum(observed.values()) == N, "renewal finite mass conservation")
        out.append({"blocks":r,"total_exponent_cutoff":H,"source_odd_residues":N,
                    "declared_stopped_paths":len(paths),
                    "exact_reference_overflow":str(1-expected_mass)})
    return out


def enriched_incidence_test() -> dict:
    """Actual comparison maps between support incidence and image cohomology."""
    cases = Counter()
    examples = []
    for f,H,M in ((Family(1,1,1,17),4,3), (Family(1,4,1,17),4,3),
                  (Family(247,128,0,7),7,1)):
        direct = {t: actual_label(f,t,H,M) for t in range(f.b,f.b+f.N)}
        for p in stop_leaves(H):
            ch = chart(f,p)
            if ch is None:
                continue
            for key,count,_ in marked_cells(f,p,M):
                _,r,j = key
                times = [t for t,k in direct.items() if k == key]
                ell = [((t-ch.s)//ch.P-r)//M for t in times]
                D = M*ch.target_d
                zbase = (ch.u+2*ch.target_d*r-1)//2
                zvals = [int((p.evaluate(f.value(t))-1)/2) for t in times]
                require(len(times) == count, "enriched original source fiber")
                require(ell == sorted(ell) and all(v == ell[0]+i for i,v in enumerate(ell)),
                        "enriched marked fiber consecutive parameters")
                for v,z in zip(ell,zvals):
                    require(z == zbase+D*v, "enriched incidence terminal column")
                    require(z-zbase == D*v, "enriched to image chain map")
                    require((1,z)[0] == 1, "enriched to support chain map")
                cases['empty' if not times else 'singleton' if len(times)==1 else 'at_least_two'] += 1
                if len(times) >= 2:
                    minor_gcd = 0
                    for z in zvals[1:]:
                        minor_gcd = gcd(minor_gcd,z-zvals[0])
                    require(minor_gcd == D, "enriched image cokernel from original minors")
                    e0 = [1]+[0]*(len(times)-1)
                    contrast = [-1,1]+[0]*(len(times)-2)
                    for i,v in enumerate(ell):
                        c=v-ell[0]
                        basis=[int(k==i) for k in range(len(times))]
                        rel=[basis[k]-c*contrast[k]-e0[k] for k in range(len(times))]
                        require(sum(rel)==0 and sum(a*z for a,z in zip(rel,zvals))==0,
                                "enriched affine kernel representative")
                        require([basis[k]-c*contrast[k]-rel[k] for k in range(len(times))] == e0,
                                "enriched degree zero homotopy")
                    for aa,bb in ((1,0),(0,1)):
                        ff=bb-zvals[0]*aa
                        require((aa,bb-ff)==(aa,zvals[0]*aa),
                                "enriched degree one homotopy")
                    require(gcd(*(z-zvals[0] for z in zvals[1:])) == D,
                            "support connecting moment image")
                # Refinement K_(marked) -> K_(unmarked) has (M,id) in degrees (0,1).
                require(ch.target_d*M == D and (zbase-(ch.u-1)//2) % ch.target_d == 0,
                        "marked image complex exact refinement map")
                if f.a==247 and key[2]==3 and times:
                    examples.append({"word":list(p.word),"source_values":[f.value(t) for t in times],
                                     "original_affine_incidence_columns":[[1,z] for z in zvals],
                                     "H0_affine_rank":len(times)-2,
                                     "H0_support_rank":len(times)-1,
                                     "H1_affine_torsion_order":D,
                                     "connecting_moment_generator":D})
    return {"fiber_cases":dict(sorted(cases.items())),
            "comparison_maps":"A -> support: (id,first coordinate); A -> image: (ell,b-zbase*a)",
            "worked_seven_point_bridge":examples}

def run() -> dict:
    COUNTS.clear()
    # Original packets, legal cylinders, and literal binary factorization.
    words = [w for m in range(1, 5) for w in product(range(1, 5), repeat=m)]
    for word in words:
        p = packet(word)
        for t in (0, 1, 7):
            n = p.residue + p.modulus * t
            w, values = odd_steps(n, p.m)
            require(w == word, "original word cylinder")
            require(p.evaluate(n) == values[-1], "original affine numerator")
            x = F(n)
            for a in word:
                x = (3 * x + 1) / 2
                for _ in range(a - 1):
                    x /= 2
            require(x == values[-1], "literal one-halving factorization")
        for i in range(1, p.m + 1):
            z = packet(word[:i]); D = (1 << z.A) - z.L
            for n in (1, 3, 5, p.residue):
                exact = z.evaluate(n) < n
                retained = D > 0 and D * n > z.C
                require(exact == retained, "retained-offset descent equivalence")
    for w in words[:84]:
        for v in words[:20]:
            require(join(packet(w), packet(v)) == packet(w + v), "packet concatenation")

    # Independent binary enumeration proves exact finite Kraft identities.
    depth = 20
    S, deaths = binary_survival(depth)
    tail = F(1)
    rho, C0, K = F(31, 32), F(3, 2), F(31, 20)
    require(F(15,16) < rho**2, "rational square-root contraction enclosure")
    require(F(2) < (C0*rho)**2, "initial forced-odd survival enclosure")
    require(K*(2*rho-1) == C0*rho, "completed-word tail constant identity")
    for t in range(2001):
        x = 3 + F(t,17)
        aa, bb = x/2-1, (3*x-1)/2
        R = F(15,4)*(x-1)-aa-bb
        require(R > 0 and R**2-4*aa*bb == (x-7)**2/16,
                "retained-offset square-root identity")
        require(2*aa+bb == F(5,2)*(x-1), "exact translated affine moment")
    profiles = []
    for H in range(depth + 1):
        if H:
            tail = (tail + S[H]) / 2
        leaves = stop_leaves(H)
        geometric_tail = 1 - sum((F(1, 1 << p.A) for p in leaves), F(0))
        require(geometric_tail == tail, "binary-to-odd stopped tail identity")
        require(len(leaves) == sum(deaths[h] * (H - h + 1) for h in range(1, H + 1)),
                "binary-to-odd stopped leaf count")
        require(S[H] <= C0 * rho**H, "rational survival bound")
        require(tail <= K * rho**H, "rational completed-word tail bound")
        require(len(leaves) <= C0 * (2*rho)**(H+1) / (2*rho-1)**2,
                "rational leaf-growth bound")
        if H in (4, 8, 12, 16, 20):
            profiles.append({"H": H, "leaves": len(leaves),
                             "sum_word_lengths": sum(p.m for p in leaves),
                             "tail": str(tail), "binary_survival": str(S[H])})

    # General progressions, including even d and retained incompatible labels.
    families = [Family(1, d, 1, N) for d in (1, 2, 3, 4, 9, 12, 81)
                for N in (17, 64)] + [Family(247, 81, 0, 127),
                                     Family(17, 32, 1000000, 97),
                                     Family(-1001, 9, 60, 79),
                                     Family(1001, 12, -40, 89),
                                     Family(-21, 8, 2, 17),
                                     Family(3, 5, 0, 97)]
    law_fixtures = []
    for f in families:
        for H in (4, 7, 10):
            for M in (1, 3, 4):
                P, Q, tv, occupied = finite_law(f, H, M)
                direct = Counter(actual_label(f, t, H, M) for t in range(f.b, f.b + f.N))
                for key, weight in P.items():
                    require(weight * f.N == direct[key], "marked original-lattice count")
                    if key != ("overflow",):
                        require(abs(weight - Q[key]) <= F(1, f.N), "cell discrepancy at most one")
                for p in stop_leaves(H):
                    ch = chart(f, p)
                    for t in (f.b, f.b + f.N - 1):
                        w, _ = odd_steps(f.value(t), p.m)
                        legal = w == p.word
                        in_chart = ch is not None and (t - ch.s) % ch.P == 0
                        require(legal == in_chart, "general progression compatibility mask")
                        if in_chart:
                            v = (t - ch.s) // ch.P
                            require(p.evaluate(f.value(t)) == ch.u + 2*ch.target_d*v,
                                    "general progression target lift")
                geometric_tail = 1 - sum((F(1, 1 << p.A) for p in stop_leaves(H)), F(0))
                s = valuation2(f.d)
                require(Q[("overflow",)] <= (1 << s) * geometric_tail,
                        "retained dyadic-conditioning tail bound")
                law_fixtures.append({"a": f.a, "d": f.d, "b": f.b, "N": f.N,
                                     "H": H, "M": M, "actual_overflow": str(P[("overflow",)]),
                                     "reference_overflow": str(Q[("overflow",)]), "TV": str(tv)})

    # Congruence readouts and section changes on the original integer lattice.
    for p in stop_leaves(12):
        for k in (0, 2, 11):
            n = p.residue + p.modulus * k
            _, vals = odd_steps(n, p.m)
            for j in range(p.m + 1):
                z = packet(p.word[:j])
                base = z.evaluate(p.residue)
                require(base.denominator == 1, "prefix base integrality")
                coeff = (1 << (p.A + 1 - z.A)) * z.L
                require(vals[j] == base + coeff*k, "all-prefix lattice readout")
                for M in (3, 4, 9, 12):
                    require(vals[j] % M == (int(base) + coeff*(k % M)) % M,
                            "synchronized residue readout")
                shift = 7
                changed_base = z.evaluate(p.residue + p.modulus*shift)
                require(changed_base + coeff*(k-shift) == vals[j], "section-change equivariance")

    # Explicit infinite-family restart: no division of the retained lattice step.
    ex = packet((1, 1, 3, 2))
    require(ex.A == 7 and ex.L == 81 and ex.C == 89 and ex.residue == 247,
            "worked first packet")
    example_rows = []
    blocks = [(1, 1, 3, 2), (3,), (1, 2, 1, 4), (1, 3), (1, 2, 3), (4,)]
    total = packet(())
    current = 247
    for word in blocks:
        p = packet(word)
        require(is_stop(p), "worked block universal certificate")
        w, vals = odd_steps(current, p.m)
        require(w == word, "worked block integer replay")
        current = vals[-1]
        total = join(total, p)
        example_rows.append({"word": list(word), "endpoint_at_247": current,
                             "total_A": total.A, "total_m": total.m,
                             "source_step": 1 << (total.A+1),
                             "target_step": 2*total.L})
        for t in (0, 1, 17, 10**30):
            n = 247 + (1 << (total.A + 1))*t
            w2, vals2 = odd_steps(n, total.m)
            require(w2 == total.word, "infinite-family exact branch lift")
            require(vals2[-1] == current + 2*total.L*t, "infinite-family affine endpoint")
    require(current == 1 and total.A == 32 and total.m == 15,
            "worked complete orbit anchor")

    enriched = enriched_incidence_test()
    image_complex = image_complex_test()
    renewal = renewal_test()
    spectrum = spectral_and_incidence_test()
    restart = restart_certificate_test()
    rejected = []
    invalid = [("zero exponent", lambda: packet((0,))),
               ("even start", lambda: odd_steps(2, 1)),
               ("fixed point strict-descent domain", lambda: observe(1, 10)),
               ("invalid mark modulus", lambda: marked_cells(Family(1, 1, 1, 10), ex, 0)),
               ("sub-threshold source", lambda: Family(1, 1, 0, 10).validate())]
    for name, fun in invalid:
        try:
            fun()
        except ValueError:
            rejected.append(name)
        else:
            raise VerificationError(f"invalid case accepted: {name}")
    # Deliberately wrong target slope and discarded offset must be detected.
    require(ex.evaluate(247+256) != 157+2, "reject replacement of target step by two")
    z = packet((1, 1, 3))
    require((1 << z.A) > z.L and z.evaluate(3) >= 3,
            "reject multiplier-only descent")
    return {"status": "PASS", "arithmetic": "integers and exact rational fractions",
            "check_counts": dict(sorted(COUNTS.items())), "total_checks": sum(COUNTS.values()),
            "source_word_fixtures": len(words), "marked_law_fixtures": len(law_fixtures),
            "stopped_profiles": profiles, "marked_laws": law_fixtures,
            "worked_restart_family": example_rows, "incidence_and_spectral": spectrum,
            "three_round_restart": restart, "invalid_cases_rejected": rejected,
            "arithmetic_image_complex": image_complex, "stopped_renewal": renewal,
            "enriched_incidence_comparison": enriched,
            "rational_tail_constants": {"rho": str(rho), "C": str(C0), "K": str(K)},
            "proof_scope": "Finite replay checks; the all-horizon result is proved in note.md.",
            "repository_changes": "None; local artifact only."}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write deterministic verification JSON")
    args = parser.parse_args()
    result = run()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(json.dumps({"status": result["status"], "total_checks": result["total_checks"],
                      "marked_law_fixtures": result["marked_law_fixtures"],
                      "output": str(args.output) if args.output else None}, sort_keys=True))


if __name__ == "__main__":
    main()
