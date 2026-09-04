"""Renderer-independent principal component analysis through the SVD."""

from __future__ import annotations

from numbers import Integral

import numpy as np

from engine.truncated_svd_approximation import TruncatedSVDApproximation


class PCASVD:
    """Center row observations and expose their principal components."""

    def __init__(self, data=None) -> None:
        if data is None:
            data = self.example_data()
        candidate = np.asarray(data, dtype=float)
        if candidate.ndim != 2 or candidate.shape[0] < 2 or not candidate.shape[1]:
            raise ValueError("data must contain at least two row observations")
        if not np.all(np.isfinite(candidate)):
            raise ValueError("data entries must be finite")

        self._data = candidate.copy()
        self._mean = np.mean(self._data, axis=0)
        self._centered = self._data - self._mean
        if np.linalg.norm(self._centered, ord="fro") == 0:
            raise ValueError("data must contain nonzero centered variation")

        self._approximation = TruncatedSVDApproximation(self._centered)
        eigenvalues, eigenvectors = np.linalg.eigh(self.gram_matrix())
        order = np.argsort(eigenvalues)[::-1]
        self._eigenvalues = np.maximum(eigenvalues[order], 0.0)
        self._directions = eigenvectors[:, order]
        self._canonicalize_direction_signs()

    @staticmethod
    def example_data() -> np.ndarray:
        return np.array(
            [
                [3.0, 2.0],
                [2.0, 3.0],
                [-3.0, -2.0],
                [-2.0, -3.0],
                [1.0, 1.0],
                [-1.0, -1.0],
            ]
        )

    @property
    def shape(self) -> tuple[int, int]:
        return self._data.shape

    @property
    def maximum_components(self) -> int:
        return self._approximation.maximum_rank

    def data(self) -> np.ndarray:
        return self._data.copy()

    def mean(self) -> np.ndarray:
        return self._mean.copy()

    def centered_data(self) -> np.ndarray:
        return self._centered.copy()

    def gram_matrix(self) -> np.ndarray:
        return self._centered.T @ self._centered

    def covariance_matrix(self) -> np.ndarray:
        return self.gram_matrix() / (self.shape[0] - 1)

    def singular_values(self) -> np.ndarray:
        return np.sqrt(self._eigenvalues)

    def principal_directions(self) -> np.ndarray:
        return self._directions.copy()

    def scores(self, components: int) -> np.ndarray:
        count = self._component_count(components)
        return self._centered @ self._directions[:, :count]

    def centered_reconstruction(self, components: int) -> np.ndarray:
        count = self._component_count(components)
        if count == 0:
            return np.zeros_like(self._centered)
        directions = self._directions[:, :count]
        return self.scores(count) @ directions.T

    def reconstruction(self, components: int) -> np.ndarray:
        return self.centered_reconstruction(components) + self._mean

    def residual(self, components: int) -> np.ndarray:
        return self._data - self.reconstruction(components)

    def frobenius_error(self, components: int) -> float:
        return float(np.linalg.norm(self.residual(components), ord="fro"))

    def relative_frobenius_error(self, components: int) -> float:
        return float(
            self.frobenius_error(components) / np.linalg.norm(self._centered, ord="fro")
        )

    def explained_variance(self) -> np.ndarray:
        return self._eigenvalues / (self.shape[0] - 1)

    def explained_variance_ratio(self, components: int) -> float:
        count = self._component_count(components)
        return float(np.sum(self._eigenvalues[:count]) / np.sum(self._eigenvalues))

    def _component_count(self, components: int) -> int:
        if not isinstance(components, Integral) or isinstance(components, bool):
            raise ValueError("components must be an integer")
        count = int(components)
        if count < 0 or count > self.maximum_components:
            raise ValueError(
                f"components must lie between 0 and {self.maximum_components}"
            )
        return count

    def _canonicalize_direction_signs(self) -> None:
        for index in range(self._directions.shape[1]):
            direction = self._directions[:, index]
            pivot = int(np.argmax(np.abs(direction)))
            if direction[pivot] < 0:
                self._directions[:, index] *= -1
