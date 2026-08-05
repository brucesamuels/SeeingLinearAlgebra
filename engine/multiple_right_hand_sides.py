"""Renderer-independent mathematics for CP121.

Checkpoint 121 solves several systems with the same coefficient matrix,
compares repeated elimination with one reusable LU factorization, and records
both exact and asymptotic operation counts.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class BlockEliminationStep:
    """One elimination operation applied to the full block [A | B]."""

    index: int
    operation_tex: str
    target_row: int
    before_block: FloatArray
    after_block: FloatArray


@dataclass(frozen=True)
class OperationCountComparison:
    """Exact scalar-operation counts under one stated counting convention."""

    matrix_size: int
    right_hand_sides: int
    factorization_operations: int
    forward_substitution_per_rhs: int
    back_substitution_per_rhs: int
    triangular_solve_per_rhs: int
    repeated_reduction_total: int
    factor_once_total: int
    savings: int


@dataclass(frozen=True)
class MultipleRightHandSidesSnapshot:
    """Immutable mathematical data consumed by the CP121 presentation."""

    coefficient_matrix: FloatArray
    right_hand_sides: FloatArray
    solution_matrix: FloatArray
    lower_triangular_matrix: FloatArray
    upper_triangular_matrix: FloatArray
    intermediate_matrix: FloatArray
    block_elimination_steps: tuple[BlockEliminationStep, ...]
    reduced_block: FloatArray
    operation_counts: OperationCountComparison
    block_system_tex: str
    forward_substitution_tex: str
    back_substitution_tex: str
    verification_tex: str


class MultipleRightHandSides:
    """Solve AX = B by block elimination and by one reusable LU factorization."""

    DEFAULT_A = np.array(
        [
            [2.0, 1.0, 1.0],
            [4.0, -6.0, 0.0],
            [-2.0, 7.0, 2.0],
        ],
        dtype=float,
    )
    DEFAULT_B = np.array(
        [
            [3.0, 0.0],
            [4.0, -6.0],
            [0.0, 5.0],
        ],
        dtype=float,
    )

    def __init__(
        self,
        coefficient_matrix: Iterable[Iterable[float]] | FloatArray | None = None,
        right_hand_sides: Iterable[Iterable[float]] | FloatArray | None = None,
        *,
        atol: float = 1e-9,
    ) -> None:
        a = np.array(self.DEFAULT_A if coefficient_matrix is None else coefficient_matrix, dtype=float, copy=True)
        b = np.array(self.DEFAULT_B if right_hand_sides is None else right_hand_sides, dtype=float, copy=True)
        if a.shape != (3, 3):
            raise ValueError("coefficient_matrix must have shape (3, 3).")
        if b.ndim != 2 or b.shape[0] != 3 or b.shape[1] < 1:
            raise ValueError("right_hand_sides must have shape (3, m) with m >= 1.")
        if not np.isfinite(a).all() or not np.isfinite(b).all():
            raise ValueError("matrix entries must be finite.")
        if atol <= 0:
            raise ValueError("atol must be positive.")
        self._a = a
        self._b = b
        self._atol = float(atol)
        self._steps, self._u, self._y, self._multipliers = self._eliminate_block()
        self._l = self._lower_factor()
        self._x = self._back_substitute_multiple(self._u, self._y)

    @property
    def coefficient_matrix(self) -> FloatArray:
        return self._a.copy()

    @property
    def right_hand_sides(self) -> FloatArray:
        return self._b.copy()

    @property
    def lower_triangular_matrix(self) -> FloatArray:
        return self._l.copy()

    @property
    def upper_triangular_matrix(self) -> FloatArray:
        return self._u.copy()

    @property
    def intermediate_matrix(self) -> FloatArray:
        return self._y.copy()

    @property
    def solution_matrix(self) -> FloatArray:
        return self._x.copy()

    @property
    def block_elimination_steps(self) -> tuple[BlockEliminationStep, ...]:
        return tuple(self._copy_step(step) for step in self._steps)

    def _eliminate_block(
        self,
    ) -> tuple[tuple[BlockEliminationStep, ...], FloatArray, FloatArray, tuple[tuple[int, int, float], ...]]:
        block = np.hstack([self._a, self._b])
        steps: list[BlockEliminationStep] = []
        multipliers: list[tuple[int, int, float]] = []
        index = 1
        for pivot_row in range(2):
            pivot = block[pivot_row, pivot_row]
            if abs(pivot) <= self._atol:
                raise ValueError("This lesson requires elimination without row exchanges.")
            for target_row in range(pivot_row + 1, 3):
                entry = block[target_row, pivot_row]
                if abs(entry) <= self._atol:
                    continue
                multiplier = entry / pivot
                before = block.copy()
                block[target_row, :] = block[target_row, :] - multiplier * block[pivot_row, :]
                block[np.abs(block) <= self._atol] = 0.0
                operation_tex = self._operation_tex(
                    target_row=target_row,
                    pivot_row=pivot_row,
                    multiplier=multiplier,
                )
                steps.append(
                    BlockEliminationStep(
                        index=index,
                        operation_tex=operation_tex,
                        target_row=target_row,
                        before_block=before,
                        after_block=block.copy(),
                    )
                )
                multipliers.append((target_row, pivot_row, float(multiplier)))
                index += 1
        if len(steps) != 3:
            raise ValueError("This checkpoint expects three nonzero elimination steps.")
        return tuple(steps), block[:, :3].copy(), block[:, 3:].copy(), tuple(multipliers)

    def _lower_factor(self) -> FloatArray:
        lower = np.eye(3, dtype=float)
        for target_row, pivot_row, multiplier in self._multipliers:
            lower[target_row, pivot_row] = multiplier
        return lower

    @staticmethod
    def _back_substitute_multiple(u: FloatArray, y: FloatArray) -> FloatArray:
        n, m = y.shape
        x = np.zeros((n, m), dtype=float)
        for row in range(n - 1, -1, -1):
            remainder = u[row, row + 1 :] @ x[row + 1 :, :]
            x[row, :] = (y[row, :] - remainder) / u[row, row]
        return x

    def forward_substitution_result(self) -> FloatArray:
        return np.linalg.solve(self._l, self._b)

    def verifies_block_elimination(self) -> bool:
        final_block = self._steps[-1].after_block
        return bool(np.allclose(final_block, np.hstack([self._u, self._y])))

    def verifies_lu_factorization(self) -> bool:
        return bool(np.allclose(self._l @ self._u, self._a))

    def verifies_forward_substitution(self) -> bool:
        return bool(np.allclose(self._l @ self._y, self._b))

    def verifies_solution(self) -> bool:
        return bool(np.allclose(self._a @ self._x, self._b))

    def operation_counts(self) -> OperationCountComparison:
        n = self._a.shape[0]
        m = self._b.shape[1]
        # Convention: one addition/subtraction, multiplication, or division is one operation.
        factorization = n * (n - 1) // 2 + 2 * sum(k * k for k in range(1, n))
        forward = n * (n - 1)
        back = n * (n - 1) + n
        triangular = forward + back
        repeated = m * (factorization + triangular)
        factor_once = factorization + m * triangular
        return OperationCountComparison(
            matrix_size=n,
            right_hand_sides=m,
            factorization_operations=factorization,
            forward_substitution_per_rhs=forward,
            back_substitution_per_rhs=back,
            triangular_solve_per_rhs=triangular,
            repeated_reduction_total=repeated,
            factor_once_total=factor_once,
            savings=repeated - factor_once,
        )

    @staticmethod
    def block_system_tex() -> str:
        return r"AX=B"

    @staticmethod
    def forward_substitution_tex() -> str:
        return r"LY=B"

    @staticmethod
    def back_substitution_tex() -> str:
        return r"UX=Y"

    @staticmethod
    def verification_tex() -> str:
        return r"AX=B"

    def snapshot(self) -> MultipleRightHandSidesSnapshot:
        return MultipleRightHandSidesSnapshot(
            coefficient_matrix=self.coefficient_matrix,
            right_hand_sides=self.right_hand_sides,
            solution_matrix=self.solution_matrix,
            lower_triangular_matrix=self.lower_triangular_matrix,
            upper_triangular_matrix=self.upper_triangular_matrix,
            intermediate_matrix=self.intermediate_matrix,
            block_elimination_steps=self.block_elimination_steps,
            reduced_block=np.hstack([self._u, self._y]),
            operation_counts=self.operation_counts(),
            block_system_tex=self.block_system_tex(),
            forward_substitution_tex=self.forward_substitution_tex(),
            back_substitution_tex=self.back_substitution_tex(),
            verification_tex=self.verification_tex(),
        )

    @classmethod
    def _operation_tex(cls, *, target_row: int, pivot_row: int, multiplier: float) -> str:
        target = target_row + 1
        pivot = pivot_row + 1
        magnitude = abs(multiplier)
        coefficient = "" if abs(magnitude - 1.0) < 1e-9 else cls._tex_number(magnitude)
        sign = "-" if multiplier > 0 else "+"
        return rf"R_{target}\leftarrow R_{target}{sign}{coefficient}R_{pivot}"

    @staticmethod
    def _tex_number(value: float) -> str:
        rounded = int(round(value))
        if abs(value - rounded) < 1e-9:
            return str(rounded)
        return f"{value:g}"

    @staticmethod
    def _copy_step(step: BlockEliminationStep) -> BlockEliminationStep:
        return BlockEliminationStep(
            index=step.index,
            operation_tex=step.operation_tex,
            target_row=step.target_row,
            before_block=step.before_block.copy(),
            after_block=step.after_block.copy(),
        )
