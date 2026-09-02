"""Evaluate an imitator against the exact solver.

Sub-commands
  states : logit-based evaluation on held-out expert states (no sampling noise).
           For every temperature tau: expected reward E[r], P(optimal), split by bias/non-bias
           states and by game phase; expert and best-expert baselines; favor distribution.
  match  : head-to-head games (model at temperature tau vs expert bot or perfect bot),
           sampling from the full vocabulary with 5 retries on illegal output (as in the paper).

Usage:
  python -m c4.evaluate states --ckpt runs/X/seed0/final.pt --data data/X_test.npz --out results/X/seed0/states.json
  python -m c4.evaluate match  --ckpt runs/X/seed0/final.pt --data data/X_test.npz --tau 0.001 --games 400 --out results/X/seed0/match_t0.001.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import torch

from .experts import ExpertConfig, Experts
from .game import Board, BOS, MOVE0, W, col_to_tok, tok_to_col, MOVE_TOKENS
from .model import GPT, GPTConfig, pick_device
from .solver import Solver, INVALID, outcome_reward
from .generate import SCORE_INVALID, SCORE_PAD
from .train import reward_matrix

TAUS = [0.001, 0.1, 0.3, 0.5, 0.75, 1.0, 1.5]


def load_model(ckpt_path, device):
    ck = torch.load(ckpt_path, map_location="cpu")
    model = GPT(GPTConfig(**ck["config"])).to(device)
    model.load_state_dict(ck["model"]); model.eval()
    return model


def load_meta(data_path: str) -> dict:
    return json.loads(Path(str(data_path).replace(".npz", "") + ".meta.json").read_text())


@torch.no_grad()
def all_logits(model, tokens, device, bs=512):
    outs = []
    for i in range(0, len(tokens), bs):
        x = torch.from_numpy(tokens[i:i + bs].astype(np.int64)).to(device)
        logits, _ = model(x)
        outs.append(logits.float().cpu().numpy())
    return np.concatenate(outs)  # (N,44,V)


def softmax(l, tau):
    z = (l - l.max(-1, keepdims=True)) / tau
    p = np.exp(z); return p / p.sum(-1, keepdims=True)


def eval_states(a):
    device = pick_device(a.device)
    model = load_model(a.ckpt, device)
    d = np.load(a.data)
    meta = load_meta(a.data)
    cfg = ExpertConfig.from_dict(meta["expert"]); experts = Experts(cfg)
    n = min(a.max_games, len(d["tokens"]))
    tokens, scores, n_moves = d["tokens"][:n], d["scores"][:n], d["n_moves"][:n].astype(int)
    bias, err = d["bias"][:n], d["err"][:n]
    logits = all_logits(model, tokens, device)

    # Flatten all non-terminal states -----------------------------------------
    gi, ti = np.nonzero(err >= 0)                          # game idx, ply idx
    L = logits[gi, ti]                                     # (S,V) prediction of move ti
    sc = scores[gi, ti]                                    # (S,7)
    r = reward_matrix(sc)                                  # (S,7) illegal -> 0
    legal = (sc != SCORE_INVALID)
    opt = (r == r.max(-1, keepdims=True)) & legal
    is_bias = bias[gi, ti] == 1
    phase = np.digitize(ti, [8, 20])                       # 0 opening (<8) / 1 middle / 2 late
    S = len(gi)

    # Expert baselines (analytic) ---------------------------------------------
    n_exp = cfg.n_experts()
    exp_er = np.zeros((S, n_exp)); exp_acc = np.zeros((S, n_exp)); mix_er = np.zeros(S); mix_acc = np.zeros(S)
    for s in range(S):
        b = Board()
        for m in tokens[gi[s], 1:1 + ti[s]]:
            b.play(tok_to_col(int(m)))
        sc_t = tuple(INVALID if v == SCORE_INVALID else int(v) for v in sc[s])
        dist = experts.dists(b, sc_t)                      # (n_exp,7)
        exp_er[s] = dist @ r[s]
        exp_acc[s] = (dist * opt[s]).sum(-1)
        w = experts.mixture_weights(b)                     # g(i|x) (uniform except in selection mode)
        mix_er[s] = w @ exp_er[s]; mix_acc[s] = w @ exp_acc[s]

    # Realized error rates of the experts on this very test set (exact, from the generator flags)
    e = err[gi, ti]
    realized = {"error_rate": float((e != 0).mean()), "random_error_rate": float((e == 1).mean()),
                "shared_error_rate": float((e == 2).mean())}
    # Theory (iid family): tau->0 learns the shared errors and denoises the random ones
    theory = {"acc_tau0": 1.0 - realized["shared_error_rate"], "acc_expert": 1.0 - realized["error_rate"],
              "acc_gain_tau0": realized["random_error_rate"]}
    if cfg.mode == "selection":
        a_, k_ = cfg.alpha, cfg.k
        theory = {"alpha_threshold": experts.alpha_threshold(), "transcends_predicted": a_ > experts.alpha_threshold(),
                  "mixture_mass_optimal": a_ + (1 - a_) / k_, "mixture_mass_shared_wrong": (1 - a_) * (k_ - 1) / k_}

    Lm = L[:, MOVE0:MOVE0 + W]
    p_full1 = softmax(L, 1.0)
    out = {
        "ckpt": a.ckpt, "data": a.data, "expert_cfg": cfg.to_dict(), "n_games": int(n), "n_states": int(S),
        "bias_state_frac": float(is_bias.mean()), "realized": realized, "theory": theory,
        "mass_on_nonmove_tokens_tau1": float(1 - p_full1[:, MOVE0:MOVE0 + W].sum(-1).mean()),
        "mass_on_illegal_cols_tau1": float((softmax(Lm, 1.0) * ~legal).sum(-1).mean()),
        "expert": {"er": float(exp_er.mean()), "acc": float(exp_acc.mean()),
                   "best_er": float(exp_er.mean(0).max()), "best_acc": float(exp_acc.mean(0).max()),
                   "mixture_er": float(mix_er.mean()), "mixture_acc": float(mix_acc.mean()),
                   "er_bias": float(exp_er[is_bias].mean()) if is_bias.any() else None,
                   "er_nonbias": float(exp_er[~is_bias].mean()),
                   "er_by_phase": [float(exp_er[phase == k].mean()) for k in range(3)]},
        "taus": {},
    }
    for tau in a.taus:
        p = softmax(Lm, tau)
        er = (p * r).sum(-1); acc = (p * opt).sum(-1)
        rec = {
            "er": float(er.mean()), "acc": float(acc.mean()),
            "er_bias": float(er[is_bias].mean()) if is_bias.any() else None,
            "er_nonbias": float(er[~is_bias].mean()),
            "acc_bias": float(acc[is_bias].mean()) if is_bias.any() else None,
            "acc_nonbias": float(acc[~is_bias].mean()),
            "er_by_phase": [float(er[phase == k].mean()) for k in range(3)],
            "transcends_best_expert": bool(er.mean() > exp_er.mean(0).max()),
            "gain_vs_best_expert": float(er.mean() - exp_er.mean(0).max()),
        }
        out["taus"][str(tau)] = rec
    # Favor distribution: E_tau[r] - E_1[r] per state -------------------------
    er_base = (softmax(Lm, 1.0) * r).sum(-1)
    fav = {}
    for tau in a.taus:
        f = (softmax(Lm, tau) * r).sum(-1) - er_base
        fav[str(tau)] = {"mean": float(f.mean()), "std": float(f.std()),
                         "frac_abs_lt_0.01": float((np.abs(f) < 0.01).mean()),
                         "frac_gt_0.1": float((f > 0.1).mean()), "frac_lt_-0.1": float((f < -0.1).mean()),
                         "q": [float(np.quantile(f, q)) for q in (0.01, 0.05, 0.5, 0.95, 0.99)]}
    out["favor"] = fav
    outp = Path(a.out); outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(out, indent=2))
    np.savez(str(outp).replace(".json", "_favor.npz"),
             favor_min_tau=(softmax(Lm, min(a.taus)) * r).sum(-1) - er_base, ply=ti, is_bias=is_bias)
    print(json.dumps({k: v for k, v in out.items() if k != "favor"}, indent=1))


# --------------------------------------------------------------------------- matches
@torch.no_grad()
def model_move(model, board: Board, tau: float, device, rng: np.random.Generator, retries=5):
    x = torch.tensor([[BOS] + [col_to_tok(m) for m in board.moves]], device=device)
    logits, _ = model(x)
    l = logits[0, -1].float().cpu().numpy()
    p = softmax(l[None], tau)[0]
    legal = set(board.legal())
    for _ in range(retries):
        t = int(rng.choice(len(p), p=p))
        if t in MOVE_TOKENS and tok_to_col(t) in legal:
            return tok_to_col(t)
    return None  # illegal after retries -> loss


def eval_match(a):
    device = pick_device(a.device)
    model = load_model(a.ckpt, device)
    meta = load_meta(a.data)
    cfg = ExpertConfig.from_dict(meta["expert"])
    if a.opponent == "perfect":
        cfg = ExpertConfig(mode="iid", rho=0.0, pi=0.0)
    experts = Experts(cfg); solver = Solver()
    rng = np.random.default_rng(a.seed)
    res = {"win": 0, "draw": 0, "loss": 0, "illegal_loss": 0}
    for g in range(a.games):
        model_first = g % 2 == 0
        b = Board(); eid = int(rng.integers(cfg.n_experts()))
        while not b.is_terminal():
            if (b.player == 0) == model_first:
                c = model_move(model, b, a.tau, device, rng)
                if c is None:
                    res["illegal_loss"] += 1; res["loss"] += 1; break
            else:
                c, _, _ = experts.sample_move(b, solver.analyze(b.solver_key()), rng, eid)
            b.play(c)
        else:
            if b.winner is None:
                res["draw"] += 1
            elif (b.winner == 0) == model_first:
                res["win"] += 1
            else:
                res["loss"] += 1
    n = a.games
    out = {"ckpt": a.ckpt, "opponent": a.opponent, "opponent_cfg": cfg.to_dict(), "tau": a.tau, "games": n, **res,
           "score": (res["win"] + 0.5 * res["draw"]) / n}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(out, indent=2))
    print(json.dumps(out))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("states")
    s.add_argument("--ckpt", required=True); s.add_argument("--data", required=True); s.add_argument("--out", required=True)
    s.add_argument("--taus", type=float, nargs="+", default=TAUS)
    s.add_argument("--max-games", type=int, default=5000)
    s.add_argument("--device", default="auto")
    m = sub.add_parser("match")
    m.add_argument("--ckpt", required=True); m.add_argument("--data", required=True); m.add_argument("--out", required=True)
    m.add_argument("--tau", type=float, default=0.001)
    m.add_argument("--games", type=int, default=200)
    m.add_argument("--opponent", default="expert", choices=["expert", "perfect"])
    m.add_argument("--seed", type=int, default=0)
    m.add_argument("--device", default="auto")
    a = ap.parse_args()
    (eval_states if a.cmd == "states" else eval_match)(a)


if __name__ == "__main__":
    main()
