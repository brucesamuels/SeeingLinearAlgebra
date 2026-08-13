import numpy as np
import pytest

from engine.vector_projection import VectorProjectionLesson, projection_onto


def test_projection_returns_vector_in_direction_span() -> None:
    result = projection_onto((3.0, 3.0), (4.0, 1.0))
    assert np.allclose(result, (60.0 / 17.0, 15.0 / 17.0))
    assert result[0] / result[1] == pytest.approx(4.0)


def test_projection_residual_is_orthogonal_to_direction() -> None:
    snapshot = VectorProjectionLesson().example()
    assert snapshot.residual_dot_direction == pytest.approx(0.0)


def test_projection_plus_residual_reconstructs_vector() -> None:
    snapshot = VectorProjectionLesson().example()
    assert snapshot.reconstructs_vector
    assert np.allclose(snapshot.projection + snapshot.residual, snapshot.vector)


def test_example_coefficient_is_fifteen_seventeenths() -> None:
    snapshot = VectorProjectionLesson().example()
    assert snapshot.coefficient == pytest.approx(15.0 / 17.0)


def test_unit_direction_projection_simplifies_to_dot_times_unit_vector() -> None:
    q = np.array((1.0, 0.0))
    x = np.array((3.0, 4.0))
    assert np.allclose(projection_onto(x, q), (x @ q) * q)


def test_projection_rejects_zero_direction() -> None:
    with pytest.raises(ValueError, match="nonzero"):
        projection_onto((1.0, 2.0), (0.0, 0.0))


def test_projection_rejects_dimension_mismatch() -> None:
    with pytest.raises(ValueError, match="same dimension"):
        projection_onto((1.0, 2.0), (1.0, 0.0, 0.0))


def test_lesson_contains_general_unit_and_residual_formulas() -> None:
    lesson = VectorProjectionLesson()
    assert r"\frac{\mathbf{x}\cdot\mathbf{u}}{\mathbf{u}\cdot\mathbf{u}}" in lesson.GENERAL_FORMULA
    assert lesson.UNIT_FORMULA == r"\operatorname{proj}_{\mathbf{q}}\mathbf{x}=(\mathbf{x}\cdot\mathbf{q})\mathbf{q}"
    assert "proj" in lesson.DECOMPOSITION
    assert lesson.ORTHOGONAL_RESIDUAL.endswith(r"\cdot\mathbf{u}=0")
