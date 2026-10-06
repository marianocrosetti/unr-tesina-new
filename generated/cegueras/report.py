"""Métricas sobre states.jsonl + partidas + round robin. Escribe REPORT_<tag>.md y lo imprime."""
import json, sys, math, itertools
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PHASES = [(0, 14, "8-14"), (15, 21, "15-21"), (22, 28, "22-28"), (29, 42, "29+")]

def load(f): return [json.loads(l) for l in open(f)]

def phase(ply):
    for lo, hi, name in PHASES:
        if lo <= ply <= hi: return name

def best_set(outcomes):
    best = max(outcomes.values()); return {int(c) for c, o in outcomes.items() if o == best}

def err_prob(policy, T):
    return 1 - len(set(policy) & T) / len(policy)

def reward_loss(policy, outcomes):
    r = {int(c): {1: 1.0, 0: 0.5, -1: 0.0}[o] for c, o in outcomes.items()}
    best = max(r.values())
    return best - np.mean([r[c] for c in policy])

def mixture(policies):
    m = Counter()
    for p in policies:
        for c in p: m[c] += 1 / len(p) / len(policies)
    return m

def argmax_correct(m, T):
    top = max(m.values()); arg = [c for c, v in m.items() if abs(v - top) < 1e-9]
    return len(set(arg) & T) / len(arg)  # desempate uniforme

CENTER = [4, 3, 5, 2, 6, 1, 7]
PERM_ORDERS = {  # preferencia fija de columnas por experto, elegidas para que no compartan el inicio
    "sin_D1": [1, 2, 3, 4, 5, 6, 7],      # izquierda primero
    "sin_D2": [7, 6, 5, 4, 3, 2, 1],      # derecha primero
    "sin_H": [4, 3, 5, 2, 6, 1, 7],       # centro primero
    "sin_V": [1, 7, 2, 6, 3, 5, 4],       # bordes primero
    "sin_D1D2": [3, 5, 4, 2, 6, 1, 7],    # semicentro
}

def apply_tiebreak(S, mode):
    """uniform: el experto elige uniformemente entre sus óptimas. center: determinista, la más central
    (misma regla para todos). hash: determinista, orden pseudoaleatorio propio de cada experto y estado."""
    import hashlib
    if mode == "uniform": return S
    out = []
    for s in S:
        s = dict(s); pol = {}
        for n, V in s["policies"].items():
            if mode == "center":
                pol[n] = [next(c for c in CENTER if c in V)]
            elif mode == "perm":
                order = PERM_ORDERS.get(n.split("@")[0], CENTER)
                pol[n] = [next(c for c in order if c in V)]
            else:
                key = lambda c: hashlib.md5(f"{s['moves']}|{n}|{c}".encode()).hexdigest()
                pol[n] = [min(V, key=key)]
        s["policies"] = pol; out.append(s)
    return out

def main(states_file, tag, games_files=None, rr_file=None, tiebreak="uniform"):
    S = apply_tiebreak(load(states_file), tiebreak)
    names = list(S[0]["policies"])
    L = []
    L.append(f"# Reporte {tag} (desempate: {tiebreak})\n")
    L.append(f"Estados decidibles analizados: {len(S)} (de partidas con apertura aleatoria; solo jugadas de expertos).\n")
    # ---- A. error por experto y fase
    L.append("## A. Tasa de error estructural por experto (prob. de jugar no óptimo en un estado decidible)\n")
    L.append("Tasa = 1 − |óptimas_variante ∩ óptimas_reales| / |óptimas_variante|. Pérdida = recompensa óptima − recompensa esperada de la jugada (1/½/0).\n")
    L.append("| experto | tasa total | pérdida media | " + " | ".join(f"tasa {p[2]}" for p in PHASES) + " | error seguro (∩=∅) |")
    L.append("|---|---|---|" + "---|" * len(PHASES) + "---|")
    E = {n: np.array([err_prob(s["policies"][n], best_set(s["outcomes"])) for s in S]) for n in names}
    ph = np.array([phase(s["ply"]) for s in S])
    for n in names:
        loss = np.mean([reward_loss(s["policies"][n], s["outcomes"]) for s in S])
        row = [f"{E[n].mean():.3f}", f"{loss:.3f}"] + [f"{E[n][ph == p[2]].mean():.3f} (n={int((ph == p[2]).sum())})" for p in PHASES] + [f"{(E[n] == 1).mean():.3f}"]
        L.append(f"| {n} | " + " | ".join(row) + " |")
    L.append("")
    # ---- B. correlación entre expertos
    L.append("## B. Correlación de errores entre pares de expertos\n")
    L.append("Pearson entre los vectores de tasa de error por estado; P(ambos erran seguro); Jaccard de las jugadas erróneas cuando ambos erran.\n")
    L.append("| par | Pearson | P(ambos erran) | P(ambos) si indep. | Jaccard jugadas erróneas |")
    L.append("|---|---|---|---|---|")
    for a, b in itertools.combinations(names, 2):
        both = (E[a] == 1) & (E[b] == 1)
        jac = []
        for s, flag in zip(S, both):
            if flag:
                T = best_set(s["outcomes"]); wa = set(s["policies"][a]) - T; wb = set(s["policies"][b]) - T
                jac.append(len(wa & wb) / len(wa | wb))
        r = np.corrcoef(E[a], E[b])[0, 1] if E[a].std() > 0 and E[b].std() > 0 else float("nan")
        L.append(f"| {a} / {b} | {r:.3f} | {both.mean():.3f} | {(E[a]==1).mean()*(E[b]==1).mean():.3f} | {np.mean(jac) if jac else float('nan'):.3f} (n={len(jac)}) |")
    L.append("")
    # ---- C. techo del voto por conjunto de expertos
    L.append("## C. Techo del voto (Proposición 2 de [1]) por conjunto de expertos\n")
    L.append("acc(argmax mezcla) = tasa de acierto de la jugada más probable de la mezcla equiponderada (τ→0); acc(τ=1) = masa de la mezcla sobre jugadas óptimas; mejor experto = mayor acc individual. Trascendencia por voto posible si argmax > mejor experto.\n")
    L.append("| conjunto | acc τ=1 | acc argmax (τ→0) | mejor experto | ganancia argmax − mejor | estados donde todos erran seguro | ídem por fase " + "/".join(p[2] for p in PHASES) + " |")
    L.append("|---|---|---|---|---|---|---|")
    sets = [list(c) for k in (2, 3, 4, 5) for c in itertools.combinations(names, k)]
    for st in sets:
        acc1 = np.mean([sum(mixture([s["policies"][n] for n in st])[c] for c in best_set(s["outcomes"])) for s in S])
        acc0 = np.mean([argmax_correct(mixture([s["policies"][n] for n in st]), best_set(s["outcomes"])) for s in S])
        best = max(1 - E[n].mean() for n in st)
        allerr = np.all([E[n] == 1 for n in st], axis=0)
        byph = "/".join(f"{allerr[ph == p[2]].mean():.3f}" for p in PHASES)
        L.append(f"| {' + '.join(st)} | {acc1:.3f} | {acc0:.3f} | {best:.3f} | {acc0 - best:+.3f} | {allerr.mean():.3f} (n={int(allerr.sum())}) | {byph} |")
    L.append("")
    # ---- C2. entropía de la mezcla por estado (diversidad de acciones, Fig. 5 de [1])
    L.append("## C2. Diversidad de acciones: entropía normalizada de la mezcla por estado\n")
    L.append("Entropía (base 2) de la distribución de jugadas de la mezcla equiponderada, dividida por log2(#legales); promedio sobre estados decidibles.\n")
    L.append("| conjunto | entropía media | estados con mezcla unánime |")
    L.append("|---|---|---|")
    for st in [names[:2], names[:3], names[:4], names]:
        hs, unan = [], 0
        for s in S:
            m = mixture([s["policies"][n] for n in st]); legal = len(s["outcomes"])
            h = -sum(v * math.log2(v) for v in m.values() if v > 0)
            hs.append(h / math.log2(legal) if legal > 1 else 0); unan += (len(m) == 1)
        L.append(f"| {' + '.join(st)} | {np.mean(hs):.3f} | {unan/len(S):.3f} |")
    L.append("")
    # ---- C3. ejemplos de estados de composición
    if "sin_D1" in names and "sin_D2" in names:
        from c4solver import Position
        ex = [s for s in S if err_prob(s["policies"]["sin_D1"], best_set(s["outcomes"])) == 1 and err_prob(s["policies"]["sin_D2"], best_set(s["outcomes"])) == 1]
        L.append(f"## C3. Ejemplos de estados donde sin_D1 y sin_D2 erran ambos (n={len(ex)} de {len(S)})\n")
        for s in ex[:4]:
            T = sorted(best_set(s["outcomes"]))
            L.append("```")
            L.append(str(Position(s["moves"])))
            L.append(f"jugadas: {s['moves']}  (mueve jugador {Position(s['moves']).player_to_move}, ply {s['ply']})")
            L.append(f"óptimas reales: {T}   sin_D1 juega {s['policies']['sin_D1']}   sin_D2 juega {s['policies']['sin_D2']}   resultados por columna: {s['outcomes']}")
            L.append("```")
        L.append("")
    # ---- D. diversidad de las partidas
    if games_files:
        L.append("## D. Diversidad de las partidas por población (riesgo de colapso)\n")
        L.append("Solo jugadas de expertos. Entropía normalizada de la acción en estados visitados ≥3 veces (como Fig. 5 de [1]). Partidas únicas: fracción de transcripciones distintas.\n")
        L.append("| población | partidas | únicas | largo medio | estados visitados | visitados ≥3 | entropía media (≥3) | % tablas | % gana 1 |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for gf in games_files:
            G = load(gf)
            acts = defaultdict(Counter)
            for g in G:
                for t in range(g["n_random"], len(g["moves"])):
                    acts[g["moves"][:t]][g["moves"][t]] += 1
            multi = {k: v for k, v in acts.items() if sum(v.values()) >= 3}
            ents = []
            for k, v in multi.items():
                n = sum(v.values()); legal = len([c for c in "1234567" if k.count(c) < 6])
                h = -sum(x / n * math.log2(x / n) for x in v.values())
                ents.append(h / math.log2(legal) if legal > 1 else 0)
            uniq = len({g["moves"] for g in G}) / len(G)
            L.append(f"| {Path(gf).stem} | {len(G)} | {uniq:.3f} | {np.mean([len(g['moves']) for g in G]):.1f} | {len(acts)} | {len(multi)} | {np.mean(ents) if ents else float('nan'):.3f} | {np.mean([g['result']==0 for g in G])*100:.0f}% | {np.mean([g['result']==1 for g in G])*100:.0f}% |")
        L.append("")
    # ---- E. round robin
    if rr_file and Path(rr_file).exists():
        R = load_json(rr_file)
        names_rr = sorted({r["a"] for r in R} | {r["b"] for r in R}, key=lambda n: ["optimo","sin_D1","sin_D2","sin_H","sin_V","sin_D1D2","random"].index(n))
        L.append("## E. Fuerza relativa (round robin, puntos de la fila contra la columna: W=1, D=½, mismas aperturas, ambos colores)\n")
        L.append("| | " + " | ".join(names_rr) + " | promedio |")
        L.append("|---|" + "---|" * (len(names_rr) + 1))
        score = {(r["a"], r["b"]): (r["a_win"] + 0.5 * r["draw"]) / (r["a_win"] + r["b_win"] + r["draw"]) for r in R}
        for a in names_rr:
            row = []
            for b in names_rr:
                v = score.get((a, b)); v = v if v is not None else (1 - score[(b, a)] if (b, a) in score else None)
                row.append(f"{v:.2f}" if v is not None else "-")
            vals = [float(x) for x in row if x != "-"]
            L.append(f"| **{a}** | " + " | ".join(row) + f" | {np.mean(vals):.2f} |")
        L.append("")
    text = "\n".join(L)
    (HERE / f"REPORT_{tag}.md").write_text(text)
    print(text)

def load_json(f): return json.load(open(f))

if __name__ == "__main__":
    states_file, tag = sys.argv[1], sys.argv[2]
    games = [a for a in sys.argv[3:] if a.endswith(".jsonl")]
    rr = next((a for a in sys.argv[3:] if a.endswith(".json")), None)
    tb = next((a.split("=")[1] for a in sys.argv[3:] if a.startswith("tiebreak=")), "uniform")
    main(states_file, tag, games, rr, tb)
