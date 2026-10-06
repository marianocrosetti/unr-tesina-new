"""Tasa de prefijos vistos por jugada, con la política del experto (rho=0.3, P=0)."""
import collections, pickle, random, sys, time
from multiprocessing import Pool
from c4solver import Position, Solver

RHO = 0.3
import os
WORKERS = int(os.environ.get('WORKERS', 8))

def expert_game(rng, solver):
    pos = Position()
    moves, nontrivial = [], []
    while not pos.is_terminal():
        outcomes = solver.move_outcomes(pos)
        best = max(outcomes.values())
        opt = [c for c, o in outcomes.items() if o == best]
        wrong = [c for c, o in outcomes.items() if o != best]
        nt = bool(wrong)
        if not nt:
            c = rng.choice(opt)
        elif rng.random() < RHO:
            c = rng.choice(wrong)
        else:
            c = rng.choice(opt)
        moves.append(c); nontrivial.append(nt)
        pos = pos.play(c)
    return moves, nontrivial

def worker(args):
    seed, n = args
    rng = random.Random(seed)
    with Solver() as s:
        return [expert_game(rng, s) for _ in range(n)]

def generate(n, seed, workers=WORKERS):
    per = n // workers
    with Pool(workers) as p:
        chunks = p.map(worker, [(seed * 1000 + i, per) for i in range(workers)])
    return [g for ch in chunks for g in ch]

if __name__ == "__main__":
    n_train, n_test = int(sys.argv[1]), int(sys.argv[2])
    t0 = time.time()
    train = generate(n_train, 1); test = generate(n_test, 2)
    print(f"generadas {len(train)}+{len(test)} partidas en {time.time()-t0:.0f}s", flush=True)
    pickle.dump((train, test), open(f"games_{n_train}.pkl", "wb"))
    # conteo de prefijos de train
    cnt = collections.Counter()
    for moves, _ in train:
        for t in range(0, len(moves) + 1):
            cnt[hash(''.join(map(str, moves[:t])))] += 1
    print(f"N_train={n_train}: por jugada t (estado ANTES de la jugada t+1 => prefijo de largo t)")
    print(" t | %test vistos | %test NO-triv vistos | mediana visitas (vistos) | n test")
    tot_nt = seen_nt = 0
    for t in range(0, 42):
        rows = [(hash(''.join(map(str, m[:t]))), nt[t]) for m, nt in test if len(m) > t]
        if not rows: break
        visits = [cnt[p] for p, _ in rows]
        seen = sum(v > 0 for v in visits)
        nt_rows = [(p, cnt[p]) for p, nt in rows if nt]
        nt_seen = sum(v > 0 for _, v in nt_rows)
        tot_nt += len(nt_rows); seen_nt += nt_seen
        sv = sorted(v for v in visits if v > 0)
        med = sv[len(sv)//2] if sv else 0
        print(f"{t:2d} | {100*seen/len(rows):5.0f}% | {100*nt_seen/max(1,len(nt_rows)):5.0f}% ({len(nt_rows):5d}) | {med:8d} | {len(rows)}")
    print(f"fraccion de estados no triviales de test vistos en train: {100*seen_nt/tot_nt:.1f}%")
    nt_all = [cnt[hash(''.join(map(str, m[:t])))] for m, nt in test for t in range(len(m)) if nt[t]]
    for th in (1, 10, 100):
        print(f"no triviales de test con >= {th} visitas en train: {100*sum(v >= th for v in nt_all)/len(nt_all):.1f}%")
