#!/usr/bin/env bash
# Remove everything setup.sh / code.sh created. Repo-local only — the sole
# out-of-repo item touched is the optional 'pst-runner' docker image.
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

printf '%s' "$CYN"
cat <<'ART'
     ____   ____   _____
    |  _ \ / ___| |_   _|   cleanup
    |  __/  ___) |  | |
    |_|    |____/   |_|
ART
printf '%s\n' "$RST"

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
if [ -n "$ENGINE" ] && "$ENGINE" image inspect pst-runner >/dev/null 2>&1; then
  if ask "Remove the 'pst-runner' image?" Y; then
    "$ENGINE" rmi pst-runner >/dev/null 2>&1 && ok "removed pst-runner image" || skip "could not remove image"
  else
    skip "kept pst-runner image"
  fi
else
  skip "no pst-runner image present"
fi

printf "\n${GRN}${BOLD}Teardown complete.${RST} Tracked repo files are untouched.\n"
printf "  ${DIM}(git identity in .git/config is left as-is; reset with: git config --unset user.email)${RST}\n\n"
