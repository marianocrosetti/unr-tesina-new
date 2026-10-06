"""Inspección rápida de una posición: `uv run python -m c4solver 4453` (sin argumento: posición vacía)."""
import sys

from . import Position, Solver


def main(argv: list[str]) -> None:
    pos = Position(argv[1] if len(argv) > 1 else "")
    print(pos)
    print(f"jugadas: {pos.moves!r}  mueve: jugador {pos.player_to_move}")
    if pos.is_terminal():
        w = pos.winner()
        print("partida terminada:", f"gana el jugador {w}" if w else "empate")
        return
    with Solver() as s:
        outcomes = s.move_outcomes(pos)
        print("resultado de la posición (para quien mueve):", s.outcome(pos).name)
        print("por columna:", "  ".join(f"{c}:{o.name}" for c, o in outcomes.items()))
        print("óptimas:", s.optimal_moves(pos), " decidible:", s.is_decidable(pos))


if __name__ == "__main__":
    main(sys.argv)
