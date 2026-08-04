"""Renderer-independent elementary row operations for CP107.

The module works with augmented matrices and keeps the mathematical rules
separate from the Manim presentation.  Every operation returns a fresh array;
the supplied matrix is never mutated.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class ElementaryRowOperationsSnapshot:
    """Immutable data used by the CP107 presentation."""

    base_augmented: FloatArray
    swapped_augmented: FloatArray
    scaled_augmented: FloatArray
    replaced_augmented: FloatArray
    solution: FloatArray


class ElementaryRowOperations:
    """Apply the three elementary row operations to augmented matrices."""

    DEFAULT_AUGMENTED = np.array(
        [
            [1.0, 1.0, 2.0],
            [2.0, -1.0, 1.0],
        ],
        dtype=float,
    )

    def __init__(
        self,
        augmented_matrix: Iterable[Iterable[float]] | FloatArray | None = None,
    ) -> None:
        candidate = np.array(
            self.DEFAULT_AUGMENTED if augmented_matrix is None else augmented_matrix,
            dtype=float,
            copy=True,
        )
        self._validate_augmented(candidate)
        self._augmented = candidate

    @property
    def augmented_matrix(self) -> FloatArray:
        return self._augmented.copy()

    @property
    def coefficient_matrix(self) -> FloatArray:
        return self._augmented[:, :-1].copy()

    @property
    def right_hand_side(self) -> FloatArray:
        return self._augmented[:, -1].copy()

    def solution(self) -> FloatArray:
        matrix = self.coefficient_matrix
        rhs = self.right_hand_side
        if matrix.shape[0] != matrix.shape[1]:
            raise ValueError("the displayed solution requires a square coefficient matrix.")
        if np.linalg.matrix_rank(matrix) != matrix.shape[1]:
            raise ValueError("the displayed system must have a unique solution.")
        return np.linalg.solve(matrix, rhs)

    def snapshot(self) -> ElementaryRowOperationsSnapshot:
        base = self.augmented_matrix
        return ElementaryRowOperationsSnapshot(
            base_augmented=base,
            swapped_augmented=self.swap_rows(base, 0, 1),
            scaled_augmented=self.scale_row(base, 0, 2.0),
            replaced_augmented=self.replace_row(base, 1, 0, -2.0),
            solution=self.solution(),
        )

    @classmethod
    def swap_rows(
        cls,
        augmented: Iterable[Iterable[float]] | FloatArray,
        first: int,
        second: int,
    ) -> FloatArray:
        result = cls._coerce_augmented(augmented)
        cls._validate_row_index(result, first)
        cls._validate_row_index(result, second)
        result[[first, second]] = result[[second, first]]
        return result

    @classmethod
    def scale_row(
        cls,
        augmented: Iterable[Iterable[float]] | FloatArray,
        row: int,
        scalar: float,
    ) -> FloatArray:
        result = cls._coerce_augmented(augmented)
        cls._validate_row_index(result, row)
        if not np.isfinite(scalar):
            raise ValueError("row scale factor must be finite.")
        if np.isclose(scalar, 0.0):
            raise ValueError("an elementary row scaling factor must be nonzero.")
        result[row] *= float(scalar)
        return result

    @classmethod
    def replace_row(
        cls,
        augmented: Iterable[Iterable[float]] | FloatArray,
        target: int,
        source: int,
        scalar: float,
    ) -> FloatArray:
        result = cls._coerce_augmented(augmented)
        cls._validate_row_index(result, target)
        cls._validate_row_index(result, source)
        if target == source:
            raise ValueError("row replacement requires distinct target and source rows.")
        if not np.isfinite(scalar):
            raise ValueError("row replacement scalar must be finite.")
        result[target] = result[target] + float(scalar) * result[source]
        return result

    @classmethod
    def satisfies(
        cls,
        augmented: Iterable[Iterable[float]] | FloatArray,
        candidate: Iterable[float] | FloatArray,
        *,
        atol: float = 1e-9,
    ) -> bool:
        system = cls._coerce_augmented(augmented)
        vector = np.array(candidate, dtype=float, copy=True)
        if vector.shape != (system.shape[1] - 1,):
            raise ValueError("candidate length must equal the number of variables.")
        if not np.isfinite(vector).all():
            raise ValueError("candidate entries must be finite.")
        return bool(
            np.allclose(system[:, :-1] @ vector, system[:, -1], atol=atol)
        )

    @classmethod
    def _coerce_augmented(
        cls,
        augmented: Iterable[Iterable[float]] | FloatArray,
    ) -> FloatArray:
        result = np.array(augmented, dtype=float, copy=True)
        cls._validate_augmented(result)
        return result

    @staticmethod
    def _validate_augmented(candidate: FloatArray) -> None:
        if candidate.ndim != 2:
            raise ValueError("augmented matrix must be two-dimensional.")
        if candidate.shape[0] == 0 or candidate.shape[1] < 2:
            raise ValueError("augmented matrix must contain rows and at least two columns.")
        if not np.isfinite(candidate).all():
            raise ValueError("augmented entries must be finite.")

    @staticmethod
    def _validate_row_index(candidate: FloatArray, row: int) -> None:
        if not isinstance(row, (int, np.integer)):
            raise TypeError("row index must be an integer.")
        if not 0 <= int(row) < candidate.shape[0]:
            raise IndexError("row index is outside the augmented matrix.")
