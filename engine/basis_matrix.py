"""Renderer-independent mathematics for the basis matrix lesson."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


DEFAULT_BASIS = np.array([[1.0, 1.0], [1.0, -1.0]])
DEFAULT_COORDINATES = np.array([3.0, 1.0])


@dataclass(frozen=True)
class BasisMatrixExample:
    basis_matrix: np.ndarray
    basis_coordinates: np.ndarray
    standard_vector: np.ndarray
    worked_coordinates: np.ndarray
    worked_standard_coordinates: np.ndarray


class BasisMatrixLesson:
    """A basis matrix synthesizes a vector from basis coordinates."""

    def __init__(
        self,
        basis_matrix: np.ndarray = DEFAULT_BASIS,
        basis_coordinates: np.ndarray = DEFAULT_COORDINATES,
    ) -> None:
        p = np.asarray(basis_matrix, dtype=float)
        c = np.asarray(basis_coordinates, dtype=float)
        if p.shape != (2, 2):
            raise ValueError("basis matrix must have shape (2, 2)")
        if c.shape != (2,):
            raise ValueError("basis coordinates must have shape (2,)")
        if not np.isfinite(p).all() or not np.isfinite(c).all():
            raise ValueError("entries must be finite")
        if abs(float(np.linalg.det(p))) < 1e-12:
            raise ValueError("basis matrix must be invertible")
        self._basis_matrix = p.copy()
        self._basis_coordinates = c.copy()

    @property
    def basis_matrix(self) -> np.ndarray:
        return self._basis_matrix.copy()

    @property
    def basis_coordinates(self) -> np.ndarray:
        return self._basis_coordinates.copy()

    def basis_vector(self, index: int) -> np.ndarray:
        if index not in (0, 1):
            raise IndexError("basis-vector index must be 0 or 1")
        return self._basis_matrix[:, index].copy()

    def synthesize(self, coordinates: np.ndarray | None = None) -> np.ndarray:
        c = self._basis_coordinates if coordinates is None else np.asarray(coordinates, dtype=float)
        if c.shape != (2,):
            raise ValueError("coordinates must have shape (2,)")
        return self._basis_matrix @ c

    def worked_standard_coordinates(self) -> np.ndarray:
        return self.synthesize(np.array([2.0, -1.0]))

    def example(self) -> BasisMatrixExample:
        return BasisMatrixExample(
            basis_matrix=self.basis_matrix,
            basis_coordinates=self.basis_coordinates,
            standard_vector=self.synthesize(),
            worked_coordinates=np.array([2.0, -1.0]),
            worked_standard_coordinates=self.worked_standard_coordinates(),
        )
