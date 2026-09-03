#!/usr/bin/env bash
# Skill composition across demonstrators with disjoint support.
#   Family A: optimal opening, transcript truncated at ply N (no endgames).  Family B: q-quality opening, optimal endgame.
#   Does the imitator play the endgame well after its OWN (optimal) openings?  Control: q=1.
# Evaluations per (q, seed):
#   states on own test set        -> in-support endgames (reached from q-openings)
#   states on the perfect test set -> endgames reached from optimal openings = the unseen support  (tag perf_test)
#   decompose vs perfect opponent  -> own-play trajectories, seen/unseen split, per phase
set -uo pipefail
cd "$(dirname "$0")/.."
PY=${PY:-python3}; export PY
QS=${QS:-"0.0 0.25 0.5 1.0"}; N=${N:-8}; FA=${FA:-0.5}; SEEDS=${SEEDS:-"0 1 2"}; N_GAMES=${N_GAMES:-80000}; WORKERS=${WORKERS:-10}; STEPS=${STEPS:-1600}
TAUS="0.001 0.1 0.3 1.0"
[ -f data/perfect_test.npz ] || OMP_NUM_THREADS=1 $PY -m c4.generate --out data/perfect_test --n-games 3000 --seed 2 --workers $WORKERS --mode iid --rho 0.0 > overnight/gen_perfect_test.json 2>/dev/null
for Q in $QS; do
  # entries: a number = random-style opening of quality q ; a word (nocenter|edges) = structured opening style
  case $Q in
    [0-9]*) TAG=comp_q${Q}_n${N}_fa${FA}; GARGS="--mode composition --q-open $Q --n-open $N --frac-a $FA" ;;
    *)      TAG=comp_${Q}_n${N}_fa${FA};  GARGS="--mode composition --b-open $Q --n-open $N --frac-a $FA" ;;
  esac
  [ -f data/${TAG}.npz ]      || { echo "[$(date +%H:%M:%S)] gen $TAG"; OMP_NUM_THREADS=1 $PY -m c4.generate --out data/${TAG} --n-games $N_GAMES --seed 1 --workers $WORKERS $GARGS > overnight/gen_${TAG}.json 2>/dev/null; }
  [ -f data/${TAG}_test.npz ] || OMP_NUM_THREADS=1 $PY -m c4.generate --out data/${TAG}_test --n-games 3000 --seed 2 --workers $WORKERS $GARGS > overnight/gen_${TAG}_test.json 2>/dev/null
  for S in $SEEDS; do
    RUN=runs/${TAG}/seed${S}; RES=results/${TAG}/seed${S}
    [ -f $RUN/final.pt ] || { echo "[$(date +%H:%M:%S)] train $TAG seed$S"; $PY -m c4.train --data data/${TAG}.npz --out $RUN --seed $S --steps $STEPS --eval-every 400 --ckpt-every 0 --warmup 100 > overnight/train_${TAG}_s${S}.log 2>&1; }
    [ -f $RES/states.json ]      || $PY -m c4.evaluate states --ckpt $RUN/final.pt --data data/${TAG}_test.npz --out $RES/states.json --taus $TAUS --max-games 3000 > overnight/eval_${TAG}_s${S}.log 2>&1
    [ -f $RES/states_perf.json ] || $PY -m c4.evaluate states --ckpt $RUN/final.pt --data data/perfect_test.npz --out $RES/states_perf.json --taus $TAUS --max-games 3000 > overnight/evalperf_${TAG}_s${S}.log 2>&1
    [ -f $RES/decompose.json ]   || $PY -m c4.decompose --ckpt $RUN/final.pt --data data/${TAG} --out $RES/decompose.json --games 300 --opponent-perfect > overnight/decomp_${TAG}_s${S}.log 2>&1
    $PY - <<PY
import json
a=json.load(open("$RES/states.json"))["taus"]["0.001"]; b=json.load(open("$RES/states_perf.json"))["taus"]["0.001"]; d=json.load(open("$RES/decompose.json"))
o=d["own_play"]["0.001"]
print(f"  $TAG seed$S | in-support endgame acc (ply>=8): mid={a['acc_nonbias_by_phase'][1]:.3f} late={a['acc_nonbias_by_phase'][2]:.3f} | optimal-opening endgame acc: mid={b['acc_nonbias_by_phase'][1]:.3f} late={b['acc_nonbias_by_phase'][2]:.3f} | own-play vs perfect: score={o['score']:.3f} acc by phase={[round(x['acc'],3) for x in o['by_phase']]} seen frac={[round(x,2) if x is not None else None for x in o['seen_frac_by_phase']]}")
PY
  done
done
echo "[$(date +%H:%M:%S)] COMPOSITION QUEUE DONE"
