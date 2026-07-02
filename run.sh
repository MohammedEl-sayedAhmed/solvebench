#!/usr/bin/env bash
# Run the polyglot test runner (and scaffolder) inside a container, so you don't
# need Python, g++, or a JDK installed on the host.
#
#   ./run.sh                              # run every solution
#   ./run.sh leetcode/easy/two_sum        # run one problem, all languages
#   ./run.sh --platform codewars          # restrict to a platform
#   ./run.sh --stats                      # inventory grouped by platform
#   ./run.sh new leetcode/easy/foo --lang cpp   # scaffold a new solution
#   ./run.sh shell                        # open a shell inside the container
#
# Runs natively (no container) if you set PST_NATIVE=1 and have the tools.
set -euo pipefail

IMAGE=pst-runner
cd "$(dirname "$0")"

# Escape hatch: run directly on the host toolchain.
if [ "${PST_NATIVE:-}" = "1" ]; then
  case "${1:-}" in
    new)   shift; exec python3 new.py "$@" ;;
    shell) exec "${SHELL:-bash}" ;;
    *)     exec python3 run.py "$@" ;;
  esac
fi

# Pick a container engine.
if command -v docker >/dev/null 2>&1; then ENGINE=docker
elif command -v podman >/dev/null 2>&1; then ENGINE=podman
else
  echo "Error: neither docker nor podman is installed." >&2
  echo "Install one, or run natively with:  PST_NATIVE=1 ./run.sh $*" >&2
  exit 1
fi

# Build the image on first use (or after the Dockerfile changes).
if ! "$ENGINE" image inspect "$IMAGE" >/dev/null 2>&1; then
  echo ">> Building $IMAGE image (first run only)…" >&2
  "$ENGINE" build -t "$IMAGE" .
fi

TTY=()
[ -t 1 ] && TTY=(-t)

engine_run() {
  "$ENGINE" run --rm -i "${TTY[@]}" \
    --user "$(id -u):$(id -g)" -e HOME=/tmp \
    -v "$PWD":/repo -w /repo "$IMAGE" "$@"
}

case "${1:-}" in
  new)   shift; engine_run python3 new.py "$@" ;;
  shell) engine_run bash ;;
  *)     engine_run python3 run.py "$@" ;;
esac
