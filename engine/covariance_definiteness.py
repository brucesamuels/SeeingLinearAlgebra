"""Renderer-independent model for covariance and positive semidefiniteness."""
from __future__ import annotations

import numpy as np


class CovarianceDefiniteness:
    """Center observations and interpret covariance as a scaled Gram matrix."""

    DEFAULT_OBSERVATIONS = np.array(
        [[1.0, 1.0], [3.0, 1.0], [3.0, 3.0], [5.0, 3.0]]
    )

    def __init__(self, observations=None):
        value = self.DEFAULT_OBSERVATIONS if observations is None else observations
        self.observations = self._observations(value)

    @staticmethod
    def _observations(value):
        observations = np.asarray(value, dtype=float)
        if observations.ndim != 2 or min(observations.shape) == 0:
            raise ValueError("observations must be a nonempty two-dimensional array")
        if not np.all(np.isfinite(observations)):
            raise ValueError("observation coordinates must be finite")
        return observations

    def _direction(self, value):
        direction = np.asarray(value, dtype=float)
        if direction.shape != (self.observations.shape[1],):
            raise ValueError(
                f"direction must have length {self.observations.shape[1]}"
            )
        if not np.all(np.isfinite(direction)):
            raise ValueError("direction entries must be finite")
        return direction

    @property
    def observation_count(self):
        return self.observations.shape[0]

    @property
    def feature_count(self):
        return self.observations.shape[1]

    def mean(self):
        return self.observations.mean(axis=0)

    def centered_matrix(self):
        return self.observations - self.mean()

    def population_covariance(self):
        centered = self.centered_matrix()
        return centered.T @ centered / self.observation_count

    def sample_covariance(self):
        if self.observation_count < 2:
            raise ValueError("sample covariance requires at least two observations")
        centered = self.centered_matrix()
        return centered.T @ centered / (self.observation_count - 1)

    def centered_projections(self, direction):
        return self.centered_matrix() @ self._direction(direction)

    def directional_variance(self, direction):
        v = self._direction(direction)
        return float(v @ self.population_covariance() @ v)

    def squared_projection_mean(self, direction):
        projections = self.centered_projections(direction)
        return float(projections @ projections / self.observation_count)

    def covariance_is_positive_semidefinite(self, tolerance=1e-10):
        if not np.isfinite(tolerance) or tolerance < 0:
            raise ValueError("tolerance must be finite and nonnegative")
        return bool(
            np.all(np.linalg.eigvalsh(self.population_covariance()) >= -tolerance)
        )

    def covariance_is_positive_definite(self):
        return np.linalg.matrix_rank(self.centered_matrix()) == self.feature_count
