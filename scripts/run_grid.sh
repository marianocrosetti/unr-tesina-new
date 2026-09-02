#!/usr/bin/env bash
# Full experiment grid. Data generation is CPU-bound (solver), training is GPU-bound.
#   N_GAMES   games per training set          (default 300k)
#   N_TEST    games per held-out test set      (default 5k)
#   SEEDS     model seeds                      (default "0 1 2")
#   EPOCHS    training epochs                  (default 3)
#   RHO       total error rate                 (default 0.3)
#   PIS       correlation knob values          (default "0.0 0.25 0.5 0.75 1.0")
#   EXTRA     also run complementary + blind conditions (default 1)
set -euo pipefail
cd "$(dirname "$0")/.."
N_GAMES=${N_GAMES:-300000}; N_TEST=${N_TEST:-5000}; SEEDS=${SEEDS:-"0 1 2"}; EPOCHS=${EPOCHS:-3}
RHO=${RHO:-0.3}; PIS=${PIS:-"0.0 0.25 0.5 0.75 1.0"}; EXTRA=${EXTRA:-1}
TAUS="0.001 0.1 0.3 0.5 0.75 1.0 1.5"

gen() { # tag, generator args...
  local TAG=$1; shift
  [ -f data/${TAG}.npz ]      || uv run python -m c4.generate --out data/${TAG}      --n-games $N_GAMES --seed 1 "$@"
  [ -f data/${TAG}_test.npz ] || uv run python -m c4.generate --out data/${TAG}_test --n-games $N_TEST  --seed 2 "$@"
}
run() { # tag
  local TAG=$1
  for S in $SEEDS; do
    [ -f runs/${TAG}/seed${S}/final.pt ] || uv run python -m c4.train --data data/${TAG}.npz --out runs/${TAG}/seed${S} \
        --seed $S --epochs $EPOCHS --ckpt-every 1000
    [ -f results/${TAG}/seed${S}/states.json ] || uv run python -m c4.evaluate states --ckpt runs/${TAG}/seed${S}/final.pt \
        --data data/${TAG}_test.npz --out results/${TAG}/seed${S}/states.json --taus $TAUS
    for T in 0.001 1.0; do
      [ -f results/${TAG}/seed${S}/match_expert_t${T}.json ] || uv run python -m c4.evaluate match \
          --ckpt runs/${TAG}/seed${S}/final.pt --data data/${TAG}_test.npz --tau $T --games 400 \
          --out results/${TAG}/seed${S}/match_expert_t${T}.json
    done
  done
}

# Core: error correlation sweep at fixed error rate ----------------------------
for PI in $PIS; do
  TAG=iid_rho${RHO}_pi${PI}
  gen $TAG --mode iid --rho $RHO --pi $PI
  run $TAG
done

if [ "$EXTRA" = "1" ]; then
  gen comp_k4 --mode complementary --k 4;                 run comp_k4        # Theorem 4
  gen blind_p4_rho0.0 --mode blind --blind-plies 4 --rho 0.0; run blind_p4_rho0.0   # user's original blindness setup
fi

uv run python -m c4.plots --results results --runs runs --out results/figs
