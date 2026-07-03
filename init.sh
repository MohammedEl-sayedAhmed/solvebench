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


# The SOLVE BENCH wordmark rows.
A1=' ___   ___   _    __   __ ___     ___  ___  _  _   ___  _  _ '
A2='/ __| / _ \ | |   \ \ / /| __|   | _ )| __|| \| | / __|| || |'
A3='\__ \| (_) || |__  \ V / | _|    | _ \| _| | .` || (__ | __ |'
A4='|___/ \___/ |____|  \_/  |___|   |___/|___||_|\_| \___||_||_|'

# One marquee light strip (72 dots, lit pairs).
lights() {
  local o=$1 i out=''
  for ((i = 0; i < 72; i++)); do
    if (( (i - o % 4 + 4) % 4 < 2 )); then out+=$'\033[38;5;220m·'
    else out+=$'\033[38;5;238m·'; fi
  done
  printf '%s\033[0m' "$out"
}

# Sweep the wordmark in (word only — the arrow makes its own entrance).
sweep_word() {
  local g=(220 214 203 196) rows=("$A1" "$A2" "$A3" "$A4") w=${#A1} i r
  printf '\033[?25l\n\n\n\n\033[4A'
  for ((i = 2; i <= w; i += 2)); do
    for r in 0 1 2 3; do
      printf '\r%11s\033[38;5;%sm%s\033[0m\033[K\n' '' "${g[r]}" "${rows[r]:0:i}"
    done
    printf '\033[4A'
    sleep 0.004
  done
  for r in 0 1 2 3; do
    printf '\r%11s\033[38;5;%sm%s\033[0m\033[K\n' '' "${g[r]}" "${rows[r]}"
  done
}

# One frame of the arrow scene at absolute rows 2-5.
#   $1 glyph-name  $2 x  $3 y(abs row of glyph top)  $4 word-off  $5 flash?  $6 dim-word?
_arrow_frame() {
  local -n gp=$1
  local x=$2 y=$3 wo=$4 fl=$5 dim=${6:-0} f=$'\0337' ra gi icon line sp vis pad wc
  local red=$'\033[38;5;203;1m' gld=$'\033[38;5;220;1m' r0=$'\033[0m'
  local g=(220 214 203 196) rows=("$A1" "$A2" "$A3" "$A4")
  for ra in 2 3 4 5; do
    gi=$(( ra - y ))
    icon=''
    if (( gi >= 0 && gi < ${#gp[@]} )); then icon="${gp[gi]}"; fi
    line=''; vis=0
    if [ -n "$icon" ]; then
      if (( x < 0 )); then
        icon="${icon:$(( -x ))}"
        line="${red}${icon}${r0}"; vis=${#icon}
      else
        printf -v line '%*s' "$x" ''
        line+="${red}${icon}${r0}"; vis=$(( x + ${#icon} ))
      fi
    fi
    pad=$(( 11 + wo - vis )); (( pad < 0 )) && pad=0
    printf -v sp '%*s' "$pad" ''
    wc=${g[ra - 2]}; (( fl )) && wc=231; (( dim )) && wc=242
    f+=$'\033['"$ra"$';1H'"${line}${sp}"$'\033[38;5;'"$wc"$'m'"${rows[ra - 2]}"$'\033[0m\033[K'
  done
  f+=$'\033[5;7H'"${gld}__${r0}"                      # cursor parked at its post
  (( fl )) && f+=$'\033[3;'$(( 11 + wo ))$'H\033[38;5;220;1m*\033[0m'
  printf '%s' "$f"$'\0338'
}

# Entrance: rise, vanish behind the lights, dive back fast, strike, recoil, settle.
arrow_intro() {
  local up=('  /\' ' /  \')
  local rt=('  \' '   \' '   /' '  /')
  local y spec
  _arrow_frame up 3 4 0 0; sleep 0.40
  for y in 3 2 1 0; do _arrow_frame up 3 "$y" 0 0; sleep 0.09; done
  _arrow_frame up 3 -9 0 0; sleep 0.50
  for spec in '-2 -2' '1 -1' '3 0' '5 1' '7 2'; do
    set -- $spec; _arrow_frame rt "$1" "$2" 0 0; sleep 0.025
  done
  _arrow_frame rt 7 2 2 1; sleep 0.11
  _arrow_frame rt 6 2 3 1; sleep 0.09
  for spec in '4 2' '1 1' '-2 1' '-4 0' '-3 0' '-1 0'; do
    set -- $spec; _arrow_frame rt "$1" 2 "$2" 0; sleep 0.07
  done
  _arrow_frame rt 0 2 0 0
}

if [ ! -t 1 ] || [ -n "${NO_COLOR:-}" ]; then
  printf '\n%s\n%s\n%s\n%s\n' "$A1" "$A2" "$A3" "$A4"
  printf "  ${DIM}init — a clean slate that's yours${RST}\n\n"
else
  printf '\033[2J\033[H'
  lights 0; printf '\n'
  sweep_word
  lights 2; printf '\n'
  printf "  ${DIM}init — a clean slate that's yours${RST}\n\n"
  arrow_intro
  printf '\033[?25h\n'
fi


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
