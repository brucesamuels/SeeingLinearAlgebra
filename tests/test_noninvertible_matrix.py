import numpy as np
import pytest

from engine.noninvertible_matrix import NoninvertibleMatrix


def test_default_matrix_is_singular_with_rank_two() -> None:
    model = NoninvertibleMatrix()
    assert model.rank == 2
    assert model.verifies_singular()
    assert not model.left_side_can_be_identity()
    assert model.pivot_columns == (0, 1)
    assert model.free_columns == (2,)


def test_gauss_jordan_steps_update_the_complete_block() -> None:
    model = NoninvertibleMatrix()
    steps = model.steps
    assert len(steps) == 3
    assert [step.operation_tex for step in steps] == [
        r"R_2\leftarrow R_2-2R_1",
        r"R_2\leftrightarrow R_3",
        r"R_1\leftarrow R_1-2R_2",
    ]
    assert all(step.before_block.shape == (3, 6) for step in steps)
    assert all(step.after_block.shape == (3, 6) for step in steps)


def test_reduced_block_has_missing_pivot_and_transformed_identity_row() -> None:
    model = NoninvertibleMatrix()
    expected_left = np.array(
        [
            [1.0, 0.0, -1.0],
            [0.0, 1.0, 1.0],
            [0.0, 0.0, 0.0],
        ]
    )
    expected_right = np.array(
        [
            [1.0, 0.0, -2.0],
            [0.0, 0.0, 1.0],
            [-2.0, 1.0, 0.0],
        ]
    )
    np.testing.assert_allclose(model.left_rref, expected_left)
    np.testing.assert_allclose(model.transformed_identity, expected_right)
    assert model.unit_system_contradictions == (-2.0, 1.0, 0.0)


def test_unit_vector_systems_are_not_all_solvable() -> None:
    model = NoninvertibleMatrix()
    assert model.unit_system_statuses == ("none", "none", "infinite")


def test_nonzero_null_vector_and_column_relation_are_verified() -> None:
    model = NoninvertibleMatrix()
    expected = np.array([1.0, -1.0, 1.0])
    np.testing.assert_allclose(model.null_vector, expected)
    np.testing.assert_allclose(model.column_relation_coefficients, expected)
    assert model.verifies_null_vector()
    assert model.verifies_column_relation()


def test_snapshot_returns_copies_and_expected_formulae() -> None:
    model = NoninvertibleMatrix()
    snapshot = model.snapshot()
    assert snapshot.failure_tex == r"[A\mid I]\not\longrightarrow[I\mid A^{-1}]"
    assert snapshot.null_space_tex == (
        r"N(A)=\operatorname{span}\left\{"
        r"\begin{bmatrix}1\\-1\\1\end{bmatrix}"
        r"\right\}"
    )
    assert snapshot.equivalence_tex[0] == r"A^{-1}\text{ exists}\iff\operatorname{rank}(A)=3"
    snapshot.coefficient_matrix[0, 0] = 99
    assert model.coefficient_matrix[0, 0] == 1


def test_invalid_input_is_rejected() -> None:
    with pytest.raises(ValueError, match="shape"):
        NoninvertibleMatrix([[1, 2], [3, 4]])
    with pytest.raises(ValueError, match="finite"):
        NoninvertibleMatrix([[1, 2, 1], [2, np.nan, 2], [0, 1, 1]])
    with pytest.raises(ValueError, match="fixed classroom matrix"):
        NoninvertibleMatrix(np.eye(3))
    with pytest.raises(ValueError, match="positive finite"):
        NoninvertibleMatrix(atol=0)
