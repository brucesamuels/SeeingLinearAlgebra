from __future__ import annotations

import numpy as np
import pytest

from engine.null_space_basis import NullSpaceBasis


def test_default_system_has_one_pivot_and_two_free_columns() -> None:
    model = NullSpaceBasis()
    assert model.pivot_columns() == (0,)
    assert model.free_columns() == (1, 2)
    assert model.rank() == 1
    assert model.nullity() == 2


def test_special_solutions_are_correct() -> None:
    model = NullSpaceBasis()
    np.testing.assert_allclose(model.first_special_solution(), [-2.0, 1.0, 0.0])
    np.testing.assert_allclose(model.second_special_solution(), [1.0, 0.0, 1.0])


def test_special_solutions_lie_in_null_space() -> None:
    model = NullSpaceBasis()
    for vector in model.basis():
        assert model.satisfies_null_space_system(vector)


def test_every_parameter_combination_lies_in_null_space() -> None:
    model = NullSpaceBasis()
    for first, second in [(-2.0, 0.0), (0.0, 3.0), (1.5, -0.5)]:
        assert model.satisfies_null_space_system(model.vector_from_parameters(first, second))


def test_basis_is_independent() -> None:
    assert NullSpaceBasis().basis_is_independent()


def test_text_representations_are_correct() -> None:
    model = NullSpaceBasis()
    assert model.general_solution_tex() == (
        r"\mathbf{x}=s\begin{bmatrix}-2\\1\\0\end{bmatrix}+"
        r"t\begin{bmatrix}1\\0\\1\end{bmatrix}"
    )
    assert model.null_space_span_tex() == (
        r"N(A)=\operatorname{span}\left\{"
        r"\begin{bmatrix}-2\\1\\0\end{bmatrix},"
        r"\begin{bmatrix}1\\0\\1\end{bmatrix}"
        r"\right\}"
    )


def test_snapshot_records_free_variable_assignments() -> None:
    snapshot = NullSpaceBasis().snapshot()
    assert snapshot.free_variables == ("y", "z")
    assert snapshot.first_assignment == (1.0, 0.0)
    assert snapshot.second_assignment == (0.0, 1.0)
    assert snapshot.nullity == 2


def test_invalid_inputs_are_rejected() -> None:
    with pytest.raises(ValueError, match="shape"):
        NullSpaceBasis([[1, 2], [3, 4]])
    with pytest.raises(ValueError, match="zero right-hand side"):
        NullSpaceBasis([[1, 2, -1, 3], [0, 0, 0, 0], [0, 0, 0, 0]])
    with pytest.raises(ValueError, match="distinct"):
        NullSpaceBasis(variable_names=("x", "x", "z"))
    with pytest.raises(ValueError, match="distinct"):
        NullSpaceBasis(parameter_names=("t", "t"))
    with pytest.raises(ValueError, match="finite"):
        NullSpaceBasis().vector_from_parameters(float("inf"), 0)
    with pytest.raises(ValueError, match="shape"):
        NullSpaceBasis().satisfies_null_space_system([1, 2])
