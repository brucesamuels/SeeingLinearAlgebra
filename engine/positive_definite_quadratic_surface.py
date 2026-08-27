"""Renderer-independent geometry for a two-variable quadratic form."""
from __future__ import annotations

import math

import numpy as np


class QuadraticSurfaceGeometry:
    """Connect directional quadratic energy to the graph ``z = x.T A x``."""

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
        """Return ``x.T @ A @ x`` as a scalar."""
        x = self._vector(vector)
        return float(x @ self.matrix @ x)

    def radial_vector(self, radius, theta):
        """Return ``radius`` times the unit direction at ``theta``."""
        if not math.isfinite(radius) or radius < 0.0:
            raise ValueError("radius must be finite and nonnegative")
        return radius * self.direction(theta)

    def radial_energy(self, radius, theta):
        """Return the energy along a ray from the origin."""
        return self.energy(self.radial_vector(radius, theta))

    def surface_point(self, x, y):
        """Return the point ``(x, y, q(x, y))`` on the quadratic graph."""
        base = self._vector([x, y])
        return np.array([base[0], base[1], self.energy(base)])

    def surface_heights(self, x_values, y_values):
        """Sample graph heights on the Cartesian product of two iterables."""
        return np.array(
            [[self.energy([x, y]) for x in x_values] for y in y_values],
            dtype=float,
        )
