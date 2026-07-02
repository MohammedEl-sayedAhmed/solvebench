#!/usr/bin/env bash
# Record an asciinema demo of the polyglot runner, and optionally render a GIF.
# Produces demo.cast in the repo root; upload it or convert to a GIF and embed
# the result in the README's Demo section.
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"

if ! command -v asciinema >/dev/null 2>&1; then
  echo "asciinema not found — install it first: https://asciinema.org/docs/install" >&2
  exit 1
fi

asciinema rec --overwrite --title "problem-solving-training — polyglot runner" \
  -c 'bash -lc "python3 run.py --stats; echo; python3 run.py --lang java --time"' \
  demo.cast

cat <<'NEXT'

Recorded demo.cast.
  play:    asciinema play demo.cast
  upload:  asciinema upload demo.cast      # then paste the returned link into README's Demo section
  GIF:     agg demo.cast demo.gif          # https://github.com/asciinema/agg  ->  ![demo](demo.gif)
NEXT
