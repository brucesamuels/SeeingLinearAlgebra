import numpy as np
import pytest

from engine.computing_eigenvalues import (
    DEFAULT_MATRIX,
    EXPECTED_EIGENVALUES,
    EigenvalueComputationLesson,
)


def test_cp172_uses_clean_3x3_example() -> None:
    assert np.array_equal(
        DEFAULT_MATRIX,
        np.array([[4.0, 1.0, 0.0], [2.0, 3.0, 0.0], [0.0, 0.0, 1.0]]),
    )


def test_identity_is_3x3() -> None:
    lesson = EigenvalueComputationLesson(DEFAULT_MATRIX)
    assert np.array_equal(lesson.identity, np.eye(3))


def test_characteristic_coefficients_are_lambda_cubed_minus_8lambda_squared_plus_17lambda_minus_10() -> None:
    lesson = EigenvalueComputationLesson(DEFAULT_MATRIX)
    assert np.allclose(
        lesson.characteristic_coefficients(),
        np.array([1.0, -8.0, 17.0, -10.0]),
    )


def test_eigenvalues_are_one_two_and_five() -> None:
    lesson = EigenvalueComputationLesson(DEFAULT_MATRIX)
    assert np.allclose(lesson.eigenvalues(), EXPECTED_EIGENVALUES)


def test_shifted_matrices_are_singular_at_all_three_roots() -> None:
    lesson = EigenvalueComputationLesson(DEFAULT_MATRIX)
    for root in EXPECTED_EIGENVALUES:
        assert np.linalg.det(lesson.shifted_matrix(root)) == pytest.approx(0.0)


def test_data_collects_3x3_information() -> None:
    data = EigenvalueComputationLesson(DEFAULT_MATRIX).data()
    assert data.matrix.shape == (3, 3)
    assert np.allclose(data.eigenvalues, EXPECTED_EIGENVALUES)


def test_non_3x3_matrix_shape_is_rejected() -> None:
    with pytest.raises(ValueError, match="shape"):
        EigenvalueComputationLesson([[1, 2], [3, 4]])
