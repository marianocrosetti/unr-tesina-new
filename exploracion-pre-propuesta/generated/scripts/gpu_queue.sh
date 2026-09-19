#!/usr/bin/env bash
# GPU-box queue (RunPod, 96 vCPU + RTX 4090). Two phases:
#   A. seeds 1..2 for every condition already generated (data/*.npz present) at the overnight settings (1600 steps)
#   B. scaling study on iid pi=0 (and pi=1, rule as controls): more data x more steps -> does tau=1 reach the mixture
#      and does the tau->0 gain approach the theoretical ceiling?
# Idempotent: skips finished runs. PY=python3 on the pod.
set -uo pipefail
cd "$(dirname "$0")/.."
PY=${PY:-python3}; export PY
TAUS="0.001 0.1 0.3 0.5 0.75 1.0 1.5"
train_eval() { # tag data_tag steps seed [extra train args]
  local TAG=$1 DATA=$2 STEPS=$3 SEED=$4; shift 4
  local RUN=runs/${TAG}/seed${SEED} RES=results/${TAG}/seed${SEED}
  [ -f $RUN/final.pt ] || { echo "[$(date +%H:%M:%S)] train $TAG seed$SEED steps=$STEPS"; $PY -m c4.train --data data/${DATA}.npz --out $RUN --seed $SEED --steps $STEPS --eval-every 400 --ckpt-every 0 --warmup 100 "$@" > overnight/train_${TAG}_s${SEED}.log 2>&1; }
  [ -f $RES/states.json ] || $PY -m c4.evaluate states --ckpt $RUN/final.pt --data data/${DATA}_test.npz --out $RES/states.json --taus $TAUS --max-games 3000 > overnight/eval_${TAG}_s${SEED}.log 2>&1
  for T in 0.001 1.0; do [ -f $RES/match_expert_t${T}.json ] || $PY -m c4.evaluate match --ckpt $RUN/final.pt --data data/${DATA}_test.npz --tau $T --games 200 --out $RES/match_expert_t${T}.json > /dev/null 2>&1; done
  $PY - <<PY
import json; d=json.load(open("$RES/states.json")); e=d["expert"]; t0=d["taus"]["0.001"]; t1=d["taus"]["1.0"]
print(f"  $TAG seed$SEED: expert acc={e['acc']:.3f} | tau=1 acc={t1['acc']:.3f} | tau->0 acc={t0['acc']:.3f} gain={t0['gain_vs_best_expert']:+.3f}")
PY
}
# ---- Phase A: extra seeds for every condition -------------------------------------------------
while IFS='|' read -r TAG ARGS; do
  [ -z "$TAG" ] && continue
  for S in ${SEEDS:-1 2}; do train_eval $TAG $TAG 1600 $S; done
done < configs/overnight_queue.txt
# ---- Phase B: scaling study --------------------------------------------------------------------
for COND in "iid_rho0.3_pi0.0|--mode iid --rho 0.3 --pi 0.0" "iid_rho0.3_pi1.0|--mode iid --rho 0.3 --pi 1.0" "rule_mod3_left_rho0.3|--mode rule --rule-mod 3 --rho 0.3"; do
  TAG=${COND%%|*}; ARGS=${COND#*|}
  BIG=${TAG}_x4
  [ -f data/${BIG}.npz ] || { echo "[$(date +%H:%M:%S)] gen $BIG (320k games)"; OMP_NUM_THREADS=1 $PY -m c4.generate --out data/${BIG} --n-games 320000 --seed 3 --workers ${WORKERS:-80} $ARGS > overnight/gen_${BIG}.json 2>/dev/null; }
  [ -f data/${BIG}_test.npz ] || cp data/${TAG}_test.npz data/${BIG}_test.npz && cp data/${TAG}_test.meta.json data/${BIG}_test.meta.json
  for STEPS in 1600 6400 25600; do
    train_eval ${TAG}_steps${STEPS} $TAG $STEPS 0            # 80k games, longer training
    train_eval ${BIG}_steps${STEPS} $BIG $STEPS 0            # 320k games
  done
done
$PY -m c4.plots --results results --runs runs --out results/figs > /dev/null 2>&1
$PY -m c4.report --results results --out RESULTS.md > /dev/null 2>&1
echo "[$(date +%H:%M:%S)] GPU QUEUE DONE"
