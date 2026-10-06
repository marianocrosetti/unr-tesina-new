"""Riesgo 1: ¿cuánto tarda cada variante en resolver (modo débil, sin libro) posiciones de apertura?"""
import subprocess, sys, time, json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

BUILD = Path(__file__).resolve().parent / "build"
POSITIONS = ["", "4", "44", "4453", "44455", "4455372", "44553721", "445537216"]
TIMEOUT = float(sys.argv[1]) if len(sys.argv) > 1 else 600

def run(variant):
    out = {}
    for pos in POSITIONS:
        t = time.time()
        try:
            r = subprocess.run([str(BUILD / variant / "c4solver"), "-a", "-w", "-b", "/dev/null"],
                               input=pos + "\n", capture_output=True, text=True, timeout=TIMEOUT)
            line = r.stdout.strip().splitlines()[-1]
            scores = line.split()[-7:]
            out[pos] = {"t": round(time.time() - t, 2), "scores": " ".join(scores)}
        except subprocess.TimeoutExpired:
            out[pos] = {"t": None, "scores": f"TIMEOUT>{TIMEOUT}s"}
            break
    return variant, out

variants = sorted(p.name for p in BUILD.iterdir() if (p / "c4solver").exists())
with ThreadPoolExecutor(max_workers=8) as ex:
    results = dict(ex.map(run, variants))
json.dump(results, open(Path(__file__).resolve().parent / "bench_results.json", "w"), indent=1)
for v in variants:
    print(f"{v:8s}", "  ".join(f"[{p or 'vacio'}] {d['t']}s {d['scores']}" for p, d in results[v].items()))
