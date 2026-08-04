"""Renderer-independent mathematics for CP112.

Checkpoint 112 continues Gaussian elimination beyond echelon form to produce
reduced row echelon form (RREF) using Gauss–Jordan elimination.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class RowOperationStep:
    """One Gauss–Jordan row operation."""

    label_tex: str
    description: str
    result_augmented: FloatArray


@dataclass(frozen=True)
class GaussJordanRREFSnapshot:
    """Immutable data used by the CP112 presentation."""

    echelon_augmented: FloatArray
    steps: tuple[RowOperationStep, ...]
    rref_augmented: FloatArray
    solution: FloatArray
    direct_readoff_tex: tuple[str, str, str]


class GaussJordanRREF:
    """Carry the CP109 echelon matrix to RREF."""

    DEFAULT_ECHELON_AUGMENTED = np.array(
        [
            [1.0, 1.0, 1.0, 3.0],
            [0.0, 1.0, -2.0, -1.0],
            [0.0, 0.0, -7.0, -7.0],
        ],
        dtype=float,
    )

    def __init__(self, echelon_augmented: Iterable[Iterable[float]] | FloatArray | None = None) -> None:
        matrix = np.array(
            self.DEFAULT_ECHELON_AUGMENTED if echelon_augmented is None else echelon_augmented,
            dtype=float,
            copy=True,
        )
        if matrix.shape != (3, 4):
            raise ValueError("echelon_augmented must have shape (3, 4).")
        if not np.isfinite(matrix).all():
            raise ValueError("echelon_augmented entries must be finite.")
        if np.linalg.matrix_rank(matrix[:, :-1]) != 3:
            raise ValueError("echelon_augmented must be full rank.")
        self._matrix = matrix

    @property
    def echelon_augmented(self) -> FloatArray:
        return self._matrix.copy()

    def steps(self) -> tuple[RowOperationStep, ...]:
        m0 = self.echelon_augmented
        m1 = m0.copy()
        m1[2] = (-1 / 7) * m1[2]

        m2 = m1.copy()
        m2[1] = m2[1] + 2 * m2[2]

        m3 = m2.copy()
        m3[0] = m3[0] - m3[2]

        m4 = m3.copy()
        m4[0] = m4[0] - m4[1]

        return (
            RowOperationStep(
                label_tex=r"R_3\leftarrow -\frac{1}{7}R_3",
                description="Scale the bottom pivot to 1.",
                result_augmented=m1,
            ),
            RowOperationStep(
                label_tex=r"R_2\leftarrow R_2+2R_3",
                description="Clear the entry above the bottom pivot.",
                result_augmented=m2,
            ),
            RowOperationStep(
                label_tex=r"R_1\leftarrow R_1-R_3",
                description="Clear the other entry above the bottom pivot.",
                result_augmented=m3,
            ),
            RowOperationStep(
                label_tex=r"R_1\leftarrow R_1-R_2",
                description="Clear the entry above the middle pivot.",
                result_augmented=m4,
            ),
        )

    def rref_augmented(self) -> FloatArray:
        return self.steps()[-1].result_augmented.copy()

    def solution(self) -> FloatArray:
        return self.rref_augmented()[:, -1].copy()

    def direct_readoff_tex(self) -> tuple[str, str, str]:
        x, y, z = self.solution()
        return (rf"x={x:g}", rf"y={y:g}", rf"z={z:g}")

    def snapshot(self) -> GaussJordanRREFSnapshot:
        steps = self.steps()
        return GaussJordanRREFSnapshot(
            echelon_augmented=self.echelon_augmented,
            steps=steps,
            rref_augmented=steps[-1].result_augmented.copy(),
            solution=self.solution(),
            direct_readoff_tex=self.direct_readoff_tex(),
        )
