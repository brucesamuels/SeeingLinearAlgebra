"""Renderer-independent mathematics for CP180: dynamics and the dominant eigenvector."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

A = np.array([[3.0, 1.0], [1.0, 3.0]])
Q = (1 / np.sqrt(2)) * np.array([[1.0, 1.0], [1.0, -1.0]])
EIGENVALUES = np.array([4.0, 2.0])
D = np.diag(EIGENVALUES)


@dataclass(frozen=True)
class DominantEigenvectorExample:
    vector: np.ndarray
    eigen_coordinates: np.ndarray


class DominantEigenvectorLesson:
    @property
    def matrix(self) -> np.ndarray:
        return A.copy()

    @property
    def eigenvectors(self) -> np.ndarray:
        return Q.copy()

    @property
    def eigenvalues(self) -> np.ndarray:
        return EIGENVALUES.copy()

    def example(self) -> DominantEigenvectorExample:
        coords = np.array([1.0, 1.0])
        return DominantEigenvectorExample(vector=Q @ coords, eigen_coordinates=coords)

    def power_on_example(self, k: int) -> np.ndarray:
        if k < 0:
            raise ValueError("k must be nonnegative")
        ex = self.example()
        return Q @ ((EIGENVALUES ** k) * ex.eigen_coordinates)

    def normalized_power_direction(self, k: int) -> np.ndarray:
        v = self.power_on_example(k)
        return v / np.linalg.norm(v)

    def dominant_direction(self) -> np.ndarray:
        return Q[:, 0].copy()
