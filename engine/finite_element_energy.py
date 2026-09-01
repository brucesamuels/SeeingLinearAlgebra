"""Renderer-independent assembly for a one-dimensional finite-element energy."""
from __future__ import annotations

import numpy as np


class FiniteElementEnergy1D:
    """Assemble and solve a uniform linear finite-element model with zero endpoints."""

    def __init__(self, element_count=3, source=1.0):
        if not isinstance(element_count, int) or element_count < 2:
            raise ValueError("element_count must be an integer of at least 2")
        if not np.isfinite(source):
            raise ValueError("source must be finite")
        self.element_count = element_count
        self.source = float(source)

    @property
    def nodes(self):
        return np.linspace(0.0, 1.0, self.element_count + 1)

    @property
    def element_length(self):
        return 1.0 / self.element_count

    @property
    def interior_count(self):
        return self.element_count - 1

    def local_stiffness(self):
        return np.array([[1.0, -1.0], [-1.0, 1.0]]) / self.element_length

    def local_load(self):
        return self.source * self.element_length * np.array([0.5, 0.5])

    def full_stiffness_matrix(self):
        size = self.element_count + 1
        matrix = np.zeros((size, size))
        local = self.local_stiffness()
        for element in range(self.element_count):
            indices = np.array([element, element + 1])
            matrix[np.ix_(indices, indices)] += local
        return matrix

    def full_load_vector(self):
        vector = np.zeros(self.element_count + 1)
        local = self.local_load()
        for element in range(self.element_count):
            vector[element : element + 2] += local
        return vector

    def stiffness_matrix(self):
        return self.full_stiffness_matrix()[1:-1, 1:-1]

    def load_vector(self):
        return self.full_load_vector()[1:-1]

    def _coefficients(self, value):
        coefficients = np.asarray(value, dtype=float)
        if coefficients.shape != (self.interior_count,):
            raise ValueError(f"coefficients must have shape ({self.interior_count},)")
        if not np.all(np.isfinite(coefficients)):
            raise ValueError("coefficients must be finite")
        return coefficients

    def discrete_energy(self, coefficients):
        c = self._coefficients(coefficients)
        return float(0.5 * c @ self.stiffness_matrix() @ c - self.load_vector() @ c)

    def energy_gradient(self, coefficients):
        c = self._coefficients(coefficients)
        return self.stiffness_matrix() @ c - self.load_vector()

    def solve(self):
        return np.linalg.solve(self.stiffness_matrix(), self.load_vector())

    def nodal_values(self):
        return np.concatenate(([0.0], self.solve(), [0.0]))

    def stiffness_energy(self, coefficients):
        c = self._coefficients(coefficients)
        return float(c @ self.stiffness_matrix() @ c)

    def basis_values(self, interior_index, x):
        if not isinstance(interior_index, int) or not 1 <= interior_index < self.element_count:
            raise ValueError(
                f"interior_index must be an integer from 1 to {self.element_count - 1}"
            )
        values = np.asarray(x, dtype=float)
        if not np.all(np.isfinite(values)):
            raise ValueError("evaluation points must be finite")
        center = self.nodes[interior_index]
        result = np.maximum(1.0 - np.abs(values - center) / self.element_length, 0.0)
        return float(result) if result.ndim == 0 else result

    def approximate_solution(self, x):
        values = np.asarray(x, dtype=float)
        if not np.all(np.isfinite(values)):
            raise ValueError("evaluation points must be finite")
        if np.any((values < 0.0) | (values > 1.0)):
            raise ValueError("evaluation points must lie in [0, 1]")
        result = np.interp(values, self.nodes, self.nodal_values())
        return float(result) if result.ndim == 0 else result

    def exact_solution(self, x):
        values = np.asarray(x, dtype=float)
        if not np.all(np.isfinite(values)):
            raise ValueError("evaluation points must be finite")
        if np.any((values < 0.0) | (values > 1.0)):
            raise ValueError("evaluation points must lie in [0, 1]")
        result = 0.5 * self.source * values * (1.0 - values)
        return float(result) if result.ndim == 0 else result
