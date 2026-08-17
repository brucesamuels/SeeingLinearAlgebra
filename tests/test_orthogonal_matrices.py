import numpy as np

from engine.orthogonal_matrices import OrthogonalMatricesLesson


def test_q_is_orthogonal() -> None:
    snapshot = OrthogonalMatricesLesson().snapshot()
    assert np.allclose(snapshot.Q.T @ snapshot.Q, np.eye(2))
    assert np.allclose(np.linalg.inv(snapshot.Q), snapshot.Q.T)


def test_lengths_are_preserved_for_sample_vectors() -> None:
    snapshot = OrthogonalMatricesLesson().snapshot()
    assert np.isclose(np.linalg.norm(snapshot.Qu), np.linalg.norm(snapshot.u))
    assert np.isclose(np.linalg.norm(snapshot.Qv), np.linalg.norm(snapshot.v))


def test_dot_products_are_preserved() -> None:
    snapshot = OrthogonalMatricesLesson().snapshot()
    assert np.isclose(float(snapshot.Qu @ snapshot.Qv), float(snapshot.u @ snapshot.v))


def test_rotation_and_reflection_are_orthogonal_with_expected_determinants() -> None:
    snapshot = OrthogonalMatricesLesson().snapshot()
    assert np.allclose(snapshot.rotation.T @ snapshot.rotation, np.eye(2))
    assert np.allclose(snapshot.reflection.T @ snapshot.reflection, np.eye(2))
    assert np.isclose(np.linalg.det(snapshot.rotation), 1.0)
    assert np.isclose(np.linalg.det(snapshot.reflection), -1.0)


def test_lesson_formulas_are_explicit() -> None:
    lesson = OrthogonalMatricesLesson()
    assert lesson.ORTHOGONAL_TEST == r"Q^TQ=I"
    assert lesson.INVERSE_RULE == r"Q^{-1}=Q^T"
    assert lesson.LENGTH_RULE == r"\|Q\mathbf v\|=\|\mathbf v\|"
    assert lesson.DOT_RULE == r"(Q\mathbf u)^T(Q\mathbf v)=\mathbf u^T\mathbf v"
