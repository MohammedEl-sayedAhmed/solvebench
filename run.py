#!/usr/bin/env python3
"""
Polyglot test runner for the solvebench repo.

Discovers self-testing solution files across languages, runs each one, and
reports pass/fail grouped by *platform*. A solution "passes" when its process
exits 0; each language self-tests via its common helper (or an inline one for
Go/Rust).

Examples
--------
    python run.py                       # run everything, all languages
    python run.py leetcode/easy/two_sum # one problem across every language
    python run.py --platform codewars   # restrict to a platform
    python run.py --lang py --lang js   # restrict languages
    python run.py --changed             # only solutions changed vs git HEAD
    python run.py --time                # print each solution's runtime
    python run.py --stats               # inventory grouped by platform
    python run.py --sort status         # failures first in the summary
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parent

# language dir -> (source extension, canonical short name, aliases)
LANGUAGES = {
    "python": {"ext": ".py", "short": "py", "aliases": {"py", "python"}},
    "cpp": {"ext": ".cpp", "short": "cpp", "aliases": {"cpp", "c++", "cc"}},
    "java": {"ext": ".java", "short": "java", "aliases": {"java"}},
    "javascript": {"ext": ".js", "short": "js", "aliases": {"js", "javascript", "node"}},
    "go": {"ext": ".go", "short": "go", "aliases": {"go", "golang"}},
    "rust": {"ext": ".rs", "short": "rust", "aliases": {"rust", "rs"}},
}
TIMEOUT = 120  # seconds per solution


@dataclass
class Solution:
    language: str
    platform: str
    group: str
    name: str
    path: Path

    @property
    def short_lang(self) -> str:
        return LANGUAGES[self.language]["short"]

    @property
    def label(self) -> str:
        return str(self.path.relative_to(REPO))


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
            if "common" in parts:  # skip shared helpers
                continue
            platform = parts[0] if len(parts) > 1 else "(root)"
            group = "/".join(parts[1:-1])
            solutions.append(Solution(lang, platform, group, path.stem, path))
    return solutions


def changed_paths() -> set[str] | None:
    """Repo-relative paths changed vs HEAD (tracked edits + untracked), or None."""
    try:
        diff = subprocess.run(["git", "diff", "--name-only", "HEAD"], cwd=REPO,
                              capture_output=True, text=True)
        untr = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"],
                              cwd=REPO, capture_output=True, text=True)
        if diff.returncode != 0:
            return None
        paths: set[str] = set()
        for out in (diff.stdout, untr.stdout):
            paths.update(line.strip() for line in out.splitlines() if line.strip())
        return paths
    except Exception:
        return None


def matches(sol, filters, langs, platform) -> bool:
    if langs and sol.short_lang not in langs:
        return False
    if platform and sol.platform != platform:
        return False
    if filters:
        rel = sol.label
        rel_no_lang = str(sol.path.relative_to(REPO / sol.language))
        # Normalized match so "two_sum" also matches Java's "TwoSum", etc.
        norm = lambda s: re.sub(r"[^a-z0-9/]", "", s.lower())
        nrl = norm(rel_no_lang)
        if not any(f in rel or f in rel_no_lang or norm(f) in nrl for f in filters):
            return False
    return True


# --------------------------------------------------------------------------- #
# Execution (one function per language)
# --------------------------------------------------------------------------- #
def _run(cmd, cwd, env=None) -> tuple[bool, str]:
    try:
        proc = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True,
                              text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return False, f"TIMEOUT after {TIMEOUT}s"
    except FileNotFoundError as e:
        return False, f"toolchain not found: {e}"
    return proc.returncode == 0, (proc.stdout or "") + (proc.stderr or "")


def run_python(sol, build):
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO / "python") + os.pathsep + env.get("PYTHONPATH", "")
    return _run([sys.executable, str(sol.path)], cwd=sol.path.parent, env=env)


def run_cpp(sol, build):
    binary = build / (sol.name + ".bin")
    ok, out = _run(["g++", "-std=c++17", "-O2", "-I", str(REPO / "cpp"),
                    str(sol.path), "-o", str(binary)], cwd=REPO)
    if not ok:
        return False, "compile error:\n" + out
    return _run([str(binary)], cwd=sol.path.parent)


def run_java(sol, build):
    outdir = build / f"java_{sol.name}"
    outdir.mkdir(parents=True, exist_ok=True)
    java_root = REPO / "java"
    framework = java_root / "common" / "TestFramework.java"
    ok, out = _run(["javac", "-encoding", "UTF-8", "-d", str(outdir), "-cp", str(java_root),
                    str(framework), str(sol.path)], cwd=REPO)
    if not ok:
        return False, "compile error:\n" + out
    fqcn = ".".join(sol.path.relative_to(java_root).with_suffix("").parts)
    return _run(["java", "-cp", str(outdir), fqcn], cwd=sol.path.parent)


def run_js(sol, build):
    env = dict(os.environ)
    env["NODE_PATH"] = str(REPO / "javascript") + os.pathsep + env.get("NODE_PATH", "")
    return _run(["node", str(sol.path)], cwd=sol.path.parent, env=env)


def run_go(sol, build):
    # Go solutions are self-contained `package main` files (Go's tooling makes a
    # shared single-file helper across dirs awkward), so we just `go run` them.
    return _run(["go", "run", str(sol.path)], cwd=sol.path.parent)


def run_rust(sol, build):
    binary = build / (sol.name + ".bin")
    ok, out = _run(["rustc", "-O", str(sol.path), "-o", str(binary)], cwd=REPO)
    if not ok:
        return False, "compile error:\n" + out
    return _run([str(binary)], cwd=sol.path.parent)


RUNNERS = {
    "python": run_python, "cpp": run_cpp, "java": run_java,
    "javascript": run_js, "go": run_go, "rust": run_rust,
}


def execute(sol, build) -> tuple[bool, str, float]:
    start = time.perf_counter()
    passed, out = RUNNERS[sol.language](sol, build)
    return passed, out, time.perf_counter() - start


# --------------------------------------------------------------------------- #
# Reporting
# --------------------------------------------------------------------------- #
def print_stats(sols, sort_key):
    from collections import defaultdict
    counts = defaultdict(int)
    for s in sols:
        counts[(s.platform, s.short_lang)] += 1
    rows = [(p, l, n) for (p, l), n in counts.items()]
    if sort_key == "language":
        rows.sort(key=lambda r: (r[1], r[0]))
    elif sort_key == "status":
        rows.sort(key=lambda r: (-r[2], r[0], r[1]))
    else:
        rows.sort(key=lambda r: (r[0], r[1]))
    print(f"\n{'PLATFORM':<16}{'LANG':<8}{'COUNT':>6}")
    print("-" * 30)
    for p, l, n in rows:
        print(f"{p:<16}{l:<8}{n:>6}")
    print("-" * 30)
    print(f"{'TOTAL':<16}{'':<8}{len(sols):>6}\n")


def print_summary(results, sort_key, show_time):
    from collections import defaultdict
    agg = defaultdict(lambda: [0, 0, 0])
    failed = []
    for sol, passed, skipped, secs in results:
        key = (sol.platform, sol.short_lang)
        agg[key][2] += 1
        if skipped:
            continue
        agg[key][0 if passed else 1] += 1
        if not passed:
            failed.append(sol.label)

    rows = [(p, l, v[0], v[1], v[2]) for (p, l), v in agg.items()]

    def key_fn(r):
        p, l, _pa, f, _t = r
        if sort_key == "status":
            return (-f, p, l)
        if sort_key == "language":
            return (l, p)
        return (p, l)

    rows.sort(key=key_fn)
    print(f"\n{'PLATFORM':<16}{'LANG':<8}{'PASS':>6}{'FAIL':>6}{'TOTAL':>7}")
    print("-" * 43)
    tp = tf = tt = 0
    for p, l, pa, f, t in rows:
        flag = "  ❌" if f else ""
        print(f"{p:<16}{l:<8}{pa:>6}{f:>6}{t:>7}{flag}")
        tp += pa; tf += f; tt += t
    print("-" * 43)
    print(f"{'TOTAL':<16}{'':<8}{tp:>6}{tf:>6}{tt:>7}")
    if show_time:
        total_s = sum(secs for _, _, sk, secs in results if not sk)
        print(f"\nTotal run time: {total_s:.2f}s")
    if failed:
        print(f"\n{tf} failure(s):")
        for lbl in failed:
            print(f"  ❌ {lbl}")
        return 1
    print("\nAll solutions passed! 🎉")
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("filters", nargs="*", help="path substrings to include")
    p.add_argument("--lang", action="append", default=[], help="restrict language: py|cpp|java|js|go|rust")
    p.add_argument("--platform", help="restrict to one platform")
    p.add_argument("--changed", action="store_true", help="only solutions changed vs git HEAD")
    p.add_argument("--time", action="store_true", help="print each solution's runtime")
    p.add_argument("--sort", default="platform", choices=["platform", "language", "status", "name"])
    p.add_argument("--stats", action="store_true", help="show inventory grouped by platform and exit")
    p.add_argument("-q", "--quiet", action="store_true", help="only print the summary")
    args = p.parse_args()

    langs = set()
    for l in args.lang:
        matched = [m["short"] for m in LANGUAGES.values() if l.lower() in m["aliases"]]
        if not matched:
            p.error(f"unknown --lang {l!r} (py, cpp, java, js, go, rust)")
        langs.add(matched[0])

    sols = [s for s in discover() if matches(s, args.filters, langs, args.platform)]

    if args.changed:
        cp = changed_paths()
        if cp is None:
            print("warning: could not read git changes; running all matched solutions")
        else:
            sols = [s for s in sols if s.label in cp]

    sols.sort(key=lambda s: (s.platform, s.short_lang, s.group, s.name))

    if not sols:
        if args.changed:
            # No changed solutions to run (e.g. a docs/config-only commit) — fine.
            print("No changed solutions to run.")
            return 0
        if args.filters or langs or args.platform:
            print("No solutions matched the given filters.")
            return 1
        print("No solutions yet — add one with:  python new.py <platform>/<name> --lang py")
        return 0

    if args.stats:
        print_stats(sols, args.sort)
        return 0

    build = Path(tempfile.mkdtemp(prefix="pst_build_"))
    results = []
    try:
        for sol in sols:
            passed, output, secs = execute(sol, build)
            icon = "✅" if passed else "❌"
            grp = f"{sol.group}/" if sol.group else ""
            tstr = f"  ({secs:.2f}s)" if args.time else ""
            print(f"{icon} [{sol.short_lang}] {sol.platform}/{grp}{sol.name}{tstr}")
            if not args.quiet and not passed:
                for line in output.strip().splitlines():
                    print(f"      {line}")
            results.append((sol, passed, False, secs))
    finally:
        shutil.rmtree(build, ignore_errors=True)

    return print_summary(results, args.sort, args.time)


if __name__ == "__main__":
    sys.exit(main())
