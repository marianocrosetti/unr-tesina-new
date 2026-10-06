"""Fuerza que no depende de la apertura: contra el jugador óptimo, un experto no puede superar el valor
teórico de la posición tras la apertura aleatoria; 'conserva' si obtiene exactamente ese valor.
Reporta, por experto, P(conservar | posición ganada), P(conservar | tablas) y P(conservar) global."""
import json, sys
from collections import defaultdict
from c4solver import Position
from experts import solver_for, FULL

R = json.load(open(sys.argv[1]))
true = solver_for(FULL)
rows = defaultdict(lambda: defaultdict(lambda: [0, 0]))
for r in R:
    if "optimo" not in (r["a"], r["b"]) or r["a"] == r["b"]: continue
    other = r["b"] if r["a"] == "optimo" else r["a"]
    for g in r["games"]:
        other_is_first = (g["a_is_first"] == (r["a"] == other))
        opening = Position(g["moves"][: g["n_random"]])
        if opening.is_terminal(): continue
        val = true.outcome(opening)  # para quien mueve en la apertura
        mover_is_other = (opening.player_to_move == 1) == other_is_first
        theo = int(val) if mover_is_other else -int(val)  # valor teórico para el experto: 1 gana, 0 tablas, -1 pierde
        res = 0 if g["result"] == 0 else (1 if (g["result"] == 1) == other_is_first else -1)
        key = {1: "ganada", 0: "tablas", -1: "perdida"}[theo]
        rows[other][key][0] += 1; rows[other][key][1] += (res == theo)
        rows[other]["total"][0] += 1; rows[other]["total"][1] += (res == theo)
print("| experto | n | conserva (total) | conserva | ganada | conserva | tablas | posiciones perdidas (nada que conservar) |")
print("|---|---|---|---|---|---|")
for e in ["sin_D1", "sin_D2", "sin_H", "sin_V", "sin_D1D2", "random"]:
    d = rows[e]
    f = lambda k: f"{d[k][1]/d[k][0]:.2f} (n={d[k][0]})" if d[k][0] else "-"
    print(f"| {e} | {d['total'][0]} | {f('total')} | {f('ganada')} | {f('tablas')} | {d['perdida'][0]} |")
