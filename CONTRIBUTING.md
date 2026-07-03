# Contributing

Thanks for your interest! This repo doubles as a **polyglot practice framework**,
so contributions fall into two buckets.

## Adding a solution

1. Scaffold it in your language of choice:
   ```bash
   ./run.sh new leetcode/easy/two_sum --lang py     # or cpp | java | js | go | rust
   ```
2. Implement the solution and fill in the example test cases.
3. Run it (all languages you solved it in):
   ```bash
   ./run.sh leetcode/easy/two_sum
   ```
4. Every solution **self-tests** and must exit non-zero on a wrong answer — that's
   how `run.py` and CI detect failures.
5. Optional: sanity-check its scaling with `./run.sh complexity <problem>`
   (Python and Java).

Layout is language-first: `‹lang›/‹platform›/‹group›/‹name›`. Advent of Code
puzzle inputs go in the shared `inputs/` tree, resolved via a helper (never a
path relative to the solution).

## Improving the framework

Runner, scaffolder, language helpers, setup/teardown, CI — PRs welcome. Please:

- Keep it dependency-free where possible (the runner uses only the stdlib).
- Run `python run.py` (or `./run.sh`) before pushing; CI runs the whole suite.
- Match the existing style of nearby code.

## Adding a language

Each language needs: a `‹lang›/common/` helper (or an inline one, like Go/Rust),
a `templates/solution.‹ext›`, a `run_‹lang›` branch + `LANGUAGES` entry in
[run.py](run.py), and a `LANGS` entry in [new.py](new.py). Add its toolchain to
the [Dockerfile](Dockerfile) and CI.

## Commit style

Conventional commits are appreciated (`feat:`, `fix:`, `docs:`, `refactor:`,
`ci:`). Keep commits focused.
