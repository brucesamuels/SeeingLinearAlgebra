import pytest

from engine.matrix_addition_subtraction import (
    MATRIX_ADDITION_SUBTRACTION_LESSON,
    add_matrices,
    entrywise_steps,
    matrix_shape,
    negate_matrix,
    same_shape,
    subtract_matrices,
)


def test_matrix_shape_and_same_shape() -> None:
    assert matrix_shape(((1, 2, 3), (4, 5, 6))) == (2, 3)
    assert same_shape(((1, 2), (3, 4)), ((5, 6), (7, 8)))
    assert not same_shape(((1, 2, 3),), ((1,), (2,), (3,)))


def test_addition_is_entrywise() -> None:
    assert add_matrices(
        ((2, -1), (3, 4)),
        ((5, 3), (-2, 1)),
    ) == ((7, 2), (1, 5))


def test_subtraction_is_addition_of_the_negative() -> None:
    left = ((4, 1), (-3, 2))
    right = ((1, -2), (5, 3))
    assert negate_matrix(right) == ((-1, 2), (-5, -3))
    assert subtract_matrices(left, right) == add_matrices(
        left,
        negate_matrix(right),
    )
    assert subtract_matrices(left, right) == ((3, 3), (-8, -1))


def test_dimension_mismatch_is_rejected() -> None:
    with pytest.raises(ValueError, match="equal dimensions"):
        add_matrices(((1, 2, 3),), ((1,), (2,), (3,)))


def test_ragged_or_empty_data_is_rejected() -> None:
    with pytest.raises(ValueError):
        matrix_shape(())
    with pytest.raises(ValueError):
        matrix_shape(((1, 2), (3,)))


def test_entrywise_steps_preserve_positions_and_results() -> None:
    steps = entrywise_steps(
        ((2, -1), (3, 4)),
        ((5, 3), (-2, 1)),
        operation="add",
    )
    assert [(step.row, step.column) for step in steps] == [
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1),
    ]
    assert [step.result for step in steps] == [7, 2, 1, 5]


def test_lesson_examples_are_consistent() -> None:
    lesson = MATRIX_ADDITION_SUBTRACTION_LESSON
    assert lesson.addition_result == ((7, 2), (1, 5))
    assert lesson.subtraction_result == ((3, 3), (-8, -1))
    assert lesson.subtraction_as_addition_result == lesson.subtraction_result
