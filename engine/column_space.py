"""Renderer-independent mathematics for a visual column-space lesson."""
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


def _vector(values: ArrayLike, name: str) -> FloatArray:
    vector = np.asarray(values, dtype=float)
    if vector.shape != (3,) or not np.all(np.isfinite(vector)):
        raise ValueError(f"{name} must be a finite 3-vector")
    return _readonly(vector)


@dataclass(frozen=True)
class ColumnSpaceSnapshot:
    matrix: FloatArray
    coefficients: FloatArray
    output: FloatArray
    columns: FloatArray
    rank: int


class ColumnSpace:
    """Compute matrix outputs and sampled points in the column space."""

    def __init__(self, matrix: ArrayLike) -> None:
        self._matrix = _matrix(matrix)
        self._columns = _readonly(self._matrix.T)
        self._rank = int(np.linalg.matrix_rank(self._matrix, tol=1e-9))
        if self._rank == 0:
            raise ValueError("matrix must have nonzero rank")

    @property
    def matrix(self) -> FloatArray:
        return self._matrix

    @property
    def columns(self) -> FloatArray:
        return self._columns

    @property
    def rank(self) -> int:
        return self._rank

    def snapshot(self, coefficients: ArrayLike) -> ColumnSpaceSnapshot:
        vector = _vector(coefficients, "coefficients")
        output = self._matrix @ vector
        return ColumnSpaceSnapshot(
            matrix=self._matrix,
            coefficients=vector,
            output=_readonly(output),
            columns=self._columns,
            rank=self._rank,
        )

    def sample_outputs(self, coefficient_vectors: ArrayLike) -> FloatArray:
        coefficients = np.asarray(coefficient_vectors, dtype=float)
        if coefficients.ndim != 2 or coefficients.shape[1] != 3 or not np.all(np.isfinite(coefficients)):
            raise ValueError("coefficient_vectors must have shape (n, 3)")
        return _readonly(coefficients @ self._matrix.T)

    def independent_columns(self) -> tuple[int, ...]:
        chosen: list[int] = []
        current = np.empty((3, 0), dtype=float)
        current_rank = 0
        for index in range(3):
            candidate = np.column_stack((current, self._matrix[:, index]))
            candidate_rank = int(np.linalg.matrix_rank(candidate, tol=1e-9))
            if candidate_rank > current_rank:
                chosen.append(index)
                current = candidate
                current_rank = candidate_rank
            if current_rank == self._rank:
                break
        return tuple(chosen)
