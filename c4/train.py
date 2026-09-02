"""Train the imitator (next-token prediction on move sequences).

Usage:
  python -m c4.train --data data/iid_rho0.3_pi0.0.npz --out runs/iid_rho0.3_pi0.0/seed0 --seed 0 --epochs 3
"""
from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

import numpy as np
import torch

from .game import PAD, MOVE0, W
from .model import GPT, GPTConfig, pick_device
from .solver import outcome_reward
from .generate import SCORE_INVALID, SCORE_PAD


def load_tokens(path):
    d = np.load(path)
    return d["tokens"].astype(np.int64), d["scores"], d["n_moves"].astype(np.int64)


def reward_matrix(scores: np.ndarray) -> np.ndarray:
    """(…,7) int8 solver scores -> (…,7) float rewards; illegal -> 0."""
    r = np.where(scores > 0, 1.0, np.where(scores == 0, 0.5, 0.0))
    r[scores == SCORE_INVALID] = 0.0
    r[scores == SCORE_PAD] = 0.0
    return r


@torch.no_grad()
def quick_eval(model, tokens, scores, n_moves, device, max_games=2000, bs=512):
    """Argmax accuracy (tau->0) and expected reward at tau=1, over all non-terminal states."""
    model.eval()
    n = min(max_games, len(tokens))
    acc_arg, er_1, er_arg, count = 0.0, 0.0, 0.0, 0
    for i in range(0, n, bs):
        x = torch.from_numpy(tokens[i:i + bs]).to(device)
        logits, _ = model(x)
        lm = logits[:, :, MOVE0:MOVE0 + W].float().cpu().numpy()      # (B,44,7): prediction at position t = move t
        sc = scores[i:i + bs]                                          # (B,42,7)
        nm = n_moves[i:i + bs]
        r = reward_matrix(sc)
        opt = (r == r.max(-1, keepdims=True)) & (sc != SCORE_INVALID) & (sc != SCORE_PAD)
        B = len(x)
        for b in range(B):
            T = nm[b]
            l = lm[b, :T]                       # (T,7)
            p = np.exp(l - l.max(-1, keepdims=True)); p /= p.sum(-1, keepdims=True)
            a = l.argmax(-1)
            acc_arg += opt[b, np.arange(T), a].sum()
            er_arg += r[b, np.arange(T), a].sum()
            er_1 += (p * r[b, :T]).sum()
            count += T
    model.train()
    return {"acc_argmax": acc_arg / count, "er_argmax": er_arg / count, "er_tau1": er_1 / count}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--epochs", type=float, default=3.0)
    ap.add_argument("--steps", type=int, default=0, help="override epochs")
    ap.add_argument("--batch", type=int, default=512)
    ap.add_argument("--lr", type=float, default=6e-4)
    ap.add_argument("--min-lr", type=float, default=6e-5)
    ap.add_argument("--warmup", type=int, default=200)
    ap.add_argument("--wd", type=float, default=0.1)
    ap.add_argument("--n-layer", type=int, default=8)
    ap.add_argument("--n-head", type=int, default=8)
    ap.add_argument("--n-embd", type=int, default=256)
    ap.add_argument("--dropout", type=float, default=0.0)
    ap.add_argument("--val-frac", type=float, default=0.02)
    ap.add_argument("--eval-every", type=int, default=500)
    ap.add_argument("--ckpt-every", type=int, default=0, help="0 = only final")
    ap.add_argument("--device", default="auto")
    a = ap.parse_args()

    torch.manual_seed(a.seed); np.random.seed(a.seed)
    device = pick_device(a.device)
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)

    tokens, scores, n_moves = load_tokens(a.data)
    n_val = max(1000, int(len(tokens) * a.val_frac))
    tr, va = tokens[:-n_val], tokens[-n_val:]
    va_scores, va_nm = scores[-n_val:], n_moves[-n_val:]
    tr_t = torch.from_numpy(tr)

    cfg = GPTConfig(n_layer=a.n_layer, n_head=a.n_head, n_embd=a.n_embd, dropout=a.dropout)
    model = GPT(cfg).to(device)
    steps = a.steps or int(math.ceil(a.epochs * len(tr) / a.batch))
    decay, no_decay = [], []
    for n_, p in model.named_parameters():
        (decay if p.dim() >= 2 else no_decay).append(p)
    opt = torch.optim.AdamW([{"params": decay, "weight_decay": a.wd}, {"params": no_decay, "weight_decay": 0.0}],
                            lr=a.lr, betas=(0.9, 0.95))
    use_amp = device.type == "cuda"
    print(f"device={device} params={model.n_params()/1e6:.2f}M train_games={len(tr)} steps={steps} tokens/epoch={len(tr)*tokens.shape[1]/1e6:.1f}M")

    def lr_at(s):
        if s < a.warmup:
            return a.lr * s / a.warmup
        t = (s - a.warmup) / max(1, steps - a.warmup)
        return a.min_lr + 0.5 * (a.lr - a.min_lr) * (1 + math.cos(math.pi * t))

    log = open(out / "log.jsonl", "a")
    (out / "config.json").write_text(json.dumps({"train_args": vars(a), "model": cfg.to_dict(), "steps": steps}, indent=2))
    g = torch.Generator().manual_seed(a.seed)
    perm = torch.randperm(len(tr_t), generator=g); ptr = 0
    t0 = time.time(); model.train()
    for step in range(1, steps + 1):
        if ptr + a.batch > len(perm):
            perm = torch.randperm(len(tr_t), generator=g); ptr = 0
        idx = perm[ptr:ptr + a.batch]; ptr += a.batch
        batch = tr_t[idx].to(device, non_blocking=True)
        x, y = batch[:, :-1], batch[:, 1:]
        for grp in opt.param_groups:
            grp["lr"] = lr_at(step)
        with torch.autocast(device_type="cuda", dtype=torch.bfloat16, enabled=use_amp):
            _, loss = model(x, y, ignore_index=PAD)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()

        if step % 50 == 0 or step == 1:
            print(f"step {step}/{steps} loss {loss.item():.4f} lr {lr_at(step):.2e} {time.time()-t0:.0f}s", flush=True)
        if step % a.eval_every == 0 or step == steps:
            with torch.no_grad():
                model.eval()
                vx = torch.from_numpy(va[:2048]).to(device)
                _, vloss = model(vx[:, :-1], vx[:, 1:], ignore_index=PAD)
                model.train()
            q = quick_eval(model, va, va_scores, va_nm, device)
            rec = {"step": step, "train_loss": loss.item(), "val_loss": vloss.item(), "elapsed": time.time() - t0, **q}
            log.write(json.dumps(rec) + "\n"); log.flush()
            print("EVAL", json.dumps(rec), flush=True)
        if a.ckpt_every and step % a.ckpt_every == 0:
            torch.save({"model": model.state_dict(), "config": cfg.to_dict(), "step": step}, out / f"ckpt_{step:07d}.pt")
    torch.save({"model": model.state_dict(), "config": cfg.to_dict(), "step": steps}, out / "final.pt")
    print("done", out)


if __name__ == "__main__":
    main()
