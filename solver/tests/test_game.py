import pytest

from c4solver import MAX_MOVES, Position


def test_empty_position():
    p = Position()
    assert p.n_moves == 0
    assert p.player_to_move == 1
    assert p.legal_moves() == [1, 2, 3, 4, 5, 6, 7]
    assert not p.is_terminal()
    assert p.winner() is None


def test_play_is_immutable_and_alternates_players():
    p0 = Position()
    p1 = p0.play(4)
    assert p0.moves == "" and p1.moves == "4"
    assert p1.player_to_move == 2
    assert p1.cell(4, 1) == 1 and p1.cell(4, 2) == 0
    assert p1.play(4).cell(4, 2) == 2


def test_full_column_is_illegal():
    p = Position("444444")
    assert p.legal_moves() == [1, 2, 3, 5, 6, 7]
    assert not p.is_legal(4)
    with pytest.raises(ValueError):
        p.play(4)
    with pytest.raises(ValueError):
        Position("4444444")


def test_horizontal_win_ends_the_game():
    p = Position("4455667")  # X: d1 e1 f1 g1
    assert p.winner() == 1
    assert p.is_terminal()
    assert not p.is_draw()
    assert p.legal_moves() == []
    with pytest.raises(ValueError):
        p.play(1)
    with pytest.raises(ValueError):
        Position("44556671")


def test_vertical_and_diagonal_wins():
    assert Position("1212121").winner() == 1          # X: a1 a2 a3 a4
    # X: a1 b2 c3 d4 (diagonal); d1 y e1 son jugadas de relleno de X.
    assert Position("1223433454").winner() is None    # una jugada antes
    assert Position("12234334544").winner() == 1


def test_invalid_characters():
    with pytest.raises(ValueError):
        Position("48")
    with pytest.raises(ValueError):
        Position("0")


def test_board_key_is_transposition_invariant():
    a, b = Position("1234"), Position("3412")
    assert a != b
    assert a.board_key() == b.board_key()
    assert Position("1234").board_key() != Position("1243").board_key()  # colores distintos


def test_draw_on_full_board():
    # Tablero lleno sin cuatro en línea: cada columna alterna X/O desde abajo, salvo la
    # columna 4 que alterna O/X. Horizontales quedan 3+1+3, verticales alternan y toda
    # diagonal alterna salvo en una única celda, así que ninguna línea llega a 4.
    # El orden de las jugadas respeta la alternancia de turnos.
    moves = "111111" + "2" + "4" + "3" + "22222" + "4" + "33333" + "5" + "4444" + "55555" + "666666" + "777777"
    assert len(moves) == MAX_MOVES
    p = Position(moves)
    assert p.is_draw() and p.is_terminal() and p.winner() is None
    assert p.legal_moves() == []
    with pytest.raises(ValueError):
        p.play(1)
