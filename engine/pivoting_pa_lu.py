"""Renderer-independent mathematics for CP124.

Checkpoint 124 introduces row pivoting and the factorization PA = LU.  A zero
first pivot forces a row exchange, while a tiny pivot motivates partial
pivoting in floating-point arithmetic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class PivotingStep:
    """One elimination step applied after the row permutation."""

    index: int
    pivot_column: int
    multiplier: float
    operation_tex: str
    explanation: str
    target_row: int
    before_matrix: FloatArray
    after_matrix: FloatArray


@dataclass(frozen=True)
class PivotingPALUSnapshot:
    """Immutable mathematical data used by the CP124 presentation."""

    coefficient_matrix: FloatArray
    permutation_matrix: FloatArray
    permuted_matrix: FloatArray
    steps: tuple[PivotingStep, ...]
    lower_triangular: FloatArray
    upper_triangular: FloatArray
    determinant: float
    tiny_matrix: FloatArray
    tiny_epsilon: float
    multiplier_without_pivoting: float
    multiplier_with_pivoting: float
    no_swap_second_entry: float
    pivoted_second_entry: float
    factorization_tex: str
    reconstruction_tex: str
    partial_pivot_rule_tex: str


class PivotingPALU:
    """Analyze a fixed 3 by 3 example requiring a row exchange."""

    DEFAULT_A = np.array(
        [
            [0.0, 2.0, 1.0],
            [2.0, 2.0, 3.0],
            [4.0, -2.0, 1.0],
        ],
        dtype=float,
    )

    DEFAULT_EPSILON = 1.0e-4

    def __init__(
        self,
        coefficient_matrix: Iterable[Iterable[float]] | FloatArray | None = None,
        *,
        epsilon: float = DEFAULT_EPSILON,
        atol: float = 1e-9,
    ) -> None:
        matrix = np.array(
            self.DEFAULT_A if coefficient_matrix is None else coefficient_matrix,
            dtype=float,
            copy=True,
        )
        if matrix.shape != (3, 3):
            raise ValueError("coefficient_matrix must have shape (3, 3).")
        if not np.isfinite(matrix).all():
            raise ValueError("matrix entries must be finite.")
        if not np.isfinite(atol) or atol <= 0:
            raise ValueError("atol must be a positive finite number.")
        if not np.allclose(matrix, self.DEFAULT_A, atol=atol):
            raise ValueError("CP124 uses the fixed classroom matrix shown in the lesson.")
        if not np.isfinite(epsilon) or not 0 < epsilon < 1:
            raise ValueError("epsilon must be finite and satisfy 0 < epsilon < 1.")

        self._a = matrix
        self._epsilon = float(epsilon)
        self._atol = float(atol)
        self._p = np.array(
            [
                [0.0, 1.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0],
            ],
            dtype=float,
        )
        self._pa = self._p @ self._a
        self._steps = self._build_steps()
        self._u = self._steps[-1].after_matrix.copy()
        self._l = self._build_lower_triangular()

    @property
    def coefficient_matrix(self) -> FloatArray:
        return self._a.copy()

    @property
    def permutation_matrix(self) -> FloatArray:
        return self._p.copy()

    @property
    def permuted_matrix(self) -> FloatArray:
        return self._pa.copy()

    @property
    def steps(self) -> tuple[PivotingStep, ...]:
        return tuple(self._copy_step(step) for step in self._steps)

    @property
    def lower_triangular(self) -> FloatArray:
        return self._l.copy()

    @property
    def upper_triangular(self) -> FloatArray:
        return self._u.copy()

    @property
    def determinant(self) -> float:
        return float(np.linalg.det(self._a))

    @property
    def tiny_matrix(self) -> FloatArray:
        return np.array(
            [
                [self._epsilon, 1.0],
                [1.0, 1.0],
            ],
            dtype=float,
        )

    @property
    def tiny_epsilon(self) -> float:
        return self._epsilon

    @property
    def multiplier_without_pivoting(self) -> float:
        return 1.0 / self._epsilon

    @property
    def multiplier_with_pivoting(self) -> float:
        return self._epsilon

    @property
    def no_swap_second_entry(self) -> float:
        return 1.0 - self.multiplier_without_pivoting

    @property
    def pivoted_second_entry(self) -> float:
        return 1.0 - self.multiplier_with_pivoting

    def verifies_factorization(self) -> bool:
        return bool(np.allclose(self._p @ self._a, self._l @ self._u, atol=self._atol))

    def verifies_reconstruction(self) -> bool:
        return bool(np.allclose(self._a, self._p.T @ self._l @ self._u, atol=self._atol))

    def verifies_permutation_properties(self) -> bool:
        identity = np.eye(3, dtype=float)
        return bool(
            np.allclose(self._p.T @ self._p, identity, atol=self._atol)
            and np.allclose(np.linalg.inv(self._p), self._p.T, atol=self._atol)
        )

    @staticmethod
    def factorization_tex() -> str:
        return r"PA=LU"

    @staticmethod
    def reconstruction_tex() -> str:
        return r"A=P^TLU"

    @staticmethod
    def partial_pivot_rule_tex() -> str:
        return r"p=\operatorname*{arg\,max}_{i\ge k}|a_{ik}|"

    def snapshot(self) -> PivotingPALUSnapshot:
        return PivotingPALUSnapshot(
            coefficient_matrix=self.coefficient_matrix,
            permutation_matrix=self.permutation_matrix,
            permuted_matrix=self.permuted_matrix,
            steps=self.steps,
            lower_triangular=self.lower_triangular,
            upper_triangular=self.upper_triangular,
            determinant=self.determinant,
            tiny_matrix=self.tiny_matrix,
            tiny_epsilon=self.tiny_epsilon,
            multiplier_without_pivoting=self.multiplier_without_pivoting,
            multiplier_with_pivoting=self.multiplier_with_pivoting,
            no_swap_second_entry=self.no_swap_second_entry,
            pivoted_second_entry=self.pivoted_second_entry,
            factorization_tex=self.factorization_tex(),
            reconstruction_tex=self.reconstruction_tex(),
            partial_pivot_rule_tex=self.partial_pivot_rule_tex(),
        )

    def _build_steps(self) -> tuple[PivotingStep, ...]:
        matrix = self._pa.copy()
        steps: list[PivotingStep] = []

        multiplier_31 = float(matrix[2, 0] / matrix[0, 0])
        before = matrix.copy()
        matrix[2, :] = matrix[2, :] - multiplier_31 * matrix[0, :]
        matrix[np.abs(matrix) <= self._atol] = 0.0
        steps.append(
            PivotingStep(
                index=1,
                pivot_column=0,
                multiplier=multiplier_31,
                operation_tex=r"m_{31}=2,\qquad R_3\leftarrow R_3-2R_1",
                explanation="Use the new first pivot to clear the entry beneath it.",
                target_row=2,
                before_matrix=before,
                after_matrix=matrix.copy(),
            )
        )

        multiplier_32 = float(matrix[2, 1] / matrix[1, 1])
        before = matrix.copy()
        matrix[2, :] = matrix[2, :] - multiplier_32 * matrix[1, :]
        matrix[np.abs(matrix) <= self._atol] = 0.0
        steps.append(
            PivotingStep(
                index=2,
                pivot_column=1,
                multiplier=multiplier_32,
                operation_tex=(
                    r"m_{32}=-3,\qquad "
                    r"R_3\leftarrow R_3-(-3)R_2=R_3+3R_2"
                ),
                explanation="The second multiplier is negative, so subtracting it adds three rows.",
                target_row=2,
                before_matrix=before,
                after_matrix=matrix.copy(),
            )
        )
        return tuple(steps)

    def _build_lower_triangular(self) -> FloatArray:
        lower = np.eye(3, dtype=float)
        lower[2, 0] = self._steps[0].multiplier
        lower[2, 1] = self._steps[1].multiplier
        return lower

    @staticmethod
    def _copy_step(step: PivotingStep) -> PivotingStep:
        return PivotingStep(
            index=step.index,
            pivot_column=step.pivot_column,
            multiplier=step.multiplier,
            operation_tex=step.operation_tex,
            explanation=step.explanation,
            target_row=step.target_row,
            before_matrix=step.before_matrix.copy(),
            after_matrix=step.after_matrix.copy(),
        )
