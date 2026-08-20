"""Renderer-independent mathematics for Chapter 7: diagonalization."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


DEFAULT_MATRIX = np.array(
    [[4.0, 1.0, 0.0],
     [2.0, 3.0, 0.0],
     [0.0, 0.0, 1.0]]
)

EIGENVECTORS = np.column_stack(
    [np.array([0.0, 0.0, 1.0]),
     np.array([1.0, -2.0, 0.0]),
     np.array([1.0, 1.0, 0.0])]
)


@dataclass(frozen=True)
class DiagonalizationData:
    matrix: np.ndarray
    eigenvector_matrix: np.ndarray
    diagonal_matrix: np.ndarray
    inverse_eigenvector_matrix: np.ndarray


class DiagonalizationLesson:
    """Derive D from A and an eigenvector basis P via D = P^{-1} A P."""

    def data(self) -> DiagonalizationData:
        p = EIGENVECTORS.copy()
        p_inv = np.linalg.inv(p)
        d = p_inv @ DEFAULT_MATRIX @ p
        return DiagonalizationData(
            matrix=DEFAULT_MATRIX.copy(),
            eigenvector_matrix=p,
            diagonal_matrix=d,
            inverse_eigenvector_matrix=p_inv,
        )

    def derived_matrix_is_diagonal(self) -> bool:
        d = self.data().diagonal_matrix
        return bool(np.allclose(d, np.diag(np.diag(d))))

    def ap_equals_pd(self) -> bool:
        data = self.data()
        return bool(np.allclose(data.matrix @ data.eigenvector_matrix,
                                data.eigenvector_matrix @ data.diagonal_matrix))

    def reconstruct(self) -> np.ndarray:
        data = self.data()
        return data.eigenvector_matrix @ data.diagonal_matrix @ data.inverse_eigenvector_matrix

    def is_valid_diagonalization(self) -> bool:
        return bool(np.allclose(self.reconstruct(), DEFAULT_MATRIX))
