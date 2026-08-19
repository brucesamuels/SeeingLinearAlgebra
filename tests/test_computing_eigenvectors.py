import numpy as np
import pytest

from engine.computing_eigenvectors import (
    DEFAULT_MATRIX,
    EXPECTED_EIGENVALUES,
    EXPECTED_EIGENVECTORS,
    EigenvectorComputationLesson,
)


def test_cp173_reuses_cp172_3x3_matrix() -> None:
    assert np.array_equal(
        DEFAULT_MATRIX,
        np.array([[4.0, 1.0, 0.0], [2.0, 3.0, 0.0], [0.0, 0.0, 1.0]]),
    )


def test_expected_eigenvalues_are_one_two_five() -> None:
    assert np.array_equal(EXPECTED_EIGENVALUES, np.array([1.0, 2.0, 5.0]))


def test_all_expected_basis_vectors_satisfy_definition() -> None:
    lesson = EigenvectorComputationLesson(DEFAULT_MATRIX)
    for value, vector in EXPECTED_EIGENVECTORS.items():
        assert lesson.verify_eigenvector(value, vector)


def test_lambda_one_eigenspace_is_z_axis() -> None:
    lesson = EigenvectorComputationLesson(DEFAULT_MATRIX)
    case = lesson.cases()[0]
    assert case.eigenvalue == 1.0
    assert np.array_equal(case.basis_vector, np.array([0.0, 0.0, 1.0]))
    assert np.array_equal(case.shifted_matrix, np.array([[3.0, 1.0, 0.0], [2.0, 2.0, 0.0], [0.0, 0.0, 0.0]]))


def test_lambda_two_eigenspace_basis() -> None:
    lesson = EigenvectorComputationLesson(DEFAULT_MATRIX)
    case = lesson.cases()[1]
    assert case.eigenvalue == 2.0
    assert np.array_equal(case.basis_vector, np.array([1.0, -2.0, 0.0]))


def test_lambda_five_eigenspace_basis() -> None:
    lesson = EigenvectorComputationLesson(DEFAULT_MATRIX)
    case = lesson.cases()[2]
    assert case.eigenvalue == 5.0
    assert np.array_equal(case.basis_vector, np.array([1.0, 1.0, 0.0]))


def test_zero_vector_is_not_accepted_as_eigenvector() -> None:
    lesson = EigenvectorComputationLesson(DEFAULT_MATRIX)
    assert not lesson.verify_eigenvector(2.0, [0.0, 0.0, 0.0])


def test_wrong_vector_shape_is_rejected() -> None:
    lesson = EigenvectorComputationLesson(DEFAULT_MATRIX)
    with pytest.raises(ValueError, match="shape"):
        lesson.verify_eigenvector(2.0, [1.0, -2.0])
