"""Numerical model for coordinates as linear-combination recipes."""
from __future__ import annotations

import numpy as np


class CoordinateLinearCombinationsLesson:
    """Keep the geometric vector fixed while changing its coordinate recipe."""

    def __init__(self, basis=None, vector=None):
        self.basis = self._basis(
            np.array([[1.0, 1.0], [0.0, 1.0]]) if basis is None else basis,
            "basis",
        )
        self.vector = self._vector(
            np.array([3.0, 2.0]) if vector is None else vector,
            "vector",
        )

    @staticmethod
    def _basis(value, name):
        matrix = np.asarray(value, dtype=float)
        if matrix.shape != (2, 2) or not np.all(np.isfinite(matrix)):
            raise ValueError(f"{name} must be a finite 2-by-2 matrix")
        if abs(float(np.linalg.det(matrix))) < 1e-10:
            raise ValueError(f"{name} must be invertible")
        return matrix

    @staticmethod
    def _vector(value, name):
        vector = np.asarray(value, dtype=float)
        if vector.shape != (2,) or not np.all(np.isfinite(vector)):
            raise ValueError(f"{name} must be a finite length-2 vector")
        return vector

    def standard_coordinates(self):
        return self.vector.copy()

    def basis_coordinates(self):
        return np.linalg.solve(self.basis, self.vector)

    def reconstruct_from_basis(self, coordinates):
        return self.basis @ self._vector(coordinates, "coordinates")

    def basis_vectors_in_standard_coordinates(self):
        return self.basis.copy()

    @classmethod
    def transition_matrix(cls, target_basis, source_basis):
        """Return Q_target<-source, whose columns are source vectors in target coordinates."""
        target = cls._basis(target_basis, "target_basis")
        source = cls._basis(source_basis, "source_basis")
        return np.linalg.solve(target, source)

