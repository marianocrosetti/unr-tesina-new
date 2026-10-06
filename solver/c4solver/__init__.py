"""Connect 4: reglas del juego + interfaz al solver exacto de Pascal Pons.

Uso típico:

    from c4solver import Position, Solver, Outcome

    pos = Position("4453")
    pos.legal_moves()            # [1, 2, 3, 4, 5, 6, 7]
    pos.player_to_move           # 1
    with Solver() as s:
        s.outcome(pos)           # Outcome.WIN / DRAW / LOSS para quien mueve
        s.move_outcomes(pos)     # {1: Outcome.LOSS, ..., 4: Outcome.WIN, ...}
        s.reward(pos, 4)         # 1.0
        s.optimal_moves(pos)     # [4]
        s.is_decidable(pos)      # True
"""
from .game import COLUMNS, HEIGHT, MAX_MOVES, WIDTH, Position
from .solver import DEFAULT_BINARY, DEFAULT_BOOK, Outcome, Solver

__all__ = [
    "COLUMNS", "HEIGHT", "MAX_MOVES", "WIDTH", "Position",
    "DEFAULT_BINARY", "DEFAULT_BOOK", "Outcome", "Solver",
]
