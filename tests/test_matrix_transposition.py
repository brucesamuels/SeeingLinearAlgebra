import pytest

from engine.matrix_transposition import (
    MATRIX_TRANSPOSITION_LESSON,
    add_matrices,
    is_symmetric,
    matrix_shape,
    multiply_matrices,
    scale_matrix,
    transpose,
)


def test_transpose_exchanges_rows_and_columns() -> None:
    assert transpose(((1, 2, -1), (3, 0, 4))) == (
        (1, 3),
        (2, 0),
        (-1, 4),
    )


def test_transpose_reverses_dimensions() -> None:
    matrix = ((1, 2, 3), (4, 5, 6))
    assert matrix_shape(matrix) == (2, 3)
    assert matrix_shape(transpose(matrix)) == (3, 2)


def test_double_transpose_returns_original() -> None:
    lesson = MATRIX_TRANSPOSITION_LESSON
    assert lesson.double_transpose == lesson.matrix


def test_transpose_respects_addition() -> None:
    lesson = MATRIX_TRANSPOSITION_LESSON
    assert lesson.transpose_sum == lesson.sum_transposes


def test_transpose_respects_scalar_multiplication() -> None:
    lesson = MATRIX_TRANSPOSITION_LESSON
    assert lesson.transpose_scaled == lesson.scaled_transpose


def test_transpose_of_product_reverses_order() -> None:
    lesson = MATRIX_TRANSPOSITION_LESSON
    assert lesson.transpose_product == lesson.reversed_transpose_product


def test_symmetric_matrix_is_unchanged() -> None:
    lesson = MATRIX_TRANSPOSITION_LESSON
    assert is_symmetric(lesson.symmetric_matrix)
    assert transpose(lesson.symmetric_matrix) == lesson.symmetric_matrix


def test_rectangular_matrix_is_not_symmetric() -> None:
    assert not is_symmetric(((1, 2, 3), (4, 5, 6)))


def test_invalid_matrices_are_rejected() -> None:
    with pytest.raises(ValueError):
        transpose(())
    with pytest.raises(ValueError):
        transpose(((1, 2), (3,)))


def test_incompatible_product_is_rejected() -> None:
    with pytest.raises(ValueError, match="inner dimensions"):
        multiply_matrices(((1, 2, 3),), ((1, 2), (3, 4)))
