#!/usr/bin/env python3
"""Compile every Java source (helper + solutions) into .pst/build/java.

Used as the F5 pre-launch task so debugging never depends on the VS Code Java
language server's project model (which can fall back to a syntax-only project
on fresh profiles and then fail with "TestFramework cannot be resolved").

    python3 scripts/build_java.py
"""
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
OUT = REPO / ".pst" / "build" / "java"

sources = sorted(str(p) for p in (REPO / "java").rglob("*.java"))
if not sources:
    print("no java sources found")
    sys.exit(0)

OUT.mkdir(parents=True, exist_ok=True)
cmd = ["javac", "-g", "-encoding", "UTF-8", "-cp", str(REPO / "java"),
       "-d", str(OUT), *sources]
proc = subprocess.run(cmd)
if proc.returncode != 0:
    sys.exit(proc.returncode)
print(f"compiled {len(sources)} java file(s) -> {OUT.relative_to(REPO)}")
