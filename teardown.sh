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

# Farewell: the arrow turns downward and slowly sinks out of sight below the
# bottom light-strip. The wordmark dims; the gold cursor stays behind, alone.
arrow_outro() {
  local rt=('  \' '   \' '   /' '  /')
  local dn=(' \  /' '  \/')
  local y
  _arrow_frame rt 0 2 0 0; sleep 0.45                   # at its post, one last time
  _arrow_frame dn 1 3 0 0; sleep 0.35                   # head bows down
  for y in 4 5 6 7; do                                  # sinking… (clipped below)
    _arrow_frame dn 1 "$y" 0 0; sleep 0.14
  done
  sleep 0.40                                            # gone
  _arrow_frame dn 1 -9 0 0 1                            # the sign dims; cursor remains
}

if [ ! -t 1 ] || [ -n "${NO_COLOR:-}" ]; then
  printf '\n%s\n%s\n%s\n%s\n' "$A1" "$A2" "$A3" "$A4"
  printf "  ${DIM}teardown — remove everything setup created${RST}\n\n"
else
  printf '\033[2J\033[H'
  lights 0; printf '\n'
  sweep_word
  lights 2; printf '\n'
  printf "  ${DIM}teardown — remove everything setup created${RST}\n\n"
  arrow_outro
  printf '\033[?25h\n'
fi


# 1) Repo-local artifacts ----------------------------------------------------
step "Repo-local artifacts"
# The code.sh editor profile lives outside the repo (same derivation as code.sh
# — it can't sit under ./.pst or the Java language server refuses to import the
# project). Remove it here so teardown still erases every trace.
PHYS="$(pwd -P)"
REPO_ID="$(basename "$PHYS")-$(printf %s "$PHYS" | cksum | cut -d' ' -f1)"
PROFILE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/solvebench/$REPO_ID"
DIRS=(.pst .venv .pytest_cache "$PROFILE_DIR")
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
