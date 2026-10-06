"""Tiempo de resolución (débil, sin libro) por variante en posiciones aleatorias a distintas profundidades."""
import subprocess, sys, time, json, random
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from c4solver import Position

BUILD = Path(__file__).resolve().parent / "build"
TIMEOUT = float(sys.argv[1]) if len(sys.argv) > 1 else 60
DEPTHS = [8, 10, 12, 14]
N_PER_DEPTH = 4

def random_positions(depth, n, seed):
    rng = random.Random(seed); out = []
    while len(out) < n:
        pos = Position()
        ok = True
        for _ in range(depth):
            if pos.is_terminal(): ok = False; break
            pos = pos.play(rng.choice(pos.legal_moves()))
        if ok and not pos.is_terminal(): out.append(pos.moves)
    return out

POS = {d: random_positions(d, N_PER_DEPTH, d) for d in DEPTHS}

def run(variant):
    out = {}
    proc = subprocess.Popen([str(BUILD / variant / "c4solver"), "-a", "-w", "-b", "/dev/null"],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, bufsize=1)
    for d in DEPTHS[::-1]:  # de más profundo a menos
        times = []
        for p in POS[d]:
            t = time.time()
            proc.stdin.write(p + "\n"); proc.stdin.flush()
            # lectura con timeout vía poll
            import select
            r, _, _ = select.select([proc.stdout], [], [], TIMEOUT)
            if not r:
                times.append(None); proc.kill(); break
            proc.stdout.readline()
            times.append(round(time.time() - t, 2))
        out[d] = times
        if None in times: break
    proc.kill()
    return variant, out

variants = sorted(p.name for p in BUILD.iterdir() if (p / "c4solver").exists())
with ThreadPoolExecutor(max_workers=8) as ex:
    results = dict(ex.map(run, variants))
json.dump(results, open(Path(__file__).resolve().parent / "bench_depth.json", "w"), indent=1)
for v in variants:
    print(f"{v:8s}", "  ".join(f"ply{d}: {t}" for d, t in sorted(results[v].items())))
