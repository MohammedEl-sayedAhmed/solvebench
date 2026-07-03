#!/usr/bin/env python3
"""
Scaffold a new solution file — from a problem URL or an explicit path.

The easy way (paste the problem link):
    python new.py https://leetcode.com/problems/two-sum/ --lang java
    # LeetCode: auto-fetches the number, title, and difficulty, then creates
    #   java/leetcode/easy/TwoSum.java  with the title + URL filled in.

The explicit way:
    python new.py leetcode/easy/two_sum --lang py
    python new.py adventofcode/2023/1/trebuchet --lang cpp --url <link>

Options:
    --lang        py | cpp | java | js | go | rust      (required)
    --difficulty  easy | medium | hard   (override / needed if a fetch fails)
    --url --title override the auto-filled values

The file lands under the matching language dir; Java classes are PascalCased.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

REPO = Path(__file__).resolve().parent

LANGS = {
    "py": ("python", ".py", "templates/solution.py"),
    "python": ("python", ".py", "templates/solution.py"),
    "cpp": ("cpp", ".cpp", "templates/solution.cpp"),
    "c++": ("cpp", ".cpp", "templates/solution.cpp"),
    "java": ("java", ".java", "templates/Solution.java"),
    "js": ("javascript", ".js", "templates/solution.js"),
    "javascript": ("javascript", ".js", "templates/solution.js"),
    "node": ("javascript", ".js", "templates/solution.js"),
    "go": ("go", ".go", "templates/solution.go"),
    "golang": ("go", ".go", "templates/solution.go"),
    "rust": ("rust", ".rs", "templates/solution.rs"),
    "rs": ("rust", ".rs", "templates/solution.rs"),
}


def pascal_case(name: str) -> str:
    cc = "".join(part.capitalize() for part in re.split(r"[_\-\s]+", name) if part)
    # A Java identifier can't start with a digit (e.g. "3sum" -> "_3sum"), so
    # prefix an underscore; keeps the class name valid and the file name in sync.
    if cc and cc[0].isdigit():
        cc = "_" + cc
    return cc


def title_from_slug(slug: str) -> str:
    return " ".join(w.capitalize() for w in re.split(r"[-_]+", slug) if w)


def fetch_leetcode(slug: str):
    """Return {id, title, difficulty} from LeetCode's GraphQL API, or None."""
    query = {
        "query": "query q($t:String!){question(titleSlug:$t){questionFrontendId title difficulty}}",
        "variables": {"t": slug},
    }
    req = urllib.request.Request(
        "https://leetcode.com/graphql",
        data=json.dumps(query).encode(),
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://leetcode.com",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            q = (json.load(resp).get("data") or {}).get("question")
        if not q:
            return None
        return {"id": q["questionFrontendId"], "title": q["title"], "difficulty": q["difficulty"].lower()}
    except Exception:
        return None


def resolve_url(url: str, difficulty: str | None):
    """Map a problem URL -> (repo_path, title, url). May hit the network."""
    host = urlparse(url).netloc.lower()
    parts = [p for p in urlparse(url).path.split("/") if p]

    if "leetcode.com" in host:
        slug = parts[parts.index("problems") + 1] if "problems" in parts else (parts[-1] if parts else "")
        if not slug:
            sys.exit("could not find a problem slug in that LeetCode URL")
        meta = fetch_leetcode(slug)
        if meta:
            diff = difficulty or meta["difficulty"]
            title = f"{meta['id']}. {meta['title']}"
        else:
            if not difficulty:
                sys.exit("couldn't reach LeetCode — re-run with --difficulty easy|medium|hard")
            diff = difficulty
            title = title_from_slug(slug)
        return f"leetcode/{diff}/{slug.replace('-', '_')}", title, url

    if "codewars.com" in host:
        slug = parts[-1]
        return f"codewars/{slug.replace('-', '_')}", title_from_slug(slug), url

    if "hackerrank.com" in host:
        slug = parts[-1]
        sub = f"{difficulty}/" if difficulty else ""
        return f"hackerrank/{sub}{slug.replace('-', '_')}", title_from_slug(slug), url

    if "codeforces.com" in host:
        name = "".join(parts[-2:]).lower() if len(parts) >= 2 else (parts[-1] if parts else "problem")
        return f"codeforces/{name}", f"Codeforces {'/'.join(parts[-2:])}", url

    if "adventofcode.com" in host:
        year = parts[0] if parts else "0000"
        day = parts[parts.index("day") + 1] if "day" in parts else "0"
        return f"adventofcode/{year}/{day}/day{day}", f"Advent of Code {year} Day {day}", url

    sys.exit(f"don't know how to map that URL's host ({host}); use an explicit path instead")


def is_url(s: str) -> bool:
    return s.startswith(("http://", "https://"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("target", help="a problem URL, or platform/group/name")
    parser.add_argument("--lang", required=True, help="py | cpp | java | js | go | rust")
    parser.add_argument("--difficulty", "-d", default="", help="easy|medium|hard (override / fetch fallback)")
    parser.add_argument("--url", default="", help="problem URL (fills the template)")
    parser.add_argument("--title", default="", help="problem title (fills the template)")
    args = parser.parse_args()

    lang = args.lang.lower()
    if lang not in LANGS:
        parser.error(f"unknown --lang {args.lang!r} (py, cpp, java, js, go, rust)")
    lang_dir, ext, template_rel = LANGS[lang]

    # Resolve where the file goes + its title/url — from a URL or an explicit path.
    if is_url(args.target):
        path_str, title, url = resolve_url(args.target, args.difficulty or None)
        title = args.title or title
        url = args.url or url
    else:
        path_str, title, url = args.target, args.title, args.url

    rel = Path(path_str)
    parent = rel.parent
    stem = rel.name

    if lang_dir == "java":
        class_name = pascal_case(stem)
        target = REPO / lang_dir / parent / f"{class_name}{ext}"
    else:
        class_name = None
        target = REPO / lang_dir / parent / f"{stem}{ext}"

    if target.exists():
        print(f"Refusing to overwrite existing file: {target.relative_to(REPO)}")
        return 1

    content = (REPO / template_rel).read_text()
    if title:
        content = content.replace("<Problem Title>", title)
    if url:
        content = content.replace("<url>", url)
    if class_name:  # Java: rename the class and set the package from the path
        content = re.sub(r"\bSolution\b", class_name, content)
        package = ".".join(parent.parts)
        if package:
            content = content.replace("PACKAGE_NAME", package)
        else:
            content = re.sub(r"^package .*;\n\n?", "", content, flags=re.M)

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    rel_path = target.relative_to(REPO)
    print(f"Created {rel_path}")
    print(f"Run it with:  python run.py {path_str}   (or ./run.sh {path_str})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
