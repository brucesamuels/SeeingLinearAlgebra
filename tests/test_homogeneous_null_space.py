from __future__ import annotations

import numpy as np
import pytest

from engine.homogeneous_null_space import HomogeneousNullSpace


def test_homogeneous_example_has_one_free_variable() -> None:
    model = HomogeneousNullSpace()
    assert model.homogeneous_pivot_columns() == (0, 1)
    assert model.homogeneous_free_columns() == (2,)
    np.testing.assert_allclose(model.special_solution(), [-2.0, 1.0, 1.0])


def test_homogeneous_parameterized_solutions_satisfy_system() -> None:
    model = HomogeneousNullSpace()
    for value in (-2.0, -1.0, 0.0, 1.0, 3.5):
        assert model.satisfies_homogeneous_system(model.homogeneous_solution_for_parameter(value))


def test_homogeneous_text_representations_are_correct() -> None:
    model = HomogeneousNullSpace()
    assert model.homogeneous_solution_tex() == (
        r"\begin{bmatrix}x\\y\\z\end{bmatrix}=t\begin{bmatrix}-2\\1\\1\end{bmatrix}"
    )
    assert model.null_space_span_tex() == (
        r"N(A)=\operatorname{span}\left\{\begin{bmatrix}-2\\1\\1\end{bmatrix}\right\}"
    )


def test_rank_one_example_has_two_free_variables_and_two_special_solutions() -> None:
    model = HomogeneousNullSpace()
    assert model.rank_one_pivot_columns() == (0,)
    assert model.rank_one_free_columns() == (1, 2)
    np.testing.assert_allclose(model.rank_one_particular_solution(), [3.0, 0.0, 0.0])
    s1, s2 = model.rank_one_special_solutions()
    np.testing.assert_allclose(s1, [-2.0, 1.0, 0.0])
    np.testing.assert_allclose(s2, [1.0, 0.0, 1.0])


def test_rank_one_parameterized_solution_satisfies_system() -> None:
    model = HomogeneousNullSpace()
    for s, t in [(-1.0, 0.0), (0.0, 2.0), (1.5, -0.5)]:
        assert model.satisfies_rank_one_system(model.rank_one_solution_for_parameters(s, t))


def test_rank_one_solution_text_is_correct() -> None:
    model = HomogeneousNullSpace()
    assert model.rank_one_solution_tex() == (
        r"\mathbf{x}=\begin{bmatrix}3\\0\\0\end{bmatrix}+"
        r"s\begin{bmatrix}-2\\1\\0\end{bmatrix}+"
        r"t\begin{bmatrix}1\\0\\1\end{bmatrix}"
    )
    assert model.rank_one_associated_null_space_tex() == (
        r"N(A)=\operatorname{span}\left\{"
        r"\begin{bmatrix}-2\\1\\0\end{bmatrix},"
        r"\begin{bmatrix}1\\0\\1\end{bmatrix}"
        r"\right\}"
    )


def test_invalid_inputs_are_rejected() -> None:
    with pytest.raises(ValueError, match="shape"):
        HomogeneousNullSpace([[1, 2], [3, 4]])
    with pytest.raises(ValueError, match="zero right-hand side"):
        HomogeneousNullSpace(homogeneous_rref_augmented=[[1, 0, 2, 1], [0, 1, -1, 0], [0, 0, 0, 0]])
    with pytest.raises(ValueError, match="nonempty"):
        HomogeneousNullSpace(parameter_name="")
    with pytest.raises(ValueError, match="distinct"):
        HomogeneousNullSpace(parameter_name="t", second_parameter_name="t")
    with pytest.raises(ValueError, match="finite"):
        HomogeneousNullSpace().homogeneous_solution_for_parameter(float("inf"))
    with pytest.raises(ValueError, match="shape"):
        HomogeneousNullSpace().satisfies_rank_one_system([1, 2])
