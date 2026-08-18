"""Renderer-independent mathematics for Chapter 7 lesson 3: eigenspaces.

Checkpoint 170.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class EigenspaceObservation:
    """An eigenvalue together with its null-space direction in R^2."""

    eigenvalue: float
    generator: np.ndarray
    shifted_matrix: np.ndarray


class EigenspacesLesson:
    """Mathematical model linking eigenvector families to null spaces."""

    def __init__(self, matrix: Iterable[Iterable[float]], *, tolerance: float = 1e-9) -> None:
        array = np.asarray(matrix, dtype=float)
        if array.shape != (2, 2):
            raise ValueError("matrix must have shape (2, 2)")
        if not np.isfinite(array).all():
            raise ValueError("matrix entries must be finite")
        if not np.isfinite(tolerance) or tolerance <= 0:
            raise ValueError("tolerance must be finite and positive")
        self._matrix = array.copy()
        self._tolerance = float(tolerance)

    @property
    def matrix(self) -> np.ndarray:
        return self._matrix.copy()

    def transform(self, vector: Iterable[float]) -> np.ndarray:
        candidate = np.asarray(vector, dtype=float)
        if candidate.shape != (2,):
            raise ValueError("vector must have shape (2,)")
        return self._matrix @ candidate

    def scalar_multiple_observation(self, generator: Iterable[float], scalar: float) -> tuple[np.ndarray, np.ndarray, float]:
        vector = np.asarray(generator, dtype=float)
        if vector.shape != (2,) or np.linalg.norm(vector) <= self._tolerance:
            raise ValueError("generator must be a nonzero vector in R^2")
        if not np.isfinite(scalar) or scalar == 0:
            raise ValueError("scalar must be finite and nonzero")
        image = self._matrix @ vector
        eigenvalue = float((vector @ image) / (vector @ vector))
        if np.linalg.norm(image - eigenvalue * vector) > self._tolerance * max(1.0, np.linalg.norm(image)):
            raise ValueError("generator is not an eigenvector")
        multiple = float(scalar) * vector
        return multiple, self._matrix @ multiple, eigenvalue

    def shifted_matrix(self, eigenvalue: float) -> np.ndarray:
        if not np.isfinite(eigenvalue):
            raise ValueError("eigenvalue must be finite")
        return self._matrix - float(eigenvalue) * np.eye(2)

    def eigenspace(self, eigenvalue: float) -> EigenspaceObservation:
        shifted = self.shifted_matrix(eigenvalue)
        _, singular_values, vh = np.linalg.svd(shifted)
        if singular_values[-1] > self._tolerance * max(1.0, singular_values[0]):
            raise ValueError("A - lambda I has trivial null space")
        generator = vh[-1].copy()
        generator /= np.linalg.norm(generator)
        # Stabilize sign for deterministic presentation/tests.
        first_nonzero = next((value for value in generator if abs(value) > self._tolerance), 1.0)
        if first_nonzero < 0:
            generator *= -1
        return EigenspaceObservation(float(eigenvalue), generator, shifted.copy())


DEFAULT_MATRIX = np.array([[5.0, 3.0], [3.0, 5.0]])
SLOW_EIGENVALUE = 2.0
FAST_EIGENVALUE = 8.0
SLOW_GENERATOR = np.array([1.0, -1.0])
FAST_GENERATOR = np.array([1.0, 1.0])
SCALAR_MULTIPLES = (-1.5, 0.7, 1.4)
