"""Renderer-independent SVD organization of the four fundamental subspaces."""

from __future__ import annotations

import numpy as np

from engine.rank_collapse import RankCollapse


class SVDFundamentalSubspaces:
    """Describe a nonzero rank-one 3-by-2 matrix through its full SVD bases."""

    DEFAULT_MATRIX = np.array([[1.0, 1.0], [1.0, 1.0], [0.0, 0.0]])

    def __init__(self, matrix=None, *, tolerance: float | None = None) -> None:
        value = self.DEFAULT_MATRIX if matrix is None else matrix
        array = np.asarray(value, dtype=float)
        if array.ndim != 2 or array.shape != (3, 2):
            raise ValueError("matrix must be two-dimensional with shape 3-by-2")
        if not np.all(np.isfinite(array)):
            raise ValueError("matrix entries must be finite")

        collapse = RankCollapse(array, target_rank=0, tolerance=tolerance)
        if collapse.initial_rank != 1:
            raise ValueError("matrix must be nonzero and rank one")

        self._matrix = np.array(array, copy=True)
        self._collapse = collapse

    @staticmethod
    def _canonical(vector) -> np.ndarray:
        result = np.asarray(vector, dtype=float).copy()
        nonzero = np.flatnonzero(np.abs(result) > 1e-12)
        if nonzero.size and result[nonzero[0]] < 0:
            result *= -1
        return result

    @property
    def matrix(self) -> np.ndarray:
        return self._matrix.copy()

    @property
    def domain_dimension(self) -> int:
        return 2

    @property
    def codomain_dimension(self) -> int:
        return 3

    def singular_values(self) -> np.ndarray:
        return self._collapse.singular_values_at(0.0)

    def rank(self) -> int:
        return self._collapse.rank_at(0.0)

    def nullity(self) -> int:
        return self.domain_dimension - self.rank()

    def left_nullity(self) -> int:
        return self.codomain_dimension - self.rank()

    def row_basis(self) -> np.ndarray:
        basis = self._collapse.row_space_basis(0.0)
        return self._canonical(basis[0]).reshape(2, 1)

    def null_basis(self) -> np.ndarray:
        basis = self._collapse.kernel_basis(0.0)
        return self._canonical(basis[:, 0]).reshape(2, 1)

    def column_basis(self) -> np.ndarray:
        right = self.row_basis()[:, 0]
        mapped = self._matrix @ right
        return (mapped / np.linalg.norm(mapped)).reshape(3, 1)

    def left_null_basis(self) -> np.ndarray:
        active = self.column_basis()[:, 0]
        selected: list[np.ndarray] = []
        for standard in np.eye(3):
            candidate = standard - np.dot(standard, active) * active
            for previous in selected:
                candidate -= np.dot(candidate, previous) * previous
            norm = float(np.linalg.norm(candidate))
            if norm > 1e-10:
                selected.append(self._canonical(candidate / norm))
            if len(selected) == 2:
                break
        return np.column_stack(selected)

    def full_v(self) -> np.ndarray:
        return np.column_stack((self.row_basis()[:, 0], self.null_basis()[:, 0]))

    def full_u(self) -> np.ndarray:
        return np.column_stack((self.column_basis()[:, 0], self.left_null_basis()))

    def full_sigma(self) -> np.ndarray:
        result = np.zeros((3, 2))
        result[0, 0] = self.singular_values()[0]
        return result

    def full_factorization(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        return self.full_u(), self.full_sigma(), self.full_v().T

    def reconstruction(self) -> np.ndarray:
        u, sigma, vt = self.full_factorization()
        return u @ sigma @ vt

    def apply(self, vector) -> np.ndarray:
        candidate = np.asarray(vector, dtype=float)
        if candidate.ndim != 1 or candidate.shape != (2,):
            raise ValueError("vector must have exactly two components")
        if not np.all(np.isfinite(candidate)):
            raise ValueError("vector entries must be finite")
        return self._matrix @ candidate

    def domain_coordinates(self, vector) -> np.ndarray:
        candidate = self._domain_vector(vector)
        return self.full_v().T @ candidate

    def domain_decomposition(self, vector) -> tuple[np.ndarray, np.ndarray]:
        coefficients = self.domain_coordinates(vector)
        row_part = coefficients[0] * self.row_basis()[:, 0]
        null_part = coefficients[1] * self.null_basis()[:, 0]
        return row_part, null_part

    def output_decomposition(self, vector) -> tuple[np.ndarray, np.ndarray]:
        candidate = np.asarray(vector, dtype=float)
        if candidate.ndim != 1 or candidate.shape != (3,):
            raise ValueError("output vector must have exactly three components")
        if not np.all(np.isfinite(candidate)):
            raise ValueError("output vector entries must be finite")
        column = self.column_basis()
        left_null = self.left_null_basis()
        column_part = column @ (column.T @ candidate)
        left_null_part = left_null @ (left_null.T @ candidate)
        return column_part, left_null_part

    def _domain_vector(self, vector) -> np.ndarray:
        candidate = np.asarray(vector, dtype=float)
        if candidate.ndim != 1 or candidate.shape != (2,):
            raise ValueError("vector must have exactly two components")
        if not np.all(np.isfinite(candidate)):
            raise ValueError("vector entries must be finite")
        return candidate
