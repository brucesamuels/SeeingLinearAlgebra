"""Renderer-independent model for uniqueness in full-rank least squares."""
from __future__ import annotations

import numpy as np


class LeastSquaresUniqueness:
    """Connect full column rank, positive-definite Gram matrices, and uniqueness."""

    DEFAULT_MATRIX = np.array([[1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])
    DEFAULT_TARGET = np.array([2.0, 1.0, 2.0])

    def __init__(self, matrix=None, target=None):
        matrix_value = self.DEFAULT_MATRIX if matrix is None else matrix
        self.matrix = self._matrix(matrix_value)
        target_value = self.DEFAULT_TARGET if target is None else target
        self.target = self._target(target_value)

    @staticmethod
    def _matrix(value):
        matrix = np.asarray(value, dtype=float)
        if matrix.ndim != 2 or min(matrix.shape) == 0:
            raise ValueError("matrix must be nonempty and two-dimensional")
        if not np.all(np.isfinite(matrix)):
            raise ValueError("matrix entries must be finite")
        return matrix

    def _target(self, value):
        target = np.asarray(value, dtype=float)
        if target.shape != (self.matrix.shape[0],) or not np.all(np.isfinite(target)):
            raise ValueError(f"target must be finite with length {self.matrix.shape[0]}")
        return target

    def _coefficient(self, value):
        coefficient = np.asarray(value, dtype=float)
        if coefficient.shape != (self.matrix.shape[1],) or not np.all(np.isfinite(coefficient)):
            raise ValueError(
                f"coefficient must be finite with length {self.matrix.shape[1]}"
            )
        return coefficient

    def gram_matrix(self):
        return self.matrix.T @ self.matrix

    def normal_right_hand_side(self):
        return self.matrix.T @ self.target

    def has_independent_columns(self):
        return np.linalg.matrix_rank(self.matrix) == self.matrix.shape[1]

    def gram_is_positive_definite(self):
        return self.has_independent_columns()

    def unique_solution(self):
        if not self.has_independent_columns():
            raise ValueError("least-squares coefficient vector is not unique")
        return np.linalg.solve(self.gram_matrix(), self.normal_right_hand_side())

    def fitted_vector(self, coefficient):
        return self.matrix @ self._coefficient(coefficient)

    def residual(self, coefficient):
        return self.target - self.fitted_vector(coefficient)

    def objective(self, coefficient):
        residual = self.residual(coefficient)
        return float(residual @ residual)

    def normal_residual(self, coefficient):
        return self.matrix.T @ self.residual(coefficient)

    def shifted_coefficient(self, coefficient, null_direction, amount):
        x = self._coefficient(coefficient)
        z = self._coefficient(null_direction)
        if not np.isfinite(amount):
            raise ValueError("amount must be finite")
        if not np.allclose(self.matrix @ z, 0.0):
            raise ValueError("null_direction must lie in the matrix null space")
        return x + float(amount) * z
