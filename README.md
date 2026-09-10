# solvebench

[![tests](https://github.com/MohammedEl-sayedAhmed/solvebench/actions/workflows/ci.yml/badge.svg)](https://github.com/MohammedEl-sayedAhmed/solvebench/actions/workflows/ci.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![stars](https://img.shields.io/github/stars/MohammedEl-sayedAhmed/solvebench?style=social)](https://github.com/MohammedEl-sayedAhmed/solvebench/stargazers)
[![forks](https://img.shields.io/github/forks/MohammedEl-sayedAhmed/solvebench?style=social)](https://github.com/MohammedEl-sayedAhmed/solvebench/network/members)

**One environment for every judge.** My solutions to LeetCode, Codewars, Advent
of Code, and more — tracked automatically, solvable in **six languages**, and
debuggable **locally with real breakpoints** (no premium subscriptions). One
containerized runner verifies everything on any OS.

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
- 🏗️ **Scaffolder** — paste a LeetCode URL and `new.py` creates the file with the
  number, title, and difficulty filled in (any of the six languages).
- 📈 **Complexity estimator** — `./run.sh complexity <problem>` empirically fits a
  solution's time & space to a Big-O class (Python and Java).
- 🧩 **VS Code extension** — an optional companion in [extension/](extension/):
  every solution in the Testing panel, Run/Debug/Complexity buttons above your
  code, and the complexity fit as an interactive chart.

## Progress

<!-- stats:start -->
![adventofcode](https://img.shields.io/badge/adventofcode-6%20solved-brightgreen) ![codewars](https://img.shields.io/badge/codewars-7%20solved-red) ![leetcode](https://img.shields.io/badge/leetcode-28%20solved-orange) ![others](https://img.shields.io/badge/others-1%20solved-lightgrey)

42 solutions · 4 platforms · 2 languages

| Platform | java | py | Total |
| --- | --- | --- | --- |
| adventofcode | 0 | 6 | 6 |
| codewars | 0 | 7 | 7 |
| leetcode | 12 | 16 | 28 |
| others | 0 | 1 | 1 |
| **Total** | 12 | 30 | **42** |
<!-- stats:end -->

## Website & demo

🌐 **[Project site](docs/index.html)** — the full pitch: features, workflow, and
command reference (`docs/index.html`; serve it with GitHub Pages → `main /docs`).
▶ **[Animated terminal demo](docs/demo.html)** — watch the one runner drive
every language. Regenerate a recording with `./scripts/record_demo.sh`.

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
│   └── common/             #   TestFramework.java + ComplexityHarness.java
├── javascript/             # JavaScript solutions
│   └── common/             #   test_framework.js
├── inputs/                 # shared, language-agnostic puzzle inputs
│   └── adventofcode/<year>/<day>/input.txt
├── templates/              # starter templates per language
├── scripts/                # generators (stats, index, profile) + build helpers
├── extension/              # optional VS Code companion (see extension/README.md)
├── docs/                   # animated terminal demo (GitHub Pages)
├── run.py                  # polyglot test runner
├── new.py                  # scaffolder for new solutions (accepts problem URLs)
├── complexity.py           # empirical Big-O estimator (py + java)
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
| `./run.sh complexity <problem>` | Estimate a solution's time/space Big-O empirically |
| `cd extension && npm run preview` | Preview the complexity chart in a browser |
| `cd extension && npm test` | Run the extension's tests |

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
| container image | docker daemon | `solvebench`; the only out-of-repo item |

- **Edit with the repo-scoped editor:** `./code.sh` (or `.\code.ps1`) launches
  VS Code using the repo-local extensions/profile under `.pst/`. Debug any open
  solution with **F5** — configs are in [.vscode/launch.json](.vscode/launch.json).
- **Remove everything:** `./teardown.sh` (or `.\teardown.ps1`) deletes `.pst/`,
  `.venv/`, caches/build files, and optionally the `solvebench` image.

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

The first invocation builds the `solvebench` image once; later runs reuse it.
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

One command per problem — works for **Python and Java** solutions. It finds the
solution, generates growing inputs from the function's type hints (Python) or
parameter types via reflection (Java, with JIT warm-up and per-call allocation
tracking), and fits runtime + memory to a Big-O class:

```bash
./run.sh complexity leetcode/easy/two_sum
#  function: twoSum · inputs: auto-generated from type hints (nums: list, target: int)
#  time  ≈ O(n) · space ≈ O(n)

./run.sh complexity two_sum --lang java         # measure the Java solution instead
./run.sh complexity three_sum --max-seconds 1   # slow solutions stop growing early
./run.sh complexity min_stack --method push     # pick the method explicitly
```

Language is auto-detected (Python first, then Java — Java-only solutions just
work). If the input shape can't come from the types (constraints, in-place
mutation), add a small hook to the solution and it takes precedence:

```python
def complexity_input(n):
    return [list(range(n)), n]   # Python: the argument list for input size n
```

```java
public static Object[] complexityInput(int n) {
    return new Object[] { /* args for size n */ };   // Java equivalent
}
```

Results are **empirical** (a fit, not a proof) — defaults are adversarial where
possible (e.g. palindromic strings so early-exit checks still scan fully), but
worst cases with tricky shapes deserve a `complexity_input`. Demo on known
cases: `python python/common/complexity.py`.

## VS Code extension (optional)

[extension/](extension/) is a companion for this repo. The Python tools still do
the work — it calls `run.py`, `new.py`, and `complexity.py` and shows the results
in the editor.

- **Testing panel** — every solution, grouped platform → difficulty → problem →
  language. One problem solved in Python and Java shows both under one label.
- **Buttons above your code** — Run, Debug, and Complexity on each solution, so
  you don't need the command palette.
- **Debug any solution** — the config is built from the open file, so nothing has
  to be added to `.vscode/launch.json` per solution. Python, Java, JavaScript,
  and C++.
- **Complexity as a chart** — your measured points against the Big-O class that
  fits best and its neighbours. Hover a line to see which class it is. Log scale
  makes every class a straight line, so the one your points follow is the answer.

```bash
cd extension
npm install
npm run preview        # look at the chart in a browser, no install needed
npm test               # 93 tests, also what CI runs
npm run package        # build solvebench-0.1.0.vsix
```

Install the `.vsix` into the repo-local extension folder that
[code.sh](code.sh) already uses, so it never touches your global VS Code:

```bash
code --extensions-dir "$PWD/.pst/extensions" \
  --install-extension extension/solvebench-0.1.0.vsix --force
./code.sh
```

`./teardown.sh` removes it with everything else under `.pst/`.

See [extension/README.md](extension/README.md) for the settings and
[extension/PLAN.md](extension/PLAN.md) for what was built and what was left out.

## Solutions

<!-- solutions:start -->
No solutions yet — add one and list it here:

```bash
./run.sh new leetcode/easy/two_sum --lang py
```

_Or skip the manual index and track progress with_ `python run.py --stats`.
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
