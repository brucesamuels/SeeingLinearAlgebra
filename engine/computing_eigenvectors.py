"""Renderer-independent mathematics for Chapter 7 lesson 6: computing eigenvectors.

Checkpoint 173.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class EigenvectorCase:
    eigenvalue: float
    shifted_matrix: np.ndarray
    basis_vector: np.ndarray


class EigenvectorComputationLesson:
    """Mathematical model for solving (A-lambda I)v=0 in the CP172 3x3 example."""

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

    def shifted_matrix(self, eigenvalue: float) -> np.ndarray:
        return self._matrix - float(eigenvalue) * np.eye(3)

    def verify_eigenvector(self, eigenvalue: float, vector: Iterable[float]) -> bool:
        v = np.asarray(vector, dtype=float)
        if v.shape != (3,):
            raise ValueError("vector must have shape (3,)")
        if np.linalg.norm(v) <= self._tolerance:
            return False
        return bool(np.linalg.norm(self._matrix @ v - float(eigenvalue) * v) <= self._tolerance)

    def cases(self) -> tuple[EigenvectorCase, ...]:
        raw = (
            (1.0, np.array([0.0, 0.0, 1.0])),
            (2.0, np.array([1.0, -2.0, 0.0])),
            (5.0, np.array([1.0, 1.0, 0.0])),
        )
        return tuple(
            EigenvectorCase(value, self.shifted_matrix(value), basis.copy())
            for value, basis in raw
        )


DEFAULT_MATRIX = np.array(
    [
        [4.0, 1.0, 0.0],
        [2.0, 3.0, 0.0],
        [0.0, 0.0, 1.0],
    ]
)
EXPECTED_EIGENVALUES = np.array([1.0, 2.0, 5.0])
EXPECTED_EIGENVECTORS = {
    1.0: np.array([0.0, 0.0, 1.0]),
    2.0: np.array([1.0, -2.0, 0.0]),
    5.0: np.array([1.0, 1.0, 0.0]),
}
