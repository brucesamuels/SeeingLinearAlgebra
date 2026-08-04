"""Renderer-independent mathematics for CP115.

Checkpoint 115 introduces homogeneous systems and the null space, then extends
that viewpoint to a rank-one system with two free variables so that students
see a particular solution together with two special solutions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class HomogeneousNullSpaceSnapshot:
    """Immutable mathematical data used by the CP115 presentation."""

    homogeneous_rref_augmented: FloatArray
    homogeneous_coefficient_matrix: FloatArray
    homogeneous_pivot_columns: tuple[int, ...]
    homogeneous_free_columns: tuple[int, ...]
    parameter_name: str
    homogeneous_scalar_equations_tex: tuple[str, ...]
    special_solution: FloatArray
    null_space_basis: tuple[FloatArray, ...]
    homogeneous_solution_tex: str
    null_space_span_tex: str
    previous_particular_solution: FloatArray
    previous_nonhomogeneous_solution_tex: str
    rank_one_rref_augmented: FloatArray
    rank_one_pivot_columns: tuple[int, ...]
    rank_one_free_columns: tuple[int, ...]
    rank_one_scalar_equations_tex: tuple[str, ...]
    rank_one_particular_solution: FloatArray
    rank_one_special_solutions: tuple[FloatArray, ...]
    rank_one_solution_tex: str
    rank_one_associated_null_space_tex: str


class HomogeneousNullSpace:
    """Analyze one-free-variable and two-free-variable solution structures."""

    DEFAULT_HOMOGENEOUS_RREF = np.array(
        [
            [1.0, 0.0, 2.0, 0.0],
            [0.0, 1.0, -1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
        ],
        dtype=float,
    )
    DEFAULT_RANK_ONE_RREF = np.array(
        [
            [1.0, 2.0, -1.0, 3.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
        ],
        dtype=float,
    )
    DEFAULT_PREVIOUS_PARTICULAR_SOLUTION = np.array([4.0, 1.0, 0.0], dtype=float)

    def __init__(
        self,
        homogeneous_rref_augmented: Iterable[Iterable[float]] | FloatArray | None = None,
        rank_one_rref_augmented: Iterable[Iterable[float]] | FloatArray | None = None,
        parameter_name: str = "t",
        second_parameter_name: str = "s",
    ) -> None:
        homogeneous = np.array(
            self.DEFAULT_HOMOGENEOUS_RREF if homogeneous_rref_augmented is None else homogeneous_rref_augmented,
            dtype=float,
            copy=True,
        )
        rank_one = np.array(
            self.DEFAULT_RANK_ONE_RREF if rank_one_rref_augmented is None else rank_one_rref_augmented,
            dtype=float,
            copy=True,
        )
        for matrix in (homogeneous, rank_one):
            if matrix.shape != (3, 4):
                raise ValueError("all augmented matrices must have shape (3, 4).")
            if not np.isfinite(matrix).all():
                raise ValueError("matrix entries must be finite.")
        if not np.allclose(homogeneous[:, -1], 0.0):
            raise ValueError("the homogeneous example must have a zero right-hand side.")
        if not parameter_name or not second_parameter_name:
            raise ValueError("parameter names must be nonempty.")
        if parameter_name == second_parameter_name:
            raise ValueError("parameter names must be distinct.")
        self._homogeneous = homogeneous
        self._rank_one = rank_one
        self._parameter = parameter_name
        self._second_parameter = second_parameter_name

    @staticmethod
    def _pivot_columns(matrix: FloatArray, *, atol: float = 1e-9) -> tuple[int, ...]:
        pivots: list[int] = []
        for row in matrix[:, :-1]:
            nonzero = np.flatnonzero(np.abs(row) > atol)
            if nonzero.size:
                pivots.append(int(nonzero[0]))
        return tuple(pivots)

    @staticmethod
    def _free_columns(matrix: FloatArray) -> tuple[int, ...]:
        pivots = set(HomogeneousNullSpace._pivot_columns(matrix))
        return tuple(index for index in range(3) if index not in pivots)

    @property
    def homogeneous_rref_augmented(self) -> FloatArray:
        return self._homogeneous.copy()

    @property
    def rank_one_rref_augmented(self) -> FloatArray:
        return self._rank_one.copy()

    def homogeneous_pivot_columns(self) -> tuple[int, ...]:
        return self._pivot_columns(self._homogeneous)

    def homogeneous_free_columns(self) -> tuple[int, ...]:
        return self._free_columns(self._homogeneous)

    def rank_one_pivot_columns(self) -> tuple[int, ...]:
        return self._pivot_columns(self._rank_one)

    def rank_one_free_columns(self) -> tuple[int, ...]:
        return self._free_columns(self._rank_one)

    def homogeneous_scalar_equations_tex(self) -> tuple[str, ...]:
        p = self._parameter
        return (r"x+2z=0", r"y-z=0", rf"z={p}", rf"x=-2{p}", rf"y={p}")

    def special_solution(self) -> FloatArray:
        return np.array([-2.0, 1.0, 1.0], dtype=float)

    def null_space_basis(self) -> tuple[FloatArray, ...]:
        return (self.special_solution(),)

    def homogeneous_solution_for_parameter(self, value: float) -> FloatArray:
        if not np.isfinite(value):
            raise ValueError("parameter value must be finite.")
        return float(value) * self.special_solution()

    def satisfies_homogeneous_system(self, point: Iterable[float] | FloatArray, *, atol: float = 1e-9) -> bool:
        candidate = np.array(point, dtype=float, copy=True)
        if candidate.shape != (3,):
            raise ValueError("point must have shape (3,).")
        residual = self._homogeneous[:, :-1] @ candidate
        return bool(np.all(np.abs(residual) <= atol))

    def homogeneous_solution_tex(self) -> str:
        return r"\begin{bmatrix}x\\y\\z\end{bmatrix}=" + self._parameter + r"\begin{bmatrix}-2\\1\\1\end{bmatrix}"

    def null_space_span_tex(self) -> str:
        return r"N(A)=\operatorname{span}\left\{\begin{bmatrix}-2\\1\\1\end{bmatrix}\right\}"

    def previous_nonhomogeneous_solution_tex(self) -> str:
        return r"\mathbf{x}=\begin{bmatrix}4\\1\\0\end{bmatrix}+" + self._parameter + r"\begin{bmatrix}-2\\1\\1\end{bmatrix}"

    def rank_one_scalar_equations_tex(self) -> tuple[str, ...]:
        s = self._second_parameter
        t = self._parameter
        return (r"x+2y-z=3", rf"y={s}", rf"z={t}", rf"x=3-2{s}+{t}")

    def rank_one_particular_solution(self) -> FloatArray:
        return np.array([3.0, 0.0, 0.0], dtype=float)

    def rank_one_special_solutions(self) -> tuple[FloatArray, ...]:
        return (np.array([-2.0, 1.0, 0.0], dtype=float), np.array([1.0, 0.0, 1.0], dtype=float))

    def rank_one_solution_for_parameters(self, first: float, second: float) -> FloatArray:
        if not np.isfinite(first) or not np.isfinite(second):
            raise ValueError("parameter values must be finite.")
        s1, s2 = self.rank_one_special_solutions()
        return self.rank_one_particular_solution() + float(first) * s1 + float(second) * s2

    def satisfies_rank_one_system(self, point: Iterable[float] | FloatArray, *, atol: float = 1e-9) -> bool:
        candidate = np.array(point, dtype=float, copy=True)
        if candidate.shape != (3,):
            raise ValueError("point must have shape (3,).")
        residual = self._rank_one[:, :-1] @ candidate - self._rank_one[:, -1]
        return bool(np.all(np.abs(residual) <= atol))

    def rank_one_solution_tex(self) -> str:
        s = self._second_parameter
        t = self._parameter
        return (
            r"\mathbf{x}=\begin{bmatrix}3\\0\\0\end{bmatrix}+"
            + s
            + r"\begin{bmatrix}-2\\1\\0\end{bmatrix}+"
            + t
            + r"\begin{bmatrix}1\\0\\1\end{bmatrix}"
        )

    def rank_one_associated_null_space_tex(self) -> str:
        return (
            r"N(A)=\operatorname{span}\left\{"
            r"\begin{bmatrix}-2\\1\\0\end{bmatrix},"
            r"\begin{bmatrix}1\\0\\1\end{bmatrix}"
            r"\right\}"
        )

    def snapshot(self) -> HomogeneousNullSpaceSnapshot:
        return HomogeneousNullSpaceSnapshot(
            homogeneous_rref_augmented=self.homogeneous_rref_augmented,
            homogeneous_coefficient_matrix=self._homogeneous[:, :-1].copy(),
            homogeneous_pivot_columns=self.homogeneous_pivot_columns(),
            homogeneous_free_columns=self.homogeneous_free_columns(),
            parameter_name=self._parameter,
            homogeneous_scalar_equations_tex=self.homogeneous_scalar_equations_tex(),
            special_solution=self.special_solution(),
            null_space_basis=self.null_space_basis(),
            homogeneous_solution_tex=self.homogeneous_solution_tex(),
            null_space_span_tex=self.null_space_span_tex(),
            previous_particular_solution=self.DEFAULT_PREVIOUS_PARTICULAR_SOLUTION.copy(),
            previous_nonhomogeneous_solution_tex=self.previous_nonhomogeneous_solution_tex(),
            rank_one_rref_augmented=self.rank_one_rref_augmented,
            rank_one_pivot_columns=self.rank_one_pivot_columns(),
            rank_one_free_columns=self.rank_one_free_columns(),
            rank_one_scalar_equations_tex=self.rank_one_scalar_equations_tex(),
            rank_one_particular_solution=self.rank_one_particular_solution(),
            rank_one_special_solutions=self.rank_one_special_solutions(),
            rank_one_solution_tex=self.rank_one_solution_tex(),
            rank_one_associated_null_space_tex=self.rank_one_associated_null_space_tex(),
        )
