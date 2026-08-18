import numpy as np
import pytest

from engine.eigenvector_special_directions import (
    DEFAULT_MATRIX,
    ROTATION_MATRIX,
    SAMPLE_VECTORS,
    SpecialDirectionsLesson,
)


def test_cp168_contrasts_quarter_turn_with_symmetric_transformation() -> None:
    assert np.array_equal(ROTATION_MATRIX, np.array([[0.0, -1.0], [1.0, 0.0]]))
    assert np.array_equal(DEFAULT_MATRIX, np.array([[5.0, 3.0], [3.0, 5.0]]))
    assert np.array_equal(DEFAULT_MATRIX, DEFAULT_MATRIX.T)


def test_quarter_turn_has_no_preserved_sample_directions() -> None:
    lesson = SpecialDirectionsLesson(ROTATION_MATRIX)
    observations = [lesson.observe(v) for v in SAMPLE_VECTORS]
    assert all(not item.preserves_line for item in observations)
    assert all(item.scale_factor is None for item in observations)


def test_symmetric_sample_contains_four_generic_and_two_special_directions() -> None:
    lesson = SpecialDirectionsLesson(DEFAULT_MATRIX)
    observations = [lesson.observe(v) for v in SAMPLE_VECTORS]
    flags = [item.preserves_line for item in observations]
    assert flags == [False, False, False, False, True, True]


def test_special_directions_have_expected_scale_factors() -> None:
    lesson = SpecialDirectionsLesson(DEFAULT_MATRIX)
    first = lesson.observe(np.array([1.0, 1.0]))
    second = lesson.observe(np.array([1.0, -1.0]))
    assert first.preserves_line and first.scale_factor == pytest.approx(8.0)
    assert second.preserves_line and second.scale_factor == pytest.approx(2.0)


def test_transform_is_renderer_independent_matrix_vector_multiplication() -> None:
    rotation = SpecialDirectionsLesson(ROTATION_MATRIX)
    special = SpecialDirectionsLesson(DEFAULT_MATRIX)
    assert np.allclose(rotation.transform([1.0, 0.0]), [0.0, 1.0])
    assert np.allclose(rotation.transform([0.0, 1.0]), [-1.0, 0.0])
    assert np.allclose(special.transform([1.0, 0.0]), [5.0, 3.0])
    assert np.allclose(special.transform([0.0, 1.0]), [3.0, 5.0])


def test_zero_vector_is_rejected_as_a_direction() -> None:
    lesson = SpecialDirectionsLesson(DEFAULT_MATRIX)
    with pytest.raises(ValueError, match="zero vector"):
        lesson.observe([0.0, 0.0])
