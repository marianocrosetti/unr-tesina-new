"""Muestra estados decidibles visitados por los expertos en un archivo de partidas y calcula, para cada
estado, el conjunto óptimo real y el conjunto óptimo de cada variante ciega.
Uso: states.py <games.jsonl> <salida.jsonl> <max_estados> [workers] [masks]"""
import json, sys, time, random
from multiprocessing import Pool
from pathlib import Path
from experts import Expert, solver_for, save_caches, FULL, blind_name
from c4solver import Position

HERE = Path(__file__).resolve().parent
MASKS = [11, 7, 13, 14, 3]

def collect_states(games_file):
    """{moves: visitas} para posiciones no terminales jugadas por expertos (ply >= n_random)."""
    visits = {}
    for line in open(games_file):
        g = json.loads(line)
        m = g["moves"]
        for t in range(g["n_random"], len(m)):
            visits[m[:t]] = visits.get(m[:t], 0) + 1
    return visits

def worker(args):
    chunk, masks = args
    true = solver_for(FULL)
    out = []
    for moves, visits in chunk:
        pos = Position(moves)
        outcomes = true.move_outcomes(pos)
        if len(set(outcomes.values())) < 2:
            continue  # no decidible
        rec = {"moves": moves, "ply": len(moves), "visits": visits,
               "outcomes": {c: int(o) for c, o in outcomes.items()},
               "policies": {blind_name(m): solver_for(m).optimal_moves(pos) for m in masks}}
        out.append(rec)
    save_caches()
    return out

if __name__ == "__main__":
    games_file, out_file, max_states = sys.argv[1], sys.argv[2], int(sys.argv[3])
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 5
    masks = [int(m) for m in sys.argv[5].split(",")] if len(sys.argv) > 5 else MASKS
    visits = collect_states(games_file)
    items = list(visits.items())
    random.Random(1).shuffle(items)
    items = items[: int(max_states * 1.6)]  # ~40% no son decidibles; sobremuestreamos
    chunks = [items[i::workers] for i in range(workers)]
    t = time.time()
    with Pool(workers) as pool:
        res = pool.map(worker, [(c, masks) for c in chunks])
    recs = [r for c in res for r in c][:max_states]
    with open(out_file, "w") as f:
        for r in recs: f.write(json.dumps(r) + "\n")
    print(f"{len(recs)} estados decidibles de {len(visits)} visitados ({time.time()-t:.0f}s) -> {out_file}")
