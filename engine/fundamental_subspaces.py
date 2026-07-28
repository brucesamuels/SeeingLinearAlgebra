"""Renderer-independent mathematics for the four fundamental subspaces lesson."""
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


def _normalized_svd_null_vector(matrix: FloatArray) -> FloatArray:
    _, _, vt = np.linalg.svd(matrix)
    vector = vt[-1]
    max_index = int(np.argmax(np.abs(vector)))
    if vector[max_index] < 0:
        vector = -vector
    return _readonly(vector / np.linalg.norm(vector))


@dataclass(frozen=True)
class FundamentalSubspacesSnapshot:
    matrix: FloatArray
    rank: int
    nullity: int
    left_nullity: int
    row_basis: tuple[FloatArray, ...]
    column_basis: tuple[FloatArray, ...]
    null_basis: tuple[FloatArray, ...]
    left_null_basis: tuple[FloatArray, ...]
    pivot_column_indices: tuple[int, ...]


class FundamentalSubspaces:
    """Describe the four fundamental subspaces of the running 3x3 example."""

    def __init__(self, matrix: ArrayLike) -> None:
        self._matrix = _matrix(matrix)
        self._rank = int(np.linalg.matrix_rank(self._matrix, tol=1e-9))
        self._nullity = self._matrix.shape[1] - self._rank
        self._left_nullity = self._matrix.shape[0] - self._rank
        if self._rank != 2 or self._nullity != 1 or self._left_nullity != 1:
            raise ValueError("this lesson expects a 3x3 matrix with rank 2, nullity 1, and left nullity 1")

        row_indices = _independent_row_indices(self._matrix)
        if len(row_indices) != 2:
            raise ValueError("this lesson expects a 2-dimensional row space")
        self._row_basis = tuple(_readonly(self._matrix[index]) for index in row_indices)

        echelon = _row_echelon(self._matrix)
        self._pivot_column_indices = _pivot_column_indices(echelon)
        if len(self._pivot_column_indices) != 2:
            raise ValueError("this lesson expects exactly two pivot columns")
        self._column_basis = tuple(
            _readonly(self._matrix[:, index])
            for index in self._pivot_column_indices
        )

        self._null_basis = (_normalized_svd_null_vector(self._matrix),)
        self._left_null_basis = (_normalized_svd_null_vector(self._matrix.T),)

    @property
    def rank(self) -> int:
        return self._rank

    @property
    def nullity(self) -> int:
        return self._nullity

    @property
    def left_nullity(self) -> int:
        return self._left_nullity

    def snapshot(self) -> FundamentalSubspacesSnapshot:
        return FundamentalSubspacesSnapshot(
            matrix=self._matrix,
            rank=self._rank,
            nullity=self._nullity,
            left_nullity=self._left_nullity,
            row_basis=self._row_basis,
            column_basis=self._column_basis,
            null_basis=self._null_basis,
            left_null_basis=self._left_null_basis,
            pivot_column_indices=self._pivot_column_indices,
        )

    def row_null_are_orthogonal(self, tolerance: float = 1e-9) -> bool:
        null_vector = self._null_basis[0]
        return all(abs(float(np.dot(row, null_vector))) <= tolerance for row in self._row_basis)

    def col_left_null_are_orthogonal(self, tolerance: float = 1e-9) -> bool:
        left_null_vector = self._left_null_basis[0]
        return all(abs(float(np.dot(column, left_null_vector))) <= tolerance for column in self._column_basis)

    def apply(self, vector: ArrayLike) -> FloatArray:
        candidate = np.asarray(vector, dtype=float)
        if candidate.shape != (3,) or not np.all(np.isfinite(candidate)):
            raise ValueError("vector must be a finite 3-vector")
        return _readonly(self._matrix @ candidate)
