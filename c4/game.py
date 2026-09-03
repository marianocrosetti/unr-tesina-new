"""Connect 4 (7x6) game state, blind-play token vocabulary.

The imitator only ever sees the move sequence (like PGN for chess), never the board.
"""
from __future__ import annotations

W, H = 7, 6
MAX_PLIES = W * H  # 42

# Vocabulary -----------------------------------------------------------------
PAD = 0
BOS = 1
MOVE0 = 2                 # tokens 2..8 = columns 0..6
RES_P1 = 9                # first player (X) wins
RES_P2 = 10               # second player (O) wins
RES_DRAW = 11
VOCAB = 12
SEQ_LEN = 1 + MAX_PLIES + 1   # BOS + moves + result = 44
MOVE_TOKENS = list(range(MOVE0, MOVE0 + W))


def col_to_tok(c: int) -> int:
    return MOVE0 + c


def tok_to_col(t: int) -> int:
    return t - MOVE0


class Board:
    """Mutable board. Player 0 (X) moves first."""

    __slots__ = ("heights", "cells", "moves", "winner")

    def __init__(self):
        self.heights = [0] * W
        self.cells = [[-1] * H for _ in range(W)]   # cells[col][row] = -1 / 0 / 1
        self.moves: list[int] = []
        self.winner: int | None = None              # None = ongoing/draw, 0/1 = winner

    @property
    def player(self) -> int:
        return len(self.moves) & 1

    @property
    def n_moves(self) -> int:
        return len(self.moves)

    def legal(self) -> list[int]:
        return [c for c in range(W) if self.heights[c] < H]

    def is_terminal(self) -> bool:
        return self.winner is not None or len(self.moves) == MAX_PLIES

    def play(self, c: int) -> None:
        r = self.heights[c]
        assert r < H, f"column {c} is full"
        p = self.player
        self.cells[c][r] = p
        self.heights[c] = r + 1
        self.moves.append(c)
        if self._wins(c, r, p):
            self.winner = p

    def _wins(self, c: int, r: int, p: int) -> bool:
        cells = self.cells
        for dc, dr in ((1, 0), (0, 1), (1, 1), (1, -1)):
            n = 1
            for s in (1, -1):
                cc, rr = c + s * dc, r + s * dr
                while 0 <= cc < W and 0 <= rr < H and cells[cc][rr] == p:
                    n += 1
                    cc += s * dc
                    rr += s * dr
            if n >= 4:
                return True
        return False

    # Keys -----------------------------------------------------------------
    def solver_key(self) -> str:
        """Move string in Pons' notation (columns 1..7)."""
        return "".join(chr(ord("1") + m) for m in self.moves)

    def board_key(self) -> str:
        """Canonical key of the *position* (independent of move order)."""
        return "".join("".join("xo."[v] if v >= 0 else "." for v in col) for col in self.cells)

    def result_token(self) -> int:
        if self.winner == 0:
            return RES_P1
        if self.winner == 1:
            return RES_P2
        return RES_DRAW


def moves_to_tokens(moves: list[int], result_tok: int | None) -> list[int]:
    """result_tok=None -> truncated transcript (no result token, padded)."""
    toks = [BOS] + [col_to_tok(m) for m in moves] + ([result_tok] if result_tok is not None else [])
    toks += [PAD] * (SEQ_LEN - len(toks))
    return toks
