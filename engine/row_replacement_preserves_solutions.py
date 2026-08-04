"""Renderer-independent mathematics for CP108.

The checkpoint explains why replacing one equation by itself plus a multiple
of another equation preserves the solution set.  The core reason is
reversibility: the original row can be recovered by the inverse replacement.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class RowReplacementPreservationSnapshot:
    """Immutable data used by the CP108 presentation."""

    original_augmented: FloatArray
    transformed_augmented: FloatArray
    recovered_augmented: FloatArray
    solution: FloatArray
    original_left_values: FloatArray
    original_right_values: FloatArray
    transformed_left_values: FloatArray
    transformed_right_values: FloatArray


class RowReplacementPreservesSolutions:
    """Model a reversible elementary row replacement."""

    DEFAULT_AUGMENTED = np.array(
        [
            [1.0, 1.0, 2.0],
            [2.0, -1.0, 1.0],
        ],
        dtype=float,
    )
    DEFAULT_TARGET = 1
    DEFAULT_SOURCE = 0
    DEFAULT_SCALAR = -2.0

    def __init__(
        self,
        augmented_matrix: Iterable[Iterable[float]] | FloatArray | None = None,
        *,
        target: int = DEFAULT_TARGET,
        source: int = DEFAULT_SOURCE,
        scalar: float = DEFAULT_SCALAR,
    ) -> None:
        candidate = np.array(
            self.DEFAULT_AUGMENTED if augmented_matrix is None else augmented_matrix,
            dtype=float,
            copy=True,
        )
        self._validate_augmented(candidate)
        self._validate_row_index(candidate, target)
        self._validate_row_index(candidate, source)
        if target == source:
            raise ValueError("row replacement requires distinct source and target rows.")
        if not np.isfinite(scalar):
            raise ValueError("row replacement scalar must be finite.")
        self._augmented = candidate
        self._target = int(target)
        self._source = int(source)
        self._scalar = float(scalar)

    @property
    def augmented_matrix(self) -> FloatArray:
        return self._augmented.copy()

    @property
    def target(self) -> int:
        return self._target

    @property
    def source(self) -> int:
        return self._source

    @property
    def scalar(self) -> float:
        return self._scalar

    def transformed_augmented(self) -> FloatArray:
        return self.replace_row(
            self._augmented,
            target=self._target,
            source=self._source,
            scalar=self._scalar,
        )

    def recovered_augmented(self) -> FloatArray:
        return self.replace_row(
            self.transformed_augmented(),
            target=self._target,
            source=self._source,
            scalar=-self._scalar,
        )

    def solution(self) -> FloatArray:
        coefficient_matrix = self._augmented[:, :-1]
        right_hand_side = self._augmented[:, -1]
        if coefficient_matrix.shape[0] != coefficient_matrix.shape[1]:
            raise ValueError("the displayed proof requires a square system.")
        if np.linalg.matrix_rank(coefficient_matrix) != coefficient_matrix.shape[1]:
            raise ValueError("the displayed proof requires a unique solution.")
        return np.linalg.solve(coefficient_matrix, right_hand_side)

    def evaluate(
        self,
        augmented: Iterable[Iterable[float]] | FloatArray,
        candidate: Iterable[float] | FloatArray,
    ) -> tuple[FloatArray, FloatArray]:
        system = self._coerce_augmented(augmented)
        vector = np.array(candidate, dtype=float, copy=True)
        if vector.shape != (system.shape[1] - 1,):
            raise ValueError("candidate length must equal the number of variables.")
        if not np.isfinite(vector).all():
            raise ValueError("candidate entries must be finite.")
        return system[:, :-1] @ vector, system[:, -1].copy()

    def satisfies(
        self,
        augmented: Iterable[Iterable[float]] | FloatArray,
        candidate: Iterable[float] | FloatArray,
        *,
        atol: float = 1e-9,
    ) -> bool:
        left, right = self.evaluate(augmented, candidate)
        return bool(np.allclose(left, right, atol=atol))

    def snapshot(self) -> RowReplacementPreservationSnapshot:
        original = self.augmented_matrix
        transformed = self.transformed_augmented()
        recovered = self.recovered_augmented()
        solution = self.solution()
        original_left, original_right = self.evaluate(original, solution)
        transformed_left, transformed_right = self.evaluate(transformed, solution)
        return RowReplacementPreservationSnapshot(
            original_augmented=original,
            transformed_augmented=transformed,
            recovered_augmented=recovered,
            solution=solution,
            original_left_values=original_left,
            original_right_values=original_right,
            transformed_left_values=transformed_left,
            transformed_right_values=transformed_right,
        )

    @classmethod
    def replace_row(
        cls,
        augmented: Iterable[Iterable[float]] | FloatArray,
        *,
        target: int,
        source: int,
        scalar: float,
    ) -> FloatArray:
        result = cls._coerce_augmented(augmented)
        cls._validate_row_index(result, target)
        cls._validate_row_index(result, source)
        if target == source:
            raise ValueError("row replacement requires distinct source and target rows.")
        if not np.isfinite(scalar):
            raise ValueError("row replacement scalar must be finite.")
        result[target] = result[target] + float(scalar) * result[source]
        return result

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
            raise ValueError("augmented matrix must contain rows and variables.")
        if not np.isfinite(candidate).all():
            raise ValueError("augmented entries must be finite.")

    @staticmethod
    def _validate_row_index(candidate: FloatArray, row: int) -> None:
        if not isinstance(row, (int, np.integer)):
            raise TypeError("row index must be an integer.")
        if not 0 <= int(row) < candidate.shape[0]:
            raise IndexError("row index is outside the augmented matrix.")
