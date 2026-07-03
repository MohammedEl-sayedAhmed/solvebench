#!/usr/bin/env bash
# Interactive one-time setup for solvebench.
#
# EVERYTHING it creates stays INSIDE this repo directory and is fully reversible
# (see ./teardown.sh):
#   .pst/extensions   repo-local VS Code extensions (never touches global VS Code)
#   .venv/            optional Python dev deps (pytest)
# The only out-of-repo artifact is the optional 'solvebench' docker image, which
# lives in the docker daemon and is removed by ./teardown.sh.
set -uo pipefail
cd "$(dirname "$0")"

PST_DIR="$PWD/.pst"
EXT_DIR="$PST_DIR/extensions"

if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
  BOLD=$'\033[1m'; DIM=$'\033[2m'; RED=$'\033[31m'; GRN=$'\033[32m'
  YLW=$'\033[33m'; BLU=$'\033[34m'; CYN=$'\033[36m'; RST=$'\033[0m'
else
  BOLD=; DIM=; RED=; GRN=; YLW=; BLU=; CYN=; RST=
fi

# The SOLVE BENCH wordmark rows (shared by the sweep-in and the shimmer loop).
A1=' ___   ___   _    __   __ ___     ___  ___  _  _   ___  _  _ '
A2='/ __| / _ \ | |   \ \ / /| __|   | _ )| __|| \| | / __|| || |'
A3='\__ \| (_) || |__  \ V / | _|    | _ \| _| | .` || (__ | __ |'
A4='|___/ \___/ |____|  \_/  |___|   |___/|___||_|\_| \___||_||_|'

# The favicon, as ANSI art: dark tile, red chevron, gold cursor (9 cols x 4 rows).
IRED=$'\033[38;5;203;1m'; IGLD=$'\033[38;5;220;1m'; IRST=$'\033[0m'
I1="${IRED}  \\      ${IRST}"
I2="${IRED}   \\     ${IRST}"
I3="${IRED}   /     ${IRST}"
I4="${IRED}  /   ${IGLD}__ ${IRST}"

# One marquee chase-light strip (72 dots; lit pairs step with the offset).
lights() {
  local o=$1 i out=''
  for ((i = 0; i < 72; i++)); do
    if (( (i - o % 4 + 4) % 4 < 2 )); then out+=$'\033[38;5;220m·'
    else out+=$'\033[38;5;238m·'; fi
  done
  printf '%s\033[0m' "$out"
}

# The arrow's entrance: it rises pointing UP, slips out of sight behind the
# marquee light-strip (the terminal's top edge), then dives back in fast —
# pointing RIGHT — strikes the wordmark (jolt + flash), recoils backwards on
# the momentum, and settles at its post. The gold cursor stays parked.
# Glyph rows above row 2 are simply not drawn: that's the "behind the wall".
arrow_intro() {
  local up=('  /\' ' /  \')
  local rt=('  \' '   \' '   /' '  /')
  local red=$'\033[38;5;203;1m' gld=$'\033[38;5;220;1m' r0=$'\033[0m'
  local g=(220 214 203 196) rows=("$A1" "$A2" "$A3" "$A4")

  _arrow_frame() {  # $1 glyph-name  $2 x  $3 y(abs row of glyph top)  $4 word-off  $5 flash?
    local -n gp=$1
    local x=$2 y=$3 wo=$4 fl=$5 f=$'\0337' ra gi icon line sp vis pad wc
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
      wc=${g[ra - 2]}; (( fl )) && wc=231
      f+=$'\033['"$ra"$';1H'"${line}${sp}"$'\033[38;5;'"$wc"$'m'"${rows[ra - 2]}"$'\033[0m\033[K'
    done
    f+=$'\033[5;7H'"${gld}__${r0}"                      # cursor parked at its post
    (( fl )) && f+=$'\033[3;'$(( 11 + wo ))$'H\033[38;5;220;1m*\033[0m'
    printf '%s' "$f"$'\0338'
  }

  local y spec
  _arrow_frame up 3 4 0 0; sleep 0.40                   # rise into view
  for y in 3 2 1 0; do                                  # fly upward…
    _arrow_frame up 3 "$y" 0 0; sleep 0.09              # …vanishing behind the lights
  done
  _arrow_frame up 3 -9 0 0; sleep 0.50                  # gone behind the wall
  for spec in '-2 -2' '1 -1' '3 0' '5 1' '7 2'; do      # dive back, fast
    set -- $spec
    _arrow_frame rt "$1" "$2" 0 0; sleep 0.025
  done
  _arrow_frame rt 7 2 2 1; sleep 0.11                   # impact!
  _arrow_frame rt 6 2 3 1; sleep 0.09
  for spec in '4 2' '1 1' '-2 1' '-4 0' '-3 0' '-1 0'; do
    set -- $spec
    _arrow_frame rt "$1" 2 "$2" 0; sleep 0.07            # momentum recoil, damped
  done
  _arrow_frame rt 0 2 0 0                                # standing still
}

# Sweep the wordmark in left-to-right with a gold->crimson gradient.
# Plain and instant when piped or NO_COLOR is set.
solvebench_banner() {
  if [ ! -t 1 ] || [ -n "${NO_COLOR:-}" ]; then
    printf '\n%s\n%s\n%s\n%s\n' "$A1" "$A2" "$A3" "$A4"
    return
  fi
  local g=(220 214 203 196) rows=("$A1" "$A2" "$A3" "$A4")
  local w=${#A1} i r
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

# Keep it alive: rotate the banner's gradient forever in the background while
# setup runs below it. The banner rows are pinned by a scroll region; each
# frame is a single write (no tearing) and everything is cleaned up on exit.
BANNER_LOOP_PID=
start_banner_loop() {
  [ -t 1 ] && [ -z "${NO_COLOR:-}" ] || return 0
  (
    g=(220 214 203 196) rows=("$A1" "$A2" "$A3" "$A4") phase=0 off=0
    icons=("$I1" "$I2" "$I3" "$I4")
    titles=(two_sum 3sum fizz_buzz min_stack lru_cache) t=0 tick=0
    while :; do
      frame=$'\0337'
      frame+=$'\033[1;1H'"$(lights "$off")"$'\033[K'
      for r in 0 1 2 3; do
        c=${g[(r + phase) % 4]}
        frame+=$'\033['$((r + 2))$';1H'"${icons[r]}"'  '$'\033[38;5;'"$c"$'m'"${rows[r]}"$'\033[0m\033[K'
      done
      frame+=$'\033[6;1H'"$(lights $((off + 2)))"$'\033[K'
      caret=$'\xE2\x96\x8B'; (( phase % 2 )) && caret=' '
      frame+=$'\033[7;1H  \033[38;5;220mnow solving: '"${titles[t]} ${caret}"$'\033[0m\033[K'
      frame+=$'\0338'
      printf '%s' "$frame"
      phase=$(( (phase + 1) % 4 ))
      off=$(( (off + 1) % 4 ))
      tick=$(( tick + 1 ))
      (( tick % 22 == 0 )) && t=$(( (t + 1) % ${#titles[@]} ))
      sleep 0.15
    done
  ) &
  BANNER_LOOP_PID=$!
  trap 'kill "$BANNER_LOOP_PID" 2>/dev/null; printf "\033[r\033[?25h"' EXIT
  trap 'exit 130' INT
  trap 'exit 143' TERM
}

banner() {
  if [ ! -t 1 ] || [ -n "${NO_COLOR:-}" ]; then
    solvebench_banner
    printf "  one environment for every judge\n\n"
    return
  fi
  printf '\033[2J\033[H'        # the banner owns the top of a fresh screen
  lights 0; printf '\n'         # marquee chase strip (row 1)
  solvebench_banner             # sweep in (art lands on rows 2-5)
  lights 2; printf '\n'         # marquee chase strip (row 6)
  printf '  \033[38;5;220mnow solving: two_sum \xE2\x96\x8B\033[0m\n'
  printf "  ${DIM}one environment for every judge${RST}\n"
  printf "  ${DIM}self-contained: everything lands in ./.pst and ./.venv${RST}\n"
  arrow_intro                   # the arrow flies in, strikes, rebounds
  printf '\033[?25h'
  printf '\033[11r\033[11;1H'   # scroll region below the pinned marquee
  start_banner_loop
}

step() { printf "\n${BLU}==>${RST} ${BOLD}%s${RST}\n" "$1"; }
ok()   { printf "    ${GRN}✔${RST} %s\n" "$1"; }
info() { printf "    ${DIM}%s${RST}\n" "$1"; }
skip() { printf "    ${DIM}– %s${RST}\n" "$1"; }
warn() { printf "    ${YLW}!${RST} %s\n" "$1"; }

# Run a command with an animated spinner. The command's stdout+stderr go to
# LOGFILE; the spinner animates on the terminal. Returns the command's exit code.
# usage: spin LOGFILE "message" -- command args...
spin() {
  local log="$1" msg="$2"; shift 2; [ "$1" = "--" ] && shift
  "$@" >"$log" 2>&1 & local pid=$!
  if [ ! -t 1 ]; then wait "$pid"; return $?; fi
  local frames=('|' '/' '-' '\') i=0
  printf '\033[?25l'
  while kill -0 "$pid" 2>/dev/null; do
    printf "\r    ${CYN}%s${RST} %s" "${frames[i % 4]}" "$msg"
    i=$((i + 1)); sleep 0.1
  done
  printf "\r\033[K\033[?25h"
  wait "$pid"; return $?
}

ask() {  # ask "question" [default Y|N] -> exit 0 for yes
  local q="$1" def="${2:-Y}" ans hint
  [ "$def" = "Y" ] && hint="[Y/n]" || hint="[y/N]"
  if [ ! -t 0 ]; then ans="$def"; else
    read -r -p "$(printf "${YLW}?${RST} %s ${DIM}%s${RST} " "$q" "$hint")" ans || ans="$def"
  fi
  ans="${ans:-$def}"
  [[ "$ans" =~ ^[Yy] ]]
}

banner

# 1) VS Code extensions (repo-local, no global footprint) --------------------
EXTS=(ms-python.python ms-python.debugpy ms-vscode.cpptools redhat.java vscjava.vscode-java-debug cweijan.vscode-office)
step "VS Code extensions (${#EXTS[@]} recommended: Python, C/C++, Java debug, Markdown preview)"
if command -v code >/dev/null 2>&1; then
  if ask "Install them into the repo (./.pst/extensions, not global)?" Y; then
    mkdir -p "$EXT_DIR"
    # One `code` call installs all — separate calls trip the extension-dir lock.
    args=(--extensions-dir "$EXT_DIR")
    for e in "${EXTS[@]}"; do args+=(--install-extension "$e"); done
    log=$(mktemp)
    spin "$log" "installing ${#EXTS[@]} extensions into .pst/extensions… (may take a minute)" -- code "${args[@]}" --force
    installed=$(code --extensions-dir "$EXT_DIR" --list-extensions 2>/dev/null | tr '[:upper:]' '[:lower:]')
    failed=0
    for e in "${EXTS[@]}"; do
      if grep -qix "$e" <<<"$installed"; then ok "$e"; else warn "failed: $e"; failed=1; fi
    done
    [ "$failed" = 1 ] && { warn "details from 'code':"; sed 's/^/        /' "$log" | tail -n 8; }
    rm -f "$log"
    info "these live only in ./.pst — open the repo with them via:  ./code.sh"
  else
    skip "skipped — they're listed in .vscode/extensions.json for the workspace prompt"
  fi
else
  warn "'code' CLI not found."
  warn "In VS Code: Command Palette → 'Shell Command: Install code command in PATH', then re-run."
fi

# 2) Python dev deps (in a repo-local venv, PEP 668 safe) --------------------
step "Python dev dependencies (optional)"
if command -v python3 >/dev/null 2>&1; then
  if ask "Install pytest into ./.venv? (the runner itself needs nothing)" N; then
    if [ ! -d .venv ] && ! python3 -m venv .venv 2>/dev/null; then
      warn "could not create .venv — install the venv module: sudo apt install python3-venv"
    else
      plog=$(mktemp)
      if spin "$plog" "installing pytest into ./.venv…" -- .venv/bin/pip install -r requirements.txt; then
        ok "pytest ready — run it with: .venv/bin/pytest  (or: source .venv/bin/activate)"
      else
        warn "pip install failed:"; sed 's/^/        /' "$plog" | tail -n 8
      fi
      rm -f "$plog"
    fi
  else
    skip "skipped pytest"
  fi
else
  warn "python3 not on host — fine, ./run.sh runs everything in a container"
fi

# 3) Container image (lives in the docker daemon; removed by teardown) -------
step "Container image (optional)"
if command -v docker >/dev/null 2>&1 || command -v podman >/dev/null 2>&1; then
  if ask "Build the solvebench image now? (otherwise built on first ./run.sh)" N; then
    blog=$(mktemp)
    if spin "$blog" "building solvebench image (first time can take a few minutes)…" -- ./run.sh --stats; then
      ok "image ready (remove later with ./teardown.sh)"
    else
      warn "build failed:"; sed 's/^/        /' "$blog" | tail -n 8
    fi
    rm -f "$blog"
  else
    skip "skipped — built automatically on first ./run.sh"
  fi
else
  skip "no docker/podman — use PST_NATIVE=1 ./run.sh with local tools"
fi

# 4) Git hooks (optional) ----------------------------------------------------
step "Git hooks (optional)"
if [ -d .git ] && [ -d .githooks ]; then
  if ask "Enable the pre-commit hook? (runs changed solutions + refreshes stats)" N; then
    git config core.hooksPath .githooks && ok "enabled (core.hooksPath=.githooks)"
  else
    skip "skipped — enable later with: git config core.hooksPath .githooks"
  fi
else
  skip "no .git / .githooks here"
fi

# 5) Toolchain summary -------------------------------------------------------
step "Toolchain check"
for t in python3 g++ javac java docker; do
  if command -v "$t" >/dev/null 2>&1; then ok "$t"; else skip "$t (optional)"; fi
done

printf "\n${GRN}${BOLD}Setup complete!${RST}  Everything is under ./.pst and ./.venv.\n"
printf "  Run:      ${BOLD}./run.sh --stats${RST}\n"
printf "  Edit:     ${BOLD}./code.sh${RST}   ${DIM}(VS Code scoped to this repo)${RST}\n"
printf "  Remove:   ${BOLD}./teardown.sh${RST}\n\n"
