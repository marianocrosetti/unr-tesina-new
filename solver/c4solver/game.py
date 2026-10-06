"""Reglas de Connect 4 (7 columnas x 6 filas) y representación de posiciones.

Convenciones (las mismas que el solver de Pons y que la redacción de la tesina):
- Las columnas se numeran 1..7 de izquierda a derecha.
- Una posición se identifica por su secuencia de jugadas, p. ej. "4453" (la notación de Pons).
- El jugador 1 mueve primero. `player_to_move` es 1 o 2.
- Una jugada es legal si la columna no está llena y la partida no terminó.
"""
from __future__ import annotations

WIDTH = 7
HEIGHT = 6
COLUMNS = tuple(range(1, WIDTH + 1))
MAX_MOVES = WIDTH * HEIGHT  # 42

_DIRECTIONS = ((1, 0), (0, 1), (1, 1), (1, -1))


class Position:
    """Posición inmutable de Connect 4, construida a partir de una secuencia de jugadas.

    Lanza ValueError si la secuencia contiene una jugada ilegal (columna fuera de rango,
    columna llena o jugada posterior al fin de la partida).
    """

    __slots__ = ("moves", "_grid", "_heights", "_winner")

    def __init__(self, moves: str = ""):
        self.moves = ""
        self._grid = [[0] * HEIGHT for _ in range(WIDTH)]  # _grid[col-1][row] = 0 vacío, 1 o 2
        self._heights = [0] * WIDTH
        self._winner: int | None = None
        for ch in moves:
            if ch not in "1234567":
                raise ValueError(f"jugada inválida {ch!r} en {moves!r}: las columnas van de 1 a 7")
            self._play_inplace(int(ch))

    # --- construcción -----------------------------------------------------------------
    def _play_inplace(self, col: int) -> None:
        if self.is_terminal():
            raise ValueError(f"la partida ya terminó después de {self.moves!r}; no se puede jugar {col}")
        if not 1 <= col <= WIDTH:
            raise ValueError(f"columna {col} fuera de rango 1..7")
        row = self._heights[col - 1]
        if row >= HEIGHT:
            raise ValueError(f"columna {col} llena en {self.moves!r}")
        player = self.player_to_move
        self._grid[col - 1][row] = player
        self._heights[col - 1] = row + 1
        self.moves += str(col)
        if self._is_winning_cell(col - 1, row, player):
            self._winner = player

    def _is_winning_cell(self, c: int, r: int, player: int) -> bool:
        grid = self._grid
        for dc, dr in _DIRECTIONS:
            n = 1
            for sign in (1, -1):
                cc, rr = c + sign * dc, r + sign * dr
                while 0 <= cc < WIDTH and 0 <= rr < HEIGHT and grid[cc][rr] == player:
                    n += 1
                    cc += sign * dc
                    rr += sign * dr
            if n >= 4:
                return True
        return False

    def play(self, col: int) -> "Position":
        """Devuelve la posición resultante de jugar `col`. No modifica `self`."""
        new = Position.__new__(Position)
        new.moves = self.moves
        new._grid = [column[:] for column in self._grid]
        new._heights = self._heights[:]
        new._winner = self._winner
        new._play_inplace(col)
        return new

    # --- consulta ---------------------------------------------------------------------
    @property
    def n_moves(self) -> int:
        return len(self.moves)

    @property
    def player_to_move(self) -> int:
        """1 o 2. Aunque la partida haya terminado, indica quién movería a continuación."""
        return 1 + (len(self.moves) & 1)

    def winner(self) -> int | None:
        """1 o 2 si alguien conectó cuatro, None si no (partida en curso o empate)."""
        return self._winner

    def is_draw(self) -> bool:
        return self._winner is None and len(self.moves) == MAX_MOVES

    def is_terminal(self) -> bool:
        return self._winner is not None or len(self.moves) == MAX_MOVES

    def legal_moves(self) -> list[int]:
        """Columnas jugables (1..7). Lista vacía si la partida terminó."""
        if self.is_terminal():
            return []
        return [c for c in COLUMNS if self._heights[c - 1] < HEIGHT]

    def is_legal(self, col: int) -> bool:
        return col in self.legal_moves()

    def cell(self, col: int, row: int) -> int:
        """Contenido de la celda (columna 1..7, fila 1..6 de abajo hacia arriba): 0, 1 o 2."""
        return self._grid[col - 1][row - 1]

    def board_key(self) -> str:
        """Clave canónica del tablero, independiente del orden de las jugadas.

        Dos secuencias distintas que llegan al mismo tablero (transposiciones) tienen la misma clave.
        """
        return "".join("".join(".XO"[v] for v in column) for column in self._grid)

    # --- representación ---------------------------------------------------------------
    def __str__(self) -> str:
        rows = []
        for r in range(HEIGHT - 1, -1, -1):
            rows.append(" ".join(".XO"[self._grid[c][r]] for c in range(WIDTH)))
        rows.append(" ".join(str(c) for c in COLUMNS))
        return "\n".join(rows)

    def __repr__(self) -> str:
        return f"Position({self.moves!r})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Position) and self.moves == other.moves

    def __hash__(self) -> int:
        return hash(self.moves)
