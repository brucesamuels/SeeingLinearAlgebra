import numpy as np

from engine.rotations_reflections import RotationsReflectionsLesson


def test_rotation_is_orthogonal_and_has_positive_determinant() -> None:
    snapshot = RotationsReflectionsLesson().snapshot()
    assert np.allclose(snapshot.R.T @ snapshot.R, np.eye(2))
    assert np.isclose(np.linalg.det(snapshot.R), 1.0)


def test_rotation_images_match_matrix_columns() -> None:
    snapshot = RotationsReflectionsLesson().snapshot()
    assert np.allclose(snapshot.Re1, snapshot.R[:, 0])
    assert np.allclose(snapshot.Re2, snapshot.R[:, 1])


def test_rotation_preserves_lengths_and_inverse_is_transpose() -> None:
    snapshot = RotationsReflectionsLesson().snapshot()
    assert np.isclose(np.linalg.norm(snapshot.Rv), np.linalg.norm(snapshot.v))
    assert np.allclose(np.linalg.inv(snapshot.R), snapshot.R.T)


def test_reflection_is_orthogonal_self_inverse_and_negative_determinant() -> None:
    snapshot = RotationsReflectionsLesson().snapshot()
    assert np.allclose(snapshot.H.T @ snapshot.H, np.eye(2))
    assert np.allclose(snapshot.H @ snapshot.H, np.eye(2))
    assert np.allclose(np.linalg.inv(snapshot.H), snapshot.H)
    assert np.isclose(np.linalg.det(snapshot.H), -1.0)


def test_reflection_keeps_x_component_and_reverses_y_component() -> None:
    snapshot = RotationsReflectionsLesson().snapshot()
    assert np.isclose(snapshot.reflected_v[0], snapshot.v[0])
    assert np.isclose(snapshot.reflected_v[1], -snapshot.v[1])


def test_lesson_formulas_are_explicit() -> None:
    lesson = RotationsReflectionsLesson()
    assert lesson.ROTATION_INVERSE == r"R_\theta^{-1}=R_{-\theta}=R_\theta^T"
    assert lesson.REFLECTION_MATRIX == r"H=\begin{bmatrix}1&0\\0&-1\end{bmatrix}"
    assert lesson.REFLECTION_INVERSE == r"H^{-1}=H=H^T"
    assert lesson.ORTHOGONAL_CRITERION == r"\text{orthogonal}\iff\text{columns are orthonormal}"
