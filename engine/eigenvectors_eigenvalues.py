"""Renderer-independent mathematics for Chapter 7 lesson 2.

Checkpoint 169: Eigenvectors and Eigenvalues.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class EigenpairObservation:
    """A nonzero vector, its image, and the scalar relating them."""

    vector: np.ndarray
    image: np.ndarray
    eigenvalue: float


class EigenvectorsEigenvaluesLesson:
    """Mathematical model for introducing ``A v = lambda v`` geometrically."""

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
        candidate = self._validated_nonzero_vector(vector)
        return self._matrix @ candidate

    def eigenpair(self, vector: Iterable[float]) -> EigenpairObservation:
        candidate = self._validated_nonzero_vector(vector)
        image = self._matrix @ candidate
        denominator = float(candidate @ candidate)
        eigenvalue = float((candidate @ image) / denominator)
        residual = image - eigenvalue * candidate
        if np.linalg.norm(residual) > self._tolerance * max(1.0, np.linalg.norm(image)):
            raise ValueError("vector is not an eigenvector of this matrix")
        return EigenpairObservation(candidate.copy(), image.copy(), eigenvalue)

    def _validated_nonzero_vector(self, vector: Iterable[float]) -> np.ndarray:
        candidate = np.asarray(vector, dtype=float)
        if candidate.shape != (2,):
            raise ValueError("vector must have shape (2,)")
        if not np.isfinite(candidate).all():
            raise ValueError("vector entries must be finite")
        if np.linalg.norm(candidate) <= self._tolerance:
            raise ValueError("eigenvectors must be nonzero")
        return candidate


# Continue directly from CP168's stronger symmetric transformation.
DEFAULT_MATRIX = np.array([[5.0, 3.0], [3.0, 5.0]])
EIGENVECTOR_FAST = np.array([1.0, 1.0])   # lambda = 8
EIGENVECTOR_SLOW = np.array([1.0, -1.0])  # lambda = 2

# Scalar-only cases used to clarify what lambda means once the defining
# equation has been established.  These are conceptual cases, not all
# eigenvalues of DEFAULT_MATRIX.
LAMBDA_CASES = (
    ("stretch", 2.0),
    ("shrink", 0.5),
    ("reverse", -1.0),
    ("fixed", 1.0),
    ("collapse", 0.0),
)
