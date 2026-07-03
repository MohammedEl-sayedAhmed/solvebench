#!/usr/bin/env bash
# Launch VS Code scoped to THIS repo only: repo-local extensions + profile under
# ./.pst, so it never reads or writes your global VS Code install. Remove it all
# with ./teardown.sh. Run ./setup.sh first to populate the extensions.
set -uo pipefail
cd "$(dirname "$0")"

if ! command -v code >/dev/null 2>&1; then
  echo "VS Code 'code' CLI not found on PATH." >&2
  echo "In VS Code: Command Palette → 'Shell Command: Install code command in PATH'." >&2
  exit 1
fi

# Seed the repo-local profile's user settings once: a fresh profile starts in
# Restricted Mode (workspace not trusted), which stops the Java language server
# from importing the project. Safe ONLY because this launcher refuses to open
# anything outside this repo (enforced below).
SETTINGS="$PWD/.pst/user-data/User/settings.json"
if [ ! -f "$SETTINGS" ]; then
  mkdir -p "$(dirname "$SETTINGS")"
  printf '{\n  "security.workspace.trust.enabled": false\n}\n' > "$SETTINGS"
fi

# Seed repo-local keybindings once (the .pst profile is git-ignored, so these
# can't be committed): duplicate the current line up/down with Ctrl+Alt+Up/Down.
# A user keybinding overrides the built-in default on those keys.
KEYBINDINGS="$PWD/.pst/user-data/User/keybindings.json"
if [ ! -f "$KEYBINDINGS" ]; then
  mkdir -p "$(dirname "$KEYBINDINGS")"
  cat > "$KEYBINDINGS" <<'EOF'
// Repo-scoped keybindings for the ./code.sh editor (--user-data-dir .pst).
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
  --user-data-dir "$PWD/.pst/user-data" \
  "${@:-.}"
