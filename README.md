# Problem Solving Training

[![tests](https://github.com/MohammedEl-sayedAhmed/problem-solving-training/actions/workflows/ci.yml/badge.svg)](https://github.com/MohammedEl-sayedAhmed/problem-solving-training/actions/workflows/ci.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![stars](https://img.shields.io/github/stars/MohammedEl-sayedAhmed/problem-solving-training?style=social)](https://github.com/MohammedEl-sayedAhmed/problem-solving-training/stargazers)
[![forks](https://img.shields.io/github/forks/MohammedEl-sayedAhmed/problem-solving-training?style=social)](https://github.com/MohammedEl-sayedAhmed/problem-solving-training/network/members)

My solutions to programming problems from LeetCode, Codewars, Advent of Code, and
other platforms — solvable in **multiple languages** and runnable **anywhere** via
a single containerized test runner (no local toolchain required).

> **Want your own?** ⭐ Star it, then **Fork** — it doubles as a ready-made
> polyglot practice framework. After forking, run `./init.sh` to make it yours
> (see [Fork & make it yours](#fork--make-it-yours)).

## Highlights

- 🌐 **Polyglot** — solve the same problem in Python, C++, Java, JavaScript, Go,
  or Rust. Each language has a tiny test helper so solutions self-verify.
- 🧪 **One runner** — `run.py` discovers every solution, runs it, and reports
  pass/fail grouped by **platform** (sortable). Wrong answers fail loudly.
- 🐳 **Containerized** — `./run.sh` (or `.\run.ps1` on Windows) runs everything
  inside Docker, so you don't need Python/g++/JDK installed.
- 🪟🐧 **Cross-platform** — works on Ubuntu, KDE/other Linux, macOS, and Windows.
- 🏗️ **Scaffolder** — `new.py` starts a new solution in any language from a template.

## Progress

<!-- stats:start -->
![adventofcode](https://img.shields.io/badge/adventofcode-6%20solved-brightgreen) ![codewars](https://img.shields.io/badge/codewars-7%20solved-red) ![leetcode](https://img.shields.io/badge/leetcode-20%20solved-orange) ![others](https://img.shields.io/badge/others-1%20solved-lightgrey)

34 solutions · 4 platforms · 2 languages

| Platform | java | py | Total |
| --- | --- | --- | --- |
| adventofcode | 0 | 6 | 6 |
| codewars | 0 | 7 | 7 |
| leetcode | 4 | 16 | 20 |
| others | 0 | 1 | 1 |
| **Total** | 4 | 30 | **34** |
<!-- stats:end -->

## Demo

▶ **[Live animated demo](docs/demo.html)** — watch the one runner drive every
language (open `docs/demo.html`, or serve it via GitHub Pages). Regenerate the
recording locally with `./scripts/record_demo.sh` (asciinema → GIF).

## Fork & make it yours

⭐ **Star** the repo, then **Fork** it (forking keeps it linked in the network
graph — that's the point). After cloning your fork:

```bash
./init.sh     # clean slate: clears the example solutions/inputs, sets your handles,
              # resets the solutions index, and (optionally) starts fresh git history
./setup.sh    # optional: repo-local VS Code extensions + venv
./run.sh new leetcode/easy/two_sum --lang py
```

`init.sh` keeps the whole framework (runner, helpers, templates, CI, setup) and
only removes the example solutions. Your profile links live in
[profile.json](profile.json) — edit it and run `python scripts/apply_profile.py`
to refresh the README. PRs that improve the framework are welcome.

## Structure

Language first, then platform, then the platform's own grouping (difficulty, year/day, …):

```
.
├── python/                 # Python solutions
│   ├── common/             #   shared helpers (run_tests, aoc.input_path)
│   ├── leetcode/{easy,medium,hard}/
│   ├── codewars/
│   ├── adventofcode/<year>/<day>/
│   └── others/
├── cpp/                    # C++ solutions (mirror the same platform tree)
│   └── common/             #   test_framework.hpp
├── java/                   # Java solutions
│   └── common/             #   TestFramework.java
├── inputs/                 # shared, language-agnostic puzzle inputs
│   └── adventofcode/<year>/<day>/input.txt
├── templates/              # starter templates per language
├── run.py                  # polyglot test runner
├── new.py                  # scaffolder for new solutions
├── setup.sh / setup.ps1    # interactive, repo-local setup (extensions, venv)
├── code.sh / code.ps1      # launch VS Code scoped to this repo (uses .pst/)
├── teardown.sh / teardown.ps1   # remove everything setup created
├── ship.sh / ship.ps1      # refresh README refs, then commit & push
├── run.sh / run.ps1 / run.cmd   # containerized wrappers (Linux·macOS / Windows)
└── Dockerfile              # toolchain image (Python, g++, JDK, Node, Go, Rust)
```

Setup artifacts (`.pst/`, `.venv/`) stay inside the repo and are git-ignored.

New platforms (e.g. `hackerrank/`) or languages just follow the same convention.

Puzzle inputs (Advent of Code) live in `inputs/`, **outside** the language trees,
so the same input is reused across languages. Solutions resolve them via a helper
(Python: `from common.aoc import input_path`) rather than a path relative to the
solution file.

## Commands

Everything lives in the repo root so the commands stay short. On Windows use the
`.ps1` equivalent (e.g. `.\run.ps1`, `.\ship.ps1`).

| Command | What it does |
| ------- | ------------ |
| `./run.sh [filter]` | Run solutions (uses a container on the host; native inside the Dev Container) |
| `./run.sh new <url\|path> --lang X` | Scaffold a solution — a LeetCode URL auto-fetches number/title/difficulty |
| `./run.sh --stats` · `--changed` · `--time` | Inventory by platform · only git-changed · with timings |
| `./setup.sh` | Interactive one-time setup (repo-local VS Code extensions, venv) |
| `./code.sh` | Open VS Code scoped to this repo (uses `.pst/`) |
| `./ship.sh "msg"` | Refresh README stats, then commit & push |
| `./teardown.sh` | Remove setup artifacts (`.pst/`, `.venv/`, the image) |
| `./init.sh` | Fork clean-slate: clear examples, set your handles |
| `python python/common/complexity.py` | Estimate a solution's time/space complexity |

## Quick start

### First-time setup (optional)

`./setup.sh` (or `.\setup.ps1` on Windows) is an interactive installer for the
recommended VS Code extensions (Python, C/C++, Java debugger) and optional dev
deps.

**Self-contained & reversible** — setup never touches your machine's global
config. Everything it creates stays inside the repo:

| Artifact | Location | Notes |
| -------- | -------- | ----- |
| VS Code extensions | `./.pst/extensions` | repo-local, not your global VS Code |
| pytest (optional) | `./.venv` | a local virtualenv (PEP 668 safe) |
| container image | docker daemon | `pst-runner`; the only out-of-repo item |

- **Edit with the repo-scoped editor:** `./code.sh` (or `.\code.ps1`) launches
  VS Code using the repo-local extensions/profile under `.pst/`. Debug any open
  solution with **F5** — configs are in [.vscode/launch.json](.vscode/launch.json).
- **Remove everything:** `./teardown.sh` (or `.\teardown.ps1`) deletes `.pst/`,
  `.venv/`, caches/build files, and optionally the `pst-runner` image.

### Run in a container (recommended — no local tools needed)

```bash
./run.sh                        # run every solution, all languages
./run.sh leetcode/easy/two_sum  # run one problem across every language it's solved in
./run.sh --platform codewars    # only Codewars
./run.sh --lang py --lang cpp   # only these languages
./run.sh --stats                # inventory grouped by platform (no runs)
```

On **Windows** use the PowerShell wrapper (or `run.cmd` from `cmd`):

```powershell
.\run.ps1                        # or:  run.cmd
.\run.ps1 leetcode/easy/two_sum
```

The first invocation builds the `pst-runner` image once; later runs reuse it.
Works with Docker or Podman.

Inside the **Dev Container** (or any container) `./run.sh` detects it and runs
natively — no `PST_NATIVE` needed. With no engine installed it also falls back
to native automatically.

### Run natively (if you have the toolchains)

```bash
python run.py                    # same flags as ./run.sh
PST_NATIVE=1 ./run.sh --stats    # force the wrapper to skip the container
.venv/bin/pytest                 # optional; create the venv with ./setup.sh
```

### Sorting / tracking by platform

```bash
python run.py --stats                 # counts per platform × language
python run.py --sort platform         # summary grouped by platform (default)
python run.py --sort status           # failures first
python run.py --sort language         # group by language
```

## Adding a new solution

**From a problem link (easiest).** Paste the URL and pick a language — for
LeetCode the number, title, and difficulty are fetched automatically and the
file lands in the right folder:

```bash
./run.sh new https://leetcode.com/problems/two-sum/ --lang java
#  → java/leetcode/easy/TwoSum.java, titled "1. Two Sum", URL filled in
```

Codewars / HackerRank / Codeforces / Advent of Code links work too; add
`--difficulty easy|medium|hard` if a site doesn't expose it.

**Or give an explicit path:**

```bash
./run.sh new leetcode/easy/valid_anagram --lang py
```

Fill in the solution + example tests, run it, then ship:

```bash
./run.sh leetcode/easy/two_sum      # runs every language you solved it in
./ship.sh "feat: two sum"           # refresh README stats, commit & push
```

### How a solution self-tests

Each language ships a minimal helper that prints ✅/❌ per case and exits non-zero
if any case fails (this is what the runner keys on):

| Language | Helper | Pattern |
| -------- | ------ | ------- |
| Python | [python/common/test_framework.py](python/common/test_framework.py) | `run_tests([(fn, args, expected, "name"), …])` |
| C++ | [cpp/common/test_framework.hpp](cpp/common/test_framework.hpp) | `tf::TestRunner t; t.check("name", got, expected); return t.summary();` |
| Java | [java/common/TestFramework.java](java/common/TestFramework.java) | `TestFramework t = new TestFramework(); t.check(...); System.exit(t.summary());` |

### Estimate complexity

Empirically check how a Python solution scales — it measures runtime and peak
memory across growing inputs and fits the growth to a Big-O class:

```python
from common.complexity import estimate
# make_input(n) returns the argument list for input size n
estimate(Solution().majorityElement, make_input=lambda n: [list(range(n))])
#  ->  time ≈ O(n) · space ≈ O(1)
```

See it live on known cases: `python python/common/complexity.py`.

## Solutions

<!-- solutions:start -->
##### Advent of Code

| Problem | Difficulty | Solutions |
| ------- | ---------- | --------- |
| [Advent of Code - Day 10: Syntax Scoring](https://adventofcode.com/2021/day/10) | 2021 | [py](python/adventofcode/2021/10/syntax_scoring.py) |
| [Advent of Code - Day 11: Dumbo Octopus](https://adventofcode.com/2021/day/11) | 2021 | [py](python/adventofcode/2021/11/dumbo_octopus.py) |
| [Advent of Code - Day 14: Extended Polymerization](https://adventofcode.com/2021/day/14) | 2021 | [py](python/adventofcode/2021/14/extended_polymerization.py) |
| [Advent of Code - Day 14: Regolith Reservoir](https://adventofcode.com/2022/day/14) | 2022 | [py](python/adventofcode/2022/14/regolith_reservoir.py) |
| [Advent of Code - Day 24: Blizzard Basin](https://adventofcode.com/2022/day/24) | 2022 | [py](python/adventofcode/2022/24/blizzard_basin.py) |
| [Advent of Code - Day 7: No Space Left On Device](https://adventofcode.com/2022/day/7) | 2022 | [py](python/adventofcode/2022/7/no_space_left_on_device.py) |

##### Codewars

| Problem | Difficulty | Solutions |
| ------- | ---------- | --------- |
| [Count IP Addresses](https://www.codewars.com/kata/count-ip-addresses) | — | [py](python/codewars/count_ip_addresses.py) |
| [Flatten](https://www.codewars.com/kata/flatten) | — | [py](python/codewars/flatten.py) |
| [Give me a Diamond](https://www.codewars.com/kata/give-me-a-diamond) | — | [py](python/codewars/give_me_diamond.py) |
| [Luck Check](https://www.codewars.com/kata/luck-check) | — | [py](python/codewars/luck_check.py) |
| [Pete, the Baker](https://www.codewars.com/kata/pete-the-baker) | — | [py](python/codewars/pete_the_baker.py) |
| [Weight for Weight](https://www.codewars.com/kata/weight-for-weight) | — | [py](python/codewars/weight_for_weight.py) |
| [Your Order, Please](https://www.codewars.com/kata/your-order-please) | — | [py](python/codewars/your_order_please.py) |

##### LeetCode

| Problem | Difficulty | Solutions |
| ------- | ---------- | --------- |
| [1. Two Sum](https://leetcode.com/problems/two-sum/) | easy | [java](java/leetcode/easy/TwoSum.java) · [py](python/leetcode/easy/two_sum.py) |
| [11. Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | medium | [py](python/leetcode/medium/container_with_most_water.py) |
| [1177. Can Make Palindrome from Substring](https://leetcode.com/problems/can-make-palindrome-from-substring/) | medium | [py](python/leetcode/medium/can_make_palindrome_from_substring.py) |
| [125. Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | easy | [java](java/leetcode/easy/ValidPalindrome.java) · [py](python/leetcode/easy/valid_palindrome.py) |
| [15. 3Sum](https://leetcode.com/problems/3sum/) | medium | [py](python/leetcode/medium/three_sum.py) |
| [150. Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) | medium | [py](python/leetcode/medium/reverse_polish_notation.py) |
| [155. Min Stack](https://leetcode.com/problems/min-stack/) | medium | [py](python/leetcode/medium/min_stack.py) |
| [167. Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | medium | [py](python/leetcode/medium/two_sum_ii.py) |
| [169. Majority Element](https://leetcode.com/problems/majority-element/) | easy | [py](python/leetcode/easy/majority_element.py) |
| [20. Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | easy | [py](python/leetcode/easy/valid_parentheses.py) |
| [35. Search Insert Position](https://leetcode.com/problems/search-insert-position/) | easy | [py](python/leetcode/easy/search_insert_position.py) |
| [392. Is Subsequence](https://leetcode.com/problems/is-subsequence/) | easy | [py](python/leetcode/easy/is_subsequence.py) |
| [412. Fizz Buzz](https://leetcode.com/problems/fizz-buzz/) | easy | [java](java/leetcode/easy/FizzBuzz.java) · [py](python/leetcode/easy/fizz_buzz.py) |
| [66. Plus One](https://leetcode.com/problems/plus-one/) | easy | [py](python/leetcode/easy/plus_one.py) |
| [88. Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) | easy | [py](python/leetcode/easy/merge_sorted_array.py) |
| [888. Fair Candy Swap](https://leetcode.com/problems/fair-candy-swap/) | easy | [py](python/leetcode/easy/fair_candy_swap.py) |
| [9. Palindrome Number](https://leetcode.com/problems/palindrome-number/) | easy | [java](java/leetcode/easy/PalindromeNumber.java) |

##### Others

| Problem | Difficulty | Solutions |
| ------- | ---------- | --------- |
| [Rectangle Partition Problem                        #](https://www.codingame.com/ide/puzzle/rectangle-partition) | — | [py](python/others/rectangle_partition.py) |
<!-- solutions:end -->

## License

Licensed under the MIT License — see [LICENSE](LICENSE).

## Profiles

<!-- profile:start -->
- **Mohammed El-sayed Ahmed**
- GitHub: [@MohammedEl-sayedAhmed](https://github.com/MohammedEl-sayedAhmed)
- LeetCode: [@MohammedElsayed](https://leetcode.com/u/MohammedElsayed/)

![LeetCode Stats](https://leetcard.jacoblin.cool/MohammedElsayed?theme=nord&font=Chakra%20Petch&animation=true&ext=activity)
<!-- profile:end -->

> Generated from [profile.json](profile.json) — edit it and run `python scripts/apply_profile.py`.

---

⭐ Star this repository if you find it helpful!
