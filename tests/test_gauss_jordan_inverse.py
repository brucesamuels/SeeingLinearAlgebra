import numpy as np
import pytest

from engine.gauss_jordan_inverse import GaussJordanInverse


def test_default_inverse_is_correct() -> None:
    model = GaussJordanInverse()
    expected = np.array(
        [
            [1.0, -2.0, 2.5],
            [0.0, 1.0, -1.5],
            [0.0, 0.0, 0.5],
        ]
    )
    np.testing.assert_allclose(model.inverse_matrix, expected)
    np.testing.assert_allclose(model.coefficient_matrix @ model.inverse_matrix, np.eye(3))


def test_gauss_jordan_steps_are_correct_and_update_the_full_block() -> None:
    model = GaussJordanInverse()
    steps = model.steps
    assert len(steps) == 4
    assert [step.operation_tex for step in steps] == [
        r"R_3\leftarrow\tfrac12R_3",
        r"R_2\leftarrow R_2-3R_3",
        r"R_1\leftarrow R_1-R_3",
        r"R_1\leftarrow R_1-2R_2",
    ]
    assert [step.target_row for step in steps] == [2, 1, 0, 0]
    assert all(step.before_block.shape == (3, 6) for step in steps)
    assert all(step.after_block.shape == (3, 6) for step in steps)


def test_reduced_block_is_identity_beside_inverse() -> None:
    model = GaussJordanInverse()
    expected = np.hstack([np.eye(3), model.inverse_matrix])
    np.testing.assert_allclose(model.reduced_block, expected)
    assert model.verifies_reduction()


def test_inverse_works_on_both_sides_and_by_columns() -> None:
    model = GaussJordanInverse()
    assert model.verifies_right_inverse()
    assert model.verifies_left_inverse()
    assert model.verifies_column_systems()
    for index, column in enumerate(model.inverse_columns):
        np.testing.assert_allclose(model.coefficient_matrix @ column, np.eye(3)[:, index])


def test_elementary_product_equals_inverse() -> None:
    model = GaussJordanInverse()
    np.testing.assert_allclose(model.elementary_product, model.inverse_matrix)


def test_snapshot_returns_copies_and_expected_formulae() -> None:
    model = GaussJordanInverse()
    snapshot = model.snapshot()
    assert snapshot.block_system_tex == r"AX=I"
    assert snapshot.reduction_tex == r"[A\mid I]\longrightarrow[I\mid A^{-1}]"
    assert snapshot.elementary_product_tex == r"A^{-1}=E_4E_3E_2E_1"
    snapshot.coefficient_matrix[0, 0] = 99
    assert model.coefficient_matrix[0, 0] == 1


def test_invalid_input_is_rejected() -> None:
    with pytest.raises(ValueError, match="shape"):
        GaussJordanInverse([[1, 2], [3, 4]])
    with pytest.raises(ValueError, match="finite"):
        GaussJordanInverse([[1, 2, 1], [0, np.nan, 3], [0, 0, 2]])
    with pytest.raises(ValueError, match="invertible"):
        GaussJordanInverse([[1, 0, 0], [0, 0, 0], [0, 0, 1]])
    with pytest.raises(ValueError, match="fixed classroom matrix"):
        GaussJordanInverse(np.eye(3))
    with pytest.raises(ValueError, match="positive"):
        GaussJordanInverse(atol=0)
