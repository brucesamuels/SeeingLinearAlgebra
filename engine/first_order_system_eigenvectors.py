"""Renderer-independent mathematics for CP181: first-order systems and eigenvectors."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

A = np.array([[3.0, 1.0], [1.0, 3.0]])
Q = (1 / np.sqrt(2)) * np.array([[1.0, 1.0], [1.0, -1.0]])
EIGENVALUES = np.array([4.0, 2.0])
X0 = np.array([2.0, 0.0])


@dataclass(frozen=True)
class FirstOrderSystemExample:
    initial_vector: np.ndarray
    eigen_coordinates: np.ndarray


class FirstOrderSystemEigenvectorsLesson:
    @property
    def matrix(self) -> np.ndarray:
        return A.copy()

    @property
    def eigenvectors(self) -> np.ndarray:
        return Q.copy()

    @property
    def eigenvalues(self) -> np.ndarray:
        return EIGENVALUES.copy()

    @property
    def initial_vector(self) -> np.ndarray:
        return X0.copy()

    def initial_eigen_coordinates(self) -> np.ndarray:
        return Q.T @ X0

    def example(self) -> FirstOrderSystemExample:
        return FirstOrderSystemExample(
            initial_vector=X0.copy(),
            eigen_coordinates=self.initial_eigen_coordinates(),
        )

    def solution(self, t: float) -> np.ndarray:
        coords = np.exp(EIGENVALUES * t) * self.initial_eigen_coordinates()
        return Q @ coords

    def closed_form_solution(self, t: float) -> np.ndarray:
        return np.array([
            np.exp(4*t) + np.exp(2*t),
            np.exp(4*t) - np.exp(2*t),
        ])

    def normalized_solution_direction(self, t: float) -> np.ndarray:
        x = self.solution(t)
        return x / np.linalg.norm(x)

    def dominant_direction(self) -> np.ndarray:
        return Q[:, 0].copy()
