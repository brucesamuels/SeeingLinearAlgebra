import numpy as np
import pytest

from engine.orthonormal_sets import OrthonormalSetExample, OrthonormalSetsLesson, normalize


def test_normalize_returns_unit_vector_without_changing_direction() -> None:
    result = normalize((3.0, 0.0, 0.0))
    assert np.allclose(result, (1.0, 0.0, 0.0))
    assert np.linalg.norm(result) == pytest.approx(1.0)


def test_scaled_example_is_orthogonal_but_not_orthonormal() -> None:
    snapshot = OrthonormalSetsLesson().scaled_orthogonal_example()
    assert snapshot.is_orthogonal
    assert not snapshot.is_orthonormal
    assert snapshot.norms == pytest.approx((2.0, 2.5, 1.6))


def test_normalized_example_has_identity_gram_matrix() -> None:
    snapshot = OrthonormalSetsLesson().normalized_example()
    assert snapshot.is_orthonormal
    assert np.allclose(snapshot.gram_matrix, np.eye(3))


def test_normalizing_scaled_example_produces_unit_axes() -> None:
    normalized = OrthonormalSetsLesson().normalize_scaled_example()
    assert np.allclose(normalized[0], (1.0, 0.0, 0.0))
    assert np.allclose(normalized[1], (0.0, 1.0, 0.0))
    assert np.allclose(normalized[2], (0.0, 0.0, 1.0))


def test_lesson_contains_definition_matrix_identity_and_coordinate_rule() -> None:
    lesson = OrthonormalSetsLesson()
    assert "is orthonormal if" in lesson.DEFINITION
    assert lesson.KRONECKER == r"\mathbf{q}_i\cdot\mathbf{q}_j=\delta_{ij}"
    assert lesson.MATRIX_IDENTITY == r"Q^TQ=I"
    assert lesson.COORDINATE_RULE == r"c_j=\mathbf{q}_j\cdot\mathbf{x}"


def test_example_rejects_mismatched_dimensions() -> None:
    with pytest.raises(ValueError, match="same dimension"):
        OrthonormalSetExample(((1, 0), (0, 1, 0)))


def test_example_rejects_zero_vector() -> None:
    with pytest.raises(ValueError, match="nonzero"):
        OrthonormalSetExample(((1, 0, 0), (0, 0, 0)))
