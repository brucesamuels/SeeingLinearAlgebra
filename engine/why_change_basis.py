"""Renderer-independent mathematics for the opening change-of-basis lesson."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


DEFAULT_VECTOR = np.array([4.0, 2.0])
DEFAULT_BASIS = np.array([[1.0, 1.0], [1.0, -1.0]])


@dataclass(frozen=True)
class CoordinateDescription:
    """One geometric vector together with two coordinate descriptions."""

    vector: np.ndarray
    standard_coordinates: np.ndarray
    basis: np.ndarray
    basis_coordinates: np.ndarray


class WhyChangeBasisLesson:
    """Mathematical model for a fixed vector viewed in different bases."""

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

    def basis_coordinates(self) -> np.ndarray:
        return np.linalg.solve(self._basis, self._vector)

    def reconstruct(self, coordinates: np.ndarray | None = None) -> np.ndarray:
        c = self.basis_coordinates() if coordinates is None else np.asarray(coordinates, dtype=float)
        if c.shape != (2,):
            raise ValueError("coordinates must have shape (2,)")
        return self._basis @ c

    def description(self) -> CoordinateDescription:
        return CoordinateDescription(
            vector=self.vector,
            standard_coordinates=self.vector,
            basis=self.basis,
            basis_coordinates=self.basis_coordinates(),
        )

