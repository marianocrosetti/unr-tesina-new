#!/usr/bin/env bash
# Night 2 (RunPod). Runs after composition_queue2 (nocenter/edges) finishes.
#  a. composition controls: family-A-only (FA=1) and family-B-only (FA=0) for styles edges and q=0
#  b. harder composition: edges with N=14
#  c. data-size law for pi=0 denoising: seen/unseen decomposition at 20k / 80k / 320k games
set -uo pipefail
cd "$(dirname "$0")/.."
PY=${PY:-python3}; export PY WORKERS=${WORKERS:-10}
while [ $(ps -eo args | grep -c "^bash scripts/composition_queue.sh") -ge 1 ]; do sleep 30; done
echo "[$(date +%H:%M:%S)] night2 start"
# a. controls
FA=1.0 QS="edges 0.0" bash scripts/composition_queue.sh
FA=0.0 QS="edges 0.0" bash scripts/composition_queue.sh
# b. harder shift
N=14 QS="edges 1.0" bash scripts/composition_queue.sh
# c. data-size law (pi=0): 20k dataset + decompositions
[ -f data/iid_rho0.3_pi0.0_20k.npz ] || { OMP_NUM_THREADS=1 $PY -m c4.generate --out data/iid_rho0.3_pi0.0_20k --n-games 20000 --seed 5 --workers $WORKERS --mode iid --rho 0.3 --pi 0.0 > overnight/gen_20k.json 2>/dev/null; cp data/iid_rho0.3_pi0.0_test.npz data/iid_rho0.3_pi0.0_20k_test.npz; cp data/iid_rho0.3_pi0.0_test.meta.json data/iid_rho0.3_pi0.0_20k_test.meta.json; }
for S in 0 1 2; do
  RUN=runs/iid_rho0.3_pi0.0_20k/seed$S
  [ -f $RUN/final.pt ] || $PY -m c4.train --data data/iid_rho0.3_pi0.0_20k.npz --out $RUN --seed $S --steps 1600 --eval-every 400 --ckpt-every 0 --warmup 100 > overnight/train_20k_s$S.log 2>&1
  [ -f results/iid_rho0.3_pi0.0_20k/seed$S/decompose.json ] || $PY -m c4.decompose --ckpt $RUN/final.pt --data data/iid_rho0.3_pi0.0_20k --out results/iid_rho0.3_pi0.0_20k/seed$S/decompose.json --games 200 > overnight/decomp_20k_s$S.log 2>&1
done
for S in 1 2; do  # 80k seeds 1,2 (seed 0 done locally)
  [ -f results/iid_rho0.3_pi0.0/seed$S/decompose.json ] || $PY -m c4.decompose --ckpt runs/iid_rho0.3_pi0.0/seed$S/final.pt --data data/iid_rho0.3_pi0.0 --out results/iid_rho0.3_pi0.0/seed$S/decompose.json --games 200 > overnight/decomp_80k_s$S.log 2>&1
done
# 320k: the x4 model at 6400 steps (10 epochs, matched to the 80k runs)
[ -f results/iid_rho0.3_pi0.0_x4_steps6400/seed0/decompose.json ] || $PY -m c4.decompose --ckpt runs/iid_rho0.3_pi0.0_x4_steps6400/seed0/final.pt --data data/iid_rho0.3_pi0.0_x4 --out results/iid_rho0.3_pi0.0_x4_steps6400/seed0/decompose.json --games 200 > overnight/decomp_x4.log 2>&1
[ -f results/iid_rho0.3_pi0.0_x4_steps1600/seed0/decompose.json ] || $PY -m c4.decompose --ckpt runs/iid_rho0.3_pi0.0_x4_steps1600/seed0/final.pt --data data/iid_rho0.3_pi0.0_x4 --out results/iid_rho0.3_pi0.0_x4_steps1600/seed0/decompose.json --games 200 > overnight/decomp_x4_1600.log 2>&1
echo "[$(date +%H:%M:%S)] NIGHT2 DONE"
