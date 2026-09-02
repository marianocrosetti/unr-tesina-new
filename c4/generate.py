"""Generate a dataset of Connect-4 games played by synthetic experts.

Output: <out>.npz with
  tokens (N,44) int8   BOS, moves, result, PAD          <- what the imitator trains on
  scores (N,42,7) int8 exact solver scores per ply       (SCORE_PAD after the game ends, SCORE_INVALID = full column)
  err    (N,42) int8   0 optimal / 1 random error / 2 shared error / -1 pad
  bias   (N,42) int8   1 if the state is a "bias state" (shared-error region) / 0 / -1 pad
  n_moves (N,) int8
and <out>.meta.json with the expert config and realized statistics.

Usage:
  python -m c4.generate --out data/iid_rho0.3_pi0.0 --n-games 300000 --rho 0.3 --pi 0.0 --seed 1
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import time
from pathlib import Path

import numpy as np

from .experts import ExpertConfig, Experts, ERR_NONE
from .game import Board, MAX_PLIES, W, moves_to_tokens, SEQ_LEN
from .solver import Solver, INVALID

SCORE_PAD = -128
SCORE_INVALID = -100


def _worker(args):
    seed, n_games, cfg_d = args
    cfg = ExpertConfig.from_dict(cfg_d)
    experts = Experts(cfg)
    solver = Solver()
    rng = np.random.default_rng(seed)

    tokens = np.zeros((n_games, SEQ_LEN), dtype=np.int8)
    scores = np.full((n_games, MAX_PLIES, W), SCORE_PAD, dtype=np.int8)
    err = np.full((n_games, MAX_PLIES), -1, dtype=np.int8)
    bias = np.full((n_games, MAX_PLIES), -1, dtype=np.int8)
    n_moves = np.zeros(n_games, dtype=np.int8)
    expert_ids = np.zeros((n_games, 2), dtype=np.int8)

    for g in range(n_games):
        b = Board()
        ids = rng.integers(cfg.n_experts(), size=2) if cfg.mode == "complementary" else np.zeros(2, dtype=int)
        expert_ids[g] = ids
        while not b.is_terminal():
            sc = solver.analyze(b.solver_key())
            t = b.n_moves
            scores[g, t] = [SCORE_INVALID if s == INVALID else s for s in sc]
            mover = experts.sample_mover(b, rng) if cfg.mode == "selection" else int(ids[b.player])
            col, e, is_bias = experts.sample_move(b, sc, rng, mover)
            err[g, t] = e
            bias[g, t] = int(is_bias)
            b.play(col)
        n_moves[g] = b.n_moves
        tokens[g] = moves_to_tokens(b.moves, b.result_token())
    solver.close()
    return tokens, scores, err, bias, n_moves, expert_ids


def generate(cfg: ExpertConfig, n_games: int, seed: int, workers: int, out: Path):
    out.parent.mkdir(parents=True, exist_ok=True)
    chunks = max(workers * 4, 1)
    per = [n_games // chunks + (1 if i < n_games % chunks else 0) for i in range(chunks)]
    jobs = [(seed * 100_000 + i, n, cfg.to_dict()) for i, n in enumerate(per) if n > 0]
    t0 = time.time()
    if workers > 1:
        with mp.get_context("spawn").Pool(workers) as pool:
            parts = pool.map(_worker, jobs)
    else:
        parts = [_worker(j) for j in jobs]
    arrays = [np.concatenate([p[i] for p in parts]) for i in range(6)]
    tokens, scores, err, bias, n_moves, expert_ids = arrays
    dt = time.time() - t0

    valid = err >= 0
    # an error is only *possible* in states where some legal move has a worse outcome class
    r = np.where(scores > 0, 1.0, np.where(scores == 0, 0.5, 0.0))
    legal = (scores != SCORE_INVALID) & (scores != SCORE_PAD)
    best = np.where(legal, r, -1).max(-1, keepdims=True)
    err_possible = ((r < best) & legal).any(-1)[valid]
    meta = {
        "expert": cfg.to_dict(),
        "tag": cfg.tag(),
        "n_games": int(n_games),
        "seed": seed,
        "seconds": round(dt, 1),
        "n_states": int(valid.sum()),
        "mean_length": float(n_moves.mean()),
        "error_rate": float((err[valid] != ERR_NONE).mean()),
        "shared_error_rate": float((err[valid] == 2).mean()),
        "random_error_rate": float((err[valid] == 1).mean()),
        "bias_state_rate": float((bias[valid] == 1).mean()),
        "error_possible_rate": float(err_possible.mean()),
        "error_rate_given_possible": float((err[valid][err_possible] != ERR_NONE).mean()),
        "result_dist": dict(zip(["p1_win", "p2_win", "draw"],
                                (np.bincount(tokens[np.arange(n_games), n_moves + 1].astype(int), minlength=12)[9:12] / n_games).tolist())),
    }
    np.savez(str(out) + ".npz", tokens=tokens, scores=scores, err=err, bias=bias, n_moves=n_moves, expert_ids=expert_ids)
    Path(str(out) + ".meta.json").write_text(json.dumps(meta, indent=2))
    return meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n-games", type=int, default=100_000)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--workers", type=int, default=max(1, mp.cpu_count() - 1))
    ap.add_argument("--mode", default="iid", choices=["iid", "complementary", "selection", "rule", "blind"])
    ap.add_argument("--rho", type=float, default=0.3)
    ap.add_argument("--pi", type=float, default=0.0)
    ap.add_argument("--k", type=int, default=4)
    ap.add_argument("--alpha", type=float, default=0.0)
    ap.add_argument("--rule-mod", type=int, default=3)
    ap.add_argument("--blind-plies", type=int, default=4)
    ap.add_argument("--bias-seed", type=int, default=12345)
    a = ap.parse_args()
    cfg = ExpertConfig(mode=a.mode, rho=a.rho, pi=a.pi, k=a.k, alpha=a.alpha, rule_mod=a.rule_mod, blind_plies=a.blind_plies, bias_seed=a.bias_seed)
    meta = generate(cfg, a.n_games, a.seed, a.workers, Path(a.out))
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
