"""Renderer-independent mathematics for changing a transformation between bases."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


DEFAULT_P_B = np.array([[1.0, 1.0], [1.0, -1.0]])
DEFAULT_P_C = np.array([[1.0, 2.0], [1.0, 0.0]])
DEFAULT_MATRIX_B = np.array([[2.0, 1.0], [0.0, 3.0]])


@dataclass(frozen=True)
class TwoBasisTransformationExample:
    transition_c_from_b: np.ndarray
    transition_b_from_c: np.ndarray
    matrix_b: np.ndarray
    matrix_c: np.ndarray


class TransformationBetweenBasesLesson:
    """Change both vector coordinates and a transformation matrix directly."""

    def __init__(
        self,
        matrix_b=DEFAULT_MATRIX_B,
        basis_b=DEFAULT_P_B,
        basis_c=DEFAULT_P_C,
    ):
        matrix_b = np.asarray(matrix_b, dtype=float)
        basis_b = np.asarray(basis_b, dtype=float)
        basis_c = np.asarray(basis_c, dtype=float)
        if matrix_b.shape != (2, 2) or basis_b.shape != (2, 2) or basis_c.shape != (2, 2):
            raise ValueError("all matrices must have shape (2, 2)")
        if not all(np.isfinite(item).all() for item in (matrix_b, basis_b, basis_c)):
            raise ValueError("all entries must be finite")
        if abs(float(np.linalg.det(basis_b))) < 1e-12:
            raise ValueError("basis B must be invertible")
        if abs(float(np.linalg.det(basis_c))) < 1e-12:
            raise ValueError("basis C must be invertible")
        self._matrix_b = matrix_b.copy()
        self._basis_b = basis_b.copy()
        self._basis_c = basis_c.copy()

    def transition_c_from_b(self):
        return np.linalg.solve(self._basis_c, self._basis_b)

    def basis_b_coordinates_in_c(self):
        """Columns are [b_1]_C and [b_2]_C, respectively."""
        return self.transition_c_from_b()

    def transition_b_from_c(self):
        return np.linalg.solve(self._basis_b, self._basis_c)

    def transition_reduction_states(self):
        """Gauss-Jordan states for [P_C | P_B] -> [I | Q_(C<-B)]."""
        augmented = np.hstack((self._basis_c, self._basis_b)).astype(float)
        states = [augmented.copy()]
        for pivot_column in range(2):
            pivot_row = pivot_column + int(
                np.argmax(np.abs(augmented[pivot_column:, pivot_column]))
            )
            if abs(float(augmented[pivot_row, pivot_column])) < 1e-12:
                raise ValueError("basis C must be invertible")
            if pivot_row != pivot_column:
                augmented[[pivot_column, pivot_row]] = augmented[[pivot_row, pivot_column]]
                states.append(augmented.copy())
            pivot = augmented[pivot_column, pivot_column]
            if not np.isclose(pivot, 1.0):
                augmented[pivot_column] /= pivot
                states.append(augmented.copy())
            for row in range(2):
                if row == pivot_column:
                    continue
                factor = augmented[row, pivot_column]
                if not np.isclose(factor, 0.0):
                    augmented[row] -= factor * augmented[pivot_column]
                    states.append(augmented.copy())
        return tuple(states)

    def matrix_c(self):
        q = self.transition_c_from_b()
        return q @ self._matrix_b @ np.linalg.inv(q)

    def coordinates_c(self, coordinates_b):
        coordinates_b = np.asarray(coordinates_b, dtype=float)
        if coordinates_b.shape != (2,):
            raise ValueError("coordinates must have shape (2,)")
        return self.transition_c_from_b() @ coordinates_b

    def transform_in_b(self, coordinates_b):
        coordinates_b = np.asarray(coordinates_b, dtype=float)
        if coordinates_b.shape != (2,):
            raise ValueError("coordinates must have shape (2,)")
        return self._matrix_b @ coordinates_b

    def transform_in_c(self, coordinates_c):
        coordinates_c = np.asarray(coordinates_c, dtype=float)
        if coordinates_c.shape != (2,):
            raise ValueError("coordinates must have shape (2,)")
        return self.matrix_c() @ coordinates_c

    def example(self):
        return TwoBasisTransformationExample(
            transition_c_from_b=self.transition_c_from_b(),
            transition_b_from_c=self.transition_b_from_c(),
            matrix_b=self._matrix_b.copy(),
            matrix_c=self.matrix_c(),
        )
