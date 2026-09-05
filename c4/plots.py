"""Figures from results/<tag>/seed*/states.json and runs/<tag>/seed*/log.jsonl.

  python -m c4.plots --results results --runs runs --out results/figs
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def load_states(results: Path):
    rows = []
    for p in sorted(results.glob("*/seed*/states.json")):
        d = json.loads(p.read_text())
        tag = p.parents[1].name
        rows.append((tag, p.parent.name, d))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default="results"); ap.add_argument("--runs", default="runs"); ap.add_argument("--out", default="results/figs")
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    rows = load_states(Path(a.results))
    if not rows:
        print("no results found"); return
    by_tag = defaultdict(list)
    for tag, seed, d in rows:
        by_tag[tag].append(d)

    # Fig 1: E[r] vs tau per condition (mean ± std over seeds) + best-expert line, two panels -------
    fam = {"iid / other": [t for t in by_tag if not t.startswith("sel_")], "selection (α sweep)": [t for t in by_tag if t.startswith("sel_")]}
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
    for ax, (name, tags) in zip(axes, fam.items()):
        for tag in sorted(tags):
            ds = by_tag[tag]
            taus = sorted(float(t) for t in ds[0]["taus"])
            er = np.array([[d["taus"][str(t)]["er"] for t in taus] for d in ds])
            m, s_ = er.mean(0), er.std(0)
            line, = ax.plot(taus, m, marker="o", ms=4, label=tag)
            ax.fill_between(taus, m - s_, m + s_, alpha=0.2, color=line.get_color())
            ax.axhline(np.mean([d["expert"]["best_er"] for d in ds]), ls="--", lw=0.8, color=line.get_color())
        ax.set_xscale("log"); ax.set_xlabel("temperature τ"); ax.set_title(name); ax.legend(fontsize=6)
    axes[0].set_ylabel("expected reward E[r] on held-out expert states")
    fig.suptitle("Imitator reward vs temperature (dashed = best expert of that condition)")
    fig.tight_layout(); fig.savefig(out / "fig1_reward_vs_tau.png", dpi=150); plt.close(fig)

    # Fig 2: transcendence gain at min tau vs pi (iid family), with theory line rho*(1-pi) -------
    pts = defaultdict(list); rho_seen = set()
    for tag, ds in by_tag.items():
        m = re.fullmatch(r"iid_rho([\d.]+)_pi([\d.]+)", tag)
        if not m:
            continue
        rho, pi = float(m.group(1)), float(m.group(2)); rho_seen.add(rho)
        for d in ds:
            tmin = str(min(float(t) for t in d["taus"]))
            pts[(rho, pi)].append((d["taus"][tmin]["acc"] - d["expert"]["best_acc"],
                                  d["taus"][tmin]["er"] - d["expert"]["best_er"],
                                  d["theory"]["acc_gain_tau0"]))
    if pts:
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        for rho in sorted(rho_seen):
            pis = sorted(pi for (r_, pi) in pts if r_ == rho)
            for j, (name, ax) in enumerate(zip(["accuracy gain (P(optimal) − expert)", "reward gain (E[r] − best expert)"], axes)):
                vals = [np.array([v[j] for v in pts[(rho, pi)]]) for pi in pis]
                ax.errorbar(pis, [v.mean() for v in vals], yerr=[v.std() for v in vals], marker="o", capsize=3, label=f"ρ={rho}")
                if j == 0:
                    ax.plot(pis, [np.mean([v[2] for v in pts[(rho, pi)]]) for pi in pis], ls=":", color="k",
                            label=f"theory: realized random-error rate, ρ={rho}")
                ax.axhline(0, color="gray", lw=0.8)
                ax.set_xlabel("π = fraction of error budget that is shared"); ax.set_ylabel(name)
        axes[0].legend(fontsize=8); axes[0].set_title("τ→0 transcendence gain vs error correlation")
        fig.tight_layout(); fig.savefig(out / "fig2_gain_vs_pi.png", dpi=150); plt.close(fig)

    # Fig 6: selection — reward gain at min tau vs alpha, with the predicted threshold --------------
    sel = {t: ds for t, ds in by_tag.items() if re.fullmatch(r"sel_k\d+_a[\d.]+", t)}
    if sel:
        fig, ax = plt.subplots(figsize=(6.5, 4))
        als = sorted((float(re.search(r"_a([\d.]+)", t).group(1)), t) for t in sel)
        xs = [al for al, _ in als]
        for j, (key, lab, mk) in enumerate([("acc", "accuracy gain, P(optimal) − best expert", "o"), ("er", "reward gain, E[r] − best expert", "s")]):
            ys, es = [], []
            for al, t in als:
                v = np.array([d["taus"][str(min(float(x) for x in d["taus"]))][key] - (d["expert"]["best_er"] if key == "er" else d["expert"]["best_acc"]) for d in sel[t]])
                ys.append(v.mean()); es.append(v.std())
            ax.errorbar(xs, ys, yerr=es, marker=mk, capsize=3, label=lab)
        thr = sel[als[0][1]][0]["theory"]["alpha_threshold"]
        ax.axvline(thr, ls=":", color="k", label=f"predicted threshold α*={thr:.2f}")
        ax.axhline(0, color="gray", lw=0.8)
        ax.set_xlabel("α (routing strength: experts generate data within their expertise)"); ax.set_ylabel("gain at τ→0")
        ax.set_title("Skill selection with fully shared errors outside expertise"); ax.legend(fontsize=8)
        fig.tight_layout(); fig.savefig(out / "fig6_selection_alpha.png", dpi=150); plt.close(fig)

    # Fig 3: accuracy on bias vs non-bias states at min tau ----------------------------------------
    fig, ax = plt.subplots(figsize=(7, 4))
    labels, ab, anb = [], [], []
    for tag, ds in sorted(by_tag.items()):
        tmin = str(min(float(t) for t in ds[0]["taus"]))
        if ds[0]["taus"][tmin]["acc_bias"] is None:
            continue
        labels.append(tag); ab.append(np.mean([d["taus"][tmin]["acc_bias"] for d in ds])); anb.append(np.mean([d["taus"][tmin]["acc_nonbias"] for d in ds]))
    if labels:
        x = np.arange(len(labels)); ax.bar(x - 0.2, anb, 0.4, label="non-bias states"); ax.bar(x + 0.2, ab, 0.4, label="bias states (shared error)")
        ax.set_xticks(x); ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=7); ax.set_ylabel("P(optimal) at τ→0"); ax.legend()
        ax.set_title("Low temperature denoises random errors but reproduces shared ones")
        fig.tight_layout(); fig.savefig(out / "fig3_bias_vs_nonbias.png", dpi=150)
    plt.close(fig)

    # Fig 4: favor distributions -------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(7, 4))
    for tag in sorted(by_tag):
        for p in sorted(Path(a.results).glob(f"{tag}/seed*/states_favor.npz"))[:1]:
            f = np.load(p)["favor_min_tau"]
            ax.hist(f, bins=np.linspace(-1, 1, 81), alpha=0.4, label=f"{tag} (mean {f.mean():+.3f})", density=True)
    ax.set_xlabel("favor F(τ→0, τ=1; x) = ΔE[r] per state"); ax.set_yscale("log"); ax.legend(fontsize=6)
    ax.set_title("Where does the gain come from? (per-state change in expected reward)")
    fig.tight_layout(); fig.savefig(out / "fig4_favor.png", dpi=150); plt.close(fig)

    # Fig 7: composition — endgame accuracy on the unseen support (after optimal openings) per condition ----
    comp = sorted(t for t in by_tag if t.startswith("comp_") and "_n" in t and "_fa" in t)
    if comp:
        fig, ax = plt.subplots(figsize=(8, 4))
        labels, ins, outs, own = [], [], [], []
        for tag in comp:
            a_mid, b_mid, o_mid = [], [], []
            for p in sorted(Path(a.results).glob(f"{tag}/seed*/states.json")):
                sp = p.parent / "states_perf.json"; dp = p.parent / "decompose.json"
                if not sp.exists():
                    continue
                A = json.loads(p.read_text())["taus"]["0.001"]; B = json.loads(sp.read_text())["taus"]["0.001"]
                av = [x for x in A["acc_nonbias_by_phase"][1:] if x is not None]
                a_mid.append(np.mean(av) if av else np.nan); b_mid.append(np.mean(B["acc_nonbias_by_phase"][1:]))
                if dp.exists():
                    O = json.loads(dp.read_text())["own_play"]["0.001"]; o_mid.append(np.mean([x["acc"] for x in O["by_phase"][1:]]))
            if not a_mid:
                continue
            labels.append(tag.replace("comp_", "")); ins.append(np.nanmean(a_mid) if not all(np.isnan(a_mid)) else 0); outs.append(np.mean(b_mid)); own.append(np.mean(o_mid) if o_mid else np.nan)
        if labels:
            x = np.arange(len(labels)); w = 0.27
            ax.bar(x - w, ins, w, label="in-support endgames (B's own openings)")
            ax.bar(x, outs, w, label="endgames after OPTIMAL openings (never in training)")
            ax.bar(x + w, own, w, label="imitator's own-play endgames vs perfect")
            ax.set_xticks(x); ax.set_xticklabels(labels, rotation=20, ha="right", fontsize=8); ax.set_ylim(0.5, 1.0)
            ax.set_ylabel("P(optimal move), ply ≥ 8, τ→0"); ax.set_title("Skill composition across demonstrators with disjoint support"); ax.legend(fontsize=7)
            fig.tight_layout(); fig.savefig(out / "fig7_composition.png", dpi=150)
        plt.close(fig)

    # Fig 5: training curves -----------------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for p in sorted(Path(a.runs).glob("*/seed*/log.jsonl")):
        recs = [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
        if not recs:
            continue
        steps = [r["step"] for r in recs]
        lab = f"{p.parents[1].name}/{p.parent.name}"
        axes[0].plot(steps, [r["val_loss"] for r in recs], label=lab)
        axes[1].plot(steps, [r["acc_argmax"] for r in recs], label=lab)
        axes[1].plot(steps, [r["er_tau1"] for r in recs], ls=":", color=axes[1].lines[-1].get_color())
    axes[0].set_title("val loss"); axes[1].set_title("val: argmax accuracy (solid), E[r] at τ=1 (dotted)")
    for ax in axes:
        ax.set_xlabel("step")
    axes[1].legend(fontsize=5)
    fig.tight_layout(); fig.savefig(out / "fig5_training.png", dpi=150); plt.close(fig)
    print("figures written to", out)


if __name__ == "__main__":
    main()
