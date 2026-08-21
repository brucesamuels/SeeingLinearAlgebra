import numpy as np
import pytest

from engine.spectral_theorem import SpectralTheoremLesson


def test_default_matrix_is_symmetric() -> None:
    lesson = SpectralTheoremLesson()
    assert np.allclose(lesson.matrix, lesson.matrix.T)


def test_q_is_orthogonal() -> None:
    q = SpectralTheoremLesson().orthogonal_eigenvector_matrix()
    assert np.allclose(q.T @ q, np.eye(2))


def test_d_is_computed_from_qtaq() -> None:
    lesson = SpectralTheoremLesson()
    assert np.allclose(lesson.diagonal_matrix(), np.diag([3.0, 1.0]))


def test_reconstruction_matches_a() -> None:
    lesson = SpectralTheoremLesson()
    assert np.allclose(lesson.reconstruction(), lesson.matrix)
    assert lesson.verifies_spectral_factorization()


def test_non_symmetric_matrix_is_rejected() -> None:
    with pytest.raises(ValueError):
        SpectralTheoremLesson(np.array([[1.0, 2.0], [0.0, 1.0]]))
