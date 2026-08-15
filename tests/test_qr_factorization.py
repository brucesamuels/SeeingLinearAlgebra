import numpy as np

from engine.qr_factorization import QRFactorizationLesson


def test_q_has_orthonormal_columns() -> None:
    snapshot = QRFactorizationLesson().snapshot()
    assert np.allclose(snapshot.Q.T @ snapshot.Q, np.eye(2))


def test_qr_reconstructs_a() -> None:
    snapshot = QRFactorizationLesson().snapshot()
    assert np.allclose(snapshot.Q @ snapshot.R, snapshot.A)


def test_r_is_q_transpose_a_and_upper_triangular() -> None:
    snapshot = QRFactorizationLesson().snapshot()
    assert np.allclose(snapshot.R, snapshot.Q.T @ snapshot.A)
    assert np.allclose(np.tril(snapshot.R, -1), np.zeros((2, 2)))


def test_column_decompositions_match_r_columns() -> None:
    snapshot = QRFactorizationLesson().snapshot()
    assert np.allclose(snapshot.a1, snapshot.a1_q1_component)
    assert np.allclose(snapshot.a2, snapshot.a2_q1_component + snapshot.a2_q2_component)
    assert np.isclose(snapshot.R[1, 0], 0.0)


def test_bridge_points_to_next_question() -> None:
    lesson = QRFactorizationLesson()
    assert "column space" in lesson.bridge_prompt


def test_inverse_shortcut_constants_are_explicit() -> None:
    lesson = QRFactorizationLesson()
    assert lesson.R_FROM_QINV_A == r"R=Q^{-1}A"
    assert lesson.Q_INVERSE_TRANSPOSE == r"Q^{-1}=Q^T"
