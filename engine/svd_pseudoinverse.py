"""Renderer-independent pseudoinverse model built from a full SVD."""

from __future__ import annotations

import numpy as np

from engine.svd_fundamental_subspaces import SVDFundamentalSubspaces


class SVDPseudoinverse:
    """Reverse the positive singular direction of a rank-one 3-by-2 map."""

    def __init__(self, matrix=None, *, tolerance: float | None = None) -> None:
        self._structure = SVDFundamentalSubspaces(matrix, tolerance=tolerance)

    @property
    def matrix(self) -> np.ndarray:
        return self._structure.matrix

    def singular_values(self) -> np.ndarray:
        return self._structure.singular_values()

    def reciprocal_singular_values(self) -> np.ndarray:
        values = self.singular_values()
        result = np.zeros_like(values)
        positive = values > 1e-12
        result[positive] = 1.0 / values[positive]
        return result

    def sigma_pseudoinverse(self) -> np.ndarray:
        result = np.zeros((2, 3))
        result[0, 0] = self.reciprocal_singular_values()[0]
        return result

    def pseudoinverse(self) -> np.ndarray:
        u = self._structure.full_u()
        v = self._structure.full_v()
        return v @ self.sigma_pseudoinverse() @ u.T

    def apply(self, vector) -> np.ndarray:
        candidate = self._domain_vector(vector)
        return self.matrix @ candidate

    def apply_pseudoinverse(self, vector) -> np.ndarray:
        candidate = self._output_vector(vector)
        return self.pseudoinverse() @ candidate

    def domain_round_trip(self, vector) -> np.ndarray:
        candidate = self._domain_vector(vector)
        return self.pseudoinverse() @ self.matrix @ candidate

    def output_round_trip(self, vector) -> np.ndarray:
        candidate = self._output_vector(vector)
        return self.matrix @ self.pseudoinverse() @ candidate

    def row_projection(self) -> np.ndarray:
        return self.pseudoinverse() @ self.matrix

    def column_projection(self) -> np.ndarray:
        return self.matrix @ self.pseudoinverse()

    def active_right_direction(self) -> np.ndarray:
        return self._structure.row_basis()[:, 0]

    def null_direction(self) -> np.ndarray:
        return self._structure.null_basis()[:, 0]

    def active_left_direction(self) -> np.ndarray:
        return self._structure.column_basis()[:, 0]

    @staticmethod
    def _domain_vector(vector) -> np.ndarray:
        candidate = np.asarray(vector, dtype=float)
        if candidate.ndim != 1 or candidate.shape != (2,):
            raise ValueError("domain vector must have exactly two components")
        if not np.all(np.isfinite(candidate)):
            raise ValueError("domain vector entries must be finite")
        return candidate

    @staticmethod
    def _output_vector(vector) -> np.ndarray:
        candidate = np.asarray(vector, dtype=float)
        if candidate.ndim != 1 or candidate.shape != (3,):
            raise ValueError("output vector must have exactly three components")
        if not np.all(np.isfinite(candidate)):
            raise ValueError("output vector entries must be finite")
        return candidate
