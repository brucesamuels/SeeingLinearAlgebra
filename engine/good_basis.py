"""Renderer-independent mathematics for the good-basis lesson."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

DEFAULT_A = np.array([[3.0, 1.0], [1.0, 3.0]])
DEFAULT_P = np.array([[1.0, 1.0], [1.0, -1.0]])


@dataclass(frozen=True)
class GoodBasisExample:
    standard_matrix: np.ndarray
    basis_matrix: np.ndarray
    matrix_in_basis: np.ndarray
    first_basis_image: np.ndarray
    second_basis_image: np.ndarray


class GoodBasisLesson:
    def __init__(self, standard_matrix=DEFAULT_A, basis_matrix=DEFAULT_P):
        a, p = np.asarray(standard_matrix, dtype=float), np.asarray(basis_matrix, dtype=float)
        if a.shape != (2, 2) or p.shape != (2, 2):
            raise ValueError("matrices must have shape (2, 2)")
        if not np.isfinite(a).all() or not np.isfinite(p).all():
            raise ValueError("entries must be finite")
        if abs(float(np.linalg.det(p))) < 1e-12:
            raise ValueError("basis matrix must be invertible")
        self._a, self._p = a.copy(), p.copy()

    def matrix_in_basis(self):
        return np.linalg.inv(self._p) @ self._a @ self._p

    def basis_image(self, index):
        if index not in (0, 1):
            raise IndexError("basis-vector index must be 0 or 1")
        return self._a @ self._p[:, index]

    def convert_basis_vector(self, coordinates):
        coordinates = np.asarray(coordinates, dtype=float)
        if coordinates.shape != (2,):
            raise ValueError("coordinates must have shape (2,)")
        return self.matrix_in_basis() @ coordinates

    def example(self):
        return GoodBasisExample(
            self._a.copy(), self._p.copy(), self.matrix_in_basis(),
            self.basis_image(0), self.basis_image(1),
        )
