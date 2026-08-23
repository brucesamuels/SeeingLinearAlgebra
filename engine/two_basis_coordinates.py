"""Renderer-independent mathematics for changing between two bases."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


DEFAULT_B = np.array([[1.0, 1.0], [1.0, -1.0]])
DEFAULT_C = np.array([[1.0, 2.0], [1.0, 0.0]])
DEFAULT_B_COORDINATES = np.array([3.0, 1.0])


@dataclass(frozen=True)
class TwoBasisExample:
    basis_b: np.ndarray
    basis_c: np.ndarray
    transition_b_to_c: np.ndarray
    coordinates_b: np.ndarray
    coordinates_c: np.ndarray
    standard_vector: np.ndarray


class TwoBasisCoordinatesLesson:
    def __init__(self, basis_b=DEFAULT_B, basis_c=DEFAULT_C, coordinates_b=DEFAULT_B_COORDINATES):
        b = np.asarray(basis_b, dtype=float)
        c = np.asarray(basis_c, dtype=float)
        coordinates = np.asarray(coordinates_b, dtype=float)
        for name, matrix in (("B", b), ("C", c)):
            if matrix.shape != (2, 2):
                raise ValueError(f"basis {name} must have shape (2, 2)")
            if not np.isfinite(matrix).all() or abs(float(np.linalg.det(matrix))) < 1e-12:
                raise ValueError(f"basis {name} must be finite and invertible")
        if coordinates.shape != (2,) or not np.isfinite(coordinates).all():
            raise ValueError("basis coordinates must be a finite vector of shape (2,)")
        self._b, self._c, self._coordinates_b = b.copy(), c.copy(), coordinates.copy()

    def transition_b_to_c(self):
        return np.linalg.inv(self._c) @ self._b

    def standard_vector(self):
        return self._b @ self._coordinates_b

    def coordinates_c(self):
        return self.transition_b_to_c() @ self._coordinates_b

    def example(self):
        return TwoBasisExample(
            basis_b=self._b.copy(), basis_c=self._c.copy(),
            transition_b_to_c=self.transition_b_to_c(),
            coordinates_b=self._coordinates_b.copy(), coordinates_c=self.coordinates_c(),
            standard_vector=self.standard_vector(),
        )
