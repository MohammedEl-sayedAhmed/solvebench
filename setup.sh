#!/usr/bin/env bash
# Interactive one-time setup for Problem Solving Training:
# installs recommended VS Code extensions, optional Python dev deps, and can
# build the container image. Safe to re-run. Honors NO_COLOR and non-TTY stdin.
set -uo pipefail
cd "$(dirname "$0")"

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
  printf "    ${DIM}polyglot practice — python · c++ · java${RST}\n\n"
}

step() { printf "\n${BLU}==>${RST} ${BOLD}%s${RST}\n" "$1"; }
ok()   { printf "    ${GRN}✔${RST} %s\n" "$1"; }
skip() { printf "    ${DIM}– %s${RST}\n" "$1"; }
warn() { printf "    ${YLW}!${RST} %s\n" "$1"; }

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

# 1) VS Code extensions ------------------------------------------------------
EXTS=(ms-python.python ms-python.debugpy ms-vscode.cpptools redhat.java vscjava.vscode-java-debug)
step "VS Code extensions (${#EXTS[@]} recommended: Python, C/C++, Java debug)"
if command -v code >/dev/null 2>&1; then
  if ask "Install them now?" Y; then
    for e in "${EXTS[@]}"; do
      if code --install-extension "$e" --force >/dev/null 2>&1; then ok "$e"; else warn "failed: $e"; fi
    done
  else
    skip "skipped — they're listed in .vscode/extensions.json for later"
  fi
else
  warn "'code' CLI not found."
  warn "In VS Code: Command Palette → 'Shell Command: Install code command in PATH', then re-run."
  warn "Or just open the folder and accept the recommended-extensions prompt."
fi

# 2) Python dev deps ---------------------------------------------------------
step "Python dev dependencies (optional)"
if command -v python3 >/dev/null 2>&1; then
  if ask "Install pytest? (the runner itself needs nothing)" N; then
    if python3 -m pip install -r requirements.txt; then ok "pytest installed"; else warn "pip install failed"; fi
  else
    skip "skipped pytest"
  fi
else
  warn "python3 not on host — fine, ./run.sh runs everything in a container"
fi

# 3) Container image ---------------------------------------------------------
step "Container image (optional)"
if command -v docker >/dev/null 2>&1 || command -v podman >/dev/null 2>&1; then
  if ask "Build the pst-runner image now? (otherwise built on first ./run.sh)" N; then
    if ./run.sh --stats >/dev/null 2>&1; then ok "image ready"; else warn "build failed"; fi
  else
    skip "skipped — built automatically on first ./run.sh"
  fi
else
  skip "no docker/podman — use PST_NATIVE=1 ./run.sh with local tools"
fi

# 4) Toolchain summary -------------------------------------------------------
step "Toolchain check"
for t in python3 g++ javac java docker; do
  if command -v "$t" >/dev/null 2>&1; then ok "$t"; else skip "$t (optional)"; fi
done

printf "\n${GRN}${BOLD}Setup complete!${RST}  Next: ${BOLD}./run.sh --stats${RST}  or  ${BOLD}./run.sh --lang py${RST}\n\n"
