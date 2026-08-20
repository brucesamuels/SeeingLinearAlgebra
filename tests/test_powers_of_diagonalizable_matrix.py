import numpy as np
import pytest

from engine.powers_of_diagonalizable_matrix import MatrixPowersLesson


def test_default_example_uses_fourth_power() -> None:
    data = MatrixPowersLesson().data()
    assert data.exponent == 4


def test_diagonal_power_is_entrywise() -> None:
    lesson = MatrixPowersLesson(4)
    data = lesson.data()
    assert lesson.diagonal_power_is_entrywise()
    assert np.allclose(data.diagonal_power, np.diag([1.0, 16.0, 625.0]))


def test_diagonalization_power_matches_direct_power() -> None:
    lesson = MatrixPowersLesson(4)
    data = lesson.data()
    assert lesson.power_formula_holds()
    expected = np.array([[422.0, 203.0, 0.0], [406.0, 219.0, 0.0], [0.0, 0.0, 1.0]])
    assert np.allclose(data.reconstructed_power, expected)
    assert np.allclose(data.direct_power, expected)


def test_zero_power_also_works() -> None:
    lesson = MatrixPowersLesson(0)
    data = lesson.data()
    assert lesson.power_formula_holds()
    assert np.allclose(data.direct_power, np.eye(3))


def test_negative_or_noninteger_exponent_rejected() -> None:
    with pytest.raises(ValueError):
        MatrixPowersLesson(-1)
    with pytest.raises(ValueError):
        MatrixPowersLesson(2.5)
