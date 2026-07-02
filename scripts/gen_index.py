#!/usr/bin/env python3
"""Regenerate the README solutions index from the files on disk, between
<!-- solutions:start --> and <!-- solutions:end -->.

Reads each solution's header for a title line and a problem URL, and groups the
same problem across languages by a normalized name. Optional — running it
REPLACES any hand-written notes in that section, so it's a convenience for
forks that prefer an auto-maintained index.

    python scripts/gen_index.py
"""
import pathlib
import re
import sys
from collections import defaultdict

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
import run  # noqa: E402

URL_RE = re.compile(r"https?://[^\s)\"']+")
PRETTY = {
    "leetcode": "LeetCode", "codewars": "Codewars", "adventofcode": "Advent of Code",
    "hackerrank": "HackerRank", "codeforces": "Codeforces", "others": "Others",
}
SKIP_PREFIXES = ("import", "from ", "package", "#include", "const ", "use ",
                 "fn ", "func ", "public", "class ", "def ", "let ", "var ", "//go")


def parse_header(path):
    title, url = "", ""
    for i, raw in enumerate(path.read_text(errors="ignore").splitlines()):
        if i > 40:
            break
        if not url:
            m = URL_RE.search(raw)
            if m:
                url = m.group(0).rstrip(').,"\'')
        s = raw.strip().lstrip('"').lstrip("/").lstrip("#").lstrip("*").strip()
        if not title and s and "http" not in s and not s.lower().startswith(SKIP_PREFIXES):
            title = s
    return title, url


def norm(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())


problems = {}
for s in run.discover():
    key = (s.platform, norm(s.name))
    p = problems.setdefault(key, {"langs": {}, "title": "", "url": "",
                                  "platform": s.platform, "group": s.group})
    p["langs"][s.short_lang] = s.label
    title, url = parse_header(s.path)
    if title and not p["title"]:
        p["title"] = title
    if url and not p["url"]:
        p["url"] = url

by_platform = defaultdict(list)
for p in problems.values():
    by_platform[p["platform"]].append(p)

out = []
for platform in sorted(by_platform):
    out.append(f"##### {PRETTY.get(platform, platform)}\n")
    out.append("| Problem | Difficulty | Solutions |")
    out.append("| ------- | ---------- | --------- |")
    for p in sorted(by_platform[platform], key=lambda x: (x["title"] or "").lower()):
        title = p["title"] or "(untitled)"
        link = f"[{title}]({p['url']})" if p["url"] else title
        diff = p["group"].split("/")[0] if p["group"] else "—"
        langs = " · ".join(f"[{lang}]({path})" for lang, path in sorted(p["langs"].items()))
        out.append(f"| {link} | {diff} | {langs} |")
    out.append("")

block = "\n".join(out).strip() if problems else "No solutions yet."
readme = REPO / "README.md"
text = readme.read_text()
new, n = re.subn(r"(?s)(<!-- solutions:start -->).*?(<!-- solutions:end -->)",
                 lambda m: f"{m.group(1)}\n{block}\n{m.group(2)}", text)
if n == 0:
    sys.exit("error: solutions markers (<!-- solutions:start/end -->) not found in README.md")
readme.write_text(new)
print(f"solutions index regenerated ({len(problems)} problems across {len(by_platform)} platforms)")
