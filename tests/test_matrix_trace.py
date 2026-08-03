import pytest

from engine.matrix_trace import (
    MATRIX_TRACE_LESSON,
    add_matrices,
    is_square,
    matrix_shape,
    multiply_matrices,
    scale_matrix,
    trace,
)


def test_trace_adds_main_diagonal_entries() -> None:
    assert trace(((3, -1, 2), (4, 5, 0), (-2, 1, 6))) == 14


def test_trace_requires_square_matrix() -> None:
    assert is_square(((1, 2), (3, 4)))
    assert not is_square(((1, 2, 3), (4, 5, 6)))
    with pytest.raises(ValueError, match="square matrices"):
        trace(((1, 2, 3), (4, 5, 6)))


def test_trace_is_additive_for_lesson_data() -> None:
    lesson = MATRIX_TRACE_LESSON
    assert lesson.sum_trace == lesson.trace_sum
    assert lesson.sum_trace == trace(
        add_matrices(lesson.matrix, lesson.second_matrix)
    )


def test_trace_respects_scalar_multiplication() -> None:
    lesson = MATRIX_TRACE_LESSON
    assert lesson.scaled_trace == lesson.scalar_trace
    assert lesson.scaled_trace == trace(
        scale_matrix(lesson.scalar, lesson.matrix)
    )


def test_trace_ab_equals_trace_ba() -> None:
    lesson = MATRIX_TRACE_LESSON
    assert lesson.ab != lesson.ba
    assert lesson.trace_ab == lesson.trace_ba
    assert lesson.trace_ab == 9


def test_matrix_products_for_lesson_data() -> None:
    lesson = MATRIX_TRACE_LESSON
    assert lesson.ab == ((11, 5), (-4, -2))
    assert lesson.ba == ((3, 5), (4, 6))


def test_matrix_shape() -> None:
    assert matrix_shape(((1, 2, 3), (4, 5, 6))) == (2, 3)


def test_invalid_matrix_inputs_are_rejected() -> None:
    with pytest.raises(ValueError):
        matrix_shape(())
    with pytest.raises(ValueError):
        matrix_shape(((1, 2), (3,)))


def test_incompatible_matrix_product_is_rejected() -> None:
    with pytest.raises(ValueError, match="inner dimensions"):
        multiply_matrices(((1, 2, 3),), ((1, 2), (3, 4)))
