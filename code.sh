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
# from importing the project. .pst only ever opens this repo, so trust it.
SETTINGS="$PWD/.pst/user-data/User/settings.json"
if [ ! -f "$SETTINGS" ]; then
  mkdir -p "$(dirname "$SETTINGS")"
  printf '{\n  "security.workspace.trust.enabled": false\n}\n' > "$SETTINGS"
fi

exec code \
  --extensions-dir "$PWD/.pst/extensions" \
  --user-data-dir "$PWD/.pst/user-data" \
  "${@:-.}"
