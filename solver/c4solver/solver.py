"""Wrapper sobre el solver exacto de Connect 4 de Pascal Pons (third_party/connect4).

Mantiene un proceso `c4solver -a` vivo y le consulta posiciones por stdin/stdout, con caché
en memoria. Cada proceso Python debe crear su propio `Solver` (no es compartible entre
procesos; sí es reutilizable dentro de uno).

Semántica de Pons: el puntaje de una posición es para el jugador que mueve. En modo débil
(`weak=True`, el usado en la tesina) solo interesa el signo: >0 gana, 0 empata, <0 pierde.
En modo fuerte el valor absoluto codifica además en cuántas jugadas se define la partida.

Pons rechaza posiciones inválidas (jugada ilegal o partida ya terminada) sin escribir nada en
stdout, lo que colgaría la lectura. Por eso toda entrada se valida antes con `Position`, y las
posiciones terminales se resuelven acá mismo sin consultar al binario.
"""
from __future__ import annotations

import os
import subprocess
from enum import IntEnum
from pathlib import Path

from .game import COLUMNS, Position

_THIRD_PARTY = Path(__file__).resolve().parents[1] / "third_party" / "connect4"
DEFAULT_BINARY = _THIRD_PARTY / "c4solver"
DEFAULT_BOOK = _THIRD_PARTY / "7x6.book"
SETUP_HINT = "ejecutar solver/setup.sh"


class Outcome(IntEnum):
    """Resultado de una posición, con juego perfecto, para el jugador que mueve."""

    LOSS = -1
    DRAW = 0
    WIN = 1

    @property
    def reward(self) -> float:
        """r ∈ {1, ½, 0}: la recompensa usada en la tesina."""
        return {Outcome.WIN: 1.0, Outcome.DRAW: 0.5, Outcome.LOSS: 0.0}[self]

    @staticmethod
    def from_score(score: int) -> "Outcome":
        return Outcome.WIN if score > 0 else Outcome.LOSS if score < 0 else Outcome.DRAW


class Solver:
    def __init__(
        self,
        binary: str | os.PathLike = DEFAULT_BINARY,
        book: str | os.PathLike = DEFAULT_BOOK,
        weak: bool = True,
        cache_size: int = 2_000_000,
    ):
        binary, book = str(binary), str(book)
        if not os.path.exists(binary):
            raise FileNotFoundError(f"no existe el binario {binary} ({SETUP_HINT})")
        if not os.path.exists(book):
            raise FileNotFoundError(f"no existe el libro de aperturas {book} ({SETUP_HINT})")
        self.weak = weak
        self.cache_size = cache_size
        self._cache: dict[str, tuple[int, ...]] = {}
        self.n_queries = 0  # consultas que llegaron al binario (no cuenta hits de caché)
        self._proc = subprocess.Popen(
            [binary, "-a", "-b", book] + (["-w"] if weak else []),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1,
        )

    # --- API de bajo nivel ----------------------------------------------------------------
    def scores(self, pos: Position | str) -> tuple[int, ...]:
        """Puntaje crudo de Pons para cada columna 1..7 (índice 0 = columna 1).

        Columnas llenas valen -1000. La posición no puede ser terminal.
        """
        pos = _as_position(pos)
        if pos.is_terminal():
            raise ValueError(f"la posición {pos.moves!r} es terminal; Pons no la acepta")
        hit = self._cache.get(pos.moves)
        if hit is not None:
            return hit
        scores = self._query(pos.moves)
        if len(self._cache) >= self.cache_size:
            self._cache.clear()
        self._cache[pos.moves] = scores
        return scores

    def _query(self, moves: str) -> tuple[int, ...]:
        if self._proc.poll() is not None:
            raise RuntimeError("el proceso c4solver murió")
        self._proc.stdin.write(moves + "\n")
        self._proc.stdin.flush()
        while True:
            line = self._proc.stdout.readline()
            if not line:
                raise RuntimeError(f"el proceso c4solver cerró stdout al consultar {moves!r}")
            parts = line.split()
            # Eco: "<moves> s1 ... s7". Para la posición vacía el eco es solo los 7 puntajes.
            if len(parts) == 8 and parts[0] == moves:
                self.n_queries += 1
                return tuple(int(x) for x in parts[1:])
            if len(parts) == 7 and moves == "":
                self.n_queries += 1
                return tuple(int(x) for x in parts)
            # cualquier otra línea (mensajes informativos) se ignora

    # --- API de alto nivel: lo que usan los experimentos -----------------------------------
    def move_outcomes(self, pos: Position | str) -> dict[int, Outcome]:
        """Resultado, para quien mueve, de cada jugada legal: {columna: Outcome}.

        Diccionario vacío si la posición es terminal.
        """
        pos = _as_position(pos)
        if pos.is_terminal():
            return {}
        scores = self.scores(pos)
        return {c: Outcome.from_score(scores[c - 1]) for c in pos.legal_moves()}

    def outcome(self, pos: Position | str) -> Outcome:
        """Resultado de la posición, con juego perfecto, para el jugador que mueve.

        En posiciones terminales se deduce de las reglas: si alguien ya ganó, quien "mueve"
        perdió; tablero lleno es empate.
        """
        pos = _as_position(pos)
        if pos.is_terminal():
            return Outcome.DRAW if pos.winner() is None else Outcome.LOSS
        return max(self.move_outcomes(pos).values())

    def reward(self, pos: Position | str, col: int) -> float:
        """r(e, c) ∈ {1, ½, 0}: recompensa de jugar la columna `col` en la posición `pos`."""
        pos = _as_position(pos)
        outcomes = self.move_outcomes(pos)
        if col not in outcomes:
            raise ValueError(f"la columna {col} no es legal en {pos.moves!r}")
        return outcomes[col].reward

    def optimal_moves(self, pos: Position | str) -> list[int]:
        """Jugadas de recompensa máxima entre las legales (puede haber varias)."""
        outcomes = self.move_outcomes(pos)
        if not outcomes:
            return []
        best = max(outcomes.values())
        return [c for c, o in outcomes.items() if o == best]

    def is_decidable(self, pos: Position | str) -> bool:
        """True si hay al menos dos clases de resultado entre las jugadas legales.

        Solo en estas posiciones es posible cometer un error (jugada legal no óptima).
        """
        return len(set(self.move_outcomes(pos).values())) >= 2

    # --- ciclo de vida --------------------------------------------------------------------
    def close(self) -> None:
        proc = getattr(self, "_proc", None)
        if proc is None or proc.poll() is not None:
            return
        try:
            proc.stdin.close()
            proc.terminate()
            proc.wait(timeout=2)
        except Exception:
            proc.kill()

    def __enter__(self) -> "Solver":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def __del__(self) -> None:
        self.close()


def _as_position(pos: Position | str) -> Position:
    return pos if isinstance(pos, Position) else Position(pos)
