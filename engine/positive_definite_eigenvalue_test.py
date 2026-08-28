"""Renderer-independent numerical model for the positive-definite eigenvalue test."""
from __future__ import annotations

import math

import numpy as np


class PositiveDefiniteEigenvalueTest:
    """Relate quadratic energy to the eigenpairs of a symmetric matrix."""

    def __init__(self, matrix=None):
        value = [[2.0, 1.0], [1.0, 2.0]] if matrix is None else matrix
        self.matrix = self._matrix(value)
        values, vectors = np.linalg.eigh(self.matrix)
        self._eigenvalues = values
        self._eigenvectors = self._orient_columns(vectors)

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

    def _vector(self, value):
        vector = np.asarray(value, dtype=float)
        if vector.shape != (self.matrix.shape[0],) or not np.all(np.isfinite(vector)):
            raise ValueError(f"vector must be finite with length {self.matrix.shape[0]}")
        return vector

    @staticmethod
    def _orient_columns(vectors):
        result = vectors.copy()
        for column in range(result.shape[1]):
            nonzero = np.flatnonzero(np.abs(result[:, column]) > 1e-12)
            if nonzero.size and result[nonzero[0], column] < 0:
                result[:, column] *= -1
        return result

    @staticmethod
    def direction(theta):
        if not math.isfinite(theta):
            raise ValueError("theta must be finite")
        return np.array([math.cos(theta), math.sin(theta)])

    def energy(self, vector):
        x = self._vector(vector)
        return float(x @ self.matrix @ x)

    def directional_energy(self, theta):
        if self.matrix.shape != (2, 2):
            raise ValueError("directional_energy is defined only for 2-by-2 matrices")
        return self.energy(self.direction(theta))

    def eigenvalues(self):
        return self._eigenvalues.copy()

    def eigenvectors(self):
        """Return orthonormal eigenvectors as columns, in ascending value order."""
        return self._eigenvectors.copy()

    def eigen_coordinates(self, vector):
        return self._eigenvectors.T @ self._vector(vector)

    def spectral_energy_terms(self, vector):
        coordinates = self.eigen_coordinates(vector)
        return self._eigenvalues * coordinates**2

    def spectral_energy(self, vector):
        return float(np.sum(self.spectral_energy_terms(vector)))

    def unit_energy_bounds(self):
        return float(self._eigenvalues[0]), float(self._eigenvalues[-1])

    def is_positive_definite(self, tolerance=1e-10):
        if not math.isfinite(tolerance) or tolerance < 0:
            raise ValueError("tolerance must be finite and nonnegative")
        return bool(np.all(self._eigenvalues > tolerance))
