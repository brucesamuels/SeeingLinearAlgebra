"""Renderer-independent model for Gram-matrix positive semidefiniteness."""
from __future__ import annotations

import math

import numpy as np


class GramMatrixDefiniteness:
    """Connect A-transpose A, squared norms, null spaces, and column rank."""

    DEFAULT_MATRIX = np.array([[1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])

    def __init__(self, matrix=None):
        value = self.DEFAULT_MATRIX if matrix is None else matrix
        self.matrix = self._matrix(value)

    @staticmethod
    def _matrix(value):
        matrix = np.asarray(value, dtype=float)
        if matrix.ndim != 2 or min(matrix.shape) == 0:
            raise ValueError("matrix must be nonempty and two-dimensional")
        if not np.all(np.isfinite(matrix)):
            raise ValueError("matrix entries must be finite")
        return matrix

    def _vector(self, value):
        vector = np.asarray(value, dtype=float)
        if vector.shape != (self.matrix.shape[1],) or not np.all(np.isfinite(vector)):
            raise ValueError(f"vector must be finite with length {self.matrix.shape[1]}")
        return vector

    def gram_matrix(self):
        return self.matrix.T @ self.matrix

    def image(self, vector):
        return self.matrix @ self._vector(vector)

    def gram_energy(self, vector):
        x = self._vector(vector)
        return float(x @ self.gram_matrix() @ x)

    def squared_norm_energy(self, vector):
        image = self.image(vector)
        return float(image @ image)

    def rank(self, tolerance=None):
        if tolerance is not None and (not math.isfinite(tolerance) or tolerance < 0):
            raise ValueError("tolerance must be finite and nonnegative")
        return int(np.linalg.matrix_rank(self.matrix, tol=tolerance))

    def has_independent_columns(self, tolerance=None):
        return self.rank(tolerance) == self.matrix.shape[1]

    def gram_is_positive_semidefinite(self, tolerance=1e-10):
        if not math.isfinite(tolerance) or tolerance < 0:
            raise ValueError("tolerance must be finite and nonnegative")
        return bool(np.all(np.linalg.eigvalsh(self.gram_matrix()) >= -tolerance))

    def gram_is_positive_definite(self, tolerance=None):
        return self.has_independent_columns(tolerance)
