"""Renderer-independent symmetric LDL-transpose factorization model."""
from __future__ import annotations

import math

import numpy as np


class PositiveDefiniteLDLT:
    """Factor a symmetric matrix without row exchanges and track its energy."""

    DEFAULT_MATRIX = np.array(
        [[4.0, 2.0, 0.0], [2.0, 3.0, 1.0], [0.0, 1.0, 2.0]]
    )

    def __init__(self, matrix=None, tolerance=1e-12):
        value = self.DEFAULT_MATRIX if matrix is None else matrix
        self.matrix = self._matrix(value)
        if not math.isfinite(tolerance) or tolerance < 0:
            raise ValueError("tolerance must be finite and nonnegative")
        self.tolerance = float(tolerance)
        self._lower, self._diagonal = self._factor()

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
        lower = np.eye(size)
        diagonal = np.zeros(size)
        for column in range(size):
            previous = slice(0, column)
            diagonal[column] = self.matrix[column, column] - np.sum(
                lower[column, previous] ** 2 * diagonal[previous]
            )
            if column == size - 1:
                continue
            if abs(diagonal[column]) <= self.tolerance:
                raise ValueError("zero pivot prevents LDL-transpose factorization without exchanges")
            for row in range(column + 1, size):
                correction = np.sum(
                    lower[row, previous]
                    * lower[column, previous]
                    * diagonal[previous]
                )
                lower[row, column] = (
                    self.matrix[row, column] - correction
                ) / diagonal[column]
        return lower, diagonal

    def _vector(self, value):
        vector = np.asarray(value, dtype=float)
        if vector.shape != (self.matrix.shape[0],) or not np.all(np.isfinite(vector)):
            raise ValueError(f"vector must be finite with length {self.matrix.shape[0]}")
        return vector

    def lower_factor(self):
        return self._lower.copy()

    def diagonal_entries(self):
        return self._diagonal.copy()

    def diagonal_factor(self):
        return np.diag(self._diagonal)

    def reconstruct(self):
        return self._lower @ self.diagonal_factor() @ self._lower.T

    def transformed_coordinates(self, vector):
        return self._lower.T @ self._vector(vector)

    def energy(self, vector):
        x = self._vector(vector)
        return float(x @ self.matrix @ x)

    def diagonal_energy_terms(self, vector):
        y = self.transformed_coordinates(vector)
        return self._diagonal * y**2

    def diagonal_energy(self, vector):
        return float(np.sum(self.diagonal_energy_terms(vector)))

    def has_positive_diagonal(self, tolerance=1e-10):
        if not math.isfinite(tolerance) or tolerance < 0:
            raise ValueError("tolerance must be finite and nonnegative")
        return bool(np.all(self._diagonal > tolerance))
