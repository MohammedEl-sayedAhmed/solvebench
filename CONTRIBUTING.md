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

- Keep it dependency-free where possible (the runner uses only the stdlib, and
  the extension's tests use only `node --test`).
- Run `python run.py` (or `./run.sh`) before pushing; CI runs the whole suite.
- If you touched `extension/`, run `npm test` there too.
- Match the existing style of nearby code.

## Working on the VS Code extension

[extension/](extension/) is a TypeScript companion that calls the Python tools.
It has its own tests, and CI runs them as a second job.

```bash
cd extension
npm install
npm run preview     # serve the complexity chart on 127.0.0.1:5178 and iterate
npm test            # unit tests + the contract with run.py / complexity.py
npm run package     # build the .vsix
```

- `media/chart.js` and `media/chart.css` are loaded by both the webview and the
  preview, so there is one renderer. Edit either and reload the preview page.
- The Big-O models in `media/chart.js` mirror `MODELS` in
  [python/common/complexity.py](python/common/complexity.py). If you change one,
  change both — a test compares them.
- Anything that must run outside VS Code (the preview, the tests) belongs in a
  module with no `vscode` import, like `src/complexityPage.ts`.
- `scripts/check_json_contract.py` guards the JSON that `run.py --json` and
  `complexity.py --json` promise the extension. Changing either shape means
  updating that script and `extension/test/cli.test.js`.

`F5` does not work on a snap-installed VS Code — snap blocks the app from
launching a second copy of itself, so the Extension Development Host never
opens. Build the `.vsix` and install it into `.pst/extensions` instead.

## Adding a language

Each language needs: a `‹lang›/common/` helper (or an inline one, like Go/Rust),
a `templates/solution.‹ext›`, a `run_‹lang›` branch + `LANGUAGES` entry in
[run.py](run.py), and a `LANGS` entry in [new.py](new.py). Add its toolchain to
the [Dockerfile](Dockerfile) and CI.

## Commit style

Conventional commits are appreciated (`feat:`, `fix:`, `docs:`, `refactor:`,
`ci:`). Keep commits focused.
