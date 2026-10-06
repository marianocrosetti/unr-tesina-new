"""Expertos "ciegos": juegan óptimo en una variante de Connect 4 donde solo cuentan algunos tipos de línea.

Máscara C4_LINES: V=1, H=2, D1=4 (diagonal \\, col+1 fila-1), D2=8 (diagonal /, col+1 fila+1). 15 = juego real. El experto `Expert(mask)` consulta
el solver compilado para esa variante y juega uniformemente entre las jugadas óptimas *de la variante*.
Las partidas se juegan con las reglas reales (termina cuando alguien alinea 4 en cualquier dirección).
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from pathlib import Path

from c4solver import Position, Solver, Outcome
from c4solver.solver import DEFAULT_BOOK

HERE = Path(__file__).resolve().parent
BUILD = HERE / "build"
NAMES = {1: "V", 2: "H", 4: "D1", 8: "D2"}
FULL = 15


def variant_name(mask: int) -> str:
    return "".join(n for b, n in NAMES.items() if mask & b) or "none"


def blind_name(mask: int) -> str:
    """Nombre por lo que NO ve: 'sin_D1', 'sin_D1D2', 'optimo'."""
    missing = FULL & ~mask
    return "optimo" if missing == 0 else "sin_" + variant_name(missing)


_solvers: dict[int, Solver] = {}
CACHE_DIR = HERE / "cache"


def solver_for(mask: int) -> Solver:
    """Un proceso c4solver por variante y por proceso Python, con caché en memoria precargada
    desde disco (cache/<variante>.*.pkl). `save_caches()` vuelca lo nuevo a un archivo por pid."""
    s = _solvers.get(mask)
    if s is None:
        binary = BUILD / variant_name(mask) / "c4solver"
        book = DEFAULT_BOOK if mask == FULL else "/dev/null"
        s = _solvers[mask] = Solver(binary=binary, book=book, weak=True, cache_size=50_000_000)
        s._cache.update(load_cache(mask))
        s._n_loaded = len(s._cache)
    return s


def load_cache(mask: int) -> dict:
    import pickle
    merged = {}
    for f in CACHE_DIR.glob(f"{variant_name(mask)}.*.pkl"):
        try:
            merged.update(pickle.load(open(f, "rb")))
        except Exception:
            pass
    return merged


def save_caches() -> None:
    import os, pickle
    CACHE_DIR.mkdir(exist_ok=True)
    for mask, s in _solvers.items():
        if mask == FULL or len(s._cache) <= getattr(s, "_n_loaded", 0):
            continue  # el juego real tiene libro; no vale la pena cachearlo
        tmp = CACHE_DIR / f"{variant_name(mask)}.{os.getpid()}.pkl.tmp"
        pickle.dump(s._cache, open(tmp, "wb"))
        tmp.rename(CACHE_DIR / f"{variant_name(mask)}.{os.getpid()}.pkl")


def compact_caches() -> None:
    """Funde los archivos por pid de cada variante en uno solo."""
    import pickle
    for name in {f.name.split(".")[0] for f in CACHE_DIR.glob("*.pkl")}:
        files = list(CACHE_DIR.glob(f"{name}.*.pkl"))
        merged = {}
        for f in files:
            try: merged.update(pickle.load(open(f, "rb")))
            except Exception: pass
        pickle.dump(merged, open(CACHE_DIR / f"{name}.merged.pkl.tmp", "wb"))
        for f in files: f.unlink()
        (CACHE_DIR / f"{name}.merged.pkl.tmp").rename(CACHE_DIR / f"{name}.0.pkl")


CENTER = [4, 3, 5, 2, 6, 1, 7]
PERM_ORDERS = {  # preferencia fija de columnas por experto, elegidas para que no compartan el inicio
    "sin_D1": [1, 2, 3, 4, 5, 6, 7],      # izquierda primero
    "sin_D2": [7, 6, 5, 4, 3, 2, 1],      # derecha primero
    "sin_H": [4, 3, 5, 2, 6, 1, 7],       # centro primero
    "sin_V": [1, 7, 2, 6, 3, 5, 4],       # bordes primero
    "sin_D1D2": [3, 5, 4, 2, 6, 1, 7],    # semicentro
}


@dataclass
class Expert:
    mask: int
    p_blind: float = 1.0        # prob. de usar la política ciega en cada visita (1 = siempre ciego)
    tiebreak: str = "hash"      # uniform: azar por visita | center: la más central (regla compartida)
                                # | hash: determinista e idiosincrático (depende de estado y experto)
    name: str = field(init=False)

    def __post_init__(self):
        self.name = blind_name(self.mask) + ("" if self.p_blind == 1.0 else f"@p{self.p_blind}")

    def policy(self, pos: Position, rng: random.Random) -> list[int]:
        """Conjunto de jugadas óptimas de la variante (o del juego real si esta visita 've')."""
        mask = self.mask if (self.p_blind >= 1.0 or rng.random() < self.p_blind) else FULL
        return solver_for(mask).optimal_moves(pos)

    def move(self, pos: Position, rng: random.Random) -> int:
        V = self.policy(pos, rng)
        if self.tiebreak == "uniform" or len(V) == 1:
            return rng.choice(V)
        if self.tiebreak == "center":
            return next(c for c in CENTER if c in V)
        if self.tiebreak == "perm":
            return next(c for c in PERM_ORDERS.get(blind_name(self.mask), CENTER) if c in V)
        import hashlib
        return min(V, key=lambda c: hashlib.md5(f"{pos.moves}|{self.name}|{c}".encode()).hexdigest())


@dataclass
class Game:
    moves: str
    result: int                 # 1 = gana jugador 1, 2 = gana jugador 2, 0 = tablas
    experts: tuple[str, str]    # nombre del experto que jugó con 1 y con 2
    n_random: int               # cantidad de jugadas iniciales aleatorias


def play_game(e1: Expert, e2: Expert, rng: random.Random, n_random: int) -> Game:
    pos = Position()
    while not pos.is_terminal():
        if len(pos.moves) < n_random:
            col = rng.choice(pos.legal_moves())
        else:
            e = e1 if pos.player_to_move == 1 else e2
            col = e.move(pos, rng)
        pos = pos.play(col)
    w = pos.winner()
    return Game(pos.moves, 0 if w is None else w, (e1.name, e2.name), n_random)


def generate_games(population: list[Expert], n: int, seed: int, random_plies=(8, 12)) -> list[Game]:
    """Cada partida: dos expertos de la población (con reposición), k jugadas aleatorias iniciales
    con k ~ U[random_plies], y luego cada experto juega su política."""
    rng = random.Random(seed)
    games = []
    for _ in range(n):
        e1, e2 = rng.choice(population), rng.choice(population)
        k = rng.randint(*random_plies)
        games.append(play_game(e1, e2, rng, k))
    return games
