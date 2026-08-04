import numpy as np
import pytest

from engine.elementary_row_operations import ElementaryRowOperations


def test_default_system_and_solution() -> None:
    operations = ElementaryRowOperations()
    np.testing.assert_allclose(
        operations.augmented_matrix,
        [[1, 1, 2], [2, -1, 1]],
    )
    np.testing.assert_allclose(operations.solution(), [1, 1])


def test_snapshot_contains_three_displayed_operations() -> None:
    snapshot = ElementaryRowOperations().snapshot()
    np.testing.assert_allclose(snapshot.swapped_augmented, [[2, -1, 1], [1, 1, 2]])
    np.testing.assert_allclose(snapshot.scaled_augmented, [[2, 2, 4], [2, -1, 1]])
    np.testing.assert_allclose(snapshot.replaced_augmented, [[1, 1, 2], [0, -3, -3]])


def test_swap_rows_returns_a_copy_and_does_not_mutate_input() -> None:
    original = np.array([[1, 2, 3], [4, 5, 6]], dtype=float)
    result = ElementaryRowOperations.swap_rows(original, 0, 1)
    np.testing.assert_allclose(result, [[4, 5, 6], [1, 2, 3]])
    np.testing.assert_allclose(original, [[1, 2, 3], [4, 5, 6]])


def test_scale_row_multiplies_the_entire_augmented_row() -> None:
    result = ElementaryRowOperations.scale_row([[1, 1, 2], [2, -1, 1]], 0, 2)
    np.testing.assert_allclose(result, [[2, 2, 4], [2, -1, 1]])


def test_scale_row_rejects_zero_and_nonfinite_scalars() -> None:
    with pytest.raises(ValueError, match="nonzero"):
        ElementaryRowOperations.scale_row([[1, 1, 2]], 0, 0)
    with pytest.raises(ValueError, match="finite"):
        ElementaryRowOperations.scale_row([[1, 1, 2]], 0, np.inf)


def test_replace_row_adds_a_multiple_of_a_distinct_source_row() -> None:
    result = ElementaryRowOperations.replace_row(
        [[1, 1, 2], [2, -1, 1]],
        1,
        0,
        -2,
    )
    np.testing.assert_allclose(result, [[1, 1, 2], [0, -3, -3]])


def test_replace_row_rejects_same_source_and_target() -> None:
    with pytest.raises(ValueError, match="distinct"):
        ElementaryRowOperations.replace_row([[1, 1, 2], [2, -1, 1]], 0, 0, 2)


def test_all_three_operations_preserve_the_displayed_solution() -> None:
    operations = ElementaryRowOperations()
    snapshot = operations.snapshot()
    for augmented in (
        snapshot.base_augmented,
        snapshot.swapped_augmented,
        snapshot.scaled_augmented,
        snapshot.replaced_augmented,
    ):
        assert operations.satisfies(augmented, snapshot.solution)


def test_satisfies_rejects_wrong_candidate_length() -> None:
    with pytest.raises(ValueError, match="length"):
        ElementaryRowOperations.satisfies([[1, 1, 2]], [1, 1, 1])


def test_constructor_validates_augmented_matrix_shape_and_finiteness() -> None:
    with pytest.raises(ValueError, match="two-dimensional"):
        ElementaryRowOperations([1, 2, 3])
    with pytest.raises(ValueError, match="at least two columns"):
        ElementaryRowOperations([[1]])
    with pytest.raises(ValueError, match="finite"):
        ElementaryRowOperations([[1, np.nan]])


def test_row_indices_are_validated() -> None:
    with pytest.raises(IndexError):
        ElementaryRowOperations.swap_rows([[1, 2], [3, 4]], 0, 2)
    with pytest.raises(TypeError):
        ElementaryRowOperations.scale_row([[1, 2]], 0.5, 2)
