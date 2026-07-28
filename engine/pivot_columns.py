"""Renderer-independent mathematics for a pivot-columns lesson."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from numpy.typing import ArrayLike, NDArray

FloatArray = NDArray[np.float64]


def _readonly(values: ArrayLike) -> FloatArray:
    array = np.asarray(values, dtype=float).copy()
    array.setflags(write=False)
    return array


def _matrix(values: ArrayLike) -> FloatArray:
    matrix = np.asarray(values, dtype=float)
    if matrix.shape != (3, 3) or not np.all(np.isfinite(matrix)):
        raise ValueError("matrix must be a finite 3x3 matrix")
    return _readonly(matrix)


def _row_echelon(matrix: FloatArray, tolerance: float = 1e-9) -> FloatArray:
    working = np.array(matrix, dtype=float)
    rows, cols = working.shape
    pivot_row = 0
    for col in range(cols):
        if pivot_row >= rows:
            break
        pivot = None
        for row in range(pivot_row, rows):
            if abs(working[row, col]) > tolerance:
                pivot = row
                break
        if pivot is None:
            continue
        if pivot != pivot_row:
            working[[pivot_row, pivot]] = working[[pivot, pivot_row]]
        pivot_value = working[pivot_row, col]
        for row in range(pivot_row + 1, rows):
            if abs(working[row, col]) <= tolerance:
                continue
            factor = working[row, col] / pivot_value
            working[row] = working[row] - factor * working[pivot_row]
            working[np.abs(working) < tolerance] = 0.0
        pivot_row += 1
    return _readonly(working)


def _pivot_column_indices(echelon: FloatArray, tolerance: float = 1e-9) -> tuple[int, ...]:
    pivots: list[int] = []
    for row in echelon:
        nonzero = np.where(np.abs(row) > tolerance)[0]
        if len(nonzero) > 0:
            pivots.append(int(nonzero[0]))
    return tuple(pivots)


@dataclass(frozen=True)
class PivotColumnsSnapshot:
    initial_matrix: FloatArray
    echelon_matrix: FloatArray
    pivot_column_indices: tuple[int, ...]
    nonpivot_column_indices: tuple[int, ...]
    pivot_columns: FloatArray
    nonpivot_columns: FloatArray
    rank: int


class PivotColumns:
    """Track the original pivot columns that form a basis for column space."""

    def __init__(self, matrix: ArrayLike) -> None:
        self._initial = _matrix(matrix)
        self._echelon = _row_echelon(self._initial)
        self._rank = int(np.linalg.matrix_rank(self._initial, tol=1e-9))
        self._pivot_column_indices = _pivot_column_indices(self._echelon)
        self._nonpivot_column_indices = tuple(
            index for index in range(self._initial.shape[1])
            if index not in self._pivot_column_indices
        )
        if self._rank != 2 or len(self._pivot_column_indices) != 2 or len(self._nonpivot_column_indices) != 1:
            raise ValueError("this lesson expects a rank-2 3x3 matrix with one nonpivot column")
        self._pivot_columns = _readonly(self._initial[:, list(self._pivot_column_indices)].T)
        self._nonpivot_columns = _readonly(self._initial[:, list(self._nonpivot_column_indices)].T)

    @property
    def initial_matrix(self) -> FloatArray:
        return self._initial

    @property
    def echelon_matrix(self) -> FloatArray:
        return self._echelon

    def snapshot(self) -> PivotColumnsSnapshot:
        return PivotColumnsSnapshot(
            initial_matrix=self._initial,
            echelon_matrix=self._echelon,
            pivot_column_indices=self._pivot_column_indices,
            nonpivot_column_indices=self._nonpivot_column_indices,
            pivot_columns=self._pivot_columns,
            nonpivot_columns=self._nonpivot_columns,
            rank=self._rank,
        )

    def sample_column_space(self, coefficient_pairs: ArrayLike) -> FloatArray:
        coeffs = np.asarray(coefficient_pairs, dtype=float)
        if coeffs.ndim != 2 or coeffs.shape[1] != 2 or not np.all(np.isfinite(coeffs)):
            raise ValueError("coefficient_pairs must have shape (n, 2)")
        matrix = self._pivot_columns.T
        return _readonly(coeffs @ matrix.T)

    def express_nonpivot_column_in_pivot_columns(self) -> FloatArray:
        coefficients, *_ = np.linalg.lstsq(self._pivot_columns.T, self._nonpivot_columns[0], rcond=None)
        return _readonly(coefficients)

    def spans_match(self, tolerance: float = 1e-9) -> bool:
        coefficients = self.express_nonpivot_column_in_pivot_columns()
        reconstruction = coefficients[0] * self._pivot_columns[0] + coefficients[1] * self._pivot_columns[1]
        return bool(np.linalg.norm(reconstruction - self._nonpivot_columns[0]) <= tolerance)
