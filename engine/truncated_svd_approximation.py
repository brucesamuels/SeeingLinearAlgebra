"""Renderer-independent model for truncated SVD approximation."""

from __future__ import annotations

from numbers import Integral

import numpy as np


class TruncatedSVDApproximation:
    """Decompose a matrix into ordered rank-one layers and truncate them."""

    def __init__(self, matrix=None) -> None:
        if matrix is None:
            matrix = np.diag([5.0, 2.0, 0.5])
        candidate = np.asarray(matrix, dtype=float)
        if candidate.ndim != 2 or not candidate.shape[0] or not candidate.shape[1]:
            raise ValueError("matrix must be a nonempty two-dimensional array")
        if not np.all(np.isfinite(candidate)):
            raise ValueError("matrix entries must be finite")
        self._matrix = candidate.copy()
        self._u, self._singular_values, self._vt = np.linalg.svd(
            self._matrix, full_matrices=False
        )

    @property
    def matrix(self) -> np.ndarray:
        return self._matrix.copy()

    @property
    def maximum_rank(self) -> int:
        return len(self._singular_values)

    def singular_values(self) -> np.ndarray:
        return self._singular_values.copy()

    def rank_one_components(self) -> tuple[np.ndarray, ...]:
        return tuple(
            singular_value * np.outer(self._u[:, index], self._vt[index, :])
            for index, singular_value in enumerate(self._singular_values)
        )

    def reconstruct(self) -> np.ndarray:
        return sum(self.rank_one_components(), np.zeros_like(self._matrix))

    def truncated(self, rank: int) -> np.ndarray:
        count = self._rank(rank)
        components = self.rank_one_components()
        return sum(components[:count], np.zeros_like(self._matrix))

    def residual(self, rank: int) -> np.ndarray:
        return self._matrix - self.truncated(rank)

    def spectral_error(self, rank: int) -> float:
        return float(np.linalg.norm(self.residual(rank), ord=2))

    def frobenius_error(self, rank: int) -> float:
        return float(np.linalg.norm(self.residual(rank), ord="fro"))

    def optimal_spectral_error(self, rank: int) -> float:
        count = self._rank(rank)
        if count == self.maximum_rank:
            return 0.0
        return float(self._singular_values[count])

    def optimal_frobenius_error(self, rank: int) -> float:
        count = self._rank(rank)
        return float(np.sqrt(np.sum(self._singular_values[count:] ** 2)))

    def selected_components(self, indices) -> np.ndarray:
        chosen = tuple(indices)
        if len(set(chosen)) != len(chosen):
            raise ValueError("component indices must be unique")
        if any(not isinstance(index, Integral) or isinstance(index, bool) for index in chosen):
            raise ValueError("component indices must be integers")
        if any(index < 0 or index >= self.maximum_rank for index in chosen):
            raise ValueError("component index is out of range")
        components = self.rank_one_components()
        return sum((components[index] for index in chosen), np.zeros_like(self._matrix))

    def selected_spectral_error(self, indices) -> float:
        approximation = self.selected_components(indices)
        return float(np.linalg.norm(self._matrix - approximation, ord=2))

    def _rank(self, rank: int) -> int:
        if not isinstance(rank, Integral) or isinstance(rank, bool):
            raise ValueError("rank must be an integer")
        count = int(rank)
        if count < 0 or count > self.maximum_rank:
            raise ValueError(f"rank must lie between 0 and {self.maximum_rank}")
        return count
