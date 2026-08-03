import pytest

from engine.row_column_rule import (
    ROW_COLUMN_RULE_LESSON,
    column_combination_product,
    dot_product,
    matrix_columns,
    matrix_vector_product,
    row_computations,
)


def test_dot_product() -> None:
    assert dot_product((2, -1, 3), (3, 2, -1)) == 1


def test_matrix_vector_product_uses_row_dot_products() -> None:
    assert matrix_vector_product(
        ((2, -1, 3), (1, 4, -2)),
        (3, 2, -1),
    ) == (1, 13)


def test_matrix_columns_are_extracted_correctly() -> None:
    assert matrix_columns(
        ((2, -1, 3), (1, 4, -2))
    ) == ((2, 1), (-1, 4), (3, -2))


def test_column_combination_matches_row_rule() -> None:
    lesson = ROW_COLUMN_RULE_LESSON
    assert lesson.column_combination_result == lesson.result
    assert lesson.result == (1, 13)


def test_row_computations_preserve_rows_and_results() -> None:
    computations = row_computations(
        ((2, -1, 3), (1, 4, -2)),
        (3, 2, -1),
    )
    assert computations[0].products == (6, -2, -3)
    assert computations[0].result == 1
    assert computations[1].products == (3, 8, 2)
    assert computations[1].result == 13


def test_dimension_mismatch_is_rejected() -> None:
    with pytest.raises(ValueError, match="columns"):
        matrix_vector_product(((1, 2, 3),), (4, 5))


def test_dot_product_length_mismatch_is_rejected() -> None:
    with pytest.raises(ValueError, match="equal lengths"):
        dot_product((1, 2), (3,))


def test_empty_inputs_are_rejected() -> None:
    with pytest.raises(ValueError):
        matrix_vector_product((), (1,))
    with pytest.raises(ValueError):
        matrix_vector_product(((1,),), ())
