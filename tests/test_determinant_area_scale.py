from __future__ import annotations

import numpy as np
import pytest

from engine.determinant_area_scale import (
    UNIT_SQUARE,
    area_scale_statement,
    as_matrix_2x2,
    build_area_scale_example,
    polygon_area,
    transform_vertices,
)


def test_unit_square_has_area_one() -> None:
    assert polygon_area(UNIT_SQUARE) == pytest.approx(1.0)


def test_example_uses_clear_integer_columns() -> None:
    example = build_area_scale_example()
    np.testing.assert_array_equal(example.matrix, np.array([[2.0, 1.0], [0.0, 2.0]]))
    first, second = example.columns
    np.testing.assert_array_equal(first, np.array([2.0, 0.0]))
    np.testing.assert_array_equal(second, np.array([1.0, 2.0]))


def test_image_is_column_generated_parallelogram() -> None:
    example = build_area_scale_example()
    expected = np.array([[0.0, 0.0], [2.0, 0.0], [3.0, 2.0], [1.0, 2.0]])
    np.testing.assert_array_equal(example.image_vertices, expected)


def test_area_scale_is_four() -> None:
    example = build_area_scale_example()
    assert example.source_area == pytest.approx(1.0)
    assert example.image_area == pytest.approx(4.0)
    assert example.area_scale == pytest.approx(4.0)


def test_transform_vertices_validates_matrix_shape() -> None:
    with pytest.raises(ValueError, match="shape"):
        transform_vertices([[1, 0, 0], [0, 1, 0]])


def test_matrix_validation_rejects_nonfinite_entries() -> None:
    with pytest.raises(ValueError, match="finite"):
        as_matrix_2x2([[1, np.inf], [0, 1]])


def test_statement_names_magnitude_not_sign() -> None:
    statement = area_scale_statement().lower()
    assert "magnitude" in statement
    assert "area scale factor" in statement
