"""Renderer-independent mathematics for CP117.

Checkpoint 117 develops the complete solution of a consistent system as one
particular solution plus an arbitrary vector from the null space.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class CompleteSolutionSnapshot:
    """Immutable mathematical data used by the CP117 presentation."""

    rref_augmented: FloatArray
    associated_homogeneous_rref: FloatArray
    coefficient_matrix: FloatArray
    right_hand_side: FloatArray
    pivot_columns: tuple[int, ...]
    free_columns: tuple[int, ...]
    particular_solution: FloatArray
    first_special_solution: FloatArray
    second_special_solution: FloatArray
    null_space_basis: tuple[FloatArray, ...]
    particular_solution_tex: str
    null_space_solution_tex: str
    complete_solution_tex: str
    verification_tex: tuple[str, ...]
    converse_tex: tuple[str, ...]


class CompleteSolution:
    """Describe the complete solution of a rank-one system in R^3."""

    DEFAULT_RREF_AUGMENTED = np.array(
        [
            [1.0, 2.0, -1.0, 3.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
        ],
        dtype=float,
    )

    def __init__(
        self,
        rref_augmented: Iterable[Iterable[float]] | FloatArray | None = None,
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
        if len(parameter_names) != 2 or len(set(parameter_names)) != 2:
            raise ValueError("parameter_names must contain two distinct names.")
        if any(not name for name in parameter_names):
            raise ValueError("parameter names must be nonempty.")
        self._matrix = matrix
        self._parameter_names = tuple(parameter_names)

    @property
    def rref_augmented(self) -> FloatArray:
        return self._matrix.copy()

    @property
    def coefficient_matrix(self) -> FloatArray:
        return self._matrix[:, :-1].copy()

    @property
    def right_hand_side(self) -> FloatArray:
        return self._matrix[:, -1].copy()

    @property
    def associated_homogeneous_rref(self) -> FloatArray:
        homogeneous = self._matrix.copy()
        homogeneous[:, -1] = 0.0
        return homogeneous

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

    def particular_solution(self) -> FloatArray:
        """Set both free variables equal to zero."""
        return np.array([3.0, 0.0, 0.0], dtype=float)

    def first_special_solution(self) -> FloatArray:
        return np.array([-2.0, 1.0, 0.0], dtype=float)

    def second_special_solution(self) -> FloatArray:
        return np.array([1.0, 0.0, 1.0], dtype=float)

    def null_space_basis(self) -> tuple[FloatArray, ...]:
        return (self.first_special_solution(), self.second_special_solution())

    def null_space_vector(self, first: float, second: float) -> FloatArray:
        if not np.isfinite(first) or not np.isfinite(second):
            raise ValueError("parameter values must be finite.")
        s1, s2 = self.null_space_basis()
        return float(first) * s1 + float(second) * s2

    def complete_solution(self, first: float, second: float) -> FloatArray:
        return self.particular_solution() + self.null_space_vector(first, second)

    def satisfies_nonhomogeneous_system(
        self,
        point: Iterable[float] | FloatArray,
        *,
        atol: float = 1e-9,
    ) -> bool:
        candidate = np.array(point, dtype=float, copy=True)
        if candidate.shape != (3,):
            raise ValueError("point must have shape (3,).")
        residual = self.coefficient_matrix @ candidate - self.right_hand_side
        return bool(np.all(np.abs(residual) <= atol))

    def satisfies_homogeneous_system(
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

    def difference_from_particular_is_null(
        self,
        point: Iterable[float] | FloatArray,
        *,
        atol: float = 1e-9,
    ) -> bool:
        candidate = np.array(point, dtype=float, copy=True)
        if candidate.shape != (3,):
            raise ValueError("point must have shape (3,).")
        if not self.satisfies_nonhomogeneous_system(candidate, atol=atol):
            return False
        return self.satisfies_homogeneous_system(candidate - self.particular_solution(), atol=atol)

    def particular_solution_tex(self) -> str:
        return r"\mathbf{x}_p=\begin{bmatrix}3\\0\\0\end{bmatrix}"

    def null_space_solution_tex(self) -> str:
        first, second = self._parameter_names
        return (
            r"\mathbf{x}_n="
            + first
            + r"\begin{bmatrix}-2\\1\\0\end{bmatrix}+"
            + second
            + r"\begin{bmatrix}1\\0\\1\end{bmatrix}"
        )

    def complete_solution_tex(self) -> str:
        first, second = self._parameter_names
        return (
            r"\mathbf{x}=\begin{bmatrix}3\\0\\0\end{bmatrix}+"
            + first
            + r"\begin{bmatrix}-2\\1\\0\end{bmatrix}+"
            + second
            + r"\begin{bmatrix}1\\0\\1\end{bmatrix}"
        )

    def verification_tex(self) -> tuple[str, ...]:
        return (
            r"A(\mathbf{x}_p+\mathbf{x}_n)=A\mathbf{x}_p+A\mathbf{x}_n",
            r"=\mathbf{b}+\mathbf{0}",
            r"=\mathbf{b}",
        )

    def converse_tex(self) -> tuple[str, ...]:
        return (
            r"A\mathbf{x}=\mathbf{b},\qquad A\mathbf{x}_p=\mathbf{b}",
            r"A(\mathbf{x}-\mathbf{x}_p)=\mathbf{0}",
            r"\mathbf{x}-\mathbf{x}_p\in N(A)",
            r"\mathbf{x}=\mathbf{x}_p+\mathbf{x}_n",
        )

    def snapshot(self) -> CompleteSolutionSnapshot:
        return CompleteSolutionSnapshot(
            rref_augmented=self.rref_augmented,
            associated_homogeneous_rref=self.associated_homogeneous_rref,
            coefficient_matrix=self.coefficient_matrix,
            right_hand_side=self.right_hand_side,
            pivot_columns=self.pivot_columns(),
            free_columns=self.free_columns(),
            particular_solution=self.particular_solution(),
            first_special_solution=self.first_special_solution(),
            second_special_solution=self.second_special_solution(),
            null_space_basis=self.null_space_basis(),
            particular_solution_tex=self.particular_solution_tex(),
            null_space_solution_tex=self.null_space_solution_tex(),
            complete_solution_tex=self.complete_solution_tex(),
            verification_tex=self.verification_tex(),
            converse_tex=self.converse_tex(),
        )
