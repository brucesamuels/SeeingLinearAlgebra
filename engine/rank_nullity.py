"""Renderer-independent mathematics for a revised rank-nullity lesson."""
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


@dataclass(frozen=True)
class RankNullityDecomposition:
    input_vector: FloatArray
    row_component: FloatArray
    null_component: FloatArray
    output_vector: FloatArray


class RankNullity:
    """Split an input vector into row-space and null-space components."""

    def __init__(self, matrix: ArrayLike) -> None:
        self._matrix = _matrix(matrix)
        self._rank = int(np.linalg.matrix_rank(self._matrix, tol=1e-9))
        self._nullity = self._matrix.shape[1] - self._rank
        if self._rank != 2 or self._nullity != 1:
            raise ValueError("this lesson expects a 3x3 matrix with rank 2 and nullity 1")

        _, _, vt = np.linalg.svd(self._matrix)
        null_direction = vt[-1]
        max_index = int(np.argmax(np.abs(null_direction)))
        if null_direction[max_index] < 0:
            null_direction = -null_direction
        self._null_direction = _readonly(null_direction / np.linalg.norm(null_direction))

        row_indices = _independent_row_indices(self._matrix)
        if len(row_indices) != 2:
            raise ValueError("this lesson expects a 2-dimensional row space")
        self._row_basis = tuple(_readonly(self._matrix[index]) for index in row_indices)

    @property
    def matrix(self) -> FloatArray:
        return self._matrix

    @property
    def rank(self) -> int:
        return self._rank

    @property
    def nullity(self) -> int:
        return self._nullity

    @property
    def null_direction(self) -> FloatArray:
        return self._null_direction

    @property
    def row_basis(self) -> tuple[FloatArray, FloatArray]:
        return self._row_basis

    def decompose(self, input_vector: ArrayLike) -> RankNullityDecomposition:
        vector = np.asarray(input_vector, dtype=float)
        if vector.shape != (3,) or not np.all(np.isfinite(vector)):
            raise ValueError("input_vector must be a finite 3-vector")
        coefficient = float(np.dot(vector, self._null_direction))
        null_component = coefficient * self._null_direction
        row_component = vector - null_component
        output_vector = self._matrix @ vector
        return RankNullityDecomposition(
            input_vector=_readonly(vector),
            row_component=_readonly(row_component),
            null_component=_readonly(null_component),
            output_vector=_readonly(output_vector),
        )

    def apply(self, input_vector: ArrayLike) -> FloatArray:
        vector = np.asarray(input_vector, dtype=float)
        if vector.shape != (3,) or not np.all(np.isfinite(vector)):
            raise ValueError("input_vector must be a finite 3-vector")
        return _readonly(self._matrix @ vector)

    def is_in_null_space(self, input_vector: ArrayLike, tolerance: float = 1e-9) -> bool:
        return bool(np.linalg.norm(self.apply(input_vector)) <= tolerance)

    def sample_row_space(self, coefficient_pairs: ArrayLike) -> FloatArray:
        coefficients = np.asarray(coefficient_pairs, dtype=float)
        if coefficients.ndim != 2 or coefficients.shape[1] != 2 or not np.all(np.isfinite(coefficients)):
            raise ValueError("coefficient_pairs must have shape (n, 2)")
        matrix = np.column_stack(self._row_basis)
        return _readonly(coefficients @ matrix.T)
