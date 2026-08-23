"""Renderer-independent mathematics for standard-to-basis coordinates."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


DEFAULT_BASIS = np.array([[1.0, 1.0], [1.0, -1.0]])
DEFAULT_STANDARD_COORDINATES = np.array([4.0, 2.0])


@dataclass(frozen=True)
class StandardToBasisExample:
    basis_matrix: np.ndarray
    inverse_basis_matrix: np.ndarray
    standard_coordinates: np.ndarray
    basis_coordinates: np.ndarray
    reconstructed_standard_coordinates: np.ndarray


class StandardToBasisLesson:
    """Analyze a standard coordinate column in a chosen basis."""

    def __init__(self, basis_matrix=DEFAULT_BASIS, standard_coordinates=DEFAULT_STANDARD_COORDINATES):
        matrix = np.asarray(basis_matrix, dtype=float)
        coordinates = np.asarray(standard_coordinates, dtype=float)
        if matrix.shape != (2, 2):
            raise ValueError("basis matrix must have shape (2, 2)")
        if coordinates.shape != (2,):
            raise ValueError("standard coordinates must have shape (2,)")
        if not np.isfinite(matrix).all() or not np.isfinite(coordinates).all():
            raise ValueError("entries must be finite")
        if abs(float(np.linalg.det(matrix))) < 1e-12:
            raise ValueError("basis matrix must be invertible")
        self._basis_matrix = matrix.copy()
        self._standard_coordinates = coordinates.copy()

    @property
    def basis_matrix(self):
        return self._basis_matrix.copy()

    @property
    def standard_coordinates(self):
        return self._standard_coordinates.copy()

    def inverse_basis_matrix(self):
        return np.linalg.inv(self._basis_matrix)

    def basis_coordinates(self, standard_coordinates=None):
        vector = self._standard_coordinates if standard_coordinates is None else np.asarray(standard_coordinates, dtype=float)
        if vector.shape != (2,):
            raise ValueError("standard coordinates must have shape (2,)")
        return self.inverse_basis_matrix() @ vector

    def reconstruct(self, basis_coordinates=None):
        coordinates = self.basis_coordinates() if basis_coordinates is None else np.asarray(basis_coordinates, dtype=float)
        if coordinates.shape != (2,):
            raise ValueError("basis coordinates must have shape (2,)")
        return self._basis_matrix @ coordinates

    def example(self):
        basis_coordinates = self.basis_coordinates()
        return StandardToBasisExample(
            basis_matrix=self.basis_matrix,
            inverse_basis_matrix=self.inverse_basis_matrix(),
            standard_coordinates=self.standard_coordinates,
            basis_coordinates=basis_coordinates,
            reconstructed_standard_coordinates=self.reconstruct(basis_coordinates),
        )
