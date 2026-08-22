"""Renderer-independent model for coordinates relative to an ordered basis."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


DEFAULT_VECTOR = np.array([4.0, 2.0])
DEFAULT_BASIS = np.array([[1.0, 1.0], [1.0, -1.0]])


@dataclass(frozen=True)
class BasisCoordinateExample:
    vector: np.ndarray
    basis: np.ndarray
    coordinates: np.ndarray
    combination_points: np.ndarray
    reversed_basis: np.ndarray
    reversed_coordinates: np.ndarray


class CoordinatesRelativeToBasisLesson:
    """Coordinates are ordered coefficients, not the geometric vector itself."""

    def __init__(
        self,
        vector: np.ndarray = DEFAULT_VECTOR,
        basis: np.ndarray = DEFAULT_BASIS,
    ) -> None:
        v = np.asarray(vector, dtype=float)
        p = np.asarray(basis, dtype=float)
        if v.shape != (2,):
            raise ValueError("vector must have shape (2,)")
        if p.shape != (2, 2):
            raise ValueError("basis must have shape (2, 2)")
        if not np.isfinite(v).all() or not np.isfinite(p).all():
            raise ValueError("vector and basis entries must be finite")
        if abs(float(np.linalg.det(p))) < 1e-12:
            raise ValueError("basis vectors must be linearly independent")
        self._vector = v.copy()
        self._basis = p.copy()

    @property
    def vector(self) -> np.ndarray:
        return self._vector.copy()

    @property
    def basis(self) -> np.ndarray:
        return self._basis.copy()

    def coordinates(self) -> np.ndarray:
        return np.linalg.solve(self._basis, self._vector)

    def reconstruct(self) -> np.ndarray:
        return self._basis @ self.coordinates()

    def combination_points(self) -> np.ndarray:
        """Vertices for 0 -> b1 -> 2b1 -> 3b1 -> 3b1+b2."""
        c = self.coordinates()
        if not np.allclose(c, [3.0, 1.0]):
            raise ValueError("combination path is defined for the default integer example")
        b1, b2 = self._basis[:, 0], self._basis[:, 1]
        return np.array([
            [0.0, 0.0],
            b1,
            2.0 * b1,
            3.0 * b1,
            3.0 * b1 + b2,
        ])

    def reversed_basis(self) -> np.ndarray:
        return self._basis[:, ::-1].copy()

    def reversed_coordinates(self) -> np.ndarray:
        return np.linalg.solve(self.reversed_basis(), self._vector)

    def example(self) -> BasisCoordinateExample:
        return BasisCoordinateExample(
            vector=self.vector,
            basis=self.basis,
            coordinates=self.coordinates(),
            combination_points=self.combination_points(),
            reversed_basis=self.reversed_basis(),
            reversed_coordinates=self.reversed_coordinates(),
        )

