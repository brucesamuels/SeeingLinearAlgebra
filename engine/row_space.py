"""Renderer-independent mathematics for a row-space lesson."""
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


def _row_echelon_steps(matrix: FloatArray, tolerance: float = 1e-9) -> tuple[FloatArray, ...]:
    working = np.array(matrix, dtype=float)
    steps: list[FloatArray] = [_readonly(working)]
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
            steps.append(_readonly(working))
        pivot_value = working[pivot_row, col]
        for row in range(pivot_row + 1, rows):
            if abs(working[row, col]) <= tolerance:
                continue
            factor = working[row, col] / pivot_value
            working[row] = working[row] - factor * working[pivot_row]
            working[np.abs(working) < tolerance] = 0.0
            steps.append(_readonly(working))
        pivot_row += 1
    return tuple(steps)


def _independent_row_indices(matrix: FloatArray, tolerance: float = 1e-9) -> tuple[int, ...]:
    chosen: list[int] = []
    current = np.empty((0, matrix.shape[1]))
    rank = 0
    for index, row in enumerate(matrix):
        trial = np.vstack([current, row])
        trial_rank = int(np.linalg.matrix_rank(trial, tol=tolerance))
        if trial_rank > rank:
            chosen.append(index)
            current = trial
            rank = trial_rank
    return tuple(chosen)


@dataclass(frozen=True)
class RowSpaceSnapshot:
    initial_matrix: FloatArray
    echelon_matrix: FloatArray
    steps: tuple[FloatArray, ...]
    pivot_rows: FloatArray
    pivot_row_indices: tuple[int, ...]
    independent_row_indices: tuple[int, ...]
    rank: int


class RowSpace:
    """Model row reduction and the preserved row space of a 3x3 matrix."""

    def __init__(self, matrix: ArrayLike) -> None:
        self._initial = _matrix(matrix)
        steps = _row_echelon_steps(self._initial)
        self._steps = steps
        self._echelon = steps[-1]
        self._rank = int(np.linalg.matrix_rank(self._initial, tol=1e-9))
        self._pivot_row_indices = tuple(
            index for index, row in enumerate(self._echelon)
            if np.linalg.norm(row) > 1e-9
        )
        self._independent_row_indices = _independent_row_indices(self._initial)
        self._pivot_rows = _readonly(self._echelon[list(self._pivot_row_indices)])
        if self._rank != 2:
            raise ValueError("this lesson expects a rank-2 matrix")

    @property
    def initial_matrix(self) -> FloatArray:
        return self._initial

    @property
    def echelon_matrix(self) -> FloatArray:
        return self._echelon

    @property
    def steps(self) -> tuple[FloatArray, ...]:
        return self._steps

    @property
    def rank(self) -> int:
        return self._rank

    def snapshot(self) -> RowSpaceSnapshot:
        return RowSpaceSnapshot(
            initial_matrix=self._initial,
            echelon_matrix=self._echelon,
            steps=self._steps,
            pivot_rows=self._pivot_rows,
            pivot_row_indices=self._pivot_row_indices,
            independent_row_indices=self._independent_row_indices,
            rank=self._rank,
        )

    def sample_initial_row_space(self, coefficient_pairs: ArrayLike) -> FloatArray:
        coeffs = np.asarray(coefficient_pairs, dtype=float)
        if coeffs.ndim != 2 or coeffs.shape[1] != 2 or not np.all(np.isfinite(coeffs)):
            raise ValueError("coefficient_pairs must have shape (n, 2)")
        basis = self._initial[list(self._independent_row_indices)]
        return _readonly(coeffs @ basis)

    def sample_pivot_row_space(self, coefficient_pairs: ArrayLike) -> FloatArray:
        coeffs = np.asarray(coefficient_pairs, dtype=float)
        if coeffs.ndim != 2 or coeffs.shape[1] != 2 or not np.all(np.isfinite(coeffs)):
            raise ValueError("coefficient_pairs must have shape (n, 2)")
        return _readonly(coeffs @ self._pivot_rows)

    def row_spaces_match(self, tolerance: float = 1e-9) -> bool:
        initial_basis = self._initial[list(self._independent_row_indices)]
        pivot_basis = self._pivot_rows
        return (
            np.linalg.matrix_rank(np.vstack([initial_basis, pivot_basis]), tol=tolerance)
            == self._rank
        )
