#!/usr/bin/env bash
# Refresh the README references (profile + progress stats), then commit and push.
#
#   ./ship.sh                       # auto message: "chore: update solutions and refresh README"
#   ./ship.sh "feat: add 3sum"      # custom commit message
#   ./ship.sh --index "msg"         # also rebuild the solutions index from files
#                                   #   (overwrites hand-written notes)
#
# Runs on the host (needs git). Uses your configured git identity; adds no
# co-author trailer. Refuses to commit if a work identity leaks into the tree.
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"

MSG=""; DO_INDEX=0
for a in "$@"; do
  case "$a" in
    --index) DO_INDEX=1 ;;
    *)       MSG="$a" ;;
  esac
done

echo "==> refreshing README references"
python3 scripts/apply_profile.py
python3 scripts/gen_stats.py
[ "$DO_INDEX" = 1 ] && python3 scripts/gen_index.py

if [ -z "$(git status --porcelain)" ]; then
  echo "nothing to commit — working tree clean"
  exit 0
fi

# Safety: never publish a work identity. Scan only committable files: git grep
# --untracked covers tracked + new files (what `git add -A` would stage) and
# skips git-ignored dirs (.venv, .pst, node_modules) — the old plain `grep -r`
# also flagged those. Exclude this guard's own machinery: ship.sh/ship.ps1 name
# the sentinel to run the check and PUBLISHING.md documents it — not leaks.
leak=$(git grep --untracked -nIiE 'witco' -- . \
  ':(exclude)ship.sh' ':(exclude)ship.ps1' ':(exclude)PUBLISHING.md' 2>/dev/null || true)
if [ -n "$leak" ]; then
  echo "refusing to commit: found a work identity in committable files:" >&2
  echo "$leak" >&2
  exit 1
fi

git add -A .
[ -z "$MSG" ] && MSG="chore: update solutions and refresh README"
git commit -q -m "$MSG"
echo "committed: $MSG"

BR=$(git rev-parse --abbrev-ref HEAD)
git fetch origin -q 2>/dev/null || true
if git rev-parse "origin/$BR" >/dev/null 2>&1 && [ -n "$(git rev-list "HEAD..origin/$BR")" ]; then
  echo "remote $BR is ahead — pull/rebase first, not pushing" >&2
  exit 1
fi
git push origin "HEAD:$BR" && echo "pushed to $BR ✅"
