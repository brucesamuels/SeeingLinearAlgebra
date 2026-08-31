"""Renderer-independent computations for the symmetric minimum principle."""
from __future__ import annotations

import numpy as np


class MinimumPrinciple:
    """Evaluate Rayleigh quotients and successive constrained minima."""

    DEFAULT_MATRIX = np.array(
        [[2.0, 1.0, 0.0], [1.0, 2.0, 0.0], [0.0, 0.0, 4.0]]
    )

    def __init__(self, matrix=None):
        value = self.DEFAULT_MATRIX if matrix is None else matrix
        self.matrix = self._symmetric_positive_definite_matrix(value)

    @staticmethod
    def _symmetric_positive_definite_matrix(value):
        matrix = np.asarray(value, dtype=float)
        if matrix.ndim != 2 or min(matrix.shape) == 0:
            raise ValueError("matrix must be nonempty and two-dimensional")
        rows, columns = matrix.shape
        if rows != columns:
            raise ValueError("matrix must be square")
        if not np.all(np.isfinite(matrix)):
            raise ValueError("matrix entries must be finite")
        if not np.allclose(matrix, matrix.T):
            raise ValueError("matrix must be symmetric")
        if np.min(np.linalg.eigvalsh(matrix)) <= 1e-12:
            raise ValueError("matrix must be positive definite")
        return matrix

    @staticmethod
    def _orient_columns(columns):
        oriented = np.array(columns, dtype=float, copy=True)
        for index in range(oriented.shape[1]):
            column = oriented[:, index]
            nonzero = np.flatnonzero(np.abs(column) > 1e-12)
            if nonzero.size and column[nonzero[0]] < 0:
                oriented[:, index] *= -1
        return oriented

    def _vector(self, value):
        vector = np.asarray(value, dtype=float)
        if vector.shape != (self.matrix.shape[0],):
            raise ValueError(f"vector must have shape ({self.matrix.shape[0]},)")
        if not np.all(np.isfinite(vector)):
            raise ValueError("vector entries must be finite")
        if np.linalg.norm(vector) <= 1e-12:
            raise ValueError("vector must be nonzero")
        return vector

    def ordered_eigenpairs(self):
        values, vectors = np.linalg.eigh(self.matrix)
        return values, self._orient_columns(vectors)

    def rayleigh_quotient(self, vector):
        x = self._vector(vector)
        return float((x @ self.matrix @ x) / (x @ x))

    def eigenbasis_coefficients(self, vector):
        x = self._vector(vector)
        _, vectors = self.ordered_eigenpairs()
        return vectors.T @ x

    def spectral_rayleigh_quotient(self, vector):
        x = self._vector(vector)
        values, _ = self.ordered_eigenpairs()
        coefficients = self.eigenbasis_coefficients(x)
        return float(
            np.dot(values, coefficients**2) / np.dot(coefficients, coefficients)
        )

    def eigenvalue_bounds(self):
        values, _ = self.ordered_eigenpairs()
        return float(values[0]), float(values[-1])

    def constrained_minimum(self, excluded_count=0):
        """Return the minimum after excluding the first eigen-directions."""
        dimension = self.matrix.shape[0]
        if not isinstance(excluded_count, int) or not 0 <= excluded_count < dimension:
            raise ValueError(
                f"excluded_count must be an integer from 0 to {dimension - 1}"
            )
        values, vectors = self.ordered_eigenpairs()
        return float(values[excluded_count]), vectors[:, excluded_count].copy()

    def scale_invariant_pair(self, vector, scale):
        x = self._vector(vector)
        if not np.isfinite(scale) or abs(scale) <= 1e-12:
            raise ValueError("scale must be finite and nonzero")
        return self.rayleigh_quotient(x), self.rayleigh_quotient(scale * x)
