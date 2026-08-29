"""Renderer-independent upper-triangular Cholesky factorization model."""
from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np


@dataclass(frozen=True)
class CholeskyEntry:
    """One upper-triangular entry created by the Cholesky algorithm."""

    row: int
    column: int
    value: float
    source_value: float
    diagonal: bool


class PositiveDefiniteCholesky:
    """Compute A=R-transpose R and connect it to quadratic energy."""

    DEFAULT_MATRIX = np.array(
        [[4.0, 2.0, 0.0], [2.0, 3.0, 1.0], [0.0, 1.0, 2.0]]
    )

    def __init__(self, matrix=None, tolerance=1e-12):
        value = self.DEFAULT_MATRIX if matrix is None else matrix
        self.matrix = self._matrix(value)
        if not math.isfinite(tolerance) or tolerance < 0:
            raise ValueError("tolerance must be finite and nonnegative")
        self.tolerance = float(tolerance)
        self._upper, self._steps = self._factor()

    @staticmethod
    def _matrix(value):
        matrix = np.asarray(value, dtype=float)
        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("matrix must be square")
        if matrix.shape[0] == 0 or not np.all(np.isfinite(matrix)):
            raise ValueError("matrix must be finite and nonempty")
        if not np.allclose(matrix, matrix.T):
            raise ValueError("matrix must be symmetric")
        return matrix

    def _factor(self):
        size = self.matrix.shape[0]
        upper = np.zeros_like(self.matrix)
        steps = []
        for row in range(size):
            diagonal_source = self.matrix[row, row] - float(
                upper[:row, row] @ upper[:row, row]
            )
            if diagonal_source <= self.tolerance:
                raise ValueError("matrix does not have a positive Cholesky pivot")
            upper[row, row] = math.sqrt(diagonal_source)
            steps.append(
                CholeskyEntry(row, row, upper[row, row], diagonal_source, True)
            )
            for column in range(row + 1, size):
                numerator = self.matrix[row, column] - float(
                    upper[:row, row] @ upper[:row, column]
                )
                upper[row, column] = numerator / upper[row, row]
                steps.append(
                    CholeskyEntry(row, column, upper[row, column], numerator, False)
                )
        return upper, tuple(steps)

    def _vector(self, value):
        vector = np.asarray(value, dtype=float)
        if vector.shape != (self.matrix.shape[0],) or not np.all(np.isfinite(vector)):
            raise ValueError(f"vector must be finite with length {self.matrix.shape[0]}")
        return vector

    def upper_factor(self):
        return self._upper.copy()

    def construction_steps(self):
        return tuple(self._steps)

    def reconstruct(self):
        return self._upper.T @ self._upper

    def transformed_vector(self, vector):
        return self._upper @ self._vector(vector)

    def energy(self, vector):
        x = self._vector(vector)
        return float(x @ self.matrix @ x)

    def squared_norm_energy(self, vector):
        transformed = self.transformed_vector(vector)
        return float(transformed @ transformed)

    def has_positive_diagonal(self, tolerance=1e-10):
        if not math.isfinite(tolerance) or tolerance < 0:
            raise ValueError("tolerance must be finite and nonnegative")
        return bool(np.all(np.diag(self._upper) > tolerance))
