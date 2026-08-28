"""Renderer-independent model for positive pivots and Sylvester's criterion."""
from __future__ import annotations

import math

import numpy as np


class PositiveDefiniteEliminationTest:
    """Connect symmetric elimination, completed squares, and leading minors."""

    def __init__(self, matrix=None):
        value = [[2.0, 1.0], [1.0, 2.0]] if matrix is None else matrix
        self.matrix = self._matrix(value)

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

    def energy(self, vector):
        x = np.asarray(vector, dtype=float)
        if x.shape != (self.matrix.shape[0],) or not np.all(np.isfinite(x)):
            raise ValueError(f"vector must be finite with length {self.matrix.shape[0]}")
        return float(x @ self.matrix @ x)

    def leading_principal_minors(self):
        return np.array(
            [
                float(np.linalg.det(self.matrix[:size, :size]))
                for size in range(1, self.matrix.shape[0] + 1)
            ]
        )

    def elimination_pivots(self, tolerance=1e-12):
        """Return no-row-swap symmetric-elimination pivots."""
        if not math.isfinite(tolerance) or tolerance < 0:
            raise ValueError("tolerance must be finite and nonnegative")
        working = self.matrix.copy()
        pivots = []
        for index in range(working.shape[0]):
            pivot = float(working[index, index])
            pivots.append(pivot)
            if index == working.shape[0] - 1:
                continue
            if abs(pivot) <= tolerance:
                raise ValueError("zero pivot prevents elimination without row swaps")
            column = working[index + 1 :, index].copy()
            working[index + 1 :, index + 1 :] -= np.outer(column, column) / pivot
            working[index + 1 :, index] = 0.0
            working[index, index + 1 :] = 0.0
        return np.array(pivots)

    def pivot_minor_ratios(self, tolerance=1e-12):
        if not math.isfinite(tolerance) or tolerance < 0:
            raise ValueError("tolerance must be finite and nonnegative")
        minors = self.leading_principal_minors()
        previous = 1.0
        ratios = []
        for minor in minors:
            if abs(previous) <= tolerance:
                raise ValueError("zero leading minor makes the next ratio undefined")
            ratios.append(float(minor / previous))
            previous = float(minor)
        return np.array(ratios)

    def completed_square_coefficients(self, tolerance=1e-12):
        """Return a, b/a, and c-b^2/a for [[a,b],[b,c]]."""
        if self.matrix.shape != (2, 2):
            raise ValueError("completed_square_coefficients requires a 2-by-2 matrix")
        if not math.isfinite(tolerance) or tolerance < 0:
            raise ValueError("tolerance must be finite and nonnegative")
        a, b, c = self.matrix[0, 0], self.matrix[0, 1], self.matrix[1, 1]
        if abs(a) <= tolerance:
            raise ValueError("the first diagonal entry must be nonzero")
        return float(a), float(b / a), float(c - b * b / a)

    def has_positive_leading_principal_minors(self, tolerance=1e-10):
        if not math.isfinite(tolerance) or tolerance < 0:
            raise ValueError("tolerance must be finite and nonnegative")
        return bool(np.all(self.leading_principal_minors() > tolerance))

    def has_positive_elimination_pivots(self, tolerance=1e-10):
        if not math.isfinite(tolerance) or tolerance < 0:
            raise ValueError("tolerance must be finite and nonnegative")
        try:
            pivots = self.elimination_pivots(tolerance=tolerance)
        except ValueError:
            return False
        return bool(np.all(pivots > tolerance))
