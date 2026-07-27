"""Renderer-independent mathematics for a visual null-space lesson."""
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
class NullSpaceSnapshot:
    matrix: FloatArray
    input_vector: FloatArray
    output_vector: FloatArray
    null_vector: FloatArray
    rank: int
    nullity: int


class NullSpace:
    """Compute outputs and a basis direction for the null space of a matrix."""

    def __init__(self, matrix: ArrayLike) -> None:
        self._matrix = _matrix(matrix)
        self._rank = int(np.linalg.matrix_rank(self._matrix, tol=1e-9))
        self._nullity = 3 - self._rank
        if self._nullity <= 0:
            raise ValueError("matrix must have nontrivial null space")

        _, singular_values, vt = np.linalg.svd(self._matrix)
        null_vector = vt[-1]
        max_index = int(np.argmax(np.abs(null_vector)))
        if null_vector[max_index] < 0:
            null_vector = -null_vector
        self._null_vector = _readonly(null_vector / np.linalg.norm(null_vector))

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
    def null_vector(self) -> FloatArray:
        return self._null_vector

    def snapshot(self, input_vector: ArrayLike) -> NullSpaceSnapshot:
        vector = _vector(input_vector, "input_vector")
        output = self._matrix @ vector
        return NullSpaceSnapshot(
            matrix=self._matrix,
            input_vector=vector,
            output_vector=_readonly(output),
            null_vector=self._null_vector,
            rank=self._rank,
            nullity=self._nullity,
        )

    def scalar_multiples(self, scalars: ArrayLike) -> FloatArray:
        scalar_values = np.asarray(scalars, dtype=float)
        if scalar_values.ndim != 1 or not np.all(np.isfinite(scalar_values)):
            raise ValueError("scalars must be a finite 1D array")
        points = scalar_values[:, None] * self._null_vector[None, :]
        return _readonly(points)

    def sample_outputs(self, input_vectors: ArrayLike) -> FloatArray:
        vectors = np.asarray(input_vectors, dtype=float)
        if vectors.ndim != 2 or vectors.shape[1] != 3 or not np.all(np.isfinite(vectors)):
            raise ValueError("input_vectors must have shape (n, 3)")
        return _readonly(vectors @ self._matrix.T)

    def is_in_null_space(self, input_vector: ArrayLike, tolerance: float = 1e-9) -> bool:
        output = self.snapshot(input_vector).output_vector
        return bool(np.linalg.norm(output) <= tolerance)
