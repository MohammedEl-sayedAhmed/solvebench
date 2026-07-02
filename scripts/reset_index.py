#!/usr/bin/env python3
"""Reset the README solutions index (between markers) to an empty placeholder.
Used by init.sh when starting from a clean slate.

    <!-- solutions:start -->
    ...tables...
    <!-- solutions:end -->
"""
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
placeholder = (
    "No solutions yet — add one and list it here:\n\n"
    "```bash\n"
    "./run.sh new leetcode/easy/two_sum --lang py\n"
    "```\n\n"
    "_Or skip the manual index and track progress with_ `python run.py --stats`."
)

path = REPO / "README.md"
readme = path.read_text()
new, n = re.subn(
    r"(?s)(<!-- solutions:start -->).*?(<!-- solutions:end -->)",
    lambda m: f"{m.group(1)}\n{placeholder}\n{m.group(2)}",
    readme,
)
if n == 0:
    sys.exit("error: solutions markers (<!-- solutions:start/end -->) not found in README.md")
path.write_text(new)
print("solutions index reset")
