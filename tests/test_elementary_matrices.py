import numpy as np
import pytest

from engine.elementary_matrices import ElementaryMatrices


def test_swap_matrix_is_identity_with_rows_interchanged() -> None:
    matrix = ElementaryMatrices.row_swap_matrix(3, 0, 1)
    np.testing.assert_array_equal(matrix, [[0, 1, 0], [1, 0, 0], [0, 0, 1]])


def test_scale_matrix_changes_one_diagonal_entry() -> None:
    matrix = ElementaryMatrices.row_scale_matrix(3, 1, -2)
    np.testing.assert_array_equal(matrix, [[1, 0, 0], [0, -2, 0], [0, 0, 1]])


def test_replacement_matrix_contains_the_added_multiple() -> None:
    matrix = ElementaryMatrices.row_replacement_matrix(3, 2, 0, 2)
    np.testing.assert_array_equal(matrix, [[1, 0, 0], [0, 1, 0], [2, 0, 1]])


def test_left_multiplication_performs_each_row_operation() -> None:
    model = ElementaryMatrices()
    swap = model.case("swap")
    np.testing.assert_array_equal(swap.product_matrix, swap.source_matrix[[1, 0, 2]])

    scale = model.case("scale")
    expected_scale = scale.source_matrix.copy()
    expected_scale[1] *= -2
    np.testing.assert_array_equal(scale.product_matrix, expected_scale)

    replacement = model.case("replacement")
    expected_replacement = replacement.source_matrix.copy()
    expected_replacement[2] += 2 * expected_replacement[0]
    np.testing.assert_array_equal(replacement.product_matrix, expected_replacement)


def test_each_inverse_restores_the_source_matrix() -> None:
    model = ElementaryMatrices()
    for name in ("swap", "scale", "replacement"):
        case = model.case(name)
        np.testing.assert_allclose(case.inverse_matrix @ case.product_matrix, case.source_matrix)
        np.testing.assert_allclose(case.inverse_matrix @ case.elementary_matrix, np.eye(3))


def test_complete_reduction_has_four_valid_steps_and_ends_at_identity() -> None:
    model = ElementaryMatrices()
    steps = model.reduction_steps()
    assert len(steps) == 4
    np.testing.assert_allclose(steps[0].source_matrix, model.REDUCTION_SOURCE)
    for previous, current in zip(steps, steps[1:], strict=False):
        np.testing.assert_allclose(previous.product_matrix, current.source_matrix)
    np.testing.assert_allclose(steps[-1].product_matrix, np.eye(3))


def test_cumulative_product_is_entire_row_reduction_matrix() -> None:
    model = ElementaryMatrices()
    products = model.cumulative_products()
    assert len(products) == 4
    reduction_matrix = products[-1]
    np.testing.assert_allclose(reduction_matrix @ model.REDUCTION_SOURCE, np.eye(3))
    np.testing.assert_allclose(reduction_matrix, np.linalg.inv(model.REDUCTION_SOURCE))
    np.testing.assert_allclose(
        reduction_matrix,
        [[1.0, -2.0, 2.5], [0.0, 1.0, -1.5], [0.0, 0.0, 0.5]],
    )


def test_reverse_steps_rebuild_original_matrix_from_identity() -> None:
    model = ElementaryMatrices()
    reverse_steps = model.reverse_steps()
    assert [step.index for step in reverse_steps] == [4, 3, 2, 1]
    np.testing.assert_allclose(reverse_steps[0].source_matrix, np.eye(3))
    for previous, current in zip(reverse_steps, reverse_steps[1:], strict=False):
        np.testing.assert_allclose(previous.product_matrix, current.source_matrix)
    np.testing.assert_allclose(reverse_steps[-1].product_matrix, model.REDUCTION_SOURCE)


def test_inverse_factorization_has_reversed_order() -> None:
    model = ElementaryMatrices()
    steps = model.reduction_steps()
    rebuilt = np.eye(3)
    for step in reversed(steps):
        rebuilt = step.inverse_matrix @ rebuilt
    np.testing.assert_allclose(rebuilt, model.REDUCTION_SOURCE)


def test_cases_are_returned_as_copies() -> None:
    model = ElementaryMatrices()
    first = model.case("swap")
    first.elementary_matrix[0, 0] = 99
    second = model.case("swap")
    assert second.elementary_matrix[0, 0] == 0


def test_invalid_source_matrix_is_rejected() -> None:
    with pytest.raises(ValueError, match="shape"):
        ElementaryMatrices(np.zeros((2, 3)))
    bad = np.eye(3)
    bad[0, 0] = np.nan
    with pytest.raises(ValueError, match="finite"):
        ElementaryMatrices(bad)


def test_invalid_elementary_operations_are_rejected() -> None:
    with pytest.raises(ValueError, match="distinct"):
        ElementaryMatrices.row_swap_matrix(3, 1, 1)
    with pytest.raises(ValueError, match="nonzero"):
        ElementaryMatrices.row_scale_matrix(3, 1, 0)
    with pytest.raises(ValueError, match="distinct"):
        ElementaryMatrices.row_replacement_matrix(3, 1, 1, 2)
    with pytest.raises(ValueError, match="range"):
        ElementaryMatrices.row_swap_matrix(3, 0, 3)


def test_apply_validates_dimensions() -> None:
    with pytest.raises(ValueError, match="square"):
        ElementaryMatrices.apply(np.zeros((2, 3)), np.zeros((3, 2)))
    with pytest.raises(ValueError, match="same number of rows"):
        ElementaryMatrices.apply(np.eye(3), np.zeros((2, 2)))


def test_snapshot_contains_forward_reverse_and_reduction_data() -> None:
    snapshot = ElementaryMatrices().snapshot()
    assert snapshot.swap.operation_tex == r"R_1\leftrightarrow R_2"
    assert snapshot.scale.inverse_operation_tex == r"R_2\leftarrow -\tfrac12R_2"
    assert snapshot.replacement.inverse_operation_tex == r"R_3\leftarrow R_3-2R_1"
    assert len(snapshot.reduction_steps) == 4
    assert len(snapshot.cumulative_products) == 4
    assert len(snapshot.reverse_steps) == 4
    np.testing.assert_allclose(snapshot.reduction_matrix @ snapshot.reduction_source, np.eye(3))
