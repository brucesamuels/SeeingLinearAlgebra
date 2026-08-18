"""Renderer-independent mathematics for Chapter 7 lesson 1.

Checkpoint 168: Why Eigenvectors? -- Special Directions of a Transformation.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class DirectionObservation:
    """One vector together with its image under a linear transformation."""

    vector: np.ndarray
    image: np.ndarray
    preserves_line: bool
    scale_factor: float | None


class SpecialDirectionsLesson:
    """Small mathematical model used by the opening eigenvector lesson.

    The model intentionally asks only whether a nonzero vector and its image
    lie on the same line. It does not introduce characteristic polynomials,
    determinants, or eigenvalue computation; those belong to later lessons.
    """

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
    def tolerance(self) -> float:
        return self._tolerance

    def transform(self, vector: Iterable[float]) -> np.ndarray:
        candidate = np.asarray(vector, dtype=float)
        if candidate.shape != (2,):
            raise ValueError("vector must have shape (2,)")
        if not np.isfinite(candidate).all():
            raise ValueError("vector entries must be finite")
        return self._matrix @ candidate

    def observe(self, vector: Iterable[float]) -> DirectionObservation:
        candidate = np.asarray(vector, dtype=float)
        if candidate.shape != (2,):
            raise ValueError("vector must have shape (2,)")
        if not np.isfinite(candidate).all():
            raise ValueError("vector entries must be finite")
        if np.linalg.norm(candidate) <= self._tolerance:
            raise ValueError("the zero vector has no direction to test")

        image = self._matrix @ candidate
        cross = candidate[0] * image[1] - candidate[1] * image[0]
        preserves_line = abs(cross) <= self._tolerance * max(
            1.0, np.linalg.norm(candidate) * np.linalg.norm(image)
        )

        scale_factor: float | None = None
        if preserves_line:
            denominator = float(candidate @ candidate)
            scale_factor = float((candidate @ image) / denominator)

        return DirectionObservation(
            vector=candidate.copy(),
            image=image.copy(),
            preserves_line=preserves_line,
            scale_factor=scale_factor,
        )


# Act I: a quarter-turn rotation. Over the real plane, every nonzero vector is
# carried to a perpendicular line, so there are no real invariant directions.
ROTATION_MATRIX = np.array([[0.0, -1.0], [1.0, 0.0]])

# Act II: a symmetric transformation with two clean invariant directions.
DEFAULT_MATRIX = np.array([[5.0, 3.0], [3.0, 5.0]])

SAMPLE_VECTORS = (
    np.array([1.0, 0.0]),
    np.array([0.0, 1.0]),
    np.array([1.0, -0.4]),
    np.array([-0.7, 1.0]),
    np.array([0.7, 0.7]),
    np.array([1.0, -1.0]),
)
