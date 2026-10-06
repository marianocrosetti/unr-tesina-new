"""Genera partidas en paralelo. Uso: gen.py <nombre> <masks separadas por coma> <n_partidas> [workers] [kmin,kmax]
Cada partida enfrenta dos expertos de la población (con reposición) tras k jugadas aleatorias."""
import json, sys, time, random
from multiprocessing import Pool
from pathlib import Path
from experts import Expert, play_game, save_caches

HERE = Path(__file__).resolve().parent

def worker(args):
    masks, n, seed, krange = args
    rng = random.Random(seed)
    import os
    pop = [Expert(m, tiebreak=os.environ.get("TIEBREAK", "hash")) for m in masks]
    out = []
    t = time.time()
    for i in range(n):
        e1, e2 = rng.choice(pop), rng.choice(pop)
        g = play_game(e1, e2, rng, rng.randint(*krange))
        out.append(g.__dict__)
        if (i + 1) % 25 == 0:
            save_caches()
            print(f"  [seed {seed}] {i+1}/{n} partidas, {(time.time()-t)/(i+1):.1f} s/partida", flush=True)
    save_caches()
    return out

if __name__ == "__main__":
    name = sys.argv[1]
    masks = [int(m) for m in sys.argv[2].split(",")]
    n = int(sys.argv[3])
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    krange = tuple(int(x) for x in sys.argv[5].split(",")) if len(sys.argv) > 5 else (8, 12)
    per = [n // workers + (1 if i < n % workers else 0) for i in range(workers)]
    base = abs(hash(name)) % 10_000
    t = time.time()
    with Pool(workers) as pool:
        chunks = pool.map(worker, [(masks, per[i], base + i, krange) for i in range(workers)])
    games = [g for c in chunks for g in c]
    (HERE / "data").mkdir(exist_ok=True)
    with open(HERE / "data" / f"{name}.jsonl", "w") as f:
        for g in games: f.write(json.dumps(g) + "\n")
    print(f"{name}: {len(games)} partidas en {time.time()-t:.0f}s -> data/{name}.jsonl")
