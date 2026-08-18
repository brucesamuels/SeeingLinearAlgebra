import numpy as np
import pytest

from engine.eigenvectors_eigenvalues import (
    DEFAULT_MATRIX,
    EIGENVECTOR_FAST,
    EIGENVECTOR_SLOW,
    EigenvectorsEigenvaluesLesson,
    LAMBDA_CASES,
)


def test_cp169_continues_cp168_symmetric_matrix() -> None:
    assert np.array_equal(DEFAULT_MATRIX, np.array([[5.0, 3.0], [3.0, 5.0]]))


def test_two_cp168_invariant_directions_have_expected_eigenvalues() -> None:
    lesson = EigenvectorsEigenvaluesLesson(DEFAULT_MATRIX)
    assert lesson.eigenpair(EIGENVECTOR_FAST).eigenvalue == pytest.approx(8.0)
    assert lesson.eigenpair(EIGENVECTOR_SLOW).eigenvalue == pytest.approx(2.0)


def test_eigenpair_images_are_scalar_multiples() -> None:
    lesson = EigenvectorsEigenvaluesLesson(DEFAULT_MATRIX)
    fast = lesson.eigenpair(EIGENVECTOR_FAST)
    slow = lesson.eigenpair(EIGENVECTOR_SLOW)
    assert np.allclose(fast.image, 8.0 * fast.vector)
    assert np.allclose(slow.image, 2.0 * slow.vector)


def test_non_eigenvector_is_rejected() -> None:
    lesson = EigenvectorsEigenvaluesLesson(DEFAULT_MATRIX)
    with pytest.raises(ValueError, match="not an eigenvector"):
        lesson.eigenpair([1.0, 0.0])


def test_zero_vector_is_not_allowed_as_an_eigenvector() -> None:
    lesson = EigenvectorsEigenvaluesLesson(DEFAULT_MATRIX)
    with pytest.raises(ValueError, match="nonzero"):
        lesson.eigenpair([0.0, 0.0])


def test_lambda_cases_cover_stretch_shrink_reverse_fixed_and_collapse() -> None:
    assert LAMBDA_CASES == (
        ("stretch", 2.0),
        ("shrink", 0.5),
        ("reverse", -1.0),
        ("fixed", 1.0),
        ("collapse", 0.0),
    )
