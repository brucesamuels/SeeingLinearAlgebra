import numpy as np

from engine.projection_matrices import ProjectionMatricesLesson


def test_projection_matrix_is_symmetric_and_idempotent() -> None:
    snapshot = ProjectionMatricesLesson().snapshot()
    assert np.allclose(snapshot.P.T, snapshot.P)
    assert np.allclose(snapshot.P @ snapshot.P, snapshot.P)


def test_q_is_unit_and_projection_matrix_is_outer_product() -> None:
    snapshot = ProjectionMatricesLesson().snapshot()
    assert np.isclose(np.linalg.norm(snapshot.q), 1.0)
    assert np.allclose(snapshot.P, np.outer(snapshot.q, snapshot.q))


def test_concrete_projection_and_residual_are_correct() -> None:
    snapshot = ProjectionMatricesLesson().snapshot()
    assert np.allclose(snapshot.Pv, np.array([6.0 / 5.0, 12.0 / 5.0]))
    assert np.allclose(snapshot.residual, np.array([14.0 / 5.0, -7.0 / 5.0]))
    assert np.isclose(snapshot.q @ snapshot.residual, 0.0)


def test_repeated_projection_does_nothing_new() -> None:
    snapshot = ProjectionMatricesLesson().snapshot()
    assert np.allclose(snapshot.repeated_projection, snapshot.Pv)


def test_projection_keeps_subspace_and_kills_orthogonal_complement() -> None:
    snapshot = ProjectionMatricesLesson().snapshot()
    assert np.allclose(snapshot.projected_q, snapshot.q)
    assert np.allclose(snapshot.projected_orthogonal_direction, np.zeros(2))
    assert np.isclose(snapshot.q @ snapshot.orthogonal_direction, 0.0)


def test_comparison_rotation_is_orthogonal_and_preserves_length() -> None:
    snapshot = ProjectionMatricesLesson().snapshot()
    assert np.allclose(snapshot.R.T @ snapshot.R, np.eye(2))
    assert np.isclose(np.linalg.norm(snapshot.Rv), np.linalg.norm(snapshot.v))


def test_lesson_formulas_are_explicit() -> None:
    lesson = ProjectionMatricesLesson()
    assert lesson.FULL_COLUMN_PROJECTION == r"P=A(A^TA)^{-1}A^T"
    assert lesson.ORTHONORMAL_PROJECTION == r"P=Q(Q^TQ)^{-1}Q^T=QQ^T"
    assert lesson.GENERAL_PROJECTION == r"P=QQ^T"
    assert lesson.IDEMPOTENT_RULE == r"P^2=P"
    assert lesson.SYMMETRY_RULE == r"P^T=P"
    assert lesson.ORTHOGONAL_MATRIX_RULE == r"Q^TQ=I"
