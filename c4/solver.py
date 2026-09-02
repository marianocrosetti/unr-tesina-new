"""Thin wrapper around Pascal Pons' exact Connect 4 solver (third_party/connect4).

One persistent `c4solver -a [-w]` subprocess per Python process, plus an in-memory cache.
`analyze(moves)` returns 7 scores (Pons' convention: >0 current player wins, 0 draw,
<0 loses) or INVALID for full columns. In weak mode (default, ~2x faster) out-of-book
positions return only the sign (+1/0/-1); in-book positions still return the exact score.
Only the outcome class is used anywhere in this project.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

INVALID = -1000
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BIN = ROOT / "third_party" / "connect4" / "c4solver"
DEFAULT_BOOK = ROOT / "third_party" / "connect4" / "7x6.book"


def outcome_reward(score: int) -> float:
    """Reward of playing a move that yields solver score `score` for the mover.

    win=1, draw=0.5, loss=0, illegal -> -1 (never chosen; treated as reward 0 in evaluation)."""
    if score == INVALID:
        return -1.0
    if score > 0:
        return 1.0
    if score == 0:
        return 0.5
    return 0.0


class Solver:
    def __init__(self, binary: str | os.PathLike = DEFAULT_BIN, book: str | os.PathLike = DEFAULT_BOOK, weak: bool = True):
        binary, book = str(binary), str(book)
        if not os.path.exists(binary):
            raise FileNotFoundError(f"solver binary not found: {binary} (run scripts/setup.sh)")
        if not os.path.exists(book):
            raise FileNotFoundError(f"opening book not found: {book} (run scripts/setup.sh)")
        self.proc = subprocess.Popen(
            [binary, "-a", "-b", book] + (["-w"] if weak else []),
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            text=True, bufsize=1,
        )
        self.cache: dict[str, tuple[int, ...]] = {}
        self.n_calls = 0

    def analyze(self, moves: str) -> tuple[int, ...]:
        """`moves` is Pons' move string ('1'..'7'). Position must be non-terminal."""
        hit = self.cache.get(moves)
        if hit is not None:
            return hit
        self.proc.stdin.write(moves + "\n")
        self.proc.stdin.flush()
        while True:
            line = self.proc.stdout.readline()
            if not line:
                raise RuntimeError("solver process died")
            parts = line.split()
            # Echo format: "<moves> s0 s1 ... s6"; for the empty position the echo is empty.
            if len(parts) == 8 and parts[0] == moves:
                scores = tuple(int(x) for x in parts[1:])
                break
            if len(parts) == 7 and moves == "":
                scores = tuple(int(x) for x in parts)
                break
            # anything else (e.g. "Loading opening book ...") is skipped
        self.cache[moves] = scores
        self.n_calls += 1
        return scores

    def close(self):
        try:
            self.proc.stdin.close()
            self.proc.terminate()
        except Exception:
            pass

    def __del__(self):
        self.close()


if __name__ == "__main__":
    import time
    s = Solver()
    for pos in ["", "4", "44", "4444", "4453", "12345671234567"]:
        t = time.perf_counter()
        sc = s.analyze(pos)
        print(f"{pos!r:20} {sc}  {1e3*(time.perf_counter()-t):.2f} ms")
