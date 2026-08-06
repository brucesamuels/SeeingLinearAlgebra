import numpy as np
import pytest

from engine.determinant_properties import (
    build_additivity_example,
    build_identity_example,
    build_row_scaling_examples,
    build_row_swap_examples,
    determinant_2x2,
    property_summary_lines,
    row_swap,
    scale_row,
    transform_unit_square,
)


def test_determinant_basic_values() -> None:
    assert determinant_2x2([[1, 0], [0, 1]]) == 1.0
    assert determinant_2x2([[2, 1], [1, 2]]) == 3.0


def test_invalid_matrix_shape_rejected() -> None:
    with pytest.raises(ValueError):
        determinant_2x2([[1, 2, 3], [4, 5, 6]])


def test_transform_unit_square_for_base_example() -> None:
    vertices = transform_unit_square([[2, 1], [1, 2]])
    np.testing.assert_allclose(vertices, [[0, 0], [2, 1], [3, 3], [1, 2]])


def test_row_swap_changes_sign() -> None:
    original = [[2, 1], [1, 2]]
    swapped = row_swap(original)
    assert determinant_2x2(swapped) == -determinant_2x2(original)


def test_scale_row_multiplies_determinant() -> None:
    original = [[2, 1], [1, 2]]
    scaled = scale_row(original, 0, 2)
    assert determinant_2x2(scaled) == 2 * determinant_2x2(original)


def test_identity_example_is_correct() -> None:
    example = build_identity_example()
    assert example.determinant == 1.0
    np.testing.assert_allclose(example.image_vertices, [[0, 0], [1, 0], [1, 1], [0, 1]])


def test_row_swap_examples_are_consistent() -> None:
    base, swapped = build_row_swap_examples()
    assert base.determinant == 3.0
    assert swapped.determinant == -3.0


def test_row_scaling_examples_are_consistent() -> None:
    base, scaled, factor = build_row_scaling_examples()
    assert base.determinant == 3.0
    assert scaled.determinant == 6.0
    assert factor == 2.0


def test_additivity_example_is_consistent() -> None:
    example = build_additivity_example()
    assert example.determinant_piece_one == 2.0
    assert example.determinant_piece_two == 1.0
    assert example.determinant_total == 3.0
    np.testing.assert_allclose(example.combined_row, [2.0, 1.0])


def test_summary_lines_cover_all_properties() -> None:
    lines = property_summary_lines()
    assert len(lines) == 4
    assert "det(I) = 1" in lines[0]
    assert "Swapping two rows" in lines[1]
    assert "Scaling one row" in lines[2]
    assert "additive in one row" in lines[3]
