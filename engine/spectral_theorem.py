"""Renderer-independent mathematics for the spectral theorem lesson."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

DEFAULT_MATRIX = np.array([[2.0, 1.0], [1.0, 2.0]])


@dataclass(frozen=True)
class SpectralExample:
    matrix: np.ndarray
    q: np.ndarray
    d: np.ndarray
    reconstructed: np.ndarray


class SpectralTheoremLesson:
    """Numerical model for orthogonal diagonalization of a real symmetric matrix."""

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

    def orthogonal_eigenvector_matrix(self) -> np.ndarray:
        s = 1.0 / np.sqrt(2.0)
        return np.array([[s, s], [s, -s]])

    def diagonal_matrix(self) -> np.ndarray:
        q = self.orthogonal_eigenvector_matrix()
        return q.T @ self._matrix @ q

    def reconstruction(self) -> np.ndarray:
        q = self.orthogonal_eigenvector_matrix()
        d = self.diagonal_matrix()
        return q @ d @ q.T

    def example(self) -> SpectralExample:
        q = self.orthogonal_eigenvector_matrix()
        d = self.diagonal_matrix()
        return SpectralExample(
            matrix=self.matrix,
            q=q,
            d=d,
            reconstructed=q @ d @ q.T,
        )

    def verifies_spectral_factorization(self) -> bool:
        ex = self.example()
        return bool(
            np.allclose(ex.q.T @ ex.q, np.eye(2))
            and np.allclose(ex.d, np.diag([3.0, 1.0]))
            and np.allclose(ex.reconstructed, ex.matrix)
        )
