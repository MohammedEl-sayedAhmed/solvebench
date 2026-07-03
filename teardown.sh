#!/usr/bin/env bash
# Remove everything setup.sh / code.sh created. Repo-local only — the sole
# out-of-repo item touched is the optional 'solvebench' docker image.
set -uo pipefail
cd "$(dirname "$0")"

if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
  BOLD=$'\033[1m'; DIM=$'\033[2m'; GRN=$'\033[32m'; YLW=$'\033[33m'; BLU=$'\033[34m'; CYN=$'\033[36m'; RST=$'\033[0m'
else BOLD=; DIM=; GRN=; YLW=; BLU=; CYN=; RST=; fi

step() { printf "\n${BLU}==>${RST} ${BOLD}%s${RST}\n" "$1"; }
ok()   { printf "    ${GRN}✔${RST} %s\n" "$1"; }
skip() { printf "    ${DIM}– %s${RST}\n" "$1"; }
ask()  {
  local q="$1" def="${2:-Y}" ans hint
  [ "$def" = "Y" ] && hint="[Y/n]" || hint="[y/N]"
  if [ ! -t 0 ]; then ans="$def"; else
    read -r -p "$(printf "${YLW}?${RST} %s ${DIM}%s${RST} " "$q" "$hint")" ans || ans="$def"
  fi
  ans="${ans:-$def}"; [[ "$ans" =~ ^[Yy] ]]
}

# Animated SOLVEBENCH wordmark: a left-to-right sweep in a gold->crimson
# gradient. Plain and instant when piped or NO_COLOR is set.
solvebench_banner() {
  local a1=' ___   ___   _    __   __ ___     ___  ___  _  _   ___  _  _ '
  local a2='/ __| / _ \ | |   \ \ / /| __|   | _ )| __|| \| | / __|| || |'
  local a3='\__ \| (_) || |__  \ V / | _|    | _ \| _| | .` || (__ | __ |'
  local a4='|___/ \___/ |____|  \_/  |___|   |___/|___||_|\_| \___||_||_|'
  if [ ! -t 1 ] || [ -n "${NO_COLOR:-}" ]; then
    printf '\n%s\n%s\n%s\n%s\n' "$a1" "$a2" "$a3" "$a4"
    return
  fi
  local g1=$'\033[38;5;220m' g2=$'\033[38;5;214m' g3=$'\033[38;5;203m' g4=$'\033[38;5;196m' r0=$'\033[0m'
  local w=${#a1} i
  printf '\n\033[?25l\n\n\n\n\033[4A'
  for ((i = 2; i <= w; i += 2)); do
    printf '\r%s%s%s\033[K\n' "$g1" "${a1:0:i}" "$r0"
    printf '\r%s%s%s\033[K\n' "$g2" "${a2:0:i}" "$r0"
    printf '\r%s%s%s\033[K\n' "$g3" "${a3:0:i}" "$r0"
    printf '\r%s%s%s\033[K\n' "$g4" "${a4:0:i}" "$r0"
    printf '\033[4A'
    sleep 0.004
  done
  printf '\r%s%s%s\033[K\n' "$g1" "$a1" "$r0"
  printf '\r%s%s%s\033[K\n' "$g2" "$a2" "$r0"
  printf '\r%s%s%s\033[K\n' "$g3" "$a3" "$r0"
  printf '\r%s%s%s\033[K\n' "$g4" "$a4" "$r0"
  printf '\033[?25h'
}
solvebench_banner
printf "  ${DIM}teardown — remove everything setup created${RST}\n\n"

# 1) Repo-local artifacts ----------------------------------------------------
step "Repo-local artifacts"
DIRS=(.pst .venv .pytest_cache)
present=()
for d in "${DIRS[@]}"; do
  if [ -e "$d" ]; then
    sz=$(du -sh "$d" 2>/dev/null | cut -f1)
    printf "    %-14s ${DIM}%s${RST}\n" "$d" "$sz"; present+=("$d")
  fi
done
[ -e report.html ] && { printf "    %-14s\n" "report.html"; present+=(report.html); }
compiled=$(find . -path ./.git -prune -o \( -name '__pycache__' -o -name '*.pyc' -o -name '*.class' -o -name '*.out' \) -print 2>/dev/null | wc -l | tr -d ' ')
[ "$compiled" -gt 0 ] && printf "    %-14s ${DIM}%s items${RST}\n" "(caches/build)" "$compiled"

if [ ${#present[@]} -eq 0 ] && [ "$compiled" -eq 0 ]; then
  ok "nothing to remove — already clean"
elif ask "Remove these?" Y; then
  for d in "${present[@]}"; do rm -rf "$d" && ok "removed $d"; done
  if [ "$compiled" -gt 0 ]; then
    find . -path ./.git -prune -o \( -name '__pycache__' -o -name '*.pyc' -o -name '*.class' -o -name '*.out' \) -exec rm -rf {} + 2>/dev/null
    ok "removed caches/build files"
  fi
else
  skip "kept repo-local artifacts"
fi

# 2) Container image ---------------------------------------------------------
step "Container image (docker daemon)"
ENGINE=""
command -v docker >/dev/null 2>&1 && ENGINE=docker
[ -z "$ENGINE" ] && command -v podman >/dev/null 2>&1 && ENGINE=podman
if [ -n "$ENGINE" ] && "$ENGINE" image inspect solvebench >/dev/null 2>&1; then
  if ask "Remove the 'solvebench' image?" Y; then
    "$ENGINE" rmi solvebench >/dev/null 2>&1 && ok "removed solvebench image" || skip "could not remove image"
  else
    skip "kept solvebench image"
  fi
else
  skip "no solvebench image present"
fi

printf "\n${GRN}${BOLD}Teardown complete.${RST} Tracked repo files are untouched.\n"
printf "  ${DIM}(git identity in .git/config is left as-is; reset with: git config --unset user.email)${RST}\n\n"
