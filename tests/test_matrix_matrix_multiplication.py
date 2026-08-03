import pytest

from engine.matrix_matrix_multiplication import (
    MATRIX_MATRIX_MULTIPLICATION_LESSON,
    entry_computations,
    matrices_are_compatible,
    matrix_columns,
    matrix_shape,
    multiply_matrices,
    product_shape,
)


def test_matrix_shape_and_columns() -> None:
    matrix = ((2, 1), (-1, 3), (5, 2))
    assert matrix_shape(matrix) == (3, 2)
    assert matrix_columns(matrix) == ((2, -1, 5), (1, 3, 2))


def test_compatibility_and_product_shape() -> None:
    left = ((1, 2, -1), (3, 0, 4))
    right = ((2, 1), (-1, 3), (5, 2))
    assert matrices_are_compatible(left, right)
    assert product_shape(left, right) == (2, 2)


def test_matrix_product() -> None:
    assert multiply_matrices(
        ((1, 2, -1), (3, 0, 4)),
        ((2, 1), (-1, 3), (5, 2)),
    ) == ((-5, 5), (26, 11))


def test_entry_computations_follow_row_major_order() -> None:
    computations = entry_computations(
        ((1, 2, -1), (3, 0, 4)),
        ((2, 1), (-1, 3), (5, 2)),
    )
    assert [(c.row_index, c.column_index) for c in computations] == [
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1),
    ]
    assert [c.result for c in computations] == [-5, 5, 26, 11]


def test_lesson_data_is_consistent() -> None:
    lesson = MATRIX_MATRIX_MULTIPLICATION_LESSON
    assert lesson.result == ((-5, 5), (26, 11))
    assert lesson.result_shape == (2, 2)


def test_incompatible_product_is_rejected() -> None:
    with pytest.raises(ValueError, match="inner dimensions"):
        multiply_matrices(
            ((1, 2, 3), (4, 5, 6)),
            ((1, 2), (3, 4)),
        )


def test_ragged_and_empty_inputs_are_rejected() -> None:
    with pytest.raises(ValueError):
        matrix_shape(())
    with pytest.raises(ValueError):
        matrix_shape(((1, 2), (3,)))
