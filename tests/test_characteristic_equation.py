import numpy as np
import pytest

from engine.characteristic_equation import (
    CharacteristicEquationLesson,
    DEFAULT_MATRIX,
    FAST_EIGENVALUE,
    SLOW_EIGENVALUE,
)


def test_cp171_continues_same_matrix() -> None:
    assert np.array_equal(DEFAULT_MATRIX, np.array([[5.0, 3.0], [3.0, 5.0]]))


def test_identity_matrix_is_available_for_algebraic_derivation() -> None:
    lesson = CharacteristicEquationLesson(DEFAULT_MATRIX)
    assert np.array_equal(lesson.identity, np.eye(2))


def test_shifted_matrix_has_expected_symbolic_pattern_numerically() -> None:
    lesson = CharacteristicEquationLesson(DEFAULT_MATRIX)
    assert np.array_equal(lesson.shifted_matrix(2), np.array([[3.0, 3.0], [3.0, 3.0]]))
    assert np.array_equal(lesson.shifted_matrix(8), np.array([[-3.0, 3.0], [3.0, -3.0]]))


def test_known_eigenvalues_make_shifted_matrix_singular() -> None:
    lesson = CharacteristicEquationLesson(DEFAULT_MATRIX)
    assert lesson.is_singular_at(SLOW_EIGENVALUE)
    assert lesson.is_singular_at(FAST_EIGENVALUE)


def test_characteristic_polynomial_coefficients_match_example() -> None:
    lesson = CharacteristicEquationLesson(DEFAULT_MATRIX)
    assert np.allclose(lesson.characteristic_coefficients(), np.array([1.0, -10.0, 16.0]))


def test_eigenvalues_are_two_and_eight() -> None:
    lesson = CharacteristicEquationLesson(DEFAULT_MATRIX)
    assert np.allclose(lesson.eigenvalues(), np.array([2.0, 8.0]))


def test_invalid_matrix_shape_is_rejected() -> None:
    with pytest.raises(ValueError, match="shape"):
        CharacteristicEquationLesson([[1, 2, 3], [4, 5, 6]])
