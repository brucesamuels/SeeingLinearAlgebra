"""Renderer-independent mathematics for CP120.

Checkpoint 120 develops Gaussian elimination as a product of elementary
matrices and then reverses that product to obtain the LU factorization.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class EliminationStep:
    """One row-elimination step represented by left multiplication."""

    index: int
    pivot_row: int
    target_row: int
    multiplier: float
    operation_tex: str
    elementary_matrix: FloatArray
    inverse_elementary_matrix: FloatArray
    before_matrix: FloatArray
    after_matrix: FloatArray


@dataclass(frozen=True)
class EliminationMatrixMultiplicationSnapshot:
    """Immutable data consumed by the CP120 presentation."""

    original_matrix: FloatArray
    elimination_steps: tuple[EliminationStep, ...]
    upper_triangular_matrix: FloatArray
    elimination_product: FloatArray
    lower_triangular_matrix: FloatArray
    elimination_product_tex: str
    inverse_product_tex: str
    lu_factorization_tex: str


class EliminationMatrixMultiplication:
    """Compute elimination matrices and the corresponding LU factorization."""

    DEFAULT_MATRIX = np.array(
        [
            [2.0, 1.0, 1.0],
            [4.0, -6.0, 0.0],
            [-2.0, 7.0, 2.0],
        ],
        dtype=float,
    )

    def __init__(
        self,
        matrix: Iterable[Iterable[float]] | FloatArray | None = None,
        *,
        atol: float = 1e-9,
    ) -> None:
        candidate = np.array(self.DEFAULT_MATRIX if matrix is None else matrix, dtype=float, copy=True)
        if candidate.shape != (3, 3):
            raise ValueError("matrix must have shape (3, 3).")
        if not np.isfinite(candidate).all():
            raise ValueError("matrix entries must be finite.")
        if atol <= 0:
            raise ValueError("atol must be positive.")
        self._matrix = candidate
        self._atol = float(atol)
        self._steps, self._upper = self._compute_steps()

    @property
    def original_matrix(self) -> FloatArray:
        return self._matrix.copy()

    @property
    def upper_triangular_matrix(self) -> FloatArray:
        return self._upper.copy()

    @property
    def elimination_steps(self) -> tuple[EliminationStep, ...]:
        return tuple(self._copy_step(step) for step in self._steps)

    def _compute_steps(self) -> tuple[tuple[EliminationStep, ...], FloatArray]:
        working = self._matrix.copy()
        steps: list[EliminationStep] = []
        index = 1
        for pivot_row in range(2):
            pivot = working[pivot_row, pivot_row]
            if abs(pivot) <= self._atol:
                raise ValueError("This lesson requires elimination without row exchanges.")
            for target_row in range(pivot_row + 1, 3):
                entry = working[target_row, pivot_row]
                if abs(entry) <= self._atol:
                    continue
                multiplier = entry / pivot
                elementary = np.eye(3, dtype=float)
                elementary[target_row, pivot_row] = -multiplier
                inverse = np.eye(3, dtype=float)
                inverse[target_row, pivot_row] = multiplier
                before = working.copy()
                working = elementary @ working
                working[np.abs(working) <= self._atol] = 0.0
                operation_tex = (
                    rf"R_{{{target_row + 1}}}\leftarrow "
                    rf"R_{{{target_row + 1}}}-({self._tex_number(multiplier)})R_{{{pivot_row + 1}}}"
                )
                steps.append(
                    EliminationStep(
                        index=index,
                        pivot_row=pivot_row,
                        target_row=target_row,
                        multiplier=float(multiplier),
                        operation_tex=operation_tex,
                        elementary_matrix=elementary.copy(),
                        inverse_elementary_matrix=inverse.copy(),
                        before_matrix=before,
                        after_matrix=working.copy(),
                    )
                )
                index += 1
        if len(steps) != 3:
            raise ValueError("This checkpoint expects three nonzero elimination steps.")
        return tuple(steps), working.copy()

    def elimination_product(self) -> FloatArray:
        product = np.eye(3, dtype=float)
        for step in self._steps:
            product = step.elementary_matrix @ product
        product[np.abs(product) <= self._atol] = 0.0
        return product

    def lower_triangular_matrix(self) -> FloatArray:
        lower = np.eye(3, dtype=float)
        for step in self._steps:
            lower = lower @ step.inverse_elementary_matrix
        lower[np.abs(lower) <= self._atol] = 0.0
        return lower

    def verifies_elimination_product(self) -> bool:
        return bool(np.allclose(self.elimination_product() @ self.original_matrix, self.upper_triangular_matrix))

    def verifies_lu_factorization(self) -> bool:
        return bool(np.allclose(self.lower_triangular_matrix() @ self.upper_triangular_matrix, self.original_matrix))

    def multiplier_positions(self) -> tuple[tuple[int, int, float], ...]:
        return tuple((step.target_row, step.pivot_row, step.multiplier) for step in self._steps)

    @staticmethod
    def elimination_product_tex() -> str:
        return r"E_3E_2E_1A=U"

    @staticmethod
    def inverse_product_tex() -> str:
        return r"A=E_1^{-1}E_2^{-1}E_3^{-1}U"

    @staticmethod
    def lu_factorization_tex() -> str:
        return r"A=LU"

    def snapshot(self) -> EliminationMatrixMultiplicationSnapshot:
        return EliminationMatrixMultiplicationSnapshot(
            original_matrix=self.original_matrix,
            elimination_steps=self.elimination_steps,
            upper_triangular_matrix=self.upper_triangular_matrix,
            elimination_product=self.elimination_product(),
            lower_triangular_matrix=self.lower_triangular_matrix(),
            elimination_product_tex=self.elimination_product_tex(),
            inverse_product_tex=self.inverse_product_tex(),
            lu_factorization_tex=self.lu_factorization_tex(),
        )

    @staticmethod
    def _copy_step(step: EliminationStep) -> EliminationStep:
        return EliminationStep(
            index=step.index,
            pivot_row=step.pivot_row,
            target_row=step.target_row,
            multiplier=step.multiplier,
            operation_tex=step.operation_tex,
            elementary_matrix=step.elementary_matrix.copy(),
            inverse_elementary_matrix=step.inverse_elementary_matrix.copy(),
            before_matrix=step.before_matrix.copy(),
            after_matrix=step.after_matrix.copy(),
        )

    @staticmethod
    def _tex_number(value: float) -> str:
        rounded = int(round(value))
        if abs(value - rounded) < 1e-9:
            return str(rounded)
        return f"{value:g}"
