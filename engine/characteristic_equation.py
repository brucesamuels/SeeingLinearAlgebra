"""Renderer-independent mathematics for Chapter 7 lesson 4: characteristic equation.

Checkpoint 171.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class CharacteristicEquationData:
    """Concrete data for a 2x2 characteristic-equation computation."""

    matrix: np.ndarray
    identity: np.ndarray
    lambda_value: float
    shifted_matrix: np.ndarray
    determinant: float


class CharacteristicEquationLesson:
    """Mathematical model for deriving and computing det(A-lambda I)=0."""

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

    @property
    def identity(self) -> np.ndarray:
        return np.eye(2)

    def shifted_matrix(self, candidate: float) -> np.ndarray:
        if not np.isfinite(candidate):
            raise ValueError("candidate must be finite")
        return self._matrix - float(candidate) * self.identity

    def determinant_at(self, candidate: float) -> float:
        return float(np.linalg.det(self.shifted_matrix(candidate)))

    def is_singular_at(self, candidate: float) -> bool:
        return abs(self.determinant_at(candidate)) <= self._tolerance

    def data_at(self, candidate: float) -> CharacteristicEquationData:
        shifted = self.shifted_matrix(candidate)
        return CharacteristicEquationData(
            matrix=self.matrix,
            identity=self.identity,
            lambda_value=float(candidate),
            shifted_matrix=shifted.copy(),
            determinant=float(np.linalg.det(shifted)),
        )

    def characteristic_coefficients(self) -> np.ndarray:
        """Return coefficients of det(A-lambda I), highest degree first."""
        trace = float(np.trace(self._matrix))
        determinant = float(np.linalg.det(self._matrix))
        return np.array([1.0, -trace, determinant])

    def eigenvalues(self) -> np.ndarray:
        roots = np.roots(self.characteristic_coefficients())
        if np.max(np.abs(roots.imag)) <= self._tolerance:
            roots = roots.real
        return np.sort(roots)


DEFAULT_MATRIX = np.array([[5.0, 3.0], [3.0, 5.0]])
SLOW_EIGENVALUE = 2.0
FAST_EIGENVALUE = 8.0
