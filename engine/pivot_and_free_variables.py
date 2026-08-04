"""Renderer-independent mathematics for CP114.

Checkpoint 114 identifies pivot and free variables in an RREF system with one
free variable, then presents both the standard parameter method and Strang's
particular-plus-special-solution viewpoint.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class PivotFreeSnapshot:
    """Immutable data used by the CP114 presentation."""

    rref_augmented: FloatArray
    variable_names: tuple[str, ...]
    pivot_columns: tuple[int, ...]
    free_columns: tuple[int, ...]
    pivot_variables: tuple[str, ...]
    free_variables: tuple[str, ...]
    parameter_name: str
    scalar_equations_tex: tuple[str, ...]
    particular_solution: FloatArray
    special_solution: FloatArray
    parametric_vector_tex: str
    strang_solution_tex: str


class PivotAndFreeVariables:
    """Analyze an RREF system with one free variable in two equivalent ways."""

    DEFAULT_RREF_AUGMENTED = np.array(
        [
            [1.0, 0.0, 2.0, 4.0],
            [0.0, 1.0, -1.0, 1.0],
            [0.0, 0.0, 0.0, 0.0],
        ],
        dtype=float,
    )

    def __init__(
        self,
        rref_augmented: Iterable[Iterable[float]] | FloatArray | None = None,
        variable_names: tuple[str, ...] = ("x", "y", "z"),
        parameter_name: str = "t",
    ) -> None:
        matrix = np.array(
            self.DEFAULT_RREF_AUGMENTED if rref_augmented is None else rref_augmented,
            dtype=float,
            copy=True,
        )
        if matrix.shape != (3, 4):
            raise ValueError("rref_augmented must have shape (3, 4).")
        if not np.isfinite(matrix).all():
            raise ValueError("rref_augmented entries must be finite.")
        if len(variable_names) != 3 or len(set(variable_names)) != 3:
            raise ValueError("variable_names must contain three distinct names.")
        if not parameter_name:
            raise ValueError("parameter_name must be nonempty.")
        self._matrix = matrix
        self._variable_names = tuple(variable_names)
        self._parameter_name = parameter_name

    @property
    def rref_augmented(self) -> FloatArray:
        return self._matrix.copy()

    def pivot_columns(self, *, atol: float = 1e-9) -> tuple[int, ...]:
        pivots: list[int] = []
        coefficient_block = self._matrix[:, :-1]
        for row in coefficient_block:
            nonzero = np.flatnonzero(np.abs(row) > atol)
            if nonzero.size:
                pivots.append(int(nonzero[0]))
        return tuple(pivots)

    def free_columns(self) -> tuple[int, ...]:
        pivots = set(self.pivot_columns())
        return tuple(index for index in range(3) if index not in pivots)

    def scalar_equations_tex(self) -> tuple[str, ...]:
        p = self._parameter_name
        return (
            r"x+2z=4",
            r"y-z=1",
            rf"z={p}",
            rf"x=4-2{p}",
            rf"y=1+{p}",
        )

    def particular_solution(self) -> FloatArray:
        return np.array([4.0, 1.0, 0.0], dtype=float)

    def special_solution(self) -> FloatArray:
        return np.array([-2.0, 1.0, 1.0], dtype=float)

    def solution_for_parameter(self, value: float) -> FloatArray:
        if not np.isfinite(value):
            raise ValueError("parameter value must be finite.")
        return self.particular_solution() + float(value) * self.special_solution()

    def satisfies_system(self, point: Iterable[float] | FloatArray, *, atol: float = 1e-9) -> bool:
        candidate = np.array(point, dtype=float, copy=True)
        if candidate.shape != (3,):
            raise ValueError("point must have shape (3,).")
        residual = self._matrix[:, :-1] @ candidate - self._matrix[:, -1]
        return bool(np.all(np.abs(residual) <= atol))

    def parametric_vector_tex(self) -> str:
        p = self._parameter_name
        return (
            r"\begin{bmatrix}x\\y\\z\end{bmatrix}="
            r"\begin{bmatrix}4\\1\\0\end{bmatrix}+"
            + p
            + r"\begin{bmatrix}-2\\1\\1\end{bmatrix}"
        )

    def strang_solution_tex(self) -> str:
        p = self._parameter_name
        return (
            r"\text{all solutions}="
            r"\begin{bmatrix}4\\1\\0\end{bmatrix}+"
            + p
            + r"\begin{bmatrix}-2\\1\\1\end{bmatrix}"
        )

    def snapshot(self) -> PivotFreeSnapshot:
        pivots = self.pivot_columns()
        free = self.free_columns()
        return PivotFreeSnapshot(
            rref_augmented=self.rref_augmented,
            variable_names=self._variable_names,
            pivot_columns=pivots,
            free_columns=free,
            pivot_variables=tuple(self._variable_names[i] for i in pivots),
            free_variables=tuple(self._variable_names[i] for i in free),
            parameter_name=self._parameter_name,
            scalar_equations_tex=self.scalar_equations_tex(),
            particular_solution=self.particular_solution(),
            special_solution=self.special_solution(),
            parametric_vector_tex=self.parametric_vector_tex(),
            strang_solution_tex=self.strang_solution_tex(),
        )
