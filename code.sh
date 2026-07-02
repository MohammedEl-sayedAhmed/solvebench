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

exec code \
  --extensions-dir "$PWD/.pst/extensions" \
  --user-data-dir "$PWD/.pst/user-data" \
  "${@:-.}"
