"""Renderer-independent model for a rank-deficient SVD discovery lesson."""

from __future__ import annotations

from numbers import Integral

import numpy as np

from engine.rank_collapse import RankCollapse


class ZeroSingularValueModel:
    """Expose the geometry and subspaces of a nonzero rank-one 2-by-2 map."""

    DEFAULT_MATRIX = np.array([[1.0, 1.0], [1.0, 1.0]])

    def __init__(self, matrix=None, *, tolerance: float | None = None) -> None:
        value = self.DEFAULT_MATRIX if matrix is None else matrix
        array = np.asarray(value, dtype=float)
        if array.ndim != 2 or array.shape != (2, 2):
            raise ValueError("matrix must be two-dimensional with shape 2-by-2")
        if not np.all(np.isfinite(array)):
            raise ValueError("matrix entries must be finite")

        collapse = RankCollapse(array, target_rank=0, tolerance=tolerance)
        if collapse.initial_rank != 1:
            raise ValueError("matrix must be nonzero and rank one")

        self._matrix = np.array(array, copy=True)
        self._collapse = collapse

    @staticmethod
    def _canonical(vector) -> np.ndarray:
        result = np.asarray(vector, dtype=float).copy()
        nonzero = np.flatnonzero(np.abs(result) > 1e-12)
        if nonzero.size and result[nonzero[0]] < 0:
            result *= -1
        return result

    @property
    def matrix(self) -> np.ndarray:
        return self._matrix.copy()

    def gram_matrix(self) -> np.ndarray:
        return self._matrix.T @ self._matrix

    def singular_values(self) -> np.ndarray:
        return self._collapse.singular_values_at(0.0)

    def rank(self) -> int:
        return self._collapse.rank_at(0.0)

    def nullity(self) -> int:
        return self._collapse.nullity_at(0.0)

    def active_right_direction(self) -> np.ndarray:
        basis = self._collapse.row_space_basis(0.0)
        return self._canonical(basis[0])

    def null_direction(self) -> np.ndarray:
        basis = self._collapse.kernel_basis(0.0)
        return self._canonical(basis[:, 0])

    def active_left_direction(self) -> np.ndarray:
        right = self.active_right_direction()
        mapped = self.apply(right)
        return mapped / np.linalg.norm(mapped)

    def apply(self, vector) -> np.ndarray:
        values = np.asarray(vector, dtype=float)
        if values.ndim != 1 or values.shape != (2,):
            raise ValueError("vector must have exactly two components")
        if not np.all(np.isfinite(values)):
            raise ValueError("vector entries must be finite")
        return self._matrix @ values

    def circle_samples(self, count: int = 32) -> np.ndarray:
        if isinstance(count, bool) or not isinstance(count, Integral) or count < 8:
            raise ValueError("count must be an integer at least 8")
        angles = np.linspace(0.0, 2.0 * np.pi, int(count), endpoint=False)
        return np.column_stack((np.cos(angles), np.sin(angles)))

    def mapped_circle_samples(self, count: int = 32) -> np.ndarray:
        return self.circle_samples(count) @ self._matrix.T

    def reduced_factorization(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        sigma = float(self.singular_values()[0])
        u = self.active_left_direction().reshape(2, 1)
        vt = self.active_right_direction().reshape(1, 2)
        return u, np.array([[sigma]]), vt

    def reduced_reconstruction(self) -> np.ndarray:
        u, sigma, vt = self.reduced_factorization()
        return u @ sigma @ vt
