import numpy as np

from engine.chapter_six_finale import ChapterSixFinaleLesson


def test_perpendicular_example_has_zero_dot_product() -> None:
    snapshot = ChapterSixFinaleLesson().snapshot()
    assert np.isclose(snapshot.u @ snapshot.v, 0.0)


def test_projection_example_is_an_orthogonal_decomposition() -> None:
    snapshot = ChapterSixFinaleLesson().snapshot()
    assert np.allclose(snapshot.sample, snapshot.projection + snapshot.residual)
    assert np.isclose(snapshot.q @ snapshot.residual, 0.0)
    assert np.allclose(snapshot.projection_matrix @ snapshot.projection, snapshot.projection)


def test_projection_matrix_is_symmetric_and_idempotent() -> None:
    snapshot = ChapterSixFinaleLesson().snapshot()
    P = snapshot.projection_matrix
    assert np.allclose(P.T, P)
    assert np.allclose(P @ P, P)


def test_least_squares_example_has_orthogonal_residual() -> None:
    snapshot = ChapterSixFinaleLesson().snapshot()
    assert np.allclose(snapshot.ls_projection, snapshot.ls_A @ snapshot.ls_xhat)
    assert np.allclose(snapshot.ls_b, snapshot.ls_projection + snapshot.ls_residual)
    assert np.allclose(snapshot.ls_A.T @ snapshot.ls_residual, np.zeros(2))


def test_finale_constants_capture_chapter_signatures() -> None:
    lesson = ChapterSixFinaleLesson()
    assert lesson.DOT_RULE == r"\mathbf u^T\mathbf v=0\iff \mathbf u\perp\mathbf v"
    assert lesson.QR_RULE == r"A=QR,\qquad Q^TQ=I"
    assert lesson.PROJECTION_SIGNATURE == r"P^T=P,\qquad P^2=P"
    assert lesson.ORTHOGONAL_SIGNATURE == r"U^TU=I,\qquad U^{-1}=U^T"
    assert lesson.CLOSING_IDEA == "Orthogonality turns geometry into computation."
