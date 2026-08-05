import numpy as np
import pytest

from engine.pivoting_pa_lu import PivotingPALU


def test_default_matrix_has_zero_first_pivot_but_is_invertible() -> None:
    model = PivotingPALU()
    assert model.coefficient_matrix[0, 0] == 0
    assert abs(model.determinant - 8.0) < 1e-9


def test_permutation_swaps_first_two_rows() -> None:
    model = PivotingPALU()
    expected_p = np.array(
        [
            [0.0, 1.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    )
    expected_pa = np.array(
        [
            [2.0, 2.0, 3.0],
            [0.0, 2.0, 1.0],
            [4.0, -2.0, 1.0],
        ]
    )
    np.testing.assert_allclose(model.permutation_matrix, expected_p)
    np.testing.assert_allclose(model.permuted_matrix, expected_pa)
    assert model.verifies_permutation_properties()


def test_elimination_steps_are_derived_after_pivoting() -> None:
    model = PivotingPALU()
    steps = model.steps
    assert len(steps) == 2
    assert [step.multiplier for step in steps] == [2.0, -3.0]
    assert steps[0].operation_tex == r"m_{31}=2,\qquad R_3\leftarrow R_3-2R_1"
    assert steps[1].operation_tex == (
        r"m_{32}=-3,\qquad R_3\leftarrow R_3-(-3)R_2=R_3+3R_2"
    )
    np.testing.assert_allclose(
        steps[0].after_matrix,
        np.array(
            [
                [2.0, 2.0, 3.0],
                [0.0, 2.0, 1.0],
                [0.0, -6.0, -5.0],
            ]
        ),
    )


def test_l_and_u_satisfy_pa_equals_lu() -> None:
    model = PivotingPALU()
    expected_l = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [2.0, -3.0, 1.0],
        ]
    )
    expected_u = np.array(
        [
            [2.0, 2.0, 3.0],
            [0.0, 2.0, 1.0],
            [0.0, 0.0, -2.0],
        ]
    )
    np.testing.assert_allclose(model.lower_triangular, expected_l)
    np.testing.assert_allclose(model.upper_triangular, expected_u)
    assert model.verifies_factorization()
    assert model.verifies_reconstruction()


def test_tiny_pivot_comparison_uses_reciprocal_multipliers() -> None:
    model = PivotingPALU()
    assert model.tiny_epsilon == pytest.approx(1e-4)
    assert model.multiplier_without_pivoting == pytest.approx(1e4)
    assert model.multiplier_with_pivoting == pytest.approx(1e-4)
    assert model.no_swap_second_entry == pytest.approx(-9999.0)
    assert model.pivoted_second_entry == pytest.approx(0.9999)


def test_snapshot_returns_copies_and_expected_formulae() -> None:
    model = PivotingPALU()
    snapshot = model.snapshot()
    assert snapshot.factorization_tex == r"PA=LU"
    assert snapshot.reconstruction_tex == r"A=P^TLU"
    assert snapshot.partial_pivot_rule_tex == r"p=\operatorname*{arg\,max}_{i\ge k}|a_{ik}|"
    snapshot.coefficient_matrix[0, 0] = 99
    assert model.coefficient_matrix[0, 0] == 0


def test_invalid_input_is_rejected() -> None:
    with pytest.raises(ValueError, match="shape"):
        PivotingPALU([[1, 2], [3, 4]])
    with pytest.raises(ValueError, match="finite"):
        PivotingPALU([[0, 2, 1], [2, np.nan, 3], [4, -2, 1]])
    with pytest.raises(ValueError, match="fixed classroom matrix"):
        PivotingPALU(np.eye(3))
    with pytest.raises(ValueError, match="positive finite"):
        PivotingPALU(atol=0)
    with pytest.raises(ValueError, match="0 < epsilon < 1"):
        PivotingPALU(epsilon=2)
