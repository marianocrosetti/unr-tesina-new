"""Fuerza relativa: W/D/L de cada jugador contra cada otro, mismas aperturas aleatorias para todos los pares,
alternando colores. Uso: roundrobin.py <n_partidas_por_par> [workers]"""
import json, sys, time, random, itertools
from multiprocessing import Pool
from pathlib import Path
from experts import Expert, play_game, save_caches, Game
from c4solver import Position

HERE = Path(__file__).resolve().parent
PLAYERS = {"optimo": 15, "sin_D1": 11, "sin_D2": 7, "sin_H": 13, "sin_V": 14, "sin_D1D2": 3, "random": 0}
KRANGE = tuple(int(x) for x in __import__("os").environ.get("KRANGE", "8,12").split(","))
OUT = __import__("os").environ.get("RR_OUT", "roundrobin.json")

class RandomExpert:
    name = "random"
    def move(self, pos, rng): return rng.choice(pos.legal_moves())

def make(name):
    return RandomExpert() if name == "random" else Expert(PLAYERS[name], tiebreak=__import__("os").environ.get("TIEBREAK", "hash"))

def worker(args):
    a, b, n, seed = args
    rng = random.Random(seed)
    ea, eb = make(a), make(b)
    res = {"a": a, "b": b, "a_win": 0, "b_win": 0, "draw": 0, "lengths": [], "games": []}
    for i in range(n):
        k = rng.randint(*KRANGE)
        # misma apertura para las dos coloraciones: la sorteamos y la reproducimos
        opening = None
        for color in (0, 1):
            r2 = random.Random(seed * 1000 + i)
            e1, e2 = (ea, eb) if color == 0 else (eb, ea)
            g = play_game(e1, e2, r2, k)
            first_is_a = (color == 0)
            if g.result == 0: res["draw"] += 1
            elif (g.result == 1) == first_is_a: res["a_win"] += 1
            else: res["b_win"] += 1
            res["lengths"].append(len(g.moves))
            res["games"].append({"moves": g.moves, "n_random": k, "a_is_first": first_is_a, "result": g.result})
    save_caches()
    return res

if __name__ == "__main__":
    n = int(sys.argv[1]); workers = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    names = list(PLAYERS)
    pairs = list(itertools.combinations(names, 2)) + [(x, x) for x in names]
    only = __import__("os").environ.get("ONLY_VS")  # p.ej. "optimo,random": solo pares que incluyen a uno de estos
    if only:
        anchors = only.split(",")
        pairs = [(a, b) for a, b in pairs if (a in anchors) != (b in anchors)]
    t = time.time()
    with Pool(workers) as pool:
        results = pool.map(worker, [(a, b, n, 7 + i) for i, (a, b) in enumerate(pairs)])
    json.dump(results, open(HERE / "data" / OUT, "w"), indent=1)
    print(f"round robin: {len(pairs)} pares x {2*n} partidas en {time.time()-t:.0f}s")
