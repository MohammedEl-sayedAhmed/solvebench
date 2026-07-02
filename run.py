#!/usr/bin/env python3
"""
Polyglot test runner for the problem-solving-training repo.

Discovers self-testing solution files across languages (``python/``, ``cpp/``,
``java/``), runs each one, and reports pass/fail grouped by *platform*.

A solution "passes" when its process exits 0. Each language self-tests via its
common helper:
    python/common/test_framework.py   (run_tests -> raises on failure)
    cpp/common/test_framework.hpp      (tf::TestRunner::summary -> exit code)
    java/common/TestFramework.java     (TestFramework.summary -> exit code)

Examples
--------
    python run.py                       # run everything
    python run.py leetcode              # only paths containing "leetcode"
    python run.py leetcode/easy/two_sum # a single problem, all languages
    python run.py --lang py --lang cpp  # restrict languages
    python run.py --platform codewars   # restrict platform
    python run.py --sort status         # failures first in the summary
    python run.py --stats               # inventory only, don't run anything
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parent

# language dir -> (source extension, canonical short name, aliases)
LANGUAGES = {
    "python": {"ext": ".py", "short": "py", "aliases": {"py", "python"}},
    "cpp": {"ext": ".cpp", "short": "cpp", "aliases": {"cpp", "c++", "cc"}},
    "java": {"ext": ".java", "short": "java", "aliases": {"java"}},
}
TIMEOUT = 120  # seconds per solution


@dataclass
class Solution:
    language: str  # "python" | "cpp" | "java"
    platform: str  # "leetcode" | "codewars" | "adventofcode" | "others" | ...
    group: str  # remaining sub-path, e.g. "easy" or "2022/7" ("" if none)
    name: str  # file stem
    path: Path  # absolute path to the source file

    @property
    def short_lang(self) -> str:
        return LANGUAGES[self.language]["short"]

    @property
    def label(self) -> str:
        rel = self.path.relative_to(REPO)
        return str(rel)


# --------------------------------------------------------------------------- #
# Discovery
# --------------------------------------------------------------------------- #
def discover() -> list[Solution]:
    solutions: list[Solution] = []
    for lang, meta in LANGUAGES.items():
        root = REPO / lang
        if not root.is_dir():
            continue
        for path in sorted(root.rglob(f"*{meta['ext']}")):
            parts = path.relative_to(root).parts
            # skip shared helpers and any non-solution scaffolding
            if "common" in parts:
                continue
            platform = parts[0] if len(parts) > 1 else "(root)"
            group = "/".join(parts[1:-1])
            solutions.append(
                Solution(lang, platform, group, path.stem, path)
            )
    return solutions


def matches(sol: Solution, filters: list[str], langs: set[str], platform: str | None) -> bool:
    if langs and sol.short_lang not in langs:
        return False
    if platform and sol.platform != platform:
        return False
    if filters:
        rel = sol.label
        rel_no_lang = str(sol.path.relative_to(REPO / sol.language))
        if not any(f in rel or f in rel_no_lang for f in filters):
            return False
    return True


# --------------------------------------------------------------------------- #
# Execution (one function per language)
# --------------------------------------------------------------------------- #
def _run(cmd, cwd, env=None) -> tuple[bool, str]:
    try:
        proc = subprocess.run(
            cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=TIMEOUT
        )
    except subprocess.TimeoutExpired:
        return False, f"TIMEOUT after {TIMEOUT}s"
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode == 0, out


def run_python(sol: Solution) -> tuple[bool, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO / "python") + os.pathsep + env.get("PYTHONPATH", "")
    return _run([sys.executable, str(sol.path)], cwd=sol.path.parent, env=env)


def run_cpp(sol: Solution, build: Path) -> tuple[bool, str]:
    binary = build / (sol.name + ".bin")
    ok, out = _run(
        ["g++", "-std=c++17", "-O2", "-I", str(REPO / "cpp"), str(sol.path), "-o", str(binary)],
        cwd=REPO,
    )
    if not ok:
        return False, "compile error:\n" + out
    return _run([str(binary)], cwd=sol.path.parent)


def run_java(sol: Solution, build: Path) -> tuple[bool, str]:
    outdir = build / f"java_{sol.name}"
    outdir.mkdir(parents=True, exist_ok=True)
    java_root = REPO / "java"
    framework = java_root / "common" / "TestFramework.java"
    ok, out = _run(
        ["javac", "-d", str(outdir), "-cp", str(java_root), str(framework), str(sol.path)],
        cwd=REPO,
    )
    if not ok:
        return False, "compile error:\n" + out
    # Fully-qualified class name: the path under java/ maps to the package.
    rel = sol.path.relative_to(java_root).with_suffix("")  # e.g. leetcode/easy/TwoSum
    fqcn = ".".join(rel.parts)  # leetcode.easy.TwoSum
    return _run(["java", "-cp", str(outdir), fqcn], cwd=sol.path.parent)


def execute(sol: Solution, build: Path) -> tuple[bool, str]:
    if sol.language == "python":
        return run_python(sol)
    if sol.language == "cpp":
        return run_cpp(sol, build)
    if sol.language == "java":
        return run_java(sol, build)
    return False, f"unknown language {sol.language}"


# --------------------------------------------------------------------------- #
# Reporting
# --------------------------------------------------------------------------- #
def print_stats(sols: list[Solution], sort_key: str) -> None:
    from collections import defaultdict

    counts: dict[tuple[str, str], int] = defaultdict(int)
    for s in sols:
        counts[(s.platform, s.short_lang)] += 1

    rows = [(plat, lang, n) for (plat, lang), n in counts.items()]
    if sort_key == "language":
        rows.sort(key=lambda r: (r[1], r[0]))
    elif sort_key == "status":  # highest count first
        rows.sort(key=lambda r: (-r[2], r[0], r[1]))
    else:  # platform (default) or name
        rows.sort(key=lambda r: (r[0], r[1]))

    print(f"\n{'PLATFORM':<16}{'LANG':<8}{'COUNT':>6}")
    print("-" * 30)
    for plat, lang, n in rows:
        print(f"{plat:<16}{lang:<8}{n:>6}")
    print("-" * 30)
    print(f"{'TOTAL':<16}{'':<8}{len(sols):>6}\n")


def print_summary(results: list[tuple[Solution, bool, bool]], sort_key: str) -> int:
    """results: list of (solution, passed, skipped). Returns process exit code."""
    from collections import defaultdict

    agg: dict[tuple[str, str], list[int]] = defaultdict(lambda: [0, 0, 0])  # passed, failed, total
    failed_labels: list[str] = []
    for sol, passed, skipped in results:
        key = (sol.platform, sol.short_lang)
        agg[key][2] += 1
        if skipped:
            continue
        if passed:
            agg[key][0] += 1
        else:
            agg[key][1] += 1
            failed_labels.append(sol.label)

    rows = [(plat, lang, p, f, t) for (plat, lang), (p, f, t) in agg.items()]

    def key_fn(r):
        plat, lang, _, f, _ = r
        if sort_key == "status":  # most failures first
            return (-f, plat, lang)
        if sort_key == "language":
            return (lang, plat)
        return (plat, lang)  # default: platform / name

    rows.sort(key=key_fn)

    print(f"\n{'PLATFORM':<16}{'LANG':<8}{'PASS':>6}{'FAIL':>6}{'TOTAL':>7}")
    print("-" * 43)
    tot_p = tot_f = tot_t = 0
    for plat, lang, p, f, t in rows:
        flag = "  ❌" if f else ""
        print(f"{plat:<16}{lang:<8}{p:>6}{f:>6}{t:>7}{flag}")
        tot_p += p
        tot_f += f
        tot_t += t
    print("-" * 43)
    print(f"{'TOTAL':<16}{'':<8}{tot_p:>6}{tot_f:>6}{tot_t:>7}")

    if failed_labels:
        print(f"\n{tot_f} failure(s):")
        for lbl in failed_labels:
            print(f"  ❌ {lbl}")
        return 1
    print("\nAll solutions passed! 🎉")
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("filters", nargs="*", help="path substrings to include (e.g. leetcode/easy/two_sum)")
    parser.add_argument("--lang", action="append", default=[], help="restrict language: py|cpp|java (repeatable)")
    parser.add_argument("--platform", help="restrict to one platform (e.g. leetcode)")
    parser.add_argument("--sort", default="platform", choices=["platform", "language", "status", "name"], help="summary sort order")
    parser.add_argument("--stats", action="store_true", help="show inventory grouped by platform and exit (no runs)")
    parser.add_argument("-q", "--quiet", action="store_true", help="don't print per-solution output, only the summary")
    args = parser.parse_args()

    langs: set[str] = set()
    for l in args.lang:
        matched = [name for name, m in LANGUAGES.items() if l.lower() in m["aliases"]]
        if not matched:
            parser.error(f"unknown --lang {l!r} (choose from py, cpp, java)")
        langs.add(LANGUAGES[matched[0]]["short"])

    all_sols = discover()
    sols = [s for s in all_sols if matches(s, args.filters, langs, args.platform)]
    sols.sort(key=lambda s: (s.platform, s.short_lang, s.group, s.name))

    if not sols:
        if args.filters or langs or args.platform:
            print("No solutions matched the given filters.")
            return 1
        # An empty repo (e.g. a freshly init'ed fork) is a valid, passing state.
        print("No solutions yet — add one with:  python new.py <platform>/<name> --lang py")
        return 0

    if args.stats:
        print_stats(sols, args.sort)
        return 0

    build = Path(tempfile.mkdtemp(prefix="pst_build_"))
    results: list[tuple[Solution, bool, bool]] = []
    try:
        for sol in sols:
            passed, output = execute(sol, build)
            icon = "✅" if passed else "❌"
            print(f"{icon} [{sol.short_lang}] {sol.platform}/{sol.group + '/' if sol.group else ''}{sol.name}")
            if not args.quiet and not passed:
                for line in output.strip().splitlines():
                    print(f"      {line}")
            results.append((sol, passed, False))
    finally:
        shutil.rmtree(build, ignore_errors=True)

    return print_summary(results, args.sort)


if __name__ == "__main__":
    sys.exit(main())
