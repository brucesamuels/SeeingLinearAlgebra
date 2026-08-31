"""Renderer-independent model for the conceptual introduction to the SVD."""
from __future__ import annotations

import numpy as np


class SingularValueDecompositionIntroduction:
    """Derive a thin full-column-rank SVD from the Gram matrix A-transpose A."""

    DEFAULT_MATRIX = np.array([[1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])

    def __init__(self, matrix=None):
        value = self.DEFAULT_MATRIX if matrix is None else matrix
        self.matrix = self._matrix(value)
        if self.matrix.shape[0] < self.matrix.shape[1]:
            raise ValueError("introductory thin SVD requires at least as many rows as columns")
        if np.linalg.matrix_rank(self.matrix) < self.matrix.shape[1]:
            raise ValueError("introductory thin SVD requires independent columns")

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
        for column_index in range(oriented.shape[1]):
            column = oriented[:, column_index]
            nonzero = np.flatnonzero(np.abs(column) > 1e-12)
            if nonzero.size and column[nonzero[0]] < 0:
                oriented[:, column_index] *= -1
        return oriented

    def gram_matrix(self):
        return self.matrix.T @ self.matrix

    def gram_eigendecomposition(self):
        eigenvalues, eigenvectors = np.linalg.eigh(self.gram_matrix())
        order = np.argsort(eigenvalues)[::-1]
        values = eigenvalues[order]
        vectors = self._orient_columns(eigenvectors[:, order])
        return values, vectors

    def singular_values(self):
        eigenvalues, _ = self.gram_eigendecomposition()
        return np.sqrt(np.maximum(eigenvalues, 0.0))

    def right_singular_vectors(self):
        _, eigenvectors = self.gram_eigendecomposition()
        return eigenvectors

    def left_singular_vectors(self):
        images = self.matrix @ self.right_singular_vectors()
        return images / self.singular_values()

    def sigma_matrix(self):
        return np.diag(self.singular_values())

    def factorization(self):
        return self.left_singular_vectors(), self.sigma_matrix(), self.right_singular_vectors().T

    def reconstruction(self):
        u, sigma, vt = self.factorization()
        return u @ sigma @ vt

    def mapped_right_directions(self):
        return self.matrix @ self.right_singular_vectors()

    def mapped_directions_are_orthogonal(self, tolerance=1e-10):
        if not np.isfinite(tolerance) or tolerance < 0:
            raise ValueError("tolerance must be finite and nonnegative")
        images = self.mapped_right_directions()
        gram = images.T @ images
        return bool(np.allclose(gram, np.diag(np.diag(gram)), atol=tolerance))
