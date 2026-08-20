"""Renderer-independent mathematics for Chapter 7 lesson 7: an eigenvector basis.

Checkpoint 174.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


DEFAULT_MATRIX = np.array(
    [
        [4.0, 1.0, 0.0],
        [2.0, 3.0, 0.0],
        [0.0, 0.0, 1.0],
    ]
)

EIGENVALUES = np.array([1.0, 2.0, 5.0])
EIGENVECTORS = np.column_stack(
    [
        np.array([0.0, 0.0, 1.0]),
        np.array([1.0, -2.0, 0.0]),
        np.array([1.0, 1.0, 0.0]),
    ]
)


@dataclass(frozen=True)
class EigenbasisExample:
    standard_vector: np.ndarray
    eigen_coordinates: np.ndarray
    transformed_vector: np.ndarray
    transformed_eigen_coordinates: np.ndarray


class EigenvectorBasisLesson:
    """Mathematical model for expressing vectors in an eigenvector basis."""

    def __init__(self, matrix: Iterable[Iterable[float]] = DEFAULT_MATRIX) -> None:
        array = np.asarray(matrix, dtype=float)
        if array.shape != (3, 3):
            raise ValueError("matrix must have shape (3, 3)")
        if not np.isfinite(array).all():
            raise ValueError("matrix entries must be finite")
        self._matrix = array.copy()

    @property
    def matrix(self) -> np.ndarray:
        return self._matrix.copy()

    @property
    def basis_matrix(self) -> np.ndarray:
        return EIGENVECTORS.copy()

    def basis_is_independent(self) -> bool:
        return bool(abs(np.linalg.det(EIGENVECTORS)) > 1e-9)

    def coordinates_in_eigenbasis(self, vector: Iterable[float]) -> np.ndarray:
        v = np.asarray(vector, dtype=float)
        if v.shape != (3,):
            raise ValueError("vector must have shape (3,)")
        return np.linalg.solve(EIGENVECTORS, v)

    def reconstruct_from_eigenbasis(self, coordinates: Iterable[float]) -> np.ndarray:
        c = np.asarray(coordinates, dtype=float)
        if c.shape != (3,):
            raise ValueError("coordinates must have shape (3,)")
        return EIGENVECTORS @ c

    def transform_eigen_coordinates(self, coordinates: Iterable[float]) -> np.ndarray:
        c = np.asarray(coordinates, dtype=float)
        if c.shape != (3,):
            raise ValueError("coordinates must have shape (3,)")
        return EIGENVALUES * c

    def example(self) -> EigenbasisExample:
        coordinates = np.array([1.0, 1.0, 1.0])
        vector = self.reconstruct_from_eigenbasis(coordinates)
        transformed = self._matrix @ vector
        transformed_coordinates = self.transform_eigen_coordinates(coordinates)
        return EigenbasisExample(
            standard_vector=vector,
            eigen_coordinates=coordinates,
            transformed_vector=transformed,
            transformed_eigen_coordinates=transformed_coordinates,
        )
