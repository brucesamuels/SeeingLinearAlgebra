import numpy as np
import pytest

from engine.orthogonal_decomposition import (
    OrthogonalDecompositionLesson,
    decompose_along_direction,
)


def test_example_has_clean_parallel_and_perpendicular_parts() -> None:
    snapshot = OrthogonalDecompositionLesson().example()
    assert np.allclose(snapshot.vector, (4.0, 2.0))
    assert np.allclose(snapshot.parallel, (3.0, 3.0))
    assert np.allclose(snapshot.perpendicular, (1.0, -1.0))


def test_decomposition_reconstructs_vector() -> None:
    snapshot = OrthogonalDecompositionLesson().example()
    assert snapshot.reconstructs_vector
    assert np.allclose(snapshot.parallel + snapshot.perpendicular, snapshot.vector)


def test_components_are_orthogonal() -> None:
    snapshot = OrthogonalDecompositionLesson().example()
    assert snapshot.pieces_are_orthogonal
    assert float(snapshot.parallel @ snapshot.perpendicular) == pytest.approx(0.0)


def test_pythagorean_identity_holds() -> None:
    snapshot = OrthogonalDecompositionLesson().example()
    assert snapshot.pythagorean_holds
    assert snapshot.vector_norm_squared == pytest.approx(20.0)
    assert snapshot.parallel_norm_squared == pytest.approx(18.0)
    assert snapshot.perpendicular_norm_squared == pytest.approx(2.0)


def test_decompose_along_direction_rejects_dimension_mismatch() -> None:
    with pytest.raises(ValueError, match="same dimension"):
        decompose_along_direction((1.0, 2.0), (1.0, 0.0, 0.0))


def test_lesson_contains_decomposition_and_pythagorean_formulas() -> None:
    lesson = OrthogonalDecompositionLesson()
    assert r"\mathbf{p}\in W" in lesson.LINE_DECOMPOSITION
    assert r"\mathbf{r}\in W^\perp" in lesson.LINE_DECOMPOSITION
    assert "proj" in lesson.PROJECTION_IDENTITIES
    assert lesson.PYTHAGOREAN == r"\|\mathbf{x}\|^2=\|\mathbf{p}\|^2+\|\mathbf{r}\|^2"
