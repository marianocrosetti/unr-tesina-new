#!/usr/bin/env bash
# Training/eval queue (MPS). Waits for each dataset, trains one seed, evaluates, refreshes plots.
#   SEED (default 0). Steps are re-read from configs/steps.txt before every run so they can be tuned mid-flight.
set -uo pipefail
cd "$(dirname "$0")/.."
SEED=${SEED:-0}
TAUS="0.001 0.1 0.3 0.5 0.75 1.0 1.5"
while IFS='|' read -r TAG ARGS; do
  [ -z "$TAG" ] && continue
  until [ -f data/${TAG}.npz ] && [ -f data/${TAG}_test.npz ]; do sleep 20; done
  STEPS=$(cat configs/steps.txt)
  if [ ! -f runs/${TAG}/seed${SEED}/final.pt ]; then
    echo "[$(date +%H:%M:%S)] train $TAG seed$SEED steps=$STEPS"
    ${PY:-uv run python} -m c4.train --data data/${TAG}.npz --out runs/${TAG}/seed${SEED} --seed $SEED --steps $STEPS \
        --eval-every 200 --ckpt-every 200 --warmup 100 > overnight/train_${TAG}_s${SEED}.log 2>&1
    grep EVAL overnight/train_${TAG}_s${SEED}.log | tail -1
  fi
  if [ ! -f results/${TAG}/seed${SEED}/states.json ]; then
    echo "[$(date +%H:%M:%S)] eval states $TAG"
    ${PY:-uv run python} -m c4.evaluate states --ckpt runs/${TAG}/seed${SEED}/final.pt --data data/${TAG}_test.npz \
        --out results/${TAG}/seed${SEED}/states.json --taus $TAUS --max-games 3000 > overnight/eval_${TAG}_s${SEED}.log 2>&1
    ${PY:-uv run python} - <<PY
import json; d=json.load(open("results/${TAG}/seed${SEED}/states.json"))
e=d["expert"]; t0=d["taus"]["0.001"]; t1=d["taus"]["1.0"]
print(f"  expert acc={e['acc']:.3f} best_er={e['best_er']:.3f} | tau=1 acc={t1['acc']:.3f} er={t1['er']:.3f} | tau=0.001 acc={t0['acc']:.3f} er={t0['er']:.3f} gain={t0['gain_vs_best_expert']:+.3f} acc_bias={t0['acc_bias']} acc_nonbias={t0['acc_nonbias']:.3f} | theory={d['theory']}")
PY
  fi
  for T in 0.001 1.0; do
    if [ ! -f results/${TAG}/seed${SEED}/match_expert_t${T}.json ]; then
      ${PY:-uv run python} -m c4.evaluate match --ckpt runs/${TAG}/seed${SEED}/final.pt --data data/${TAG}_test.npz --tau $T --games 150 \
          --out results/${TAG}/seed${SEED}/match_expert_t${T}.json > /dev/null 2>&1
      grep -o '"score": [0-9.]*\|"illegal_loss": [0-9]*' results/${TAG}/seed${SEED}/match_expert_t${T}.json | tr '\n' ' '; echo " (tau=$T)"
    fi
  done
  ${PY:-uv run python} -m c4.plots --results results --runs runs --out results/figs > /dev/null 2>&1
done < ${QUEUE:-configs/overnight_queue.txt}
echo "[$(date +%H:%M:%S)] TRAIN QUEUE DONE seed=$SEED"
