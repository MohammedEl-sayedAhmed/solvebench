#!/usr/bin/env bash
# Launch VS Code scoped to THIS repo only: repo-local extensions (./.pst) + a
# dedicated profile (~/.cache/solvebench/<repo>-<id>), so it never reads or
# writes your global VS Code install. Remove it all with ./teardown.sh.
# Run ./setup.sh first to populate the extensions.
set -uo pipefail
cd "$(dirname "$0")"

if ! command -v code >/dev/null 2>&1; then
  echo "VS Code 'code' CLI not found on PATH." >&2
  echo "In VS Code: Command Palette → 'Shell Command: Install code command in PATH'." >&2
  exit 1
fi

# Where this launcher keeps VS Code state:
#   extensions -> ./.pst/extensions            (repo-local, populated by setup.sh)
#   profile    -> ~/.cache/solvebench/<repo>-<id>/user-data   (OUTSIDE the repo)
# The profile can't live under ./.pst: the Java language server (Eclipse-based)
# refuses to import any project whose folder contains its own workspace
# metadata — "project overlaps the workspace location" — which broke the Java
# Run|Debug CodeLens. teardown.sh removes this directory too.
# Key the profile to the PHYSICAL path (pwd -P): symlinked spellings of the
# same repo then share one profile, and teardown.sh finds it from any of them.
PHYS="$(pwd -P)"
REPO_ID="$(basename "$PHYS")-$(printf %s "$PHYS" | cksum | cut -d' ' -f1)"
DATA_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/solvebench/$REPO_ID/user-data"

# Seed the profile's user settings once: a fresh profile starts in Restricted
# Mode (workspace not trusted), which stops the Java language server from
# importing the project. Safe ONLY because this launcher refuses to open
# anything outside this repo (enforced below).
SETTINGS="$DATA_DIR/User/settings.json"
if [ ! -f "$SETTINGS" ]; then
  mkdir -p "$(dirname "$SETTINGS")"
  printf '{\n  "security.workspace.trust.enabled": false\n}\n' > "$SETTINGS"
fi

# Seed the profile's keybindings once (the profile lives outside git, so these
# can't be committed): duplicate the current line up/down with Ctrl+Alt+Up/Down.
# A user keybinding overrides the built-in default on those keys.
KEYBINDINGS="$DATA_DIR/User/keybindings.json"
if [ ! -f "$KEYBINDINGS" ]; then
  mkdir -p "$(dirname "$KEYBINDINGS")"
  cat > "$KEYBINDINGS" <<'EOF'
// Keybindings for the repo-scoped editor launched by ./code.sh.
// Seeded by code.sh / code.ps1 if missing; safe to edit.
[
  {
    "key": "ctrl+alt+up",
    "command": "editor.action.copyLinesUpAction",
    "when": "editorTextFocus && !editorReadonly"
  },
  {
    "key": "ctrl+alt+down",
    "command": "editor.action.copyLinesDownAction",
    "when": "editorTextFocus && !editorReadonly"
  }
]
EOF
fi

# Guard: since the .pst profile skips the trust prompt, only paths INSIDE this
# repo may be opened with it. Use your normal VS Code for anything else.
for a in "$@"; do
  case "$a" in -*) continue ;; esac                 # skip CLI flags
  p="${a%%:[0-9]*}"                                  # tolerate --goto file:line
  abs=$(realpath -m -- "$p" 2>/dev/null || echo "")
  case "$abs" in
    "$PWD"|"$PWD"/*) ;;
    *)
      echo "code.sh only opens paths inside this repo (the .pst profile skips the trust prompt)." >&2
      echo "Refusing: $a" >&2
      exit 1
      ;;
  esac
done

exec code \
  --extensions-dir "$PWD/.pst/extensions" \
  --user-data-dir "$DATA_DIR" \
  "${@:-.}"
