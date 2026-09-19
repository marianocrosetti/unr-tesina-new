"""Decompose the imitator's gain over the experts by *where* it is measured.

Three state populations:
  seen        : held-out expert states whose board position occurs in the training set
  unseen      : held-out expert states never seen in training (same expert distribution)
  own-play    : states the imitator itself reaches when playing against the expert bot
                (the distribution behind head-to-head match scores and, in the chess paper, ratings)

For each population and temperature: imitator E[r], expert E[r] on the same states (analytic),
mixture-argmax E[r] (the theoretical tau->0 ceiling), P(optimal), and the gain.

  python -m c4.decompose --ckpt runs/iid_rho0.3_pi1.0/seed0/final.pt --data data/iid_rho0.3_pi1.0 \
      --out results/iid_rho0.3_pi1.0/seed0/decompose.json --games 300
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import torch

from .evaluate import load_model, load_meta, all_logits, softmax
from .experts import ExpertConfig, Experts
from .game import Board, BOS, MOVE0, W, col_to_tok, tok_to_col, MOVE_TOKENS
from .generate import SCORE_INVALID
from .model import pick_device
from .solver import Solver, INVALID
from .train import reward_matrix


def training_positions(train_npz: str, val_frac=0.02) -> set[str]:
    d = np.load(train_npz)
    toks, nm = d["tokens"], d["n_moves"].astype(int)
    n_val = max(1000, int(len(toks) * val_frac))
    seen = set()
    for g in range(len(toks) - n_val):
        b = Board()
        seen.add(b.board_key())
        for t in range(nm[g]):
            b.play(tok_to_col(int(toks[g, 1 + t])))
            if not b.is_terminal():
                seen.add(b.board_key())
    return seen


def summarize(er_model: dict, er_exp, er_argmax, acc_model: dict, mask, name):
    n = int(mask.sum())
    if n == 0:
        return {"n": 0}
    out = {"n": n, "expert_er": float(er_exp[mask].mean()), "mixture_argmax_er": float(er_argmax[mask].mean())}
    for tau, er in er_model.items():
        out[f"model_er_tau{tau}"] = float(er[mask].mean())
        out[f"gain_tau{tau}"] = float(er[mask].mean() - er_exp[mask].mean())
        out[f"acc_tau{tau}"] = float(acc_model[tau][mask].mean())
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True); ap.add_argument("--data", required=True, help="dataset prefix (without .npz)")
    ap.add_argument("--out", required=True); ap.add_argument("--games", type=int, default=300)
    ap.add_argument("--max-test-games", type=int, default=3000); ap.add_argument("--device", default="auto")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--opponent-perfect", action="store_true", help="own-play vs a perfect (solver) opponent instead of the dataset's expert")
    a = ap.parse_args()
    device = pick_device(a.device); model = load_model(a.ckpt, device)
    meta = load_meta(a.data + "_test.npz"); cfg = ExpertConfig.from_dict(meta["expert"]); experts = Experts(cfg)
    taus = [0.001, 1.0]

    print("indexing training positions ...", flush=True)
    seen = training_positions(a.data + ".npz")
    print(f"  {len(seen)} distinct training positions", flush=True)

    # ---- held-out expert states -------------------------------------------------------------
    d = np.load(a.data + "_test.npz"); n = min(a.max_test_games, len(d["tokens"]))
    tokens, scores, err = d["tokens"][:n], d["scores"][:n], d["err"][:n]
    logits = all_logits(model, tokens, device)
    gi, ti = np.nonzero(err >= 0)
    Lm = logits[gi, ti][:, MOVE0:MOVE0 + W]; sc = scores[gi, ti]; r = reward_matrix(sc)
    legal = sc != SCORE_INVALID; opt = (r == r.max(-1, keepdims=True)) & legal
    S = len(gi); is_seen = np.zeros(S, bool); er_exp = np.zeros(S); er_arg = np.zeros(S); phase = np.digitize(ti, [8, 20])
    for s in range(S):
        b = Board()
        for m in tokens[gi[s], 1:1 + ti[s]]:
            b.play(tok_to_col(int(m)))
        is_seen[s] = b.board_key() in seen
        sc_t = tuple(INVALID if v == SCORE_INVALID else int(v) for v in sc[s])
        dist = experts.dists(b, sc_t); w = experts.mixture_weights(b)
        er_exp[s] = (w @ dist) @ r[s]                       # the mixture's expected reward (= a random expert's)
        mix = w @ dist
        er_arg[s] = r[s][int(np.argmax(mix))]               # theoretical tau->0 ceiling: argmax of the true mixture
    er_model = {t: (softmax(Lm, t) * r).sum(-1) for t in taus}
    acc_model = {t: (softmax(Lm, t) * opt).sum(-1) for t in taus}
    res = {"ckpt": a.ckpt, "data": a.data, "expert_cfg": cfg.to_dict(), "n_train_positions": len(seen),
           "expert_states": {
               "all": summarize(er_model, er_exp, er_arg, acc_model, np.ones(S, bool), "all"),
               "seen": summarize(er_model, er_exp, er_arg, acc_model, is_seen, "seen"),
               "unseen": summarize(er_model, er_exp, er_arg, acc_model, ~is_seen, "unseen"),
               "seen_frac_by_phase": [float(is_seen[phase == k].mean()) for k in range(3)],
               "unseen_by_phase": [summarize(er_model, er_exp, er_arg, acc_model, ~is_seen & (phase == k), f"unseen_p{k}") for k in range(3)],
           }}
    print(json.dumps(res["expert_states"], indent=1), flush=True)

    # ---- own-play states: imitator (tau) vs expert bot --------------------------------------
    solver = Solver(); rng = np.random.default_rng(a.seed)
    opp = Experts(ExpertConfig(mode="iid", rho=0.0)) if a.opponent_perfect else experts
    opp_cfg = opp.cfg
    own = {}
    for tau in taus:
        rows = []  # (seen, ply, er_model_move, er_expert, er_argmax, model_acc)
        results = {"win": 0, "draw": 0, "loss": 0, "illegal": 0}
        for g in range(a.games):
            model_first = g % 2 == 0; b = Board(); eid = int(rng.integers(opp_cfg.n_experts()))
            while not b.is_terminal():
                sc_t = solver.analyze(b.solver_key()); rv = np.array([0.0 if v == INVALID else (1.0 if v > 0 else 0.5 if v == 0 else 0.0) for v in sc_t])
                if (b.player == 0) == model_first:
                    with torch.no_grad():
                        x = torch.tensor([[BOS] + [col_to_tok(m) for m in b.moves]], device=device)
                        l = model(x)[0][0, -1].float().cpu().numpy()
                    p = softmax(l[None], tau)[0]; legal_set = set(b.legal()); col = None
                    for _ in range(5):
                        t = int(rng.choice(len(p), p=p))
                        if t in MOVE_TOKENS and tok_to_col(t) in legal_set:
                            col = tok_to_col(t); break
                    dist = experts.dists(b, sc_t); mix = experts.mixture_weights(b) @ dist
                    best = rv.max()
                    rows.append((b.board_key() in seen, b.n_moves, rv[col] if col is not None else 0.0, float(mix @ rv), rv[int(np.argmax(mix))],
                                 float(rv[col] == best) if col is not None else 0.0))
                    if col is None:
                        results["illegal"] += 1; results["loss"] += 1; break
                else:
                    col, _, _ = opp.sample_move(b, sc_t, rng, eid)
                b.play(col)
            else:
                if b.winner is None: results["draw"] += 1
                elif (b.winner == 0) == model_first: results["win"] += 1
                else: results["loss"] += 1
        A = np.array(rows, dtype=float); sn = A[:, 0] > 0.5; ph = np.digitize(A[:, 1], [8, 20])
        def summ(m):
            return {"n": int(m.sum()), "model_er": float(A[m, 2].mean()), "expert_er": float(A[m, 3].mean()),
                    "mixture_argmax_er": float(A[m, 4].mean()), "gain": float(A[m, 2].mean() - A[m, 3].mean()), "acc": float(A[m, 5].mean())} if m.any() else {"n": 0}
        own[str(tau)] = {"match": results, "score": (results["win"] + 0.5 * results["draw"]) / a.games,
                         "all": summ(np.ones(len(A), bool)), "seen": summ(sn), "unseen": summ(~sn),
                         "seen_frac_by_phase": [float(sn[ph == k].mean()) if (ph == k).any() else None for k in range(3)],
                         "by_phase": [summ(ph == k) for k in range(3)]}
        print(f"own-play tau={tau}: {json.dumps(own[str(tau)]['match'])} score={own[str(tau)]['score']:.3f}", flush=True)
    res["own_play"] = own; res["own_play_opponent"] = opp_cfg.to_dict()
    Path(a.out).parent.mkdir(parents=True, exist_ok=True); Path(a.out).write_text(json.dumps(res, indent=2))
    print("wrote", a.out)


if __name__ == "__main__":
    main()
