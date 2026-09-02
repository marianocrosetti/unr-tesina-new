#!/usr/bin/env bash
# End-to-end smoke test at toy scale (few minutes on a laptop). Validates the whole pipeline.
set -euo pipefail
cd "$(dirname "$0")/.."
N=${N:-4000}; STEPS=${STEPS:-400}
for PI in 0.0 1.0; do
  TAG=iid_rho0.3_pi${PI}
  uv run python -m c4.generate --out data/smoke_${TAG}       --n-games $N   --rho 0.3 --pi $PI --seed 1
  uv run python -m c4.generate --out data/smoke_${TAG}_test  --n-games 500  --rho 0.3 --pi $PI --seed 2
  uv run python -m c4.train --data data/smoke_${TAG}.npz --out runs/smoke_${TAG}/seed0 --steps $STEPS --batch 128 \
      --n-layer 4 --n-head 4 --n-embd 128 --eval-every 100 --warmup 50
  uv run python -m c4.evaluate states --ckpt runs/smoke_${TAG}/seed0/final.pt --data data/smoke_${TAG}_test.npz \
      --out results/smoke_${TAG}/seed0/states.json --max-games 500
  uv run python -m c4.evaluate match --ckpt runs/smoke_${TAG}/seed0/final.pt --data data/smoke_${TAG}_test.npz \
      --tau 0.001 --games 40 --out results/smoke_${TAG}/seed0/match_t0.001.json
done
uv run python -m c4.plots --results results --runs runs --out results/figs_smoke
