import pytest

from engine.matrix_multiplication_composition import (
    MATRIX_COMPOSITION_LESSON,
    compose_on_vector,
    matrix_shape,
    matrix_vector_product,
    multiply_matrices,
)


def test_first_and_second_transformations() -> None:
    lesson = MATRIX_COMPOSITION_LESSON
    assert lesson.after_first == (3, 1)
    assert lesson.after_second == (-3, 1)


def test_product_matrix_matches_composition() -> None:
    lesson = MATRIX_COMPOSITION_LESSON
    assert lesson.product_matrix == ((-1, -1), (0, 1))
    assert lesson.product_result == lesson.after_second


def test_compose_on_vector() -> None:
    assert compose_on_vector(
        ((-1, 0), (0, 1)),
        ((1, 1), (0, 1)),
        (2, 1),
    ) == (-3, 1)


def test_product_matrix_shape() -> None:
    lesson = MATRIX_COMPOSITION_LESSON
    assert matrix_shape(lesson.product_matrix) == (2, 2)


def test_matrix_vector_dimension_mismatch_is_rejected() -> None:
    with pytest.raises(ValueError, match="columns"):
        matrix_vector_product(((1, 2, 3),), (1, 2))


def test_matrix_product_dimension_mismatch_is_rejected() -> None:
    with pytest.raises(ValueError, match="inner dimensions"):
        multiply_matrices(
            ((1, 2, 3),),
            ((1, 2), (3, 4)),
        )


def test_empty_and_ragged_matrices_are_rejected() -> None:
    with pytest.raises(ValueError):
        matrix_shape(())
    with pytest.raises(ValueError):
        matrix_shape(((1, 2), (3,)))
