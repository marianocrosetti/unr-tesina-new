#!/usr/bin/env bash
# Night 3 (after night2): where does composition break? capacity and data for the hardest style (edges).
set -uo pipefail
cd "$(dirname "$0")/.."
PY=${PY:-python3}; export PY WORKERS=${WORKERS:-10}
until grep -q "NIGHT2 DONE" overnight/night2.log 2>/dev/null; do sleep 60; done
echo "[$(date +%H:%M:%S)] night3 start"
# small model (2 layers, 64 d ≈ 0.1M params) on edges and control
EXTRA_TRAIN_ARGS="--n-layer 2 --n-head 4 --n-embd 64" RUN_SUFFIX="_small" QS="edges 1.0" bash scripts/composition_queue.sh
# 20k games on edges and control
N_GAMES=20000 N_GAMES_TAG="20k" QS="edges 1.0" bash scripts/composition_queue.sh
# mid-size model (4 layers, 128 d ≈ 0.8M params)
EXTRA_TRAIN_ARGS="--n-layer 4 --n-head 4 --n-embd 128" RUN_SUFFIX="_mid" QS="edges 1.0" bash scripts/composition_queue.sh
echo "[$(date +%H:%M:%S)] NIGHT3 DONE"
