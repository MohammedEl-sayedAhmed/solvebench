#!/usr/bin/env bash
# init.sh — after forking, reset the repo to a clean slate for YOU.
# Removes the example solutions + puzzle inputs, resets the README solutions
# index, writes your platform handles to profile.json, and (optionally) starts
# fresh git history. Keeps all tooling: runner, helpers, templates, setup, CI.
set -uo pipefail
cd "$(dirname "$0")"

if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
  BOLD=$'\033[1m'; DIM=$'\033[2m'; GRN=$'\033[32m'; YLW=$'\033[33m'; BLU=$'\033[34m'; CYN=$'\033[36m'; RST=$'\033[0m'
else BOLD=; DIM=; GRN=; YLW=; BLU=; CYN=; RST=; fi

step() { printf "\n${BLU}==>${RST} ${BOLD}%s${RST}\n" "$1"; }
ok()   { printf "    ${GRN}✔${RST} %s\n" "$1"; }
skip() { printf "    ${DIM}– %s${RST}\n" "$1"; }
warn() { printf "    ${YLW}!${RST} %s\n" "$1"; }
ask()  {
  local q="$1" def="${2:-Y}" ans hint
  [ "$def" = "Y" ] && hint="[Y/n]" || hint="[y/N]"
  read -r -p "$(printf "${YLW}?${RST} %s ${DIM}%s${RST} " "$q" "$hint")" ans || ans="$def"
  ans="${ans:-$def}"; [[ "$ans" =~ ^[Yy] ]]
}
prompt() { local ans; read -r -p "$(printf "${YLW}?${RST} %s: " "$1")" ans || ans=""; printf '%s' "$ans"; }

printf '%s' "$CYN"
cat <<'ART'
     ____   ____   _____    init
    |  _ \ / ___| |_   _|
    |  __/  ___) |  | |
    |_|    |____/   |_|
ART
printf '%s\n' "$RST"

warn "This clears ALL solutions and puzzle inputs from the working tree and"
warn "resets the README solutions index. Tooling (runner, helpers, CI) is kept."
ask "Continue?" N || { printf "    ${DIM}aborted — nothing changed${RST}\n"; exit 0; }

# 1) Clear example solutions + inputs (keep common/ and templates/) -----------
step "Clearing example solutions and inputs"
for lang in python cpp java; do
  [ -d "$lang" ] && find "$lang" -mindepth 1 -maxdepth 1 -type d ! -name common -exec rm -rf {} +
done
[ -d inputs ] && find inputs -mindepth 1 -maxdepth 1 -exec rm -rf {} +
ok "removed solutions (kept common/ + templates/) and puzzle inputs"

# 2) Profile ------------------------------------------------------------------
step "Your profile (leave blank to skip a platform)"
name=$(prompt "Your name")
gh=$(prompt "GitHub username")
lc=$(prompt "LeetCode username")
cw=$(prompt "Codewars username")
hr=$(prompt "HackerRank username")
cf=$(prompt "Codeforces username")
python3 - "$name" "$gh" "$lc" "$cw" "$hr" "$cf" <<'PY'
import json, sys
keys = ["name", "github", "leetcode", "codewars", "hackerrank", "codeforces"]
with open("profile.json", "w") as f:
    json.dump(dict(zip(keys, sys.argv[1:])), f, indent=2)
    f.write("\n")
PY
python3 scripts/apply_profile.py >/dev/null && ok "wrote profile.json and updated the README profile"

# 3) Reset README solutions index --------------------------------------------
step "Resetting the solutions index"
python3 scripts/reset_index.py >/dev/null && ok "README solutions index cleared"

# 4) Optional fresh git history ----------------------------------------------
step "Git history"
if ask "Start fresh git history? (removes ALL past commits)" N; then
  rm -rf .git && git init -q && git add -A \
    && git commit -q -m "Initial commit" && ok "fresh git history created"
else
  skip "kept existing git history"
fi

printf "\n${GRN}${BOLD}Clean slate ready!${RST}\n"
printf "  Add a solution:  ${BOLD}./run.sh new leetcode/easy/two_sum --lang py${RST}\n"
printf "  Set up tooling:  ${BOLD}./setup.sh${RST}\n\n"
