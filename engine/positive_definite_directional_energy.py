"""Renderer-independent numerical model for directional quadratic energy."""
from __future__ import annotations

import math

import numpy as np


class DirectionalQuadraticEnergy:
    """Evaluate ``x.T @ A @ x`` along directions in the plane."""

    def __init__(self, matrix=None):
        value = [[2.0, 1.0], [1.0, 2.0]] if matrix is None else matrix
        self.matrix = self._matrix(value)

    @staticmethod
    def _matrix(value):
        matrix = np.asarray(value, dtype=float)
        if matrix.shape != (2, 2) or not np.all(np.isfinite(matrix)):
            raise ValueError("matrix must be a finite 2-by-2 matrix")
        if not np.allclose(matrix, matrix.T):
            raise ValueError("matrix must be symmetric")
        return matrix

    @staticmethod
    def _vector(value):
        vector = np.asarray(value, dtype=float)
        if vector.shape != (2,) or not np.all(np.isfinite(vector)):
            raise ValueError("vector must be a finite length-2 vector")
        return vector

    @staticmethod
    def direction(theta):
        """Return the unit vector at angle ``theta`` radians."""
        if not math.isfinite(theta):
            raise ValueError("theta must be finite")
        return np.array([math.cos(theta), math.sin(theta)])

    def energy(self, vector):
        """Return the scalar quadratic energy of a vector."""
        x = self._vector(vector)
        return float(x @ self.matrix @ x)

    def directional_energy(self, theta):
        """Return the quadratic energy in the unit direction ``theta``."""
        return self.energy(self.direction(theta))

    def directional_samples(self, angles):
        """Return ``(direction, energy)`` pairs for an iterable of angles."""
        return [(self.direction(theta), self.directional_energy(theta)) for theta in angles]
