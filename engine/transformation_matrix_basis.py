"""Renderer-independent mathematics for a transformation in another basis."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

DEFAULT_A = np.array([[2.0, 0.0], [0.0, 1.0]])
DEFAULT_P = np.array([[1.0, 1.0], [0.0, 1.0]])
DEFAULT_B_COORDINATES = np.array([1.0, 2.0])


@dataclass(frozen=True)
class TransformationBasisExample:
    standard_matrix: np.ndarray
    basis_matrix: np.ndarray
    matrix_in_basis: np.ndarray
    input_standard: np.ndarray
    output_standard: np.ndarray
    input_basis: np.ndarray
    output_basis: np.ndarray


class TransformationMatrixBasisLesson:
    def __init__(self, standard_matrix=DEFAULT_A, basis_matrix=DEFAULT_P, input_basis=DEFAULT_B_COORDINATES):
        a, p, x = map(lambda value: np.asarray(value, dtype=float), (standard_matrix, basis_matrix, input_basis))
        if a.shape != (2, 2) or p.shape != (2, 2):
            raise ValueError("matrices must have shape (2, 2)")
        if x.shape != (2,):
            raise ValueError("input coordinates must have shape (2,)")
        if not np.isfinite(a).all() or not np.isfinite(p).all() or not np.isfinite(x).all():
            raise ValueError("entries must be finite")
        if abs(float(np.linalg.det(p))) < 1e-12:
            raise ValueError("basis matrix must be invertible")
        self._a, self._p, self._x = a.copy(), p.copy(), x.copy()

    def matrix_in_basis(self):
        return np.linalg.inv(self._p) @ self._a @ self._p

    def input_standard(self):
        return self._p @ self._x

    def output_standard(self):
        return self._a @ self.input_standard()

    def output_basis(self):
        return self.matrix_in_basis() @ self._x

    def example(self):
        return TransformationBasisExample(
            self._a.copy(), self._p.copy(), self.matrix_in_basis(),
            self.input_standard(), self.output_standard(), self._x.copy(), self.output_basis(),
        )
