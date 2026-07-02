#!/usr/bin/env python3
"""Regenerate the README profile block from profile.json (the single source of
truth for identity). Fills the region between the markers:

    <!-- profile:start -->
    ...generated...
    <!-- profile:end -->

Run after editing profile.json:  python scripts/apply_profile.py
"""
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
prof = json.loads((REPO / "profile.json").read_text())


def h(key):
    return str(prof.get(key) or "").strip()


lines = [f"- **{h('name') or 'Your Name'}**"]
links = [
    ("GitHub", "github", "https://github.com/{}"),
    ("LeetCode", "leetcode", "https://leetcode.com/u/{}/"),
    ("Codewars", "codewars", "https://www.codewars.com/users/{}"),
    ("HackerRank", "hackerrank", "https://www.hackerrank.com/{}"),
    ("Codeforces", "codeforces", "https://codeforces.com/profile/{}"),
]
for label, key, url in links:
    if h(key):
        lines.append(f"- {label}: [@{h(key)}]({url.format(h(key))})")

block = "\n".join(lines)
if h("leetcode"):
    block += (
        "\n\n![LeetCode Stats](https://leetcard.jacoblin.cool/"
        f"{h('leetcode')}?theme=nord&font=Chakra%20Petch&animation=true&ext=activity)"
    )

path = REPO / "README.md"
readme = path.read_text()
new, n = re.subn(
    r"(?s)(<!-- profile:start -->).*?(<!-- profile:end -->)",
    lambda m: f"{m.group(1)}\n{block}\n{m.group(2)}",
    readme,
)
if n == 0:
    sys.exit("error: profile markers (<!-- profile:start/end -->) not found in README.md")
path.write_text(new)
print("README profile block updated from profile.json")
