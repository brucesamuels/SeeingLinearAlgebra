"""Renderer-independent mathematics for symmetric matrices and orthogonal eigenvectors."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

DEFAULT_MATRIX = np.array([[2.0, 1.0], [1.0, 2.0]])


@dataclass(frozen=True)
class SymmetricEigenExample:
    matrix: np.ndarray
    eigenvalue_1: float
    eigenvector_1: np.ndarray
    eigenvalue_2: float
    eigenvector_2: np.ndarray
    dot_product: float


class SymmetricOrthogonalEigenvectorsLesson:
    """Mathematical model for the distinct-eigenvalue orthogonality theorem."""

    def __init__(self, matrix: np.ndarray = DEFAULT_MATRIX) -> None:
        a = np.asarray(matrix, dtype=float)
        if a.shape != (2, 2):
            raise ValueError("matrix must have shape (2, 2)")
        if not np.isfinite(a).all():
            raise ValueError("matrix entries must be finite")
        if not np.allclose(a, a.T):
            raise ValueError("matrix must be symmetric")
        self._matrix = a.copy()

    @property
    def matrix(self) -> np.ndarray:
        return self._matrix.copy()

    def example(self) -> SymmetricEigenExample:
        v1 = np.array([1.0, 1.0])
        v2 = np.array([1.0, -1.0])
        l1 = 3.0
        l2 = 1.0
        return SymmetricEigenExample(
            matrix=self.matrix,
            eigenvalue_1=l1,
            eigenvector_1=v1,
            eigenvalue_2=l2,
            eigenvector_2=v2,
            dot_product=float(v1 @ v2),
        )

    def verifies_eigenpairs(self) -> bool:
        ex = self.example()
        return bool(
            np.allclose(self._matrix @ ex.eigenvector_1, ex.eigenvalue_1 * ex.eigenvector_1)
            and np.allclose(self._matrix @ ex.eigenvector_2, ex.eigenvalue_2 * ex.eigenvector_2)
        )

    def distinct_eigenvectors_are_orthogonal(self) -> bool:
        ex = self.example()
        return bool(abs(ex.dot_product) < 1e-12 and ex.eigenvalue_1 != ex.eigenvalue_2)

    def orthonormal_eigenbasis(self) -> np.ndarray:
        ex = self.example()
        q1 = ex.eigenvector_1 / np.linalg.norm(ex.eigenvector_1)
        q2 = ex.eigenvector_2 / np.linalg.norm(ex.eigenvector_2)
        return np.column_stack([q1, q2])

    def diagonal_matrix(self) -> np.ndarray:
        q = self.orthonormal_eigenbasis()
        return q.T @ self._matrix @ q
