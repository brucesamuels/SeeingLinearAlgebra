import pytest

from engine.matrix_order_identity_undoing import (
    MATRIX_ORDER_IDENTITY_UNDOING_LESSON,
    identity_matrix,
    matrix_shape,
    matrix_vector_product,
    multiply_matrices,
)


def test_order_matters_for_lesson_data() -> None:
    lesson = MATRIX_ORDER_IDENTITY_UNDOING_LESSON
    assert lesson.shear_then_reflection_matrix == ((-1, -1), (0, 1))
    assert lesson.reflection_then_shear_matrix == ((-1, 1), (0, 1))
    assert lesson.shear_then_reflection_vector == (-3, 1)
    assert lesson.reflection_then_shear_vector == (-1, 1)


def test_identity_matrix_and_identity_action() -> None:
    assert identity_matrix(2) == ((1, 0), (0, 1))
    lesson = MATRIX_ORDER_IDENTITY_UNDOING_LESSON
    assert lesson.identity_result == lesson.vector


def test_projection_collapses_information() -> None:
    lesson = MATRIX_ORDER_IDENTITY_UNDOING_LESSON
    assert lesson.projected_vector == (2, 0)


def test_shear_inverse_recovers_identity_on_both_sides() -> None:
    lesson = MATRIX_ORDER_IDENTITY_UNDOING_LESSON
    assert lesson.shear_inverse == ((1, -1), (0, 1))
    assert lesson.inverse_then_shear == lesson.identity
    assert lesson.shear_then_inverse == lesson.identity


def test_matrix_shape() -> None:
    assert matrix_shape(((1, 2, 3), (4, 5, 6))) == (2, 3)


def test_matrix_vector_dimension_mismatch_is_rejected() -> None:
    with pytest.raises(ValueError, match="columns"):
        matrix_vector_product(((1, 2, 3),), (1, 2))


def test_matrix_product_dimension_mismatch_is_rejected() -> None:
    with pytest.raises(ValueError, match="inner dimensions"):
        multiply_matrices(((1, 2, 3),), ((1, 2), (3, 4)))


def test_invalid_identity_size_is_rejected() -> None:
    with pytest.raises(ValueError, match="positive"):
        identity_matrix(0)
