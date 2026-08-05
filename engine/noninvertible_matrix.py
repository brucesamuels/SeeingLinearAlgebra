"""Renderer-independent mathematics for CP123.

Checkpoint 123 contrasts Gauss-Jordan inversion with a rank-deficient matrix.
The left side of [A | I] cannot become I, and the failure is connected to a
missing pivot, a nontrivial null space, dependent columns, and unit-vector
systems that are not all solvable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class NoninvertibilityStep:
    """One row operation applied across the augmented block [A | I]."""

    index: int
    operation_tex: str
    explanation: str
    target_row: int
    before_block: FloatArray
    after_block: FloatArray


@dataclass(frozen=True)
class NoninvertibleMatrixSnapshot:
    """Immutable mathematical data used by the CP123 presentation."""

    coefficient_matrix: FloatArray
    identity_matrix: FloatArray
    augmented_start: FloatArray
    steps: tuple[NoninvertibilityStep, ...]
    reduced_block: FloatArray
    left_rref: FloatArray
    transformed_identity: FloatArray
    rank: int
    pivot_columns: tuple[int, ...]
    free_columns: tuple[int, ...]
    null_vector: FloatArray
    column_relation_coefficients: FloatArray
    unit_system_statuses: tuple[str, ...]
    unit_system_contradictions: tuple[float, ...]
    failure_tex: str
    null_space_tex: str
    equivalence_tex: tuple[str, ...]


class NoninvertibleMatrix:
    """Analyze a fixed singular 3 by 3 classroom matrix."""

    DEFAULT_A = np.array(
        [
            [1.0, 2.0, 1.0],
            [2.0, 4.0, 2.0],
            [0.0, 1.0, 1.0],
        ],
        dtype=float,
    )

    def __init__(
        self,
        coefficient_matrix: Iterable[Iterable[float]] | FloatArray | None = None,
        *,
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
            raise ValueError("CP123 uses the fixed classroom matrix shown in the lesson.")

        self._a = matrix
        self._identity = np.eye(3, dtype=float)
        self._atol = float(atol)
        self._steps = self._build_steps()
        self._reduced = self._steps[-1].after_block.copy()

    @property
    def coefficient_matrix(self) -> FloatArray:
        return self._a.copy()

    @property
    def identity_matrix(self) -> FloatArray:
        return self._identity.copy()

    @property
    def augmented_start(self) -> FloatArray:
        return np.hstack([self._a, self._identity])

    @property
    def steps(self) -> tuple[NoninvertibilityStep, ...]:
        return tuple(self._copy_step(step) for step in self._steps)

    @property
    def reduced_block(self) -> FloatArray:
        return self._reduced.copy()

    @property
    def left_rref(self) -> FloatArray:
        return self._reduced[:, :3].copy()

    @property
    def transformed_identity(self) -> FloatArray:
        return self._reduced[:, 3:].copy()

    @property
    def rank(self) -> int:
        return int(np.linalg.matrix_rank(self._a, tol=self._atol))

    @property
    def pivot_columns(self) -> tuple[int, ...]:
        pivots: list[int] = []
        for row in self.left_rref:
            nonzero = np.flatnonzero(np.abs(row) > self._atol)
            if nonzero.size:
                pivots.append(int(nonzero[0]))
        return tuple(pivots)

    @property
    def free_columns(self) -> tuple[int, ...]:
        pivots = set(self.pivot_columns)
        return tuple(index for index in range(3) if index not in pivots)

    @property
    def null_vector(self) -> FloatArray:
        return np.array([1.0, -1.0, 1.0], dtype=float)

    @property
    def column_relation_coefficients(self) -> FloatArray:
        return self.null_vector

    @property
    def unit_system_statuses(self) -> tuple[str, ...]:
        statuses: list[str] = []
        for column in range(3):
            rhs = self._identity[:, column]
            augmented_rank = int(
                np.linalg.matrix_rank(np.column_stack([self._a, rhs]), tol=self._atol)
            )
            if augmented_rank > self.rank:
                statuses.append("none")
            elif self.rank < 3:
                statuses.append("infinite")
            else:
                statuses.append("unique")
        return tuple(statuses)

    @property
    def unit_system_contradictions(self) -> tuple[float, ...]:
        """Final zero-row right-hand entries for e1, e2, and e3."""
        return tuple(float(value) for value in self.transformed_identity[2, :])

    def verifies_singular(self) -> bool:
        return bool(abs(float(np.linalg.det(self._a))) <= self._atol)

    def verifies_null_vector(self) -> bool:
        return bool(np.allclose(self._a @ self.null_vector, np.zeros(3), atol=self._atol))

    def verifies_column_relation(self) -> bool:
        return bool(
            np.allclose(
                self._a @ self.column_relation_coefficients,
                np.zeros(3),
                atol=self._atol,
            )
        )

    def left_side_can_be_identity(self) -> bool:
        return self.rank == 3

    @staticmethod
    def failure_tex() -> str:
        return r"[A\mid I]\not\longrightarrow[I\mid A^{-1}]"

    @staticmethod
    def null_space_tex() -> str:
        return (
            r"N(A)=\operatorname{span}\left\{"
            r"\begin{bmatrix}1\\-1\\1\end{bmatrix}"
            r"\right\}"
        )

    @staticmethod
    def equivalence_tex() -> tuple[str, ...]:
        return (
            r"A^{-1}\text{ exists}\iff\operatorname{rank}(A)=3",
            r"\iff N(A)=\{\mathbf0\}",
            r"\iff A\mathbf{x}=\mathbf{b}\text{ has one solution for every }\mathbf{b}",
        )

    def snapshot(self) -> NoninvertibleMatrixSnapshot:
        return NoninvertibleMatrixSnapshot(
            coefficient_matrix=self.coefficient_matrix,
            identity_matrix=self.identity_matrix,
            augmented_start=self.augmented_start,
            steps=self.steps,
            reduced_block=self.reduced_block,
            left_rref=self.left_rref,
            transformed_identity=self.transformed_identity,
            rank=self.rank,
            pivot_columns=self.pivot_columns,
            free_columns=self.free_columns,
            null_vector=self.null_vector.copy(),
            column_relation_coefficients=self.column_relation_coefficients.copy(),
            unit_system_statuses=self.unit_system_statuses,
            unit_system_contradictions=self.unit_system_contradictions,
            failure_tex=self.failure_tex(),
            null_space_tex=self.null_space_tex(),
            equivalence_tex=self.equivalence_tex(),
        )

    def _build_steps(self) -> tuple[NoninvertibilityStep, ...]:
        block = self.augmented_start
        operations = (
            (
                r"R_2\leftarrow R_2-2R_1",
                "The coefficient entries vanish, but the identity entries do not.",
                1,
                "replacement",
            ),
            (
                r"R_2\leftrightarrow R_3",
                "Move the remaining pivot row above the zero coefficient row.",
                1,
                "swap",
            ),
            (
                r"R_1\leftarrow R_1-2R_2",
                "Clear the entry above the second pivot.",
                0,
                "replacement",
            ),
        )
        steps: list[NoninvertibilityStep] = []
        for index, (operation_tex, explanation, target_row, kind) in enumerate(operations, start=1):
            before = block.copy()
            if kind == "swap":
                block[[1, 2], :] = block[[2, 1], :]
            elif index == 1:
                block[1, :] = block[1, :] - 2.0 * block[0, :]
            else:
                block[0, :] = block[0, :] - 2.0 * block[1, :]
            block[np.abs(block) <= self._atol] = 0.0
            steps.append(
                NoninvertibilityStep(
                    index=index,
                    operation_tex=operation_tex,
                    explanation=explanation,
                    target_row=target_row,
                    before_block=before,
                    after_block=block.copy(),
                )
            )
        return tuple(steps)

    @staticmethod
    def _copy_step(step: NoninvertibilityStep) -> NoninvertibilityStep:
        return NoninvertibilityStep(
            index=step.index,
            operation_tex=step.operation_tex,
            explanation=step.explanation,
            target_row=step.target_row,
            before_block=step.before_block.copy(),
            after_block=step.after_block.copy(),
        )
