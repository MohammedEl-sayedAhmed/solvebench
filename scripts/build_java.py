#!/usr/bin/env python3
"""Compile every Java source (helper + solutions) into .pst/build/java.

Used as the F5 pre-launch task so debugging never depends on the VS Code Java
language server's project model (which can fall back to a syntax-only project
on fresh profiles and then fail with "TestFramework cannot be resolved").

A half-solved file must not break debugging a finished one: if the one-shot
batch compile fails, we evict every solution's stale classes and rebuild
file-by-file, skipping whatever doesn't compile (with its javac errors shown).
If every file compiles alone but the batch still fails, that's a cross-file
conflict (e.g. the same helper class declared in two files of one package) —
surfaced loudly instead of letting the last-compiled bytecode silently win.

    python3 scripts/build_java.py
"""
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
SRC = REPO / "java"
OUT = REPO / ".pst" / "build" / "java"

sources = sorted(SRC.rglob("*.java"))
if not sources:
    print("no java sources found")
    sys.exit(0)

OUT.mkdir(parents=True, exist_ok=True)
BASE = ["javac", "-g", "-encoding", "UTF-8", "-cp", str(SRC), "-d", str(OUT)]

# Top-level type declarations in a source file (class Foo, record Bar, ...) —
# used to evict their .class files, including package-private helpers that
# don't share the file's name.
TYPE_RE = re.compile(
    r"^\s*(?:@\w+\s+)?(?:public\s+|final\s+|abstract\s+|strictfp\s+|sealed\s+|non-sealed\s+)*"
    r"(?:class|interface|enum|record)\s+(\w+)", re.M)


def evict(source: pathlib.Path) -> None:
    """Remove the classes a source file produces (filename class, any other
    top-level types it declares, and their inner classes). No globbing, so
    odd characters in file names can't wipe unrelated classes."""
    rel = source.relative_to(SRC)
    names = set(TYPE_RE.findall(source.read_text(encoding="utf-8", errors="replace")))
    names.add(rel.stem)
    outdir = OUT / rel.parent
    if not outdir.is_dir():
        return
    for cls in outdir.iterdir():
        if cls.suffix == ".class" and cls.stem.split("$", 1)[0] in names:
            cls.unlink()


def run(cmd, **kw):
    try:
        return subprocess.run(cmd, **kw)
    except OSError as exc:  # e.g. argv over the platform limit
        print(f"javac failed to launch: {exc}", file=sys.stderr)
        return None


# Fast path: everything compiles in one javac call.
batch = run(BASE + [str(p) for p in sources], capture_output=True, text=True)
if batch is not None and batch.returncode == 0:
    print(f"compiled {len(sources)} java file(s) -> {OUT.relative_to(REPO)}")
    sys.exit(0)

# Slow path: some WIP file is broken. Shared helpers must compile — nothing
# builds without them — then each solution stands alone.
common = [p for p in sources if "common" in p.relative_to(SRC).parts]
rest = [p for p in sources if "common" not in p.relative_to(SRC).parts]
if common:
    proc = run(BASE + [str(p) for p in common])
    if proc is None or proc.returncode != 0:
        print("java/common/ doesn't compile — fix the shared helpers first", file=sys.stderr)
        sys.exit(1)

# Clear all solution classes first, then recompile: files that still compile
# regenerate theirs, broken ones leave nothing stale behind for F5 to run.
for p in rest:
    evict(p)
skipped = []
for p in rest:
    proc = run(BASE + [str(p)], capture_output=True, text=True)
    if proc is None or proc.returncode != 0:
        skipped.append((p.relative_to(REPO), proc.stderr if proc else ""))

if not skipped and batch is not None:
    print("cross-file conflict: every file compiles alone, but not together —\n"
          "likely the same helper class declared in two files of one package:",
          file=sys.stderr)
    sys.stderr.write(batch.stderr or "")
    sys.exit(1)

print(f"compiled {len(sources) - len(skipped)}/{len(sources)} java file(s) -> {OUT.relative_to(REPO)}")
for rel, err in skipped:
    print(f"  skipped (doesn't compile): {rel}")
    for line in (err or "").splitlines()[:8]:
        print(f"      {line}")
sys.exit(0)
