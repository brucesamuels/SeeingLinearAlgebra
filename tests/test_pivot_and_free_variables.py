from __future__ import annotations

import numpy as np
import pytest

from engine.pivot_and_free_variables import PivotAndFreeVariables


def test_default_pivot_and_free_columns() -> None:
    model = PivotAndFreeVariables()
    assert model.pivot_columns() == (0, 1)
    assert model.free_columns() == (2,)


def test_parametric_and_strang_components_are_correct() -> None:
    model = PivotAndFreeVariables()
    np.testing.assert_allclose(model.particular_solution(), [4.0, 1.0, 0.0])
    np.testing.assert_allclose(model.special_solution(), [-2.0, 1.0, 1.0])
    assert model.parametric_vector_tex() == (
        r"\begin{bmatrix}x\\y\\z\end{bmatrix}="
        r"\begin{bmatrix}4\\1\\0\end{bmatrix}+"
        r"t\begin{bmatrix}-2\\1\\1\end{bmatrix}"
    )
    assert model.strang_solution_tex() == (
        r"\text{all solutions}="
        r"\begin{bmatrix}4\\1\\0\end{bmatrix}+"
        r"t\begin{bmatrix}-2\\1\\1\end{bmatrix}"
    )


def test_every_parameter_value_satisfies_system() -> None:
    model = PivotAndFreeVariables()
    for value in (-3.0, 0.0, 2.5):
        assert model.satisfies_system(model.solution_for_parameter(value))


def test_snapshot_identifies_variable_roles() -> None:
    snapshot = PivotAndFreeVariables().snapshot()
    assert snapshot.pivot_variables == ("x", "y")
    assert snapshot.free_variables == ("z",)
    assert snapshot.parameter_name == "t"


def test_invalid_inputs_are_rejected() -> None:
    with pytest.raises(ValueError, match="shape"):
        PivotAndFreeVariables([[1, 2], [3, 4]])
    with pytest.raises(ValueError, match="distinct"):
        PivotAndFreeVariables(variable_names=("x", "x", "z"))
    with pytest.raises(ValueError, match="nonempty"):
        PivotAndFreeVariables(parameter_name="")
    with pytest.raises(ValueError, match="finite"):
        PivotAndFreeVariables().solution_for_parameter(float("inf"))
    with pytest.raises(ValueError, match="shape"):
        PivotAndFreeVariables().satisfies_system([1, 2])
