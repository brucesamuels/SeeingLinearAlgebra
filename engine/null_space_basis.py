"""Renderer-independent mathematics for CP116.

Checkpoint 116 constructs a basis for the null space by assigning one free
variable the value 1 and the remaining free variables the value 0, one at a
time.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class NullSpaceBasisSnapshot:
    """Immutable mathematical data used by the CP116 presentation."""

    rref_augmented: FloatArray
    coefficient_matrix: FloatArray
    pivot_columns: tuple[int, ...]
    free_columns: tuple[int, ...]
    free_variables: tuple[str, ...]
    first_assignment: tuple[float, float]
    second_assignment: tuple[float, float]
    first_special_solution: FloatArray
    second_special_solution: FloatArray
    basis: tuple[FloatArray, ...]
    nullity: int
    rank: int
    general_solution_tex: str
    null_space_span_tex: str


class NullSpaceBasis:
    """Construct and verify a basis for a rank-one null space in R^3."""

    DEFAULT_RREF_AUGMENTED = np.array(
        [
            [1.0, 2.0, -1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
        ],
        dtype=float,
    )

    def __init__(
        self,
        rref_augmented: Iterable[Iterable[float]] | FloatArray | None = None,
        variable_names: tuple[str, ...] = ("x", "y", "z"),
        parameter_names: tuple[str, str] = ("s", "t"),
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
        if not np.allclose(matrix[:, -1], 0.0):
            raise ValueError("the null-space system must have a zero right-hand side.")
        if len(variable_names) != 3 or len(set(variable_names)) != 3:
            raise ValueError("variable_names must contain three distinct names.")
        if len(parameter_names) != 2 or len(set(parameter_names)) != 2:
            raise ValueError("parameter_names must contain two distinct names.")
        if any(not name for name in parameter_names):
            raise ValueError("parameter names must be nonempty.")
        self._matrix = matrix
        self._variable_names = tuple(variable_names)
        self._parameter_names = tuple(parameter_names)

    @property
    def rref_augmented(self) -> FloatArray:
        return self._matrix.copy()

    @property
    def coefficient_matrix(self) -> FloatArray:
        return self._matrix[:, :-1].copy()

    def pivot_columns(self, *, atol: float = 1e-9) -> tuple[int, ...]:
        pivots: list[int] = []
        for row in self.coefficient_matrix:
            nonzero = np.flatnonzero(np.abs(row) > atol)
            if nonzero.size:
                pivots.append(int(nonzero[0]))
        return tuple(pivots)

    def free_columns(self) -> tuple[int, ...]:
        pivots = set(self.pivot_columns())
        return tuple(index for index in range(3) if index not in pivots)

    def first_special_solution(self) -> FloatArray:
        """Set y=1 and z=0."""
        return np.array([-2.0, 1.0, 0.0], dtype=float)

    def second_special_solution(self) -> FloatArray:
        """Set y=0 and z=1."""
        return np.array([1.0, 0.0, 1.0], dtype=float)

    def basis(self) -> tuple[FloatArray, ...]:
        return (self.first_special_solution(), self.second_special_solution())

    def vector_from_parameters(self, first: float, second: float) -> FloatArray:
        if not np.isfinite(first) or not np.isfinite(second):
            raise ValueError("parameter values must be finite.")
        s1, s2 = self.basis()
        return float(first) * s1 + float(second) * s2

    def satisfies_null_space_system(
        self,
        point: Iterable[float] | FloatArray,
        *,
        atol: float = 1e-9,
    ) -> bool:
        candidate = np.array(point, dtype=float, copy=True)
        if candidate.shape != (3,):
            raise ValueError("point must have shape (3,).")
        residual = self.coefficient_matrix @ candidate
        return bool(np.all(np.abs(residual) <= atol))

    def basis_is_independent(self, *, atol: float = 1e-9) -> bool:
        basis_matrix = np.column_stack(self.basis())
        return bool(np.linalg.matrix_rank(basis_matrix, tol=atol) == 2)

    def rank(self) -> int:
        return len(self.pivot_columns())

    def nullity(self) -> int:
        return len(self.free_columns())

    def general_solution_tex(self) -> str:
        first, second = self._parameter_names
        return (
            r"\mathbf{x}="
            + first
            + r"\begin{bmatrix}-2\\1\\0\end{bmatrix}+"
            + second
            + r"\begin{bmatrix}1\\0\\1\end{bmatrix}"
        )

    def null_space_span_tex(self) -> str:
        return (
            r"N(A)=\operatorname{span}\left\{"
            r"\begin{bmatrix}-2\\1\\0\end{bmatrix},"
            r"\begin{bmatrix}1\\0\\1\end{bmatrix}"
            r"\right\}"
        )

    def snapshot(self) -> NullSpaceBasisSnapshot:
        free = self.free_columns()
        return NullSpaceBasisSnapshot(
            rref_augmented=self.rref_augmented,
            coefficient_matrix=self.coefficient_matrix,
            pivot_columns=self.pivot_columns(),
            free_columns=free,
            free_variables=tuple(self._variable_names[index] for index in free),
            first_assignment=(1.0, 0.0),
            second_assignment=(0.0, 1.0),
            first_special_solution=self.first_special_solution(),
            second_special_solution=self.second_special_solution(),
            basis=self.basis(),
            nullity=self.nullity(),
            rank=self.rank(),
            general_solution_tex=self.general_solution_tex(),
            null_space_span_tex=self.null_space_span_tex(),
        )
