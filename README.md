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

- 🌐 **Polyglot** — solve the same problem in Python, C++, or Java. Each language
  has a tiny shared test helper so solutions self-verify.
- 🧪 **One runner** — `run.py` discovers every solution, runs it, and reports
  pass/fail grouped by **platform** (sortable). Wrong answers fail loudly.
- 🐳 **Containerized** — `./run.sh` (or `.\run.ps1` on Windows) runs everything
  inside Docker, so you don't need Python/g++/JDK installed.
- 🪟🐧 **Cross-platform** — works on Ubuntu, KDE/other Linux, macOS, and Windows.
- 🏗️ **Scaffolder** — `new.py` starts a new solution in any language from a template.

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
├── run.sh / run.ps1 / run.cmd   # containerized wrappers (Linux·macOS / Windows)
└── Dockerfile              # toolchain image (Python + g++ + JDK)
```

Setup artifacts (`.pst/`, `.venv/`) stay inside the repo and are git-ignored.

New platforms (e.g. `hackerrank/`) or languages just follow the same convention.

Puzzle inputs (Advent of Code) live in `inputs/`, **outside** the language trees,
so the same input is reused across languages. Solutions resolve them via a helper
(Python: `from common.aoc import input_path`) rather than a path relative to the
solution file.

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

```bash
./run.sh new leetcode/easy/valid_anagram --lang py
./run.sh new leetcode/easy/valid_anagram --lang cpp  --url https://leetcode.com/problems/valid-anagram/
./run.sh new leetcode/easy/valid_anagram --lang java --title "Valid Anagram"
```

This creates the file under the right language directory (Java files/classes are
auto-named in PascalCase). Fill in the solution and its example test cases, then:

```bash
./run.sh leetcode/easy/valid_anagram
```

### How a solution self-tests

Each language ships a minimal helper that prints ✅/❌ per case and exits non-zero
if any case fails (this is what the runner keys on):

| Language | Helper | Pattern |
| -------- | ------ | ------- |
| Python | [python/common/test_framework.py](python/common/test_framework.py) | `run_tests([(fn, args, expected, "name"), …])` |
| C++ | [cpp/common/test_framework.hpp](cpp/common/test_framework.hpp) | `tf::TestRunner t; t.check("name", got, expected); return t.summary();` |
| Java | [java/common/TestFramework.java](java/common/TestFramework.java) | `TestFramework t = new TestFramework(); t.check(...); System.exit(t.summary());` |

## Solutions

<!-- solutions:start -->

##### LeetCode &nbsp;·&nbsp; profile: [@MohammedElsayed](https://leetcode.com/u/MohammedElsayed/)

| #    | Title                                                                                                   | Solution                                                              | Difficulty | Notes                                                                                                      |
| ---- | ------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | ---------- | ---------------------------------------------------------------------------------------------------------- |
| 1    | [Two Sum](https://leetcode.com/problems/two-sum/)                                                       | [Python](python/leetcode/easy/two_sum.py) · [Java](java/leetcode/easy/TwoSum.java) | Easy       | Hash map approach                                                                                          |
| 11   | [Container With Most Water](https://leetcode.com/problems/container-with-most-water/)                   | [Python](python/leetcode/medium/container_with_most_water.py)         | Medium     | Two-pointer approach                                                                                       |
| 15   | [3Sum](https://leetcode.com/problems/3sum/)                                                             | [Python](python/leetcode/medium/three_sum.py)                         | Medium     | Two-pointer approach with sorting                                                                          |
| 20   | [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/)                                   | [Python](python/leetcode/easy/valid_parentheses.py)                   | Easy       | Stack approach                                                                                             |
| 35   | [Search Insert Position](https://leetcode.com/problems/search-insert-position/)                         | [Python](python/leetcode/easy/search_insert_position.py)              | Easy       | Binary search approach                                                                                     |
| 66   | [Plus One](https://leetcode.com/problems/plus-one/)                                                     | [Python](python/leetcode/easy/plus_one.py)                            | Easy       | Str and Int conversions in lists                                                                           |
| 88   | [Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/)                                 | [Python](python/leetcode/easy/merge_sorted_array.py)                  | Easy       | Merge in reverse order using 3 pointer counters                                                            |
| 125  | [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/)                                     | [Python](python/leetcode/easy/valid_palindrome.py) · [Java](java/leetcode/easy/ValidPalindrome.java) | Easy       | Two-pointer or string reverse approach                                                                     |
| 150  | [Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/)     | [Python](python/leetcode/medium/reverse_polish_notation.py)           | Medium     | Stack; use int() to truncate division towards zero                                                        |
| 155  | [Min Stack](https://leetcode.com/problems/min-stack/)                                                   | [Python](python/leetcode/medium/min_stack.py)                         | Medium     | Extra stack to track the min value for each index                                                          |
| 167  | [Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)                           | [Python](python/leetcode/medium/two_sum_ii.py)                        | Medium     | Two-pointer approach with sorted array                                                                     |
| 169  | [Majority Element](https://leetcode.com/problems/majority-element/)                                     | [Python](python/leetcode/easy/majority_element.py)                    | Easy       | Boyer-Moore Voting Algorithm                                                                               |
| 392  | [Is Subsequence](https://leetcode.com/problems/is-subsequence/)                                         | [Python](python/leetcode/easy/is_subsequence.py)                      | Easy       | Two-pointer approach                                                                                       |
| 412  | [Fizz Buzz](https://leetcode.com/problems/fizz-buzz/)                                                   | [Python](python/leetcode/easy/fizz_buzz.py) · [Java](java/leetcode/easy/FizzBuzz.java) | Easy       | String array based on divisibility                                                                         |
| 888  | [Fair Candy Swap](https://leetcode.com/problems/fair-candy-swap/)                                       | [Python](python/leetcode/easy/fair_candy_swap.py)                     | Easy       | Exchange candy boxes to equalize totals                                                                    |
| 1177 | [Can Make Palindrome from Substring](https://leetcode.com/problems/can-make-palindrome-from-substring/) | [Python](python/leetcode/medium/can_make_palindrome_from_substring.py)| Medium     | Frequency count via prefix sums                                                                            |

##### Codewars

| # | Title                                                                  | Solution                                        | Difficulty | Notes                                                                                                    |
| - | ---------------------------------------------------------------------- | ----------------------------------------------- | ---------- | -------------------------------------------------------------------------------------------------------- |
| 1 | [Weight for Weight](https://www.codewars.com/kata/weight-for-weight)   | [Python](python/codewars/weight_for_weight.py)  | 5 kyu      | Sort by digit-sum using a lambda key                                                                     |
| 2 | [Pete, the Baker](https://www.codewars.com/kata/pete-the-baker)        | [Python](python/codewars/pete_the_baker.py)     | 5 kyu      | Greedy: max cakes bounded by the limiting ingredient                                                     |
| 3 | [Count IP Addresses](https://www.codewars.com/kata/count-ip-addresses) | [Python](python/codewars/count_ip_addresses.py) | 5 kyu      | Convert IPs to integers and subtract                                                                     |
| 4 | [Flatten](https://www.codewars.com/kata/flatten)                       | [Python](python/codewars/flatten.py)            | 5 kyu      | Recursively flatten nested lists                                                                         |
| 5 | [Your Order, Please](https://www.codewars.com/kata/your-order-please)  | [Python](python/codewars/your_order_please.py)  | 6 kyu      | Sort words by the embedded digit                                                                         |
| 6 | [Luck Check](https://www.codewars.com/kata/luck-check)                 | [Python](python/codewars/luck_check.py)         | 5 kyu      | Compare left/right digit-sum halves, with input validation                                               |
| 7 | [Give me a Diamond](https://www.codewars.com/kata/give-me-a-diamond)   | [Python](python/codewars/give_me_diamond.py)    | 6 kyu      | Build a diamond string from asterisks                                                                    |

##### Advent of Code

| Year | Day | Title                                                              | Solution                                                          | Notes                                                                                     |
| ---- | --- | ------------------------------------------------------------------ | ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| 2021 | 10  | [Syntax Scoring](https://adventofcode.com/2021/day/10)             | [Python](python/adventofcode/2021/10/syntax_scoring.py)           | Syntax-error score for corrupted lines using a stack                                      |
| 2021 | 11  | [Dumbo Octopus](https://adventofcode.com/2021/day/11)              | [Python](python/adventofcode/2021/11/dumbo_octopus.py)            | Simulate energy levels and flashes on a 2D grid with recursion                            |
| 2021 | 14  | [Extended Polymerization](https://adventofcode.com/2021/day/14)    | [Python](python/adventofcode/2021/14/extended_polymerization.py)  | Pair insertion via `defaultdict`/`Counter`                                                |
| 2022 | 7   | [No Space Left On Device](https://adventofcode.com/2022/day/7)     | [Python](python/adventofcode/2022/7/no_space_left_on_device.py)   | Compute directory sizes, pick the smallest dir to delete                                  |
| 2022 | 14  | [Regolith Reservoir](https://adventofcode.com/2022/day/14)         | [Python](python/adventofcode/2022/14/regolith_reservoir.py)       | Simulate falling sand with a set-based grid (abyss + infinite floor)                      |
| 2022 | 24  | [Blizzard Basin](https://adventofcode.com/2022/day/24)             | [Python](python/adventofcode/2022/24/blizzard_basin.py)           | BFS with cached blizzard positions across multiple trips                                  |

##### Others

| Platform    | Challenge                                                                       | Solution                                       | Difficulty | Notes                                                             |
| ----------- | ------------------------------------------------------------------------------- | ---------------------------------------------- | ---------- | ----------------------------------------------------------------- |
| CodinGame   | [Rectangle Partition](https://www.codingame.com/ide/puzzle/rectangle-partition) | [Python](python/others/rectangle_partition.py) | Hard       | Brute-force + optimized length-frequency counting (both tested)   |

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
