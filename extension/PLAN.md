# solvebench VS Code extension — plan

## What this is

A VS Code extension that adds buttons and panels for the Python tools that are
already here. You get a test panel instead of reading terminal output, debug
buttons instead of writing launch configs by hand, and commands instead of shell
scripts.

The tools still do the work. `run.py`, `new.py`, and `complexity.py` are not
replaced. The extension just calls them and shows what comes back.

## Two ways to build it, and which one we picked

**Way 1: a helper for the repo.** People still fork and clone solvebench. The
extension adds UI on top. The repo stays the main product. **This is what we are
building.**

**Way 2: the extension is the product.** People install it from the Marketplace
and it sets up a workspace for them. No forking. The repo becomes just an
example.

We are not doing Way 2, for three reasons:

1. The README asks people to star and fork the repo, and [init.sh](../init.sh)
   exists to help with that. Way 2 gives this up.
2. On the Marketplace we would compete with `vscode-leetcode`. It has about a
   million installs and can send solutions to LeetCode. We cannot send
   solutions. What we do differently is six languages, real breakpoints, and
   complexity estimates. Some people want that, but fewer people.
3. Way 2 is mostly marketing work, not coding work.

Way 1 also needs no Marketplace account. We build a `.vsix` file from this
folder. We can still publish later if we want to.

## Checked before starting

- `target/classes` has compiled `common/` and `leetcode/` packages in it. So the
  Java language server reads [pom.xml](../pom.xml) fine and the Run|Debug
  CodeLens works.
- [.vscode/launch.json](../.vscode/launch.json) has `skip-worktree` set, and the
  committed version holds only 4 generic current-file configs. So the repo is
  already clean. What was in the *local* copy was 9 named per-class Java configs
  that the Java extension adds by itself when you click Run on a class. They had
  drifted: one pointed at `TrappingRainWater`, which no longer exists, and 4 of
  the 12 Java solutions had no config at all.

  **So the gain is smaller than it first looked.** The extension does not clean
  up the repo, because there is nothing there to clean. It stops per-class
  configs from piling up in the local file, and it covers all 12 Java solutions
  instead of 8 working ones. Phase 5 does not touch launch.json.
- Node v22.22.3, npm 10.9.8, `tsc` is installed.
- `run.py` only prints text. A program cannot read its results. This blocks
  everything else, so it goes first.

## What is included

| Phase | Work | Why |
|---|---|---|
| 1 | `run.py --json` | Needed before the rest |
| 2 | Extension setup and finding Python | Base for the rest |
| 3 | Test panel (`TestController`) | The biggest gain |
| 4 | Debug configs (`DebugConfigurationProvider`) | No hand-written config per solution |
| 5 | Commands | Shell scripts become editor commands |
| 6 | CodeLens, status bar, `complexity.py --json` | Buttons instead of the command palette |

## What we left out, on purpose

- **Moving the 42 solutions out of the repo.** Only needed for Way 2. A helper
  extension works fine with the solutions where they are. It would also mean
  deleting working solutions, and that is not our call to make while changing
  tooling.
- **Publishing to the Marketplace.** Still not doing this yet. See below.
- **Deleting `setup.sh`, `code.sh`, `teardown.sh`.** The extension makes the
  `.pst` folder unnecessary, but these scripts also help people who never open
  VS Code. Deleting them is a separate choice.
- **Go and Rust debugging.** These need the `golang.go` and
  `vadimcn.vscode-lldb` extensions, and there is no Go or Rust solution in the
  repo yet. The extension says which one is missing instead of guessing.

## Phase 1 — `run.py --json`

Add a `--json` flag:

- `--json` runs the solutions and writes one JSON object to **stdout**.
- `--stats --json` only lists them and does not run them. This builds the test
  tree.
- With `--json`, text output is turned off, so stdout has JSON and nothing else.
  Warnings go to stderr.
- Exit codes stay the same (1 when something fails), so CI keeps working.

```json
{
  "schema": 1,
  "solutions": [
    { "language": "python", "lang": "py", "platform": "leetcode",
      "group": "easy", "name": "two_sum",
      "path": "python/leetcode/easy/two_sum.py",
      "status": "pass", "seconds": 0.12, "output": "" }
  ],
  "summary": { "pass": 41, "fail": 1, "total": 42, "seconds": 12.34 }
}
```

`--stats --json` leaves out `status` and `seconds`. `path` is relative to the
repo, and the test panel uses it as the id for each solution.

One bug got fixed along the way. `Solution.label` used the path separator of the
current OS. Git always uses forward slashes, so `--changed` matched nothing on
Windows. It now always uses forward slashes. This also keeps the JSON the same
on every OS.

## Phase 2 — Extension setup and finding Python

`extension/` is its own npm package. Compiled JavaScript goes into `out/`. Both
`out/` and `node_modules/` are in `.gitignore`. The extension only starts when
the folder has a `run.py` in it, so it stays off in other projects.

Which Python to use. The first one found wins:

1. The `solvebench.pythonPath` setting
2. `.venv/bin/python` in the workspace (`Scripts/python.exe` on Windows), which
   is what [setup.sh](../setup.sh) makes
3. The interpreter that `ms-python.python` has selected, read from its API
4. `python3`, then `python`, from PATH

If none of these work, commands show one clear message instead of a stack trace.
Python is here to stay, so it is worth doing this in one place. `complexity.py`
in particular reads a function's type hints while Python is running and builds
test inputs from them. TypeScript cannot do that at all.

**We do not force other extensions to install.** Requiring all six language
extensions would install five useless ones for someone who only writes Python.
Instead, each debug config checks for the one extension it needs and offers to
install it. Same result as the `.pst` folder, without the extra weight.

## Phase 3 — Test panel

A `TestController` with four levels: platform → group → problem → language.

The language level is there because one problem solved in both Python and Java
is two things you can run. `group` is empty for platforms like Codewars, and it
is skipped when empty.

- The tree comes from `run.py --stats --json`.
- To run picked items, their paths are passed to `run.py` as filters. `matches()`
  already compares filters against the repo-relative path, so a full path picks
  exactly one solution. If nothing is picked, everything runs.
- Results are matched back by `path`. Failure output is attached to the item.
- There is a run profile and a debug profile. The debug one calls Phase 4.
- Runs are native, not Docker. Starting a container for every run is too slow,
  and `run.py` allows 120 seconds per solution. Full container runs stay in the
  terminal with `./run.sh`.

## Phase 4 — Debug configs

A `DebugConfigurationProvider` builds the config from the open file, for any
solution inside a language folder.

| Language | Type | Notes |
|---|---|---|
| Python | `debugpy` | `PYTHONPATH=<repo>/python` |
| Java | `java` | Class name from the path, `scripts/build_java.py` runs first, classpath `.pst/build/java` |
| JavaScript | `node` | `NODE_PATH=<repo>/javascript` |
| C++ | `cppdbg` | compiled with `-g` first |
| Go / Rust | — | says which extension is missing |

Java class names come from the path. `java/leetcode/easy/TwoSum.java` becomes
`leetcode.easy.TwoSum`. The build step calls
[scripts/build_java.py](../scripts/build_java.py) instead of copying its logic.
That script already handles the case where one half-finished file would stop you
from debugging a finished one.

## Phase 5 — Commands

| Command | Calls |
|---|---|
| New solution | `new.py`, with a language picker and a box for the URL or path |
| Run current solution | `run.py <dir>` |
| Run all | `run.py` |
| Estimate complexity | `complexity.py <file>` |
| Show stats | `run.py --stats` |
| Refresh solution list | lists the solutions again |

`.vscode/launch.json` is left alone. It has `skip-worktree` set, so changes to it
are local and git does not record them, and the committed version is already just
the 4 generic configs. Those stay as the fallback for anyone without the
extension installed.

## Phase 6 — Buttons instead of the command palette

Done:

- **CodeLens.** `Run`, `Debug` and `Complexity` links above the code in every
  solution file. They sit on the first `class`/`def`/`func` line, falling back
  to the top of the file. Complexity only appears for Python and Java, because
  that is all `complexity.py` measures. The clicked file's uri is passed to the
  command, so a click acts on that file even if focus moved. Turn it off with
  `solvebench.showCodeLens`.
- **Solve count in the status bar.** Counts problems, not files, so a problem
  solved in Python and Java counts once. Click it for the breakdown.
- **`complexity.py --json`.** `report()` in `python/common/complexity.py` took a
  `quiet` flag, since it already returned the sizes, times and fitted classes
  and only needed to stop printing them. Both the Python and Java paths return
  the numbers now.

  One bug came out of this: `find_solution_file` printed its "also solved in
  java" hint to stdout, which corrupted the JSON. It is a hint, not data, so it
  goes to stderr now.

- **Complexity chart.** The Complexity command opens a panel instead of
  printing to a terminal. It draws the measured points, the class that fitted
  best, and that class's neighbours, each scaled to the data the same way. That
  answers the question the text output cannot: the estimator says O(n log n),
  but do the points actually track O(n) more closely?

  The chart is inline SVG with no scripts, so the webview runs with
  `enableScripts: false` and a `default-src 'none'` policy. That rules out a
  hover tooltip; the measurements table below the charts is what stands in for
  it, which is fine at five or six points.

  **Colours.** Blue for the measured data, orange for the fitted class, a
  recessive neutral for the reference curves. Explicit hex, not
  `--vscode-charts-*`, because those vary a lot between themes and some leave
  them muddy. Each mode gets its own steps rather than a flip, and both were
  validated for colour-vision-deficiency separation, chroma, lightness band and
  3:1 contrast against their surface: worst pair CVD dE 24.7 light / 26.8 dark,
  against a target of 8. Line style carries the same information as hue (solid
  with dots / dashed / dotted) plus a legend, so nothing depends on colour
  alone. `solvebench.chartMeasuredColor` and `solvebench.chartFittedColor`
  override them; only a hex or `var(--name)` is accepted, since the value goes
  into a `<style>` block.

  **Scale.** The y axis follows the measured data, not the curves. Scaling to
  include the curves let a steep neighbour like O(n^2) flatten the real
  measurements into the bottom quarter of the plot -- the memory chart topped out
  at 1,120 KB for data that peaked at 293. Curves are clipped to the plot box
  instead, so one running off the top reads as "does not fit", which is the
  useful signal. X labels are dropped when they would collide, because the sizes
  grow geometrically on a linear axis.

  `MODELS` and the log-space scale fit are mirrored from
  `python/common/complexity.py`. That duplication is deliberate: the drawn curve
  has to be the curve that actually won, not an approximation of it. A check
  compares the TypeScript fit against Python's on real solutions.

Still to do:

- Offer to make a file when you paste a problem URL
- Go and Rust debugging

## Fixed along the way

`.vscode/settings.json` set `python.testing.pytestArgs` to `["."]`, which
overrode `testpaths = ["python"]` in `pyproject.toml`. Together with
`python_files = ["*.py"]` that made pytest import `scripts/build_java.py`, whose
module-level `sys.exit(0)` crashed collection with `INTERNALERROR`. The Testing
view showed "pytest Discovery Error" because of it. Set to `["python"]` now, so
it matches the repo config: 30 tests collected, 30 passed.

This was there before the extension and is not related to it. It only showed up
in VS Code, because running `pytest` from a terminal uses `testpaths` and is
fine.

## Publishing

Still not doing it. No account, icon, or release setup until the extension has
been used for a while.

## How we check it

`run.py --json` and `--stats --json` have to be valid JSON, match the counts in
the text output, and keep the same exit codes. The extension has to compile with
`tsc` in strict mode.

The parts that do not need VS Code are checked by loading the compiled code with
a stub for the `vscode` module and feeding it real files from this repo:

- Java class names match what `run.py` computes, for all 12 Java solutions.
- Every solution's problem id selects its own solution in `run.py`, all 42.
- `problemTitle` gives one label for both `two_sum` and `TwoSum`.
- `solutionRef` skips `common/` helpers, root files and wrong extensions.
- CodeLens anchors on `class Solution:` and `public class TwoSum {`.
- The chart's Big-O fit agrees with `_best_fit` in Python, and its curves land
  within about 1.2x of every measured point.
- The chart's SVG has nothing clipped or off-canvas.

What needs a person to look at it, and has been confirmed that way: the test
panel tree, running a test, the CodeLens links, and the Complexity command.

F5 does not work on a snap-installed VS Code: snap stops the app launching a
second copy of itself, so the Extension Development Host window never opens and
the debug session just sits there. Build the `.vsix` and install it into
`.pst/extensions` instead:

```bash
cd extension && npm run compile && npm run package && cd ..
code --extensions-dir "$PWD/.pst/extensions" \
  --install-extension extension/solvebench-0.1.0.vsix --force
```

Then reload the window. `./code.sh` picks it up from there.
