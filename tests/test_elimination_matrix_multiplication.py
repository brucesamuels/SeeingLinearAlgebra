import numpy as np
import pytest

from engine.elimination_matrix_multiplication import EliminationMatrixMultiplication


def test_default_matrix_and_upper_triangular_result() -> None:
    model = EliminationMatrixMultiplication()
    np.testing.assert_allclose(
        model.original_matrix,
        np.array([[2, 1, 1], [4, -6, 0], [-2, 7, 2]], dtype=float),
    )
    np.testing.assert_allclose(
        model.upper_triangular_matrix,
        np.array([[2, 1, 1], [0, -8, -2], [0, 0, 1]], dtype=float),
    )


def test_three_elimination_multipliers_are_computed() -> None:
    model = EliminationMatrixMultiplication()
    steps = model.elimination_steps
    assert len(steps) == 3
    assert [step.multiplier for step in steps] == pytest.approx([2.0, -1.0, -1.0])
    assert [(step.target_row, step.pivot_row) for step in steps] == [(1, 0), (2, 0), (2, 1)]


def test_each_elementary_matrix_performs_its_step() -> None:
    model = EliminationMatrixMultiplication()
    for step in model.elimination_steps:
        np.testing.assert_allclose(step.elementary_matrix @ step.before_matrix, step.after_matrix)


def test_inverse_elementary_matrices_reverse_each_step() -> None:
    model = EliminationMatrixMultiplication()
    for step in model.elimination_steps:
        np.testing.assert_allclose(step.inverse_elementary_matrix @ step.after_matrix, step.before_matrix)
        np.testing.assert_allclose(step.inverse_elementary_matrix @ step.elementary_matrix, np.eye(3))


def test_elimination_product_reduces_a_to_u() -> None:
    model = EliminationMatrixMultiplication()
    expected = np.array([[1, 0, 0], [-2, 1, 0], [-1, 1, 1]], dtype=float)
    np.testing.assert_allclose(model.elimination_product(), expected)
    assert model.verifies_elimination_product()


def test_lower_triangular_factor_is_inverse_product() -> None:
    model = EliminationMatrixMultiplication()
    expected = np.array([[1, 0, 0], [2, 1, 0], [-1, -1, 1]], dtype=float)
    np.testing.assert_allclose(model.lower_triangular_matrix(), expected)
    np.testing.assert_allclose(model.lower_triangular_matrix(), np.linalg.inv(model.elimination_product()))


def test_lu_factorization_recovers_a() -> None:
    model = EliminationMatrixMultiplication()
    assert model.verifies_lu_factorization()
    np.testing.assert_allclose(
        model.lower_triangular_matrix() @ model.upper_triangular_matrix,
        model.original_matrix,
    )


def test_multiplier_positions_are_exposed() -> None:
    model = EliminationMatrixMultiplication()
    assert model.multiplier_positions() == ((1, 0, 2.0), (2, 0, -1.0), (2, 1, -1.0))


def test_snapshot_contains_expected_formulae_and_copies() -> None:
    model = EliminationMatrixMultiplication()
    snapshot = model.snapshot()
    assert snapshot.elimination_product_tex == r"E_3E_2E_1A=U"
    assert snapshot.inverse_product_tex == r"A=E_1^{-1}E_2^{-1}E_3^{-1}U"
    assert snapshot.lu_factorization_tex == r"A=LU"
    snapshot.original_matrix[0, 0] = 99
    assert model.original_matrix[0, 0] == 2


def test_invalid_shape_and_nonfinite_entries_are_rejected() -> None:
    with pytest.raises(ValueError, match="shape"):
        EliminationMatrixMultiplication([[1, 2], [3, 4]])
    with pytest.raises(ValueError, match="finite"):
        EliminationMatrixMultiplication([[1, 0, 0], [0, np.nan, 0], [0, 0, 1]])


def test_zero_pivot_without_row_exchange_is_rejected() -> None:
    with pytest.raises(ValueError, match="without row exchanges"):
        EliminationMatrixMultiplication([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
