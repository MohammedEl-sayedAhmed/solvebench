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
    """Return the MODELS key whose scaled curve best matches `values`.

    Fits in LOG space: the scale factor drops out as a constant offset and every
    data point carries equal weight, so one noisy large-n sample can't flip the
    class the way a raw least-squares fit can.
    """
    if not any(v > 0 for v in values):
        return "O(1)"
    floor = max(v for v in values) * 1e-9  # clamp zeros so log() is defined
    logs = [math.log(max(v, floor)) for v in values]
    best, best_err = "O(1)", math.inf
    for name, f in MODELS.items():
        basis = [math.log(f(n)) for n in sizes]
        offset = sum(lv - lb for lv, lb in zip(logs, basis)) / len(logs)  # log(c)
        err = sum((lv - (offset + lb)) ** 2 for lv, lb in zip(logs, basis))
        if err < best_err:
            best, best_err = name, err
    return best


def estimate(func, make_input, sizes=None, repeat=3, label=None, measure_space=True,
             max_seconds=None):
    """Measure `func` across growing inputs and print an estimated complexity.

    :param func: the function under test.
    :param make_input: ``n -> list`` returning the args for input size n.
    :param sizes: input sizes to try (default a geometric sweep).
    :param repeat: timing repeats per size (the median is used).
    :param max_seconds: stop growing sizes once one run exceeds this (keeps the
        tool responsive for O(n^2)+ solutions); collected points are still fit.
    :returns: dict with sizes, times, time_class (+ spaces, space_class).
    """
    sizes = list(sizes or (1000, 2000, 4000, 8000, 16000))
    name = label or getattr(func, "__name__", "func")

    times, spaces, used_sizes = [], [], []
    for i, n in enumerate(sizes):
        trials = []
        for _ in range(repeat):
            args = make_input(n)  # fresh args each trial (mutation-safe)
            start = time.perf_counter()
            func(*args)
            trials.append(time.perf_counter() - start)
        # Best-of-trials: system noise only ever ADDS time, so the minimum is
        # the most faithful sample of the algorithm itself.
        times.append(min(trials))
        used_sizes.append(n)

        # tracemalloc multiplies runtime ~10x, so skip the space probe for a
        # size whose plain run already reached the cap.
        if measure_space and (max_seconds is None or times[-1] <= max_seconds):
            args = make_input(n)
            tracemalloc.start()
            func(*args)
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            spaces.append(float(peak))

        if max_seconds is not None:
            nxt = sizes[i + 1] if i + 1 < len(sizes) else None
            # Stop when this size hit the cap, or the NEXT one predictably
            # would (linear projection — an underestimate for superlinear
            # solutions, which is exactly when stopping matters most).
            if times[-1] > max_seconds or (nxt and times[-1] * (nxt / n) > max_seconds):
                print(f"(stopping after n={n}: the next size would exceed the {max_seconds:.2f}s cap)")
                break
    return report(used_sizes, times, spaces if measure_space else None, name)


def report(sizes, times, spaces, label, space_label="peak (KB)"):
    """Render the measurement table, fit the Big-O classes, and return them.

    Shared by estimate() and other measurement front-ends (e.g. the Java
    harness driven by complexity.py) so every language reports identically.
    ``spaces`` may be None (no space data) or shorter than ``sizes`` (probe
    skipped near the time cap).
    """
    spaces = spaces or []
    header = f"{'n':>10}{'time (ms)':>14}" + (f"{space_label:>14}" if spaces else "")
    print(f"\n📈  Complexity estimate — {label}")
    print(header)
    print("─" * len(header))
    for i, n in enumerate(sizes):
        row = f"{n:>10}{times[i] * 1e3:>14.3f}"
        if spaces:
            row += f"{spaces[i] / 1024:>14.1f}" if i < len(spaces) else f"{'—':>14}"
        print(row)
    print("─" * len(header))

    if len(sizes) < 3:
        print("⚠  fewer than 3 data points — the fit below is unreliable; try smaller --sizes")
    result = {"sizes": sizes, "times": times, "time_class": _best_fit(sizes, times)}
    print(f"time  ≈ {result['time_class']}")
    if spaces:
        result["spaces"] = spaces
        result["space_class"] = _best_fit(sizes[:len(spaces)], spaces)
        print(f"space ≈ {result['space_class']}  (auxiliary — allocations during the call)")
    print("(empirical: measured growth fit to common classes, not a proof)")
    return result


if __name__ == "__main__":
    # Demo three functions whose complexity we already know.
    import random

    estimate(lambda xs: sum(xs),
             make_input=lambda n: [list(range(n))], label="sum  (expected O(n) time)")

    def shuffled(n):
        # A reversed list is Timsort's O(n) BEST case (one descending run);
        # shuffling forces the real O(n log n) path.
        xs = list(range(n))
        random.Random(n).shuffle(xs)
        return [xs]

    estimate(sorted, make_input=shuffled, label="sorted  (expected O(n log n))")

    def count_pairs(xs):
        c = 0
        for a in xs:
            for b in xs:
                c += 1 if a == b else 0
        return c

    estimate(count_pairs,
             make_input=lambda n: [list(range(n))],
             sizes=(200, 400, 800, 1600), label="nested loops  (expected O(n^2))")
