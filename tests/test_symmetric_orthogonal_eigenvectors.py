import numpy as np
from engine.symmetric_orthogonal_eigenvectors import SymmetricOrthogonalEigenvectorsLesson


def test_default_matrix_is_symmetric() -> None:
    lesson = SymmetricOrthogonalEigenvectorsLesson()
    assert np.allclose(lesson.matrix, lesson.matrix.T)


def test_example_eigenpairs_are_correct() -> None:
    lesson = SymmetricOrthogonalEigenvectorsLesson()
    assert lesson.verifies_eigenpairs()


def test_distinct_eigenvectors_are_orthogonal() -> None:
    lesson = SymmetricOrthogonalEigenvectorsLesson()
    assert lesson.distinct_eigenvectors_are_orthogonal()
    assert lesson.example().dot_product == 0.0


def test_orthonormal_eigenbasis_is_orthogonal_matrix() -> None:
    lesson = SymmetricOrthogonalEigenvectorsLesson()
    q = lesson.orthonormal_eigenbasis()
    assert np.allclose(q.T @ q, np.eye(2))


def test_qtaq_is_diagonal_with_eigenvalues() -> None:
    lesson = SymmetricOrthogonalEigenvectorsLesson()
    assert np.allclose(lesson.diagonal_matrix(), np.diag([3.0, 1.0]))
