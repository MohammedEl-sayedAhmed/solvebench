#!/usr/bin/env python3
"""Estimate a solution's empirical time & space complexity — per problem.

    python complexity.py leetcode/easy/two_sum
    ./run.sh complexity leetcode/easy/two_sum          # same, via the wrapper
    python complexity.py three_sum --max-seconds 1     # cap slow runs sooner
    python complexity.py min_stack --method getMin     # pick the method yourself

How it works
------------
Finds the Python solution file, picks the function to measure (the `Solution`
method or top-level function whose name best matches the file name — override
with --method), generates growing inputs from the function's TYPE HINTS
(list[int], str, int, ...), and fits runtime + peak memory to common Big-O
classes using common.complexity.estimate.

When type hints aren't enough (special input shapes, constraints, in-place
mutation like merge_sorted_array), add a 2-line hook to the solution file and
the tool will use it instead:

    def complexity_input(n):
        return [list(range(n)), n]      # the ARGUMENT LIST for input size n

Note: results are empirical — generated inputs may not hit the worst case, and
the measured class is a fit, not a proof. For solutions ported to other
languages the algorithm (and class) is the same; measure the Python version.
"""
from __future__ import annotations

import argparse
import importlib.util
import inspect
import random
import re
import string
import sys
from pathlib import Path
from typing import Callable, NoReturn, cast

REPO = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO / "python"))
from common.complexity import estimate  # noqa: E402


def die(msg: str) -> NoReturn:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


# --------------------------------------------------------------------------- #
# Locate the solution file
# --------------------------------------------------------------------------- #
def find_solution_file(fragment: str) -> Path:
    root = REPO / "python"
    norm = lambda s: re.sub(r"[^a-z0-9/]", "", s.lower())
    nfrag = norm(fragment.replace("\\", "/"))
    rels = {p: norm(str(p.relative_to(root).with_suffix("")))
            for p in sorted(root.rglob("*.py")) if "common" not in p.parts}
    hits = [p for p, r in rels.items() if nfrag in r]
    if not hits:
        die(f"no Python solution matches {fragment!r} (searched python/)")
    if len(hits) > 1:
        # An exact name/path match beats substring matches (two_sum vs two_sum_ii).
        exact = [p for p in hits if rels[p] == nfrag or rels[p].endswith("/" + nfrag)]
        if len(exact) == 1:
            return exact[0]
        opts = ", ".join(str(p.relative_to(root)) for p in hits)
        die(f"{fragment!r} is ambiguous: {opts}")
    return hits[0]


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        die(f"could not import {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --------------------------------------------------------------------------- #
# Pick the function to measure
# --------------------------------------------------------------------------- #
def _tokens(name: str) -> set[str]:
    snake = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name)
    return {t.lower() for t in re.split(r"[_\W]+", snake) if t}


def pick_callable(mod, file_stem: str, method: str | None):
    candidates: dict[str, Callable] = {}
    sol_cls = getattr(mod, "Solution", None)
    if sol_cls is not None:
        inst = sol_cls()
        for name, fn in inspect.getmembers(inst, callable):
            if not name.startswith("_"):
                candidates[name] = fn
    else:
        skip = {"test_solution", "complexity_input", "run_tests", "input_path", "estimate"}
        for name, fn in vars(mod).items():
            if (inspect.isfunction(fn) and fn.__module__ == mod.__name__
                    and not name.startswith("_") and name not in skip
                    and not name.startswith("solve_from")):
                candidates[name] = fn

    if not candidates:
        die("no candidate function found — pass --method or add complexity_input(n)")
    if method:
        if method in candidates:
            return method, candidates[method]
        die(f"--method {method!r} not found; available: {', '.join(sorted(candidates))}")

    ft = _tokens(file_stem)
    scored = sorted(candidates, key=lambda nm: (-len(_tokens(nm) & ft), nm))
    best = len(_tokens(scored[0]) & ft)
    ties = [nm for nm in scored if len(_tokens(nm) & ft) == best]
    if len(candidates) > 1 and (best == 0 or len(ties) > 1):
        die(f"can't guess which function to measure; pass --method one of: "
            f"{', '.join(sorted(candidates))}")
    return scored[0], candidates[scored[0]]


# --------------------------------------------------------------------------- #
# Build inputs: complexity_input(n) override, else from type hints
# --------------------------------------------------------------------------- #
def _palindrome(n: int) -> str:
    """A non-uniform palindromic string — worst case for symmetric scans
    (random text early-exits at the first mismatch and reads as O(1))."""
    half = "".join(string.ascii_lowercase[i % 26] for i in range(n // 2))
    mid = "z" if n % 2 else ""
    return half + mid + half[::-1]


def _gen_for(ann, rng):
    if ann is inspect.Parameter.empty or ann is int:
        return lambda n: n
    if ann is float:
        return lambda n: float(n)
    if ann is bool:
        return lambda n: True
    if ann is str:
        return _palindrome
    origin, args = getattr(ann, "__origin__", None), getattr(ann, "__args__", ())
    if origin is list:
        inner = args[0] if args else int
        if inner is int:
            # Deterministic 0..n-1: search problems can't early-exit on a lucky
            # random pair, and sorted-precondition problems stay valid.
            return lambda n: list(range(n))
        if inner is str:
            return lambda n: ["".join(rng.choice(string.ascii_lowercase) for _ in range(8))
                              for _ in range(n)]
        if getattr(inner, "__origin__", None) is list:
            return lambda n: [[rng.randrange(-100, 100) for _ in range(8)] for _ in range(n)]
    return None


def make_input_builder(mod, fn) -> tuple[Callable[[int], list], str]:
    custom = getattr(mod, "complexity_input", None)
    if callable(custom):
        hook = cast(Callable[[int], list], custom)  # duck-typed user hook
        return (lambda n: list(hook(n))), "complexity_input(n) from the solution file"

    params = [p for p in inspect.signature(fn).parameters.values() if p.name != "self"]
    rng = random.Random(20260703)
    gens = []
    for p in params:
        g = _gen_for(p.annotation, rng)
        if g is None:
            die(f"can't auto-generate the {p.name!r} parameter "
                f"(annotation: {p.annotation}). Add this to the solution file:\n\n"
                f"    def complexity_input(n):\n"
                f"        return [...]   # the argument list for input size n")
        gens.append(g)
    desc = "auto-generated from type hints (" + \
           ", ".join(f"{p.name}: {getattr(p.annotation, '__name__', p.annotation)}"
                     if p.annotation is not inspect.Parameter.empty else f"{p.name}: int"
                     for p in params) + ")"
    return (lambda n: [g(n) for g in gens]), desc


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("problem", help="solution path fragment, e.g. leetcode/easy/two_sum")
    ap.add_argument("--method", help="function/method name to measure")
    ap.add_argument("--sizes", help="comma-separated input sizes (default 500,1000,2000,4000,8000)")
    ap.add_argument("--repeat", type=int, default=3, help="timing repeats per size (default 3)")
    ap.add_argument("--max-seconds", type=float, default=2.0,
                    help="stop growing sizes once one run exceeds this (default 2.0)")
    args = ap.parse_args()

    path = find_solution_file(args.problem)
    print(f"solution: {path.relative_to(REPO)}")
    mod = load_module(path)
    name, fn = pick_callable(mod, path.stem, args.method)
    builder, how = make_input_builder(mod, fn)
    print(f"function: {name}  ·  inputs: {how}")

    sizes = [int(s) for s in args.sizes.split(",")] if args.sizes else None

    # Probe once with the smallest size so input problems fail with a clear hint.
    probe_n = (sizes or [500])[0]
    try:
        fn(*builder(probe_n))
    except Exception as e:  # noqa: BLE001
        die(f"the function raised on a generated input ({type(e).__name__}: {e}).\n"
            f"Its input probably has constraints the generator doesn't know — add a\n"
            f"complexity_input(n) function to {path.name} returning valid args for size n.")

    estimate(fn, builder, sizes=sizes or (500, 1000, 2000, 4000, 8000),
             repeat=args.repeat, label=name, max_seconds=args.max_seconds)
    return 0


if __name__ == "__main__":
    sys.exit(main())
