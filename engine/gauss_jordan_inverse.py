"""Renderer-independent mathematics for CP122.

Checkpoint 122 interprets Gauss-Jordan inversion as the multiple-right-hand-side
problem AX = I.  Row operations applied to [A | I] produce [I | A^{-1}].
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class GaussJordanStep:
    """One row operation applied across the complete augmented block [A | I]."""

    index: int
    operation_tex: str
    explanation: str
    target_row: int
    before_block: FloatArray
    after_block: FloatArray


@dataclass(frozen=True)
class GaussJordanInverseSnapshot:
    """Immutable mathematical data consumed by the CP122 presentation."""

    coefficient_matrix: FloatArray
    identity_matrix: FloatArray
    augmented_start: FloatArray
    steps: tuple[GaussJordanStep, ...]
    reduced_block: FloatArray
    inverse_matrix: FloatArray
    inverse_columns: tuple[FloatArray, ...]
    elementary_product: FloatArray
    block_system_tex: str
    reduction_tex: str
    elementary_product_tex: str


class GaussJordanInverse:
    """Compute A^{-1} by applying Gauss-Jordan operations to [A | I]."""

    DEFAULT_A = np.array(
        [
            [1.0, 2.0, 1.0],
            [0.0, 1.0, 3.0],
            [0.0, 0.0, 2.0],
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
        if atol <= 0:
            raise ValueError("atol must be positive.")
        if abs(float(np.linalg.det(matrix))) <= atol:
            raise ValueError("coefficient_matrix must be invertible.")
        if not np.allclose(matrix, self.DEFAULT_A, atol=atol):
            raise ValueError("CP122 uses the fixed classroom matrix shown in the lesson.")

        self._a = matrix
        self._identity = np.eye(3, dtype=float)
        self._atol = float(atol)
        self._steps = self._build_steps()
        self._reduced = self._steps[-1].after_block.copy()
        self._inverse = self._reduced[:, 3:].copy()

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
    def steps(self) -> tuple[GaussJordanStep, ...]:
        return tuple(self._copy_step(step) for step in self._steps)

    @property
    def reduced_block(self) -> FloatArray:
        return self._reduced.copy()

    @property
    def inverse_matrix(self) -> FloatArray:
        return self._inverse.copy()

    @property
    def inverse_columns(self) -> tuple[FloatArray, ...]:
        return tuple(self._inverse[:, column].copy() for column in range(3))

    @property
    def elementary_product(self) -> FloatArray:
        """The product of row-operation matrices equals the transformed identity."""
        return self._inverse.copy()

    def verifies_reduction(self) -> bool:
        expected = np.hstack([np.eye(3), self._inverse])
        return bool(np.allclose(self._reduced, expected, atol=self._atol))

    def verifies_right_inverse(self) -> bool:
        return bool(np.allclose(self._a @ self._inverse, np.eye(3), atol=self._atol))

    def verifies_left_inverse(self) -> bool:
        return bool(np.allclose(self._inverse @ self._a, np.eye(3), atol=self._atol))

    def verifies_column_systems(self) -> bool:
        return all(
            np.allclose(self._a @ column, self._identity[:, index], atol=self._atol)
            for index, column in enumerate(self.inverse_columns)
        )

    @staticmethod
    def block_system_tex() -> str:
        return r"AX=I"

    @staticmethod
    def reduction_tex() -> str:
        return r"[A\mid I]\longrightarrow[I\mid A^{-1}]"

    @staticmethod
    def elementary_product_tex() -> str:
        return r"A^{-1}=E_4E_3E_2E_1"

    def snapshot(self) -> GaussJordanInverseSnapshot:
        return GaussJordanInverseSnapshot(
            coefficient_matrix=self.coefficient_matrix,
            identity_matrix=self.identity_matrix,
            augmented_start=self.augmented_start,
            steps=self.steps,
            reduced_block=self.reduced_block,
            inverse_matrix=self.inverse_matrix,
            inverse_columns=self.inverse_columns,
            elementary_product=self.elementary_product,
            block_system_tex=self.block_system_tex(),
            reduction_tex=self.reduction_tex(),
            elementary_product_tex=self.elementary_product_tex(),
        )

    def _build_steps(self) -> tuple[GaussJordanStep, ...]:
        block = self.augmented_start
        operations = (
            (r"R_3\leftarrow\tfrac12R_3", "Scale the third row to create the final pivot.", 2, 2, 0.5),
            (r"R_2\leftarrow R_2-3R_3", "Clear the entry above the third pivot.", 1, 2, -3.0),
            (r"R_1\leftarrow R_1-R_3", "Clear the first-row entry in column 3.", 0, 2, -1.0),
            (r"R_1\leftarrow R_1-2R_2", "Clear the first-row entry in column 2.", 0, 1, -2.0),
        )
        steps: list[GaussJordanStep] = []
        for index, (operation_tex, explanation, target_row, source_row, multiplier) in enumerate(operations, start=1):
            before = block.copy()
            if target_row == source_row:
                block[target_row, :] = multiplier * block[target_row, :]
            else:
                block[target_row, :] = block[target_row, :] + multiplier * block[source_row, :]
            block[np.abs(block) <= self._atol] = 0.0
            steps.append(
                GaussJordanStep(
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
    def _copy_step(step: GaussJordanStep) -> GaussJordanStep:
        return GaussJordanStep(
            index=step.index,
            operation_tex=step.operation_tex,
            explanation=step.explanation,
            target_row=step.target_row,
            before_block=step.before_block.copy(),
            after_block=step.after_block.copy(),
        )
