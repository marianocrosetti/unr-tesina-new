import os

import pytest

from c4solver import DEFAULT_BINARY, DEFAULT_BOOK, Outcome, Position, Solver

pytestmark = pytest.mark.skipif(
    not (os.path.exists(DEFAULT_BINARY) and os.path.exists(DEFAULT_BOOK)),
    reason="falta el solver de Pons: ejecutar solver/setup.sh",
)

L, D, W = Outcome.LOSS, Outcome.DRAW, Outcome.WIN


@pytest.fixture(scope="module")
def weak():
    with Solver(weak=True) as s:
        yield s


@pytest.fixture(scope="module")
def strong():
    with Solver(weak=False) as s:
        yield s


def test_empty_position_only_center_wins(weak):
    assert weak.move_outcomes("") == {1: L, 2: L, 3: D, 4: W, 5: D, 6: L, 7: L}
    assert weak.outcome("") == W
    assert weak.optimal_moves("") == [4]
    assert weak.is_decidable("")


def test_after_center_second_player_is_lost_everywhere(weak):
    assert weak.outcome("4") == L
    assert set(weak.move_outcomes("4").values()) == {L}
    assert not weak.is_decidable("4")           # sin error posible: todas las jugadas son igual de malas
    assert weak.optimal_moves("4") == [1, 2, 3, 4, 5, 6, 7]


def test_rewards(weak):
    assert weak.reward("", 4) == 1.0
    assert weak.reward("", 3) == 0.5
    assert weak.reward("", 1) == 0.0
    with pytest.raises(ValueError):
        weak.reward("444444", 4)               # columna llena


def test_full_column_excluded(weak):
    outcomes = weak.move_outcomes("444444")
    assert 4 not in outcomes and len(outcomes) == 6
    assert weak.scores("444444")[3] == -1000   # crudo de Pons para columna llena


def test_immediate_win_detected(weak):
    # X tiene d1 e1 f1; jugar 3 o 7 gana en el acto.
    outcomes = weak.move_outcomes("445566")
    assert outcomes[3] == W and outcomes[7] == W


def test_terminal_positions_do_not_hit_the_binary(weak):
    before = weak.n_queries
    won = Position("4455667")
    assert weak.outcome(won) == L               # mueve el jugador 2, que ya perdió
    assert weak.move_outcomes(won) == {}
    assert weak.optimal_moves(won) == []
    assert not weak.is_decidable(won)
    assert weak.n_queries == before
    with pytest.raises(ValueError):
        weak.scores(won)


def test_strong_mode_gives_exact_scores(strong):
    assert strong.scores("") == (-2, -1, 0, 1, 0, -1, -2)
    assert strong.outcome("44") == W


def test_weak_mode_agrees_in_sign_with_strong(weak, strong):
    for m in ["", "4", "44", "4453", "12345671234567", "444444"]:
        ws, ss = weak.scores(m), strong.scores(m)
        assert [(x > 0) - (x < 0) for x in ws] == [(x > 0) - (x < 0) for x in ss]


def test_cache_and_position_or_string_inputs(weak):
    weak.move_outcomes("4453")
    n = weak.n_queries
    assert weak.move_outcomes(Position("4453")) == weak.move_outcomes("4453")
    assert weak.n_queries == n
