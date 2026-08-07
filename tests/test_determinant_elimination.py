from fractions import Fraction

import numpy as np
import pytest

from engine.determinant_elimination import (
    EXAMPLE_MATRIX,
    build_elimination_example,
    determinant_3x3,
    overview_rule_lines,
    triangular_diagonal_product,
)


def test_example_matrix_has_expected_determinant() -> None:
    assert round(determinant_3x3(EXAMPLE_MATRIX)) == -7


def test_invalid_shape_rejected() -> None:
    with pytest.raises(ValueError):
        determinant_3x3([[1, 2], [3, 4]])


def test_build_elimination_example_tracks_steps() -> None:
    example = build_elimination_example()
    assert example.initial_matrix.shape == (3, 3)
    assert len(example.steps) == 4
    assert example.steps[0].factor_from_start == Fraction(-1, 1)
    assert example.steps[1].factor_from_start == Fraction(-1, 2)
    assert example.steps[3].factor_from_start == Fraction(-1, 2)
    np.testing.assert_allclose(example.triangular_matrix, [[1, 1, 0], [0, 1, 0.5], [0, 0, 3.5]])


def test_triangular_diagonal_product_matches_example() -> None:
    example = build_elimination_example()
    assert triangular_diagonal_product(example.triangular_matrix) == 3.5
    assert example.triangular_determinant == Fraction(7, 2)


def test_original_determinant_recovered_correctly() -> None:
    example = build_elimination_example()
    assert example.original_determinant == Fraction(-7, 1)


def test_overview_rule_lines_cover_all_operations() -> None:
    lines = overview_rule_lines()
    assert len(lines) == 4
    assert "Swap rows" in lines[0]
    assert "Scale a row" in lines[1]
    assert "Add a multiple" in lines[2]
    assert "resulting triangular matrix U" in lines[3]
