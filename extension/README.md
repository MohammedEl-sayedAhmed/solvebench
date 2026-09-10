# solvebench VS Code extension

Adds editor UI for the tools in this repo. The tools still do the work: this
calls `run.py`, `new.py`, and `complexity.py` and shows what comes back.

See [PLAN.md](PLAN.md) for what is built, what is left out, and why.

## Build and install

```bash
cd extension
npm install
npm run compile        # writes out/
npm run package        # writes solvebench-0.1.0.vsix
```

Then install the `.vsix`: in VS Code, Extensions → `...` menu → **Install from
VSIX**, or:

```bash
code --install-extension solvebench-0.1.0.vsix
```

To try it without packaging, open the `extension/` folder in VS Code and press
F5. That opens a second window with the extension loaded.

## What you get

**Test panel.** Every solution shows up in the Testing view, grouped platform →
difficulty → problem → language. Run one, run a group, or run all. Failures show
the output from the solution's own test helper. There is also a Debug profile,
for one solution at a time.

**Debug Current Solution.** Builds the debug config from the open file, so you
do not add one to `.vscode/launch.json` for every new solution. Works for
Python, Java, JavaScript, and C++. For Go and Rust it tells you which extension
is missing instead of failing quietly.

**Buttons in the editor.** Every solution file gets `Run`, `Debug` and
`Complexity` links above the code, so you do not need the command palette.
Complexity only shows for Python and Java, since that is all `complexity.py`
measures. Turn the links off with `solvebench.showCodeLens`.

**Solve count in the status bar.** Counts problems rather than files, so one
problem solved in two languages counts once. Click it for the breakdown.

**Commands** (all start with `solvebench:` in the command palette):

| Command | Calls |
| --- | --- |
| New Solution | `new.py`, asks for a language and a URL or path, then opens the file |
| Run Current Solution | `run.py <folder>` — every language the problem is solved in |
| Debug Current Solution | starts a debug session for the open file |
| Run All Solutions | `run.py` |
| Estimate Complexity of Current Solution | `complexity.py` (Python and Java only) |
| Show Stats | `run.py --stats` |
| Refresh Solution List | lists the solutions again |

## Settings

| Setting | Default | What it does |
| --- | --- | --- |
| `solvebench.pythonPath` | `""` | Which Python to use. Empty means find one: `.venv`, then the interpreter the Python extension has picked, then `python3` on PATH. |
| `solvebench.runInContainer` | `false` | Use `./run.sh` (Docker or Podman) for Run All and Run Current. The test panel always runs natively, because starting a container for every run is too slow. |
| `solvebench.showCodeLens` | `true` | Show the Run / Debug / Complexity links above the code. |

## Notes

The extension only starts in a folder that has `run.py` in it, so it stays off
in your other projects.

It does not install the language extensions for you. Requiring all six would
install five useless ones for someone who only writes Python. Each debug config
checks for the one it needs and offers to install it then.
