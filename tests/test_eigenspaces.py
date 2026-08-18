import numpy as np
import pytest

from engine.eigenspaces import (
    DEFAULT_MATRIX,
    EigenspacesLesson,
    FAST_EIGENVALUE,
    SCALAR_MULTIPLES,
    SLOW_EIGENVALUE,
    SLOW_GENERATOR,
)


def test_cp170_continues_cp169_matrix() -> None:
    assert np.array_equal(DEFAULT_MATRIX, np.array([[5.0, 3.0], [3.0, 5.0]]))


def test_every_nonzero_scalar_multiple_remains_eigenvector() -> None:
    lesson = EigenspacesLesson(DEFAULT_MATRIX)
    for scalar in SCALAR_MULTIPLES:
        vector, image, eigenvalue = lesson.scalar_multiple_observation(SLOW_GENERATOR, scalar)
        assert eigenvalue == pytest.approx(2.0)
        assert np.allclose(image, 2.0 * vector)


def test_zero_scalar_is_rejected_as_eigenvector_multiple() -> None:
    lesson = EigenspacesLesson(DEFAULT_MATRIX)
    with pytest.raises(ValueError, match="nonzero"):
        lesson.scalar_multiple_observation(SLOW_GENERATOR, 0.0)


def test_shifted_matrix_for_lambda_two_has_expected_null_direction() -> None:
    lesson = EigenspacesLesson(DEFAULT_MATRIX)
    shifted = lesson.shifted_matrix(SLOW_EIGENVALUE)
    assert np.array_equal(shifted, np.array([[3.0, 3.0], [3.0, 3.0]]))
    assert np.allclose(shifted @ SLOW_GENERATOR, np.zeros(2))


def test_eigenspaces_are_null_spaces_for_both_eigenvalues() -> None:
    lesson = EigenspacesLesson(DEFAULT_MATRIX)
    for eigenvalue in (SLOW_EIGENVALUE, FAST_EIGENVALUE):
        observation = lesson.eigenspace(eigenvalue)
        assert np.linalg.norm(observation.generator) == pytest.approx(1.0)
        assert np.allclose(observation.shifted_matrix @ observation.generator, np.zeros(2), atol=1e-9)


def test_non_eigenvalue_has_trivial_null_space() -> None:
    lesson = EigenspacesLesson(DEFAULT_MATRIX)
    with pytest.raises(ValueError, match="trivial null space"):
        lesson.eigenspace(4.0)
