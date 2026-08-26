"""Numerical spine for the Change of Basis synthesis lesson."""
from __future__ import annotations

import numpy as np


class ChangeOfBasisReview:
    """Relate vectors and transformations across two nonstandard bases."""

    def __init__(self, basis_b=None, basis_c=None, vector=None, transformation_b=None):
        self.basis_b = self._basis(
            [[1.0, 1.0], [1.0, -1.0]] if basis_b is None else basis_b,
            "basis_b",
        )
        self.basis_c = self._basis(
            [[1.0, 2.0], [1.0, 0.0]] if basis_c is None else basis_c,
            "basis_c",
        )
        self.vector = self._vector([3.0, 1.0] if vector is None else vector, "vector")
        self.transformation_b = self._matrix(
            [[2.0, 1.0], [0.0, 3.0]] if transformation_b is None else transformation_b,
            "transformation_b",
        )

    @staticmethod
    def _matrix(value, name):
        matrix = np.asarray(value, dtype=float)
        if matrix.shape != (2, 2) or not np.all(np.isfinite(matrix)):
            raise ValueError(f"{name} must be a finite 2-by-2 matrix")
        return matrix

    @classmethod
    def _basis(cls, value, name):
        matrix = cls._matrix(value, name)
        if abs(float(np.linalg.det(matrix))) < 1e-10:
            raise ValueError(f"{name} must be invertible")
        return matrix

    @staticmethod
    def _vector(value, name):
        vector = np.asarray(value, dtype=float)
        if vector.shape != (2,) or not np.all(np.isfinite(vector)):
            raise ValueError(f"{name} must be a finite length-2 vector")
        return vector

    def coordinates(self, basis):
        return np.linalg.solve(self._basis(basis, "basis"), self.vector)

    def coordinates_b(self):
        return self.coordinates(self.basis_b)

    def coordinates_c(self):
        return self.coordinates(self.basis_c)

    @classmethod
    def transition(cls, target_basis, source_basis):
        target = cls._basis(target_basis, "target_basis")
        source = cls._basis(source_basis, "source_basis")
        return np.linalg.solve(target, source)

    def transition_c_from_b(self):
        return self.transition(self.basis_c, self.basis_b)

    def transition_b_from_c(self):
        return self.transition(self.basis_b, self.basis_c)

    def convert_b_to_c(self, coordinates_b):
        return self.transition_c_from_b() @ self._vector(coordinates_b, "coordinates_b")

    def transformation_c(self):
        q_c_from_b = self.transition_c_from_b()
        q_b_from_c = self.transition_b_from_c()
        return q_c_from_b @ self.transformation_b @ q_b_from_c

    def standard_transformation(self):
        return self.basis_b @ self.transformation_b @ np.linalg.inv(self.basis_b)

