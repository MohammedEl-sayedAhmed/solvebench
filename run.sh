#!/usr/bin/env bash
# Run the polyglot test runner (and scaffolder). Uses a container on the host so
# you don't need Python/g++/JDK/etc installed — but runs natively automatically
# when you're already inside the Dev Container (or any container), or when no
# container engine is available.
#
#   ./run.sh                              # run every solution
#   ./run.sh leetcode/easy/two_sum        # run one problem, all languages
#   ./run.sh --platform codewars          # restrict to a platform
#   ./run.sh --stats                      # inventory grouped by platform
#   ./run.sh new <url|path> --lang cpp    # scaffold a new solution
#   ./run.sh complexity <problem>         # estimate a solution's Big-O
#   ./run.sh shell                        # open a shell inside the container
#
# Force native execution with PST_NATIVE=1.
set -euo pipefail

IMAGE=solvebench
cd "$(dirname "$0")"

run_native() {
  case "${1:-}" in
    new)        shift; exec python3 new.py "$@" ;;
    complexity) shift; exec python3 complexity.py "$@" ;;
    shell)      exec "${SHELL:-bash}" ;;
    *)          exec python3 run.py "$@" ;;
  esac
}

# Already inside the toolchain image / a Dev Container / any container?
in_container() {
  [ -n "${PST_IN_CONTAINER:-}" ] || [ -f /.dockerenv ] \
    || grep -qaE '(docker|containerd|kubepods|/lxc/)' /proc/1/cgroup 2>/dev/null
}

# Native path: asked for it, already containerized, or the tools are right here.
if [ "${PST_NATIVE:-}" = "1" ] || in_container; then
  run_native "$@"
fi

# Otherwise use a container engine; if none, fall back to native (don't error).
if command -v docker >/dev/null 2>&1; then ENGINE=docker
elif command -v podman >/dev/null 2>&1; then ENGINE=podman
else
  echo "note: no docker/podman found — running on the local toolchain." >&2
  run_native "$@"
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
  new)        shift; engine_run python3 new.py "$@" ;;
  complexity) shift; engine_run python3 complexity.py "$@" ;;
  shell)      engine_run bash ;;
  *)          engine_run python3 run.py "$@" ;;
esac
