"""Renderer-independent linear-combination mathematics.

This module provides the mathematical state that future coefficient-sweep
paths and renderer adapters can consume.  It deliberately contains no Manim
or display-coordinate dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

import numpy as np
from numpy.typing import ArrayLike, NDArray


FloatArray: TypeAlias = NDArray[np.float64]


def _readonly_float_array(values: ArrayLike, *, ndim: int, name: str) -> FloatArray:
    """Return an owned, finite, read-only float array with the requested rank."""

    array = np.array(values, dtype=float, copy=True)
    if array.ndim != ndim:
        raise ValueError(f"{name} must be a {ndim}-dimensional array")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")
    array.setflags(write=False)
    return array


@dataclass(frozen=True, slots=True)
class LinearCombinationSnapshot:
    """Immutable mathematical state of one linear combination.

    Array conventions
    -----------------
    ``coefficients`` has shape ``(vector_count,)``.
    ``terms`` has shape ``(vector_count, dimension)`` and stores
    ``coefficient[i] * vector[i]`` row by row.
    ``partial_sums`` has shape ``(vector_count + 1, dimension)``.  Its first
    row is the origin and its last row is ``result``.
    ``result`` has shape ``(dimension,)``.
    """

    coefficients: FloatArray
    terms: FloatArray
    partial_sums: FloatArray
    result: FloatArray

    def __post_init__(self) -> None:
        coefficients = _readonly_float_array(
            self.coefficients, ndim=1, name="coefficients"
        )
        terms = _readonly_float_array(self.terms, ndim=2, name="terms")
        partial_sums = _readonly_float_array(
            self.partial_sums, ndim=2, name="partial_sums"
        )
        result = _readonly_float_array(self.result, ndim=1, name="result")

        vector_count = coefficients.shape[0]
        if terms.shape[0] != vector_count:
            raise ValueError(
                "terms must contain one row for each coefficient"
            )

        dimension = terms.shape[1]
        if dimension < 1:
            raise ValueError("linear-combination vectors must have dimension at least 1")
        if partial_sums.shape != (vector_count + 1, dimension):
            raise ValueError(
                "partial_sums must have shape "
                "(number of coefficients + 1, vector dimension)"
            )
        if result.shape != (dimension,):
            raise ValueError("result must have the same dimension as each term")

        expected_partial_sums = np.vstack(
            (np.zeros((1, dimension), dtype=float), np.cumsum(terms, axis=0))
        )
        if not np.allclose(partial_sums, expected_partial_sums):
            raise ValueError("partial_sums must be the cumulative sums of terms")
        if not np.allclose(result, partial_sums[-1]):
            raise ValueError("result must equal the final partial sum")

        object.__setattr__(self, "coefficients", coefficients)
        object.__setattr__(self, "terms", terms)
        object.__setattr__(self, "partial_sums", partial_sums)
        object.__setattr__(self, "result", result)

    @property
    def vector_count(self) -> int:
        """Number of scaled vectors represented by the snapshot."""

        return int(self.coefficients.shape[0])

    @property
    def dimension(self) -> int:
        """Ambient mathematical dimension of the vectors."""

        return int(self.result.shape[0])


class LinearCombination:
    """Evaluate linear combinations of a fixed ordered vector family.

    Vectors are stored row by row.  Passing a one-dimensional input is treated
    as a family containing one vector, which keeps the single-vector case
    convenient without weakening validation for larger families.
    """

    def __init__(self, vectors: ArrayLike) -> None:
        array = np.array(vectors, dtype=float, copy=True)
        if array.ndim == 1:
            array = array.reshape(1, -1)
        if array.ndim != 2:
            raise ValueError("vectors must be a one- or two-dimensional array")
        if array.shape[0] < 1:
            raise ValueError("at least one vector is required")
        if array.shape[1] < 1:
            raise ValueError("vectors must have dimension at least 1")
        if not np.all(np.isfinite(array)):
            raise ValueError("vectors must contain only finite values")

        array.setflags(write=False)
        self._vectors = array

    @property
    def vectors(self) -> FloatArray:
        """The fixed ordered vector family as a read-only array."""

        return self._vectors

    @property
    def vector_count(self) -> int:
        """Number of vectors in the family."""

        return int(self._vectors.shape[0])

    @property
    def dimension(self) -> int:
        """Ambient mathematical dimension of each vector."""

        return int(self._vectors.shape[1])

    def snapshot(self, coefficients: ArrayLike) -> LinearCombinationSnapshot:
        """Return the complete mathematical state for ``coefficients``."""

        coefficient_array = np.array(coefficients, dtype=float, copy=True)
        if coefficient_array.ndim == 0 and self.vector_count == 1:
            coefficient_array = coefficient_array.reshape(1)
        if coefficient_array.ndim != 1:
            raise ValueError("coefficients must be a one-dimensional array")
        if coefficient_array.shape[0] != self.vector_count:
            raise ValueError(
                "coefficient count must equal the number of vectors"
            )
        if not np.all(np.isfinite(coefficient_array)):
            raise ValueError("coefficients must contain only finite values")

        terms = coefficient_array[:, np.newaxis] * self._vectors
        partial_sums = np.vstack(
            (
                np.zeros((1, self.dimension), dtype=float),
                np.cumsum(terms, axis=0),
            )
        )
        result = partial_sums[-1]

        return LinearCombinationSnapshot(
            coefficients=coefficient_array,
            terms=terms,
            partial_sums=partial_sums,
            result=result,
        )

    def evaluate(self, coefficients: ArrayLike) -> FloatArray:
        """Return only the resulting vector for ``coefficients``."""

        return self.snapshot(coefficients).result

    def __call__(self, coefficients: ArrayLike) -> FloatArray:
        """Shorthand for :meth:`evaluate`."""

        return self.evaluate(coefficients)
