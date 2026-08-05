import numpy as np
import pytest

from engine.multiple_right_hand_sides import MultipleRightHandSides


def test_default_matrices_and_solution_are_correct() -> None:
    model = MultipleRightHandSides()
    expected_x = np.array([[1, 0], [0, 1], [1, -1]], dtype=float)
    np.testing.assert_allclose(model.solution_matrix, expected_x)
    np.testing.assert_allclose(model.coefficient_matrix @ model.solution_matrix, model.right_hand_sides)


def test_block_elimination_has_three_steps_and_updates_all_columns() -> None:
    model = MultipleRightHandSides()
    steps = model.block_elimination_steps
    assert len(steps) == 3
    assert [step.operation_tex for step in steps] == [
        r"R_2\leftarrow R_2-2R_1",
        r"R_3\leftarrow R_3+R_1",
        r"R_3\leftarrow R_3+R_2",
    ]
    assert all(step.before_block.shape == (3, 5) for step in steps)
    assert all(step.after_block.shape == (3, 5) for step in steps)
    assert model.verifies_block_elimination()


def test_lu_factors_and_intermediate_matrix_are_correct() -> None:
    model = MultipleRightHandSides()
    expected_l = np.array([[1, 0, 0], [2, 1, 0], [-1, -1, 1]], dtype=float)
    expected_u = np.array([[2, 1, 1], [0, -8, -2], [0, 0, 1]], dtype=float)
    expected_y = np.array([[3, 0], [-2, -6], [1, -1]], dtype=float)
    np.testing.assert_allclose(model.lower_triangular_matrix, expected_l)
    np.testing.assert_allclose(model.upper_triangular_matrix, expected_u)
    np.testing.assert_allclose(model.intermediate_matrix, expected_y)
    np.testing.assert_allclose(model.forward_substitution_result(), expected_y)
    assert model.verifies_lu_factorization()
    assert model.verifies_forward_substitution()
    assert model.verifies_solution()


def test_exact_operation_counts_match_stated_convention() -> None:
    counts = MultipleRightHandSides().operation_counts()
    assert counts.matrix_size == 3
    assert counts.right_hand_sides == 2
    assert counts.factorization_operations == 13
    assert counts.forward_substitution_per_rhs == 6
    assert counts.back_substitution_per_rhs == 9
    assert counts.triangular_solve_per_rhs == 15
    assert counts.repeated_reduction_total == 56
    assert counts.factor_once_total == 43
    assert counts.savings == 13


def test_more_right_hand_sides_change_only_linear_solve_work() -> None:
    b = np.column_stack(
        [
            MultipleRightHandSides.DEFAULT_B,
            np.array([1.0, 2.0, 3.0]),
        ]
    )
    counts = MultipleRightHandSides(right_hand_sides=b).operation_counts()
    assert counts.right_hand_sides == 3
    assert counts.repeated_reduction_total == 84
    assert counts.factor_once_total == 58
    assert counts.savings == 26


def test_snapshot_returns_copies_and_formulae() -> None:
    model = MultipleRightHandSides()
    snapshot = model.snapshot()
    assert snapshot.block_system_tex == r"AX=B"
    assert snapshot.forward_substitution_tex == r"LY=B"
    assert snapshot.back_substitution_tex == r"UX=Y"
    assert snapshot.verification_tex == r"AX=B"
    snapshot.coefficient_matrix[0, 0] = 99
    assert model.coefficient_matrix[0, 0] == 2


def test_invalid_shapes_and_nonfinite_entries_are_rejected() -> None:
    with pytest.raises(ValueError, match="shape"):
        MultipleRightHandSides(coefficient_matrix=[[1, 2], [3, 4]])
    with pytest.raises(ValueError, match="shape"):
        MultipleRightHandSides(right_hand_sides=[[1, 2], [3, 4]])
    with pytest.raises(ValueError, match="finite"):
        MultipleRightHandSides(right_hand_sides=[[1], [np.nan], [3]])
    with pytest.raises(ValueError, match="positive"):
        MultipleRightHandSides(atol=0)
