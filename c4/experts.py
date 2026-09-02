"""Synthetic experts with controllable error rate and error *correlation*.

All experts know the exact solver. Errors are injected in one of three modes:

  iid            (Theorem 3 of Zhang et al. 2024, plus a correlation knob)
      Per state, total error rate `rho`. A fraction `pi` of that error budget is
      *shared*: on "bias states" (deterministic hash of the position, h < beta = pi*rho)
      every expert plays the same deterministic wrong move. On the remaining states
      each expert independently errs with prob rho_r = (rho-beta)/(1-beta), choosing a
      uniformly random *non-optimal* legal move.
        pi = 0  -> all errors idiosyncratic  (denoisable by low temperature)
        pi = 1  -> all errors shared          (argmax of the mixture is wrong on bias states)
      Prediction: accuracy(tau->0) ~= 1 - pi*rho ; expert accuracy = 1 - rho.

  complementary  (Theorem 4). K experts; the position space is hashed into K regions;
      expert i is optimal in region i and uniformly random over legal moves elsewhere.

  blind          (shared bias localised in the opening). Every expert is optimal except
      that it never plays the centre column during the first `blind_plies` plies.
      Optional extra iid noise `rho`.

Optimality is defined by the *outcome class* (win/draw/loss) of the resulting position,
i.e. the same reward we evaluate the imitator on.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, asdict, field

import numpy as np

from .game import W, Board
from .solver import INVALID, outcome_reward

ERR_NONE, ERR_RANDOM, ERR_SHARED = 0, 1, 2


def hash01(key: str, seed: int) -> float:
    h = hashlib.blake2b(f"{seed}|{key}".encode(), digest_size=8).digest()
    return int.from_bytes(h, "little") / 2**64


@dataclass
class ExpertConfig:
    mode: str = "iid"          # iid | complementary | blind
    rho: float = 0.3           # total error rate per visited state (iid / blind extra noise)
    pi: float = 0.0            # fraction of error budget that is shared (iid only)
    k: int = 4                 # number of experts (complementary only)
    blind_plies: int = 4       # (blind only)
    bias_seed: int = 12345     # seed of the shared hash (must be common to all experts)

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(d):
        return ExpertConfig(**{k: v for k, v in d.items() if k in ExpertConfig.__dataclass_fields__})

    def n_experts(self) -> int:
        return self.k if self.mode == "complementary" else 1

    def tag(self) -> str:
        if self.mode == "iid":
            return f"iid_rho{self.rho}_pi{self.pi}"
        if self.mode == "complementary":
            return f"comp_k{self.k}"
        return f"blind_p{self.blind_plies}_rho{self.rho}"


def split_moves(scores: tuple[int, ...]):
    """-> (legal cols, optimal cols, non-optimal legal cols) under the outcome-class reward."""
    legal = [c for c in range(W) if scores[c] != INVALID]
    best = max(outcome_reward(scores[c]) for c in legal)
    opt = [c for c in legal if outcome_reward(scores[c]) == best]
    nonopt = [c for c in legal if outcome_reward(scores[c]) != best]
    return legal, opt, nonopt


class Experts:
    """Sampling + analytic move distributions for a given ExpertConfig."""

    def __init__(self, cfg: ExpertConfig):
        self.cfg = cfg
        beta = cfg.pi * cfg.rho if cfg.mode == "iid" else 0.0
        self.beta = beta
        self.rho_r = (cfg.rho - beta) / (1.0 - beta) if beta < 1 else 0.0

    # --- shared structures -------------------------------------------------
    def is_bias_state(self, board: Board) -> bool:
        return self.cfg.mode == "iid" and self.beta > 0 and hash01(board.board_key(), self.cfg.bias_seed) < self.beta

    def shared_wrong_move(self, board: Board, nonopt: list[int]) -> int:
        u = hash01(board.board_key(), self.cfg.bias_seed + 1)
        return nonopt[min(int(u * len(nonopt)), len(nonopt) - 1)]

    def region(self, board: Board) -> int:
        return min(int(hash01(board.board_key(), self.cfg.bias_seed + 2) * self.cfg.k), self.cfg.k - 1)

    # --- sampling -------------------------------------------------------------
    def sample_move(self, board: Board, scores, rng: np.random.Generator, expert_id: int = 0):
        """-> (col, err_flag, is_bias_state)."""
        legal, opt, nonopt = split_moves(scores)
        cfg = self.cfg
        if cfg.mode == "iid":
            if nonopt and self.is_bias_state(board):
                return self.shared_wrong_move(board, nonopt), ERR_SHARED, True
            if nonopt and rng.random() < self.rho_r:
                return int(rng.choice(nonopt)), ERR_RANDOM, False
            return int(rng.choice(opt)), ERR_NONE, False

        if cfg.mode == "complementary":
            if self.region(board) == expert_id:
                return int(rng.choice(opt)), ERR_NONE, False
            c = int(rng.choice(legal))
            return c, (ERR_RANDOM if c in nonopt else ERR_NONE), False

        if cfg.mode == "blind":
            if board.n_moves < cfg.blind_plies:
                cand_opt = [c for c in opt if c != W // 2]
                cand_non = [c for c in nonopt if c != W // 2]
                if cand_opt:
                    return int(rng.choice(cand_opt)), ERR_NONE, True
                if cand_non:
                    return int(rng.choice(cand_non)), ERR_SHARED, True
                return int(rng.choice(opt)), ERR_NONE, True
            if nonopt and rng.random() < cfg.rho:
                return int(rng.choice(nonopt)), ERR_RANDOM, False
            return int(rng.choice(opt)), ERR_NONE, False
        raise ValueError(cfg.mode)

    # --- analytic distributions (for evaluation) ----------------------------
    def dists(self, board: Board, scores) -> np.ndarray:
        """(n_experts, 7) move distribution of every expert at this state."""
        legal, opt, nonopt = split_moves(scores)
        cfg = self.cfg
        n = self.cfg.n_experts()
        out = np.zeros((n, W))
        if cfg.mode == "iid":
            if nonopt and self.is_bias_state(board):
                out[0, self.shared_wrong_move(board, nonopt)] = 1.0
            else:
                pr = self.rho_r if nonopt else 0.0
                out[0, opt] = (1 - pr) / len(opt)
                if nonopt:
                    out[0, nonopt] = pr / len(nonopt)
        elif cfg.mode == "complementary":
            r = self.region(board)
            for i in range(n):
                if i == r:
                    out[i, opt] = 1.0 / len(opt)
                else:
                    out[i, legal] = 1.0 / len(legal)
        elif cfg.mode == "blind":
            if board.n_moves < cfg.blind_plies:
                cand_opt = [c for c in opt if c != W // 2]
                cand_non = [c for c in nonopt if c != W // 2]
                cand = cand_opt or cand_non or opt
                out[0, cand] = 1.0 / len(cand)
            else:
                pr = cfg.rho if nonopt else 0.0
                out[0, opt] = (1 - pr) / len(opt)
                if nonopt:
                    out[0, nonopt] = pr / len(nonopt)
        return out
