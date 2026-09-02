#!/usr/bin/env bash
# Data-generation queue (CPU). Reads configs/overnight_queue.txt in order; skips existing files.
set -uo pipefail
cd "$(dirname "$0")/.."
N_GAMES=${N_GAMES:-80000}; N_TEST=${N_TEST:-3000}; WORKERS=${WORKERS:-8}
while IFS='|' read -r TAG ARGS; do
  [ -z "$TAG" ] && continue
  if [ ! -f data/${TAG}_test.npz ]; then
    echo "[$(date +%H:%M:%S)] gen test $TAG"
    ${PY:-uv run python} -m c4.generate --out data/${TAG}_test --n-games $N_TEST --seed 2 --workers $WORKERS $ARGS > overnight/gen_${TAG}_test.json 2>/dev/null
  fi
  if [ ! -f data/${TAG}.npz ]; then
    echo "[$(date +%H:%M:%S)] gen train $TAG ($N_GAMES games)"
    ${PY:-uv run python} -m c4.generate --out data/${TAG} --n-games $N_GAMES --seed 1 --workers $WORKERS $ARGS > overnight/gen_${TAG}.json 2>/dev/null
    grep -E '"seconds"|"error_rate"|"shared_error_rate"|"mean_length"' overnight/gen_${TAG}.json | tr -d '\n'; echo
  fi
done < configs/overnight_queue.txt
echo "[$(date +%H:%M:%S)] GEN QUEUE DONE"
