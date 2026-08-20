import numpy as np
from engine.diagonalization import DEFAULT_MATRIX, DiagonalizationLesson


def test_eigenvector_matrix_is_invertible() -> None:
    lesson = DiagonalizationLesson()
    assert abs(np.linalg.det(lesson.data().eigenvector_matrix)) > 1e-9


def test_d_is_derived_from_p_inverse_a_p() -> None:
    lesson = DiagonalizationLesson()
    data = lesson.data()
    expected = data.inverse_eigenvector_matrix @ data.matrix @ data.eigenvector_matrix
    assert np.allclose(data.diagonal_matrix, expected)


def test_derived_matrix_is_diagonal() -> None:
    lesson = DiagonalizationLesson()
    assert lesson.derived_matrix_is_diagonal()
    assert np.allclose(np.diag(lesson.data().diagonal_matrix), [1.0, 2.0, 5.0])


def test_ap_equals_pd() -> None:
    assert DiagonalizationLesson().ap_equals_pd()


def test_pdp_inverse_reconstructs_a() -> None:
    lesson = DiagonalizationLesson()
    assert lesson.is_valid_diagonalization()
    assert np.allclose(lesson.reconstruct(), DEFAULT_MATRIX)
