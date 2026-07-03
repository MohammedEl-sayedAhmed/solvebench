#!/usr/bin/env pwsh
# Refresh README references (profile + progress stats), then commit and push.
#
#   .\ship.ps1                     # auto commit message
#   .\ship.ps1 "feat: add 3sum"    # custom message
#   .\ship.ps1 --index "msg"       # also rebuild the solutions index from files
#
# Uses your configured git identity; adds no co-author trailer.
Set-Location (git rev-parse --show-toplevel)

$msg = ""; $doIndex = $false
foreach ($a in $args) {
    if ($a -eq '--index') { $doIndex = $true } else { $msg = $a }
}

Write-Host "==> refreshing README references"
python scripts/apply_profile.py
python scripts/gen_stats.py
if ($doIndex) { python scripts/gen_index.py }

if (-not (git status --porcelain)) {
    Write-Host "nothing to commit — working tree clean"
    exit 0
}

# Safety: never publish a work identity. Scan only committable files (git grep
# --untracked = tracked + new files, skipping git-ignored .venv/.pst/node_modules).
# Exclude this guard's own machinery — ship.sh/ship.ps1 name the sentinel to run
# the check and PUBLISHING.md documents it, so those aren't leaks.
$leak = git grep --untracked -nIiE 'witco' -- . `
    ':(exclude)ship.sh' ':(exclude)ship.ps1' ':(exclude)PUBLISHING.md'
if ($leak) {
    Write-Error "refusing to commit: found a work identity in committable files:`n$leak"
    exit 1
}

git add -A .
if (-not $msg) { $msg = "chore: update solutions and refresh README" }
# Don't blindly proceed: a rejecting pre-commit hook (e.g. a failing solution)
# makes `git commit` exit non-zero — without this check we'd falsely report
# "committed" and try to push a commit that was never made.
git commit -q -m $msg
if ($LASTEXITCODE -ne 0) {
    Write-Error "commit failed (pre-commit hook rejected it?) — nothing pushed"
    exit 1
}
Write-Host "committed: $msg"

$br = git rev-parse --abbrev-ref HEAD
git fetch origin -q 2>$null
git push origin "HEAD:$br"
Write-Host "pushed to $br"
