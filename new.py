#!/usr/bin/env python3
"""
Scaffold a new solution file from a language template.

Usage
-----
    python new.py <platform>/<group...>/<name> --lang py|cpp|java [--url URL] [--title TITLE]

Examples
--------
    python new.py leetcode/easy/valid_anagram --lang py
    python new.py leetcode/easy/valid_anagram --lang cpp  --url https://leetcode.com/problems/valid-anagram/
    python new.py adventofcode/2023/1/trebuchet --lang java

The path is language-agnostic; the file lands under the matching language dir:
    py   -> python/<path>.py
    cpp  -> cpp/<path>.cpp
    java -> java/<dir>/<PascalName>.java   (class name matches the file name)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent

LANGS = {
    "py": ("python", ".py", "templates/solution.py"),
    "python": ("python", ".py", "templates/solution.py"),
    "cpp": ("cpp", ".cpp", "templates/solution.cpp"),
    "c++": ("cpp", ".cpp", "templates/solution.cpp"),
    "java": ("java", ".java", "templates/Solution.java"),
}


def pascal_case(name: str) -> str:
    return "".join(part.capitalize() for part in re.split(r"[_\-\s]+", name) if part)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("path", help="platform/group/name, e.g. leetcode/easy/two_sum")
    parser.add_argument("--lang", required=True, help="py | cpp | java")
    parser.add_argument("--url", default="", help="problem URL (fills the template)")
    parser.add_argument("--title", default="", help="problem title (fills the template)")
    args = parser.parse_args()

    lang = args.lang.lower()
    if lang not in LANGS:
        parser.error(f"unknown --lang {args.lang!r} (choose from py, cpp, java)")
    lang_dir, ext, template_rel = LANGS[lang]

    rel = Path(args.path)
    parent = rel.parent  # platform/group...
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

    template = (REPO / template_rel).read_text()
    content = template
    if args.title:
        content = content.replace("<Problem Title>", args.title)
    if args.url:
        content = content.replace("<url>", args.url)
    if class_name:  # Java: rename the class and set the package from the path
        content = re.sub(r"\bSolution\b", class_name, content)
        package = ".".join(parent.parts)
        if package:
            content = content.replace("PACKAGE_NAME", package)
        else:  # solution directly under java/ -> default package
            content = re.sub(r"^package .*;\n\n?", "", content, flags=re.M)

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    print(f"Created {target.relative_to(REPO)}")
    print(f"Run it with:  python run.py {args.path}   (or ./run.sh {args.path})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
