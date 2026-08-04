from __future__ import annotations

import numpy as np
import pytest

from engine.complete_solution import CompleteSolution


def test_default_system_has_one_pivot_and_two_free_columns() -> None:
    model = CompleteSolution()
    assert model.pivot_columns() == (0,)
    assert model.free_columns() == (1, 2)


def test_particular_solution_satisfies_nonhomogeneous_system() -> None:
    model = CompleteSolution()
    np.testing.assert_allclose(model.particular_solution(), [3.0, 0.0, 0.0])
    assert model.satisfies_nonhomogeneous_system(model.particular_solution())


def test_null_space_basis_vectors_satisfy_homogeneous_system() -> None:
    model = CompleteSolution()
    s1, s2 = model.null_space_basis()
    np.testing.assert_allclose(s1, [-2.0, 1.0, 0.0])
    np.testing.assert_allclose(s2, [1.0, 0.0, 1.0])
    assert model.satisfies_homogeneous_system(s1)
    assert model.satisfies_homogeneous_system(s2)


def test_every_parameterized_complete_solution_satisfies_system() -> None:
    model = CompleteSolution()
    for first, second in [(-1.0, 0.0), (0.0, 2.0), (1.5, -0.5), (3.0, 4.0)]:
        point = model.complete_solution(first, second)
        assert model.satisfies_nonhomogeneous_system(point)
        assert model.difference_from_particular_is_null(point)


def test_associated_homogeneous_rref_only_changes_right_hand_side() -> None:
    model = CompleteSolution()
    homogeneous = model.associated_homogeneous_rref
    np.testing.assert_allclose(homogeneous[:, :-1], model.coefficient_matrix)
    np.testing.assert_allclose(homogeneous[:, -1], 0.0)


def test_tex_representations_are_correct() -> None:
    model = CompleteSolution()
    assert model.particular_solution_tex() == r"\mathbf{x}_p=\begin{bmatrix}3\\0\\0\end{bmatrix}"
    assert model.null_space_solution_tex() == (
        r"\mathbf{x}_n=s\begin{bmatrix}-2\\1\\0\end{bmatrix}+"
        r"t\begin{bmatrix}1\\0\\1\end{bmatrix}"
    )
    assert model.complete_solution_tex() == (
        r"\mathbf{x}=\begin{bmatrix}3\\0\\0\end{bmatrix}+"
        r"s\begin{bmatrix}-2\\1\\0\end{bmatrix}+"
        r"t\begin{bmatrix}1\\0\\1\end{bmatrix}"
    )


def test_verification_and_converse_sequences_are_present() -> None:
    model = CompleteSolution()
    assert model.verification_tex() == (
        r"A(\mathbf{x}_p+\mathbf{x}_n)=A\mathbf{x}_p+A\mathbf{x}_n",
        r"=\mathbf{b}+\mathbf{0}",
        r"=\mathbf{b}",
    )
    assert model.converse_tex()[-1] == r"\mathbf{x}=\mathbf{x}_p+\mathbf{x}_n"


def test_invalid_inputs_are_rejected() -> None:
    with pytest.raises(ValueError, match="shape"):
        CompleteSolution([[1, 2], [3, 4]])
    with pytest.raises(ValueError, match="distinct"):
        CompleteSolution(parameter_names=("t", "t"))
    with pytest.raises(ValueError, match="nonempty"):
        CompleteSolution(parameter_names=("", "t"))
    with pytest.raises(ValueError, match="finite"):
        CompleteSolution().null_space_vector(float("inf"), 0.0)
    with pytest.raises(ValueError, match="shape"):
        CompleteSolution().satisfies_nonhomogeneous_system([1, 2])
