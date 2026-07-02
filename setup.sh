#!/usr/bin/env bash
# Interactive one-time setup for Problem Solving Training.
#
# EVERYTHING it creates stays INSIDE this repo directory and is fully reversible
# (see ./teardown.sh):
#   .pst/extensions   repo-local VS Code extensions (never touches global VS Code)
#   .venv/            optional Python dev deps (pytest)
# The only out-of-repo artifact is the optional 'pst-runner' docker image, which
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

banner() {
  printf '%s' "$CYN"
  cat <<'ART'
     ____   ____   _____
    |  _ \ / ___| |_   _|
    | |_) |\___ \   | |
    |  __/  ___) |  | |
    |_|    |____/   |_|
ART
  printf '%s' "$RST"
  printf "    ${BOLD}Problem · Solving · Training${RST}\n"
  printf "    ${DIM}polyglot practice — python · c++ · java${RST}\n"
  printf "    ${DIM}self-contained: everything lands in ./.pst and ./.venv${RST}\n\n"
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
EXTS=(ms-python.python ms-python.debugpy ms-vscode.cpptools redhat.java vscjava.vscode-java-debug)
step "VS Code extensions (${#EXTS[@]} recommended: Python, C/C++, Java debug)"
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
  if ask "Build the pst-runner image now? (otherwise built on first ./run.sh)" N; then
    blog=$(mktemp)
    if spin "$blog" "building pst-runner image (first time can take a few minutes)…" -- ./run.sh --stats; then
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
