#!/usr/bin/env python3
"""Check the JSON that run.py and complexity.py promise the VS Code extension.

The extension parses this output and hands the paths back as filters, so a
change to either shape silently breaks its test panel. Run it in CI:

    python scripts/check_json_contract.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FAILURES: list[str] = []


def check(condition: bool, message: str) -> None:
    if condition:
        print(f"  ok   {message}")
    else:
        print(f"  FAIL {message}")
        FAILURES.append(message)


def run(args: list[str], expect_code: int | None = 0) -> tuple[str, int]:
    proc = subprocess.run([sys.executable, *args], cwd=REPO, capture_output=True, text=True)
    if expect_code is not None and proc.returncode != expect_code:
        FAILURES.append(f"{' '.join(args)} exited {proc.returncode}, wanted {expect_code}")
        print(f"  FAIL {' '.join(args)} exited {proc.returncode}\n{proc.stderr}")
    return proc.stdout, proc.returncode


def main() -> int:
    print("run.py --stats --json")
    out, _ = run(["run.py", "--stats", "--json"])
    stats = json.loads(out)
    check(stats["schema"] == 1, "schema is 1")
    check(bool(stats["solutions"]), "solutions were discovered")
    check("summary" not in stats, "discovery carries no summary")

    paths = [s["path"] for s in stats["solutions"]]
    check(len(set(paths)) == len(paths), "paths are unique (they are test item ids)")
    check(all("\\" not in p for p in paths), "paths use forward slashes on every OS")
    fields = {"language", "lang", "platform", "group", "name", "path"}
    check(
        all(fields <= set(s) for s in stats["solutions"]),
        "every solution has the fields the tree needs",
    )

    # The count has to agree with what a person reads in the terminal.
    text, _ = run(["run.py", "--stats"])
    total_line = [ln for ln in text.splitlines() if ln.startswith("TOTAL")]
    check(bool(total_line), "text output has a TOTAL line")
    if total_line:
        check(
            int(total_line[0].split()[-1]) == len(paths),
            f"json count matches the text total ({len(paths)})",
        )

    # A reported path must select only itself, or running one test runs several.
    print("\npath round-trip")
    for path in paths[:8]:
        one, _ = run(["run.py", "--stats", "--json", path])
        selected = [s["path"] for s in json.loads(one)["solutions"]]
        check(selected == [path], f"{path} selects only itself")

    print("\nempty result")
    out, code = run(["run.py", "--stats", "--json", "definitely-not-a-solution"], expect_code=1)
    check(json.loads(out)["solutions"] == [], "no match is still valid JSON")
    check(code == 1, "no match exits 1, as the text output does")

    print("\ncomplexity.py --json")
    out, _ = run(
        ["complexity.py", "leetcode/easy/two_sum", "--json", "--sizes", "200,400,800,1600"]
    )
    cx = json.loads(out)
    check(cx["schema"] == 1, "schema is 1")
    check(len(cx["sizes"]) == len(cx["times"]), "one time per input size")
    check(cx["time_class"].startswith("O("), f"time class looks like a class ({cx['time_class']})")
    check("solution" in cx and "function" in cx, "carries the solution and function names")

    print()
    if FAILURES:
        print(f"{len(FAILURES)} contract failure(s)")
        return 1
    print("JSON contract holds")
    return 0


if __name__ == "__main__":
    sys.exit(main())
