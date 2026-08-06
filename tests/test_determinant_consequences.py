import numpy as np
import pytest

from engine.determinant_consequences import (
    build_dependent_rows_example,
    build_equal_rows_example,
    build_row_replacement_example,
    build_zero_row_example,
    determinant_2x2,
    row_replacement,
    summary_lines,
    transform_unit_square,
)


def test_determinant_values() -> None:
    assert determinant_2x2([[1, 2], [1, 2]]) == 0.0
    assert determinant_2x2([[2, 1], [1, 2]]) == 3.0


def test_invalid_shape_rejected() -> None:
    with pytest.raises(ValueError):
        determinant_2x2([[1, 2, 3], [4, 5, 6]])


def test_transform_unit_square_for_equal_rows() -> None:
    vertices = transform_unit_square([[1, 2], [1, 2]])
    np.testing.assert_allclose(vertices, [[0, 0], [1, 1], [3, 3], [2, 2]])


def test_row_replacement_preserves_determinant() -> None:
    original = [[2, 1], [1, 2]]
    replaced = row_replacement(original, 0, 1, -2)
    assert determinant_2x2(replaced) == determinant_2x2(original)


def test_equal_rows_example() -> None:
    example = build_equal_rows_example()
    assert example.determinant == 0.0


def test_zero_row_example() -> None:
    example = build_zero_row_example()
    assert example.determinant == 0.0
    np.testing.assert_allclose(example.image_vertices, [[0, 0], [0, 1], [0, 3], [0, 2]])


def test_row_replacement_example() -> None:
    example = build_row_replacement_example()
    assert example.original.determinant == 3.0
    assert example.replaced.determinant == 3.0
    assert example.multiple == -2.0
    np.testing.assert_allclose(example.replaced.matrix, [[0, -3], [1, 2]])


def test_dependent_rows_example() -> None:
    example = build_dependent_rows_example()
    assert example.determinant == 0.0


def test_summary_lines() -> None:
    lines = summary_lines()
    assert len(lines) == 4
    assert "Equal rows" in lines[0]
    assert "zero row" in lines[1].lower()
    assert "leaves the determinant unchanged" in lines[2]
    assert "Dependent rows" in lines[3]
