import numpy as np
import pytest

from engine.augmented_matrix_encoding import AugmentedMatrixEncoding


def test_default_snapshot_preserves_cp105_system() -> None:
    snapshot = AugmentedMatrixEncoding().snapshot()
    np.testing.assert_allclose(
        snapshot.coefficient_matrix,
        [[1, 1, 1], [2, -1, 1], [1, 2, -1]],
    )
    np.testing.assert_allclose(snapshot.right_hand_side, [3, 2, 2])
    np.testing.assert_allclose(
        snapshot.augmented_matrix,
        [[1, 1, 1, 3], [2, -1, 1, 2], [1, 2, -1, 2]],
    )
    assert snapshot.variable_names == ("x", "y", "z")


def test_snapshot_records_natural_and_explicit_equations() -> None:
    snapshot = AugmentedMatrixEncoding().snapshot()
    assert snapshot.natural_equation_tex == (
        "x+y+z=3",
        "2x-y+z=2",
        "x+2y-z=2",
    )
    assert snapshot.explicit_equation_tex == (
        "1x+1y+1z=3",
        "2x+(-1)y+1z=2",
        "1x+2y+(-1)z=2",
    )


def test_augmented_rows_and_columns_are_returned_as_copies() -> None:
    encoding = AugmentedMatrixEncoding()
    np.testing.assert_allclose(encoding.augmented_row(1), [2, -1, 1, 2])
    np.testing.assert_allclose(encoding.column_for("y"), [1, -1, 2])

    row = encoding.augmented_row(0)
    row[0] = 99
    assert encoding.augmented_row(0)[0] == 1


def test_split_augmented_recovers_matrix_and_rhs() -> None:
    augmented = np.array([[1, 0, -1, 4], [2, 3, 5, 7]], dtype=float)
    matrix, rhs = AugmentedMatrixEncoding.split_augmented(augmented)
    np.testing.assert_allclose(matrix, [[1, 0, -1], [2, 3, 5]])
    np.testing.assert_allclose(rhs, [4, 7])


def test_encode_row_inserts_zero_placeholder_without_losing_position() -> None:
    row = AugmentedMatrixEncoding.encode_row([1, 0, -1], 4)
    np.testing.assert_allclose(row, [1, 0, -1, 4])


def test_invalid_shapes_and_names_are_rejected() -> None:
    with pytest.raises(ValueError, match="two-dimensional"):
        AugmentedMatrixEncoding([1, 2, 3], [4])
    with pytest.raises(ValueError, match="number of equations"):
        AugmentedMatrixEncoding([[1, 2], [3, 4]], [5])
    with pytest.raises(ValueError, match="coefficient columns"):
        AugmentedMatrixEncoding([[1, 2]], [3], ["x"])
    with pytest.raises(ValueError, match="unique"):
        AugmentedMatrixEncoding([[1, 2]], [3], ["x", "x"])


def test_nonfinite_data_and_invalid_indices_are_rejected() -> None:
    with pytest.raises(ValueError, match="finite"):
        AugmentedMatrixEncoding([[1, np.inf]], [2], ["x", "y"])
    with pytest.raises(IndexError, match="outside"):
        AugmentedMatrixEncoding().augmented_row(3)
    with pytest.raises(KeyError, match="unknown variable"):
        AugmentedMatrixEncoding().column_for("w")
    with pytest.raises(ValueError, match="at least two columns"):
        AugmentedMatrixEncoding.split_augmented([[1]])
