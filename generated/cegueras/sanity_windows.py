"""Chequeo semántico: un experto ciego a la línea L solo puede errar si queda alguna ventana de 4 de tipo L
'viva' (sin fichas de ambos colores). Si no queda ninguna, la variante y el juego real coinciden desde ahí.
Tabla: tasa de error del experto según cantidad de ventanas vivas de su tipo ciego (desempate hash)."""
import json, sys, hashlib
from collections import defaultdict
sys.path.insert(0, ".")
from report import load, best_set, apply_tiebreak
from c4solver import Position

W, H = 7, 6
DIRS = {"V": (0, 1), "H": (1, 0), "D1": (1, -1), "D2": (1, 1)}  # D1 = "\\" como en Pons (shift HEIGHT), D2 = "/"
WINDOWS = {}
for name, (dc, dr) in DIRS.items():
    ws = []
    for c in range(W):
        for r in range(H):
            cells = [(c + i * dc, r + i * dr) for i in range(4)]
            if all(0 <= cc < W and 0 <= rr < H for cc, rr in cells): ws.append(cells)
    WINDOWS[name] = ws
assert [len(WINDOWS[k]) for k in ("V","H","D1","D2")] == [21, 24, 12, 12]

def live_windows(pos, kinds):
    g = pos._grid
    n = 0
    for k in kinds:
        for cells in WINDOWS[k]:
            colors = {g[c][r] for c, r in cells} - {0}
            if len(colors) <= 1: n += 1
    return n

S = apply_tiebreak(load(sys.argv[1]), "hash")
BLIND = {"sin_D1": ["D1"], "sin_D2": ["D2"], "sin_H": ["H"], "sin_V": ["V"], "sin_D1D2": ["D1", "D2"]}
print("| experto | ventanas vivas del tipo ciego | n estados | tasa de error |")
print("|---|---|---|---|")
for name, kinds in BLIND.items():
    buckets = defaultdict(lambda: [0, 0])
    for s in S:
        pos = Position(s["moves"]); n = live_windows(pos, kinds)
        b = "0" if n == 0 else "1-2" if n <= 2 else "3-5" if n <= 5 else "6-10" if n <= 10 else "11+"
        err = s["policies"][name][0] not in best_set(s["outcomes"])
        buckets[b][0] += 1; buckets[b][1] += err
    for b in ["0", "1-2", "3-5", "6-10", "11+"]:
        if b in buckets:
            n, e = buckets[b]; print(f"| {name} | {b} | {n} | {e/n:.3f} |")
