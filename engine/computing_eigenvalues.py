"""Renderer-independent mathematics for Chapter 7 lesson 5: computing eigenvalues.

Checkpoint 172.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class EigenvalueComputationData:
    matrix: np.ndarray
    characteristic_coefficients: np.ndarray
    eigenvalues: np.ndarray


class EigenvalueComputationLesson:
    """Mathematical model for a hand-solvable 3x3 eigenvalue example."""

    def __init__(self, matrix: Iterable[Iterable[float]], *, tolerance: float = 1e-9) -> None:
        array = np.asarray(matrix, dtype=float)
        if array.shape != (3, 3):
            raise ValueError("matrix must have shape (3, 3)")
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
        return np.eye(3)

    def shifted_matrix(self, candidate: float) -> np.ndarray:
        if not np.isfinite(candidate):
            raise ValueError("candidate must be finite")
        return self._matrix - float(candidate) * self.identity

    def characteristic_coefficients(self) -> np.ndarray:
        """Return coefficients of det(lambda I - A)."""
        return np.poly(self._matrix)

    def eigenvalues(self) -> np.ndarray:
        roots = np.linalg.eigvals(self._matrix)
        if np.max(np.abs(roots.imag)) <= self._tolerance:
            roots = roots.real
        return np.sort(roots)

    def data(self) -> EigenvalueComputationData:
        return EigenvalueComputationData(
            matrix=self.matrix,
            characteristic_coefficients=self.characteristic_coefficients().copy(),
            eigenvalues=self.eigenvalues().copy(),
        )


DEFAULT_MATRIX = np.array(
    [
        [4.0, 1.0, 0.0],
        [2.0, 3.0, 0.0],
        [0.0, 0.0, 1.0],
    ]
)
EXPECTED_EIGENVALUES = np.array([1.0, 2.0, 5.0])
