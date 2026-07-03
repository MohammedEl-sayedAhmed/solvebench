"""Empirical time & space complexity estimator for Python solutions.

Big-O can't be computed statically, but you CAN measure how a function's runtime
and peak memory grow as the input grows, and fit that curve to common classes.

    from common.complexity import estimate

    # make_input(n) returns the ARGUMENT LIST passed to the function for size n.
    # It's called fresh for every trial, so in-place mutation is fine.
    estimate(sorted, make_input=lambda n: [list(range(n, 0, -1))], label="sorted")

Run a live demo with:

    python python/common/complexity.py
"""
from __future__ import annotations

import math
import time
import tracemalloc
from statistics import median

# Candidate growth curves. estimate() fits a scale factor to each and keeps the
# one with the smallest error.
MODELS = {
    "O(1)": lambda n: 1.0,
    "O(log n)": lambda n: math.log2(n) if n > 1 else 1.0,
    "O(n)": lambda n: float(n),
    "O(n log n)": lambda n: n * math.log2(n) if n > 1 else float(n),
    "O(n^2)": lambda n: float(n) * n,
    "O(n^3)": lambda n: float(n) ** 3,
    "O(2^n)": lambda n: 2.0 ** min(n, 60),
}


def _best_fit(sizes, values):
    """Return the MODELS key whose scaled curve best matches `values`."""
    if not any(v > 0 for v in values):
        return "O(1)"
    scale = sum(v * v for v in values) or 1.0
    best, best_err = "O(1)", math.inf
    for name, f in MODELS.items():
        basis = [f(n) for n in sizes]
        denom = sum(b * b for b in basis)
        if denom == 0:
            continue
        c = sum(v * b for v, b in zip(values, basis)) / denom  # least-squares scale
        if c <= 0:
            continue
        err = sum((v - c * b) ** 2 for v, b in zip(values, basis)) / scale
        if err < best_err:
            best, best_err = name, err
    return best


def estimate(func, make_input, sizes=None, repeat=3, label=None, measure_space=True):
    """Measure `func` across growing inputs and print an estimated complexity.

    :param func: the function under test.
    :param make_input: ``n -> list`` returning the args for input size n.
    :param sizes: input sizes to try (default a geometric sweep).
    :param repeat: timing repeats per size (the median is used).
    :returns: dict with sizes, times, time_class (+ spaces, space_class).
    """
    sizes = list(sizes or (1000, 2000, 4000, 8000, 16000))
    name = label or getattr(func, "__name__", "func")

    times, spaces = [], []
    for n in sizes:
        trials = []
        for _ in range(repeat):
            args = make_input(n)  # fresh args each trial (mutation-safe)
            start = time.perf_counter()
            func(*args)
            trials.append(time.perf_counter() - start)
        times.append(median(trials))

        if measure_space:
            args = make_input(n)
            tracemalloc.start()
            func(*args)
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            spaces.append(float(peak))

    header = f"{'n':>10}{'time (ms)':>14}" + (f"{'peak (KB)':>14}" if measure_space else "")
    print(f"\n📈  Complexity estimate — {name}")
    print(header)
    print("─" * len(header))
    for i, n in enumerate(sizes):
        row = f"{n:>10}{times[i] * 1e3:>14.3f}"
        if measure_space:
            row += f"{spaces[i] / 1024:>14.1f}"
        print(row)
    print("─" * len(header))

    result = {"sizes": sizes, "times": times, "time_class": _best_fit(sizes, times)}
    print(f"time  ≈ {result['time_class']}")
    if measure_space:
        result["spaces"] = spaces
        result["space_class"] = _best_fit(sizes, spaces)
        print(f"space ≈ {result['space_class']}  (auxiliary — allocations during the call)")
    print("(empirical: measured growth fit to common classes, not a proof)")
    return result


if __name__ == "__main__":
    # Demo three functions whose complexity we already know.
    estimate(lambda xs: sum(xs),
             make_input=lambda n: [list(range(n))], label="sum  (expected O(n) time)")

    estimate(sorted,
             make_input=lambda n: [list(range(n, 0, -1))], label="sorted  (expected O(n log n))")

    def count_pairs(xs):
        c = 0
        for a in xs:
            for b in xs:
                c += 1 if a == b else 0
        return c

    estimate(count_pairs,
             make_input=lambda n: [list(range(n))],
             sizes=(200, 400, 800, 1600), label="nested loops  (expected O(n^2))")
