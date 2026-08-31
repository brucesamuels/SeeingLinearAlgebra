"""Renderer-independent computations for a thin singular value decomposition."""
from __future__ import annotations

import numpy as np


class SingularValueDecompositionComputation:
    """Compute a thin full-column-rank SVD from eigenpairs of A-transpose A."""

    DEFAULT_MATRIX = np.array([[1.0, 1.0], [1.0, -1.0], [1.0, 1.0]])

    def __init__(self, matrix=None):
        value = self.DEFAULT_MATRIX if matrix is None else matrix
        self.matrix = self._matrix(value)
        rows, columns = self.matrix.shape
        if rows < columns:
            raise ValueError("thin SVD example requires at least as many rows as columns")
        if np.linalg.matrix_rank(self.matrix) < columns:
            raise ValueError("thin SVD computation requires independent columns")

    @staticmethod
    def _matrix(value):
        matrix = np.asarray(value, dtype=float)
        if matrix.ndim != 2 or min(matrix.shape) == 0:
            raise ValueError("matrix must be nonempty and two-dimensional")
        if not np.all(np.isfinite(matrix)):
            raise ValueError("matrix entries must be finite")
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

    def gram_matrix(self):
        return self.matrix.T @ self.matrix

    def gram_eigenpairs(self):
        values, vectors = np.linalg.eigh(self.gram_matrix())
        order = np.argsort(values)[::-1]
        return values[order], self._orient_columns(vectors[:, order])

    def singular_values(self):
        values, _ = self.gram_eigenpairs()
        return np.sqrt(np.maximum(values, 0.0))

    def right_singular_vectors(self):
        _, vectors = self.gram_eigenpairs()
        return vectors

    def left_singular_vectors(self):
        mapped = self.matrix @ self.right_singular_vectors()
        return mapped / self.singular_values()

    def factorization(self):
        u = self.left_singular_vectors()
        sigma = np.diag(self.singular_values())
        vt = self.right_singular_vectors().T
        return u, sigma, vt

    def reconstruction(self):
        u, sigma, vt = self.factorization()
        return u @ sigma @ vt

    def thin_dimensions(self):
        rows, columns = self.matrix.shape
        return (rows, columns), (columns, columns), (columns, columns)

    def sign_flipped_factorization(self, component_index):
        columns = self.matrix.shape[1]
        if not isinstance(component_index, int) or not 0 <= component_index < columns:
            raise ValueError(f"component_index must be between 0 and {columns - 1}")
        u, sigma, vt = self.factorization()
        u = u.copy()
        vt = vt.copy()
        u[:, component_index] *= -1
        vt[component_index, :] *= -1
        return u, sigma, vt
