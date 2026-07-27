"""Renderer-independent mathematics for a basis and dimension lesson."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from numpy.typing import ArrayLike, NDArray

FloatArray = NDArray[np.float64]


def _readonly(values: ArrayLike) -> FloatArray:
    array = np.asarray(values, dtype=float).copy()
    array.setflags(write=False)
    return array


def _vector(values: ArrayLike, name: str) -> FloatArray:
    vector = np.asarray(values, dtype=float)
    if vector.shape != (3,) or not np.all(np.isfinite(vector)):
        raise ValueError(f"{name} must be a finite 3-vector")
    if np.linalg.norm(vector) == 0:
        raise ValueError(f"{name} must be nonzero")
    return _readonly(vector)


@dataclass(frozen=True)
class BasisDimensionSnapshot:
    vectors: tuple[FloatArray, FloatArray, FloatArray]
    basis_vectors: tuple[FloatArray, FloatArray]
    endpoints_three: FloatArray
    endpoints_basis: FloatArray
    rank: int
    dimension: int


class BasisDimension:
    """Model a spanning set with one redundant vector."""

    def __init__(
        self,
        vector_1: ArrayLike,
        vector_2: ArrayLike,
        vector_3: ArrayLike,
        coefficient_pairs: ArrayLike,
        coefficient_triples: ArrayLike,
    ) -> None:
        self._v1 = _vector(vector_1, "vector_1")
        self._v2 = _vector(vector_2, "vector_2")
        self._v3 = _vector(vector_3, "vector_3")

        pairs = np.asarray(coefficient_pairs, dtype=float)
        triples = np.asarray(coefficient_triples, dtype=float)
        if pairs.ndim != 2 or pairs.shape[1] != 2 or not np.all(np.isfinite(pairs)):
            raise ValueError("coefficient_pairs must have shape (n, 2)")
        if triples.ndim != 2 or triples.shape[1] != 3 or not np.all(np.isfinite(triples)):
            raise ValueError("coefficient_triples must have shape (n, 3)")
        if np.linalg.matrix_rank(np.column_stack((self._v1, self._v2))) != 2:
            raise ValueError("vector_1 and vector_2 must be independent")
        if np.linalg.matrix_rank(np.column_stack((self._v1, self._v2, self._v3))) != 2:
            raise ValueError("vector_3 must be redundant so the full set has rank 2")

        self._pairs = _readonly(pairs)
        self._triples = _readonly(triples)

    @property
    def vector_1(self) -> FloatArray:
        return self._v1

    @property
    def vector_2(self) -> FloatArray:
        return self._v2

    @property
    def vector_3(self) -> FloatArray:
        return self._v3

    @property
    def basis_vectors(self) -> tuple[FloatArray, FloatArray]:
        return self._v1, self._v2

    def snapshot(self) -> BasisDimensionSnapshot:
        endpoints_three = self.endpoints_from_triples(self._triples)
        endpoints_basis = self.endpoints_from_pairs(self._pairs)
        return BasisDimensionSnapshot(
            vectors=(self._v1, self._v2, self._v3),
            basis_vectors=(self._v1, self._v2),
            endpoints_three=endpoints_three,
            endpoints_basis=endpoints_basis,
            rank=2,
            dimension=2,
        )

    def endpoints_from_pairs(self, pairs: ArrayLike) -> FloatArray:
        coefficients = np.asarray(pairs, dtype=float)
        if coefficients.ndim != 2 or coefficients.shape[1] != 2 or not np.all(np.isfinite(coefficients)):
            raise ValueError("pairs must have shape (n, 2)")
        basis_matrix = np.column_stack((self._v1, self._v2))
        return _readonly(coefficients @ basis_matrix.T)

    def endpoints_from_triples(self, triples: ArrayLike) -> FloatArray:
        coefficients = np.asarray(triples, dtype=float)
        if coefficients.ndim != 2 or coefficients.shape[1] != 3 or not np.all(np.isfinite(coefficients)):
            raise ValueError("triples must have shape (n, 3)")
        full_matrix = np.column_stack((self._v1, self._v2, self._v3))
        return _readonly(coefficients @ full_matrix.T)

    def express_vector_3_in_basis(self) -> FloatArray:
        coefficients, *_ = np.linalg.lstsq(
            np.column_stack((self._v1, self._v2)),
            self._v3,
            rcond=None,
        )
        return _readonly(coefficients)

    def spans_match(self, tolerance: float = 1e-9) -> bool:
        coefficients = self.express_vector_3_in_basis()
        reconstruction = coefficients[0] * self._v1 + coefficients[1] * self._v2
        return bool(np.linalg.norm(reconstruction - self._v3) <= tolerance)
