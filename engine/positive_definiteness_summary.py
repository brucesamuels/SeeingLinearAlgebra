"""Renderer-independent synthesis of tests for symmetric matrix definiteness."""
from __future__ import annotations

import numpy as np


class PositiveDefinitenessSummary:
    """Classify a symmetric matrix and expose its principal definiteness tests."""

    DEFAULT_MATRIX = np.array([[2.0, 1.0], [1.0, 2.0]])

    def __init__(self, matrix=None, tolerance=1e-10):
        value = self.DEFAULT_MATRIX if matrix is None else matrix
        self.matrix = self._symmetric_matrix(value)
        if not np.isfinite(tolerance) or tolerance <= 0:
            raise ValueError("tolerance must be finite and positive")
        self.tolerance = float(tolerance)

    @staticmethod
    def _symmetric_matrix(value):
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
        return matrix

    def _vector(self, value):
        vector = np.asarray(value, dtype=float)
        if vector.shape != (self.matrix.shape[0],):
            raise ValueError(f"vector must have shape ({self.matrix.shape[0]},)")
        if not np.all(np.isfinite(vector)):
            raise ValueError("vector entries must be finite")
        return vector

    def eigenvalues(self):
        return np.linalg.eigvalsh(self.matrix)

    def inertia(self):
        values = self.eigenvalues()
        positive = int(np.sum(values > self.tolerance))
        negative = int(np.sum(values < -self.tolerance))
        zero = int(values.size - positive - negative)
        return positive, negative, zero

    def classification(self):
        positive, negative, zero = self.inertia()
        dimension = self.matrix.shape[0]
        if positive == dimension:
            return "positive definite"
        if negative == dimension:
            return "negative definite"
        if positive and not negative:
            return "positive semidefinite"
        if negative and not positive:
            return "negative semidefinite"
        if not positive and not negative:
            return "zero"
        return "indefinite"

    def energy(self, vector):
        x = self._vector(vector)
        return float(x @ self.matrix @ x)

    def leading_principal_minors(self):
        return np.array(
            [np.linalg.det(self.matrix[:size, :size]) for size in range(1, self.matrix.shape[0] + 1)]
        )

    def ldl_factorization(self):
        dimension = self.matrix.shape[0]
        lower = np.eye(dimension)
        diagonal = np.zeros(dimension)
        for column in range(dimension):
            diagonal[column] = self.matrix[column, column] - np.sum(
                lower[column, :column] ** 2 * diagonal[:column]
            )
            for row in range(column + 1, dimension):
                numerator = self.matrix[row, column] - np.sum(
                    lower[row, :column]
                    * lower[column, :column]
                    * diagonal[:column]
                )
                if abs(diagonal[column]) <= self.tolerance:
                    if abs(numerator) <= self.tolerance:
                        lower[row, column] = 0.0
                    else:
                        raise ValueError("LDL factorization requires a nonzero pivot")
                else:
                    lower[row, column] = numerator / diagonal[column]
        return lower, np.diag(diagonal)

    def elimination_pivots(self):
        _, diagonal = self.ldl_factorization()
        return np.diag(diagonal)

    def cholesky_upper(self):
        return np.linalg.cholesky(self.matrix).T

    def positive_definite_checks(self):
        values_positive = bool(np.all(self.eigenvalues() > self.tolerance))
        minors_positive = bool(
            np.all(self.leading_principal_minors() > self.tolerance)
        )
        try:
            pivots_positive = bool(
                np.all(self.elimination_pivots() > self.tolerance)
            )
        except ValueError:
            pivots_positive = False
        try:
            self.cholesky_upper()
            cholesky_exists = True
        except np.linalg.LinAlgError:
            cholesky_exists = False
        return {
            "eigenvalues": values_positive,
            "leading_principal_minors": minors_positive,
            "elimination_pivots": pivots_positive,
            "cholesky": cholesky_exists,
        }
