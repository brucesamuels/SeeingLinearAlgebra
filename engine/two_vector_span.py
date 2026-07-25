"""Renderer-independent mathematics for the span of two vectors.

Checkpoint 69 reveals a two-vector span as a family of parallel affine lines:
for fixed ``a``, varying ``b`` traces ``a*u + b*v``; varying ``a`` then moves
that line through the plane.  This module contains only that mathematics.
"""

from __future__ import annotations

from dataclasses import dataclass
from numbers import Real

import numpy as np
from numpy.typing import ArrayLike, NDArray


FloatArray = NDArray[np.float64]


def _readonly_copy(values: ArrayLike) -> FloatArray:
    array = np.asarray(values, dtype=float).copy()
    array.setflags(write=False)
    return array


def _finite_real(value: Real, *, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number")
    result = float(value)
    if not np.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


@dataclass(frozen=True)
class TwoVectorSpanSnapshot:
    """One exact linear combination ``a*u + b*v``."""

    coefficient_u: float
    coefficient_v: float
    generator_u: FloatArray
    generator_v: FloatArray
    term_u: FloatArray
    term_v: FloatArray
    endpoint: FloatArray

    @property
    def dimension(self) -> int:
        return int(self.generator_u.size)


@dataclass(frozen=True)
class FixedCoefficientLineSnapshot:
    """A finite displayed segment of ``a*u + b*v`` for fixed ``a``."""

    coefficient_u: float
    coefficient_v_min: float
    coefficient_v_max: float
    start: FloatArray
    end: FloatArray
    anchor: FloatArray
    direction: FloatArray


class TwoVectorSpan:
    """Compute two-generator linear combinations in any finite dimension."""

    def __init__(self, generator_u: ArrayLike, generator_v: ArrayLike) -> None:
        u = np.asarray(generator_u, dtype=float)
        v = np.asarray(generator_v, dtype=float)
        for name, vector in (("generator_u", u), ("generator_v", v)):
            if vector.ndim != 1:
                raise ValueError(f"{name} must be one-dimensional")
            if vector.size == 0:
                raise ValueError(f"{name} must contain at least one coordinate")
            if not np.all(np.isfinite(vector)):
                raise ValueError(f"{name} coordinates must be finite")
        if u.shape != v.shape:
            raise ValueError("generators must have the same dimension")
        self._u = _readonly_copy(u)
        self._v = _readonly_copy(v)

    @property
    def generator_u(self) -> FloatArray:
        return _readonly_copy(self._u)

    @property
    def generator_v(self) -> FloatArray:
        return _readonly_copy(self._v)

    @property
    def dimension(self) -> int:
        return int(self._u.size)

    @property
    def rank(self) -> int:
        matrix = np.column_stack((self._u, self._v))
        return int(np.linalg.matrix_rank(matrix, tol=1.0e-12))

    @property
    def generators_are_independent(self) -> bool:
        return self.rank == 2

    def snapshot(self, coefficient_u: Real, coefficient_v: Real) -> TwoVectorSpanSnapshot:
        a = _finite_real(coefficient_u, name="coefficient_u")
        b = _finite_real(coefficient_v, name="coefficient_v")
        term_u = a * self._u
        term_v = b * self._v
        endpoint = term_u + term_v
        return TwoVectorSpanSnapshot(
            coefficient_u=a,
            coefficient_v=b,
            generator_u=_readonly_copy(self._u),
            generator_v=_readonly_copy(self._v),
            term_u=_readonly_copy(term_u),
            term_v=_readonly_copy(term_v),
            endpoint=_readonly_copy(endpoint),
        )

    def fixed_u_line(
        self,
        coefficient_u: Real,
        coefficient_v_min: Real,
        coefficient_v_max: Real,
    ) -> FixedCoefficientLineSnapshot:
        """Return a displayed segment of the line obtained by varying ``b``."""

        a = _finite_real(coefficient_u, name="coefficient_u")
        b_min = _finite_real(coefficient_v_min, name="coefficient_v_min")
        b_max = _finite_real(coefficient_v_max, name="coefficient_v_max")
        if b_min >= b_max:
            raise ValueError("coefficient_v_min must be less than coefficient_v_max")
        anchor = a * self._u
        start = anchor + b_min * self._v
        end = anchor + b_max * self._v
        return FixedCoefficientLineSnapshot(
            coefficient_u=a,
            coefficient_v_min=b_min,
            coefficient_v_max=b_max,
            start=_readonly_copy(start),
            end=_readonly_copy(end),
            anchor=_readonly_copy(anchor),
            direction=_readonly_copy(self._v),
        )

    def endpoints_for(self, coefficient_pairs: ArrayLike) -> FloatArray:
        pairs = np.asarray(coefficient_pairs, dtype=float)
        if pairs.ndim != 2 or pairs.shape[1] != 2:
            raise ValueError("coefficient_pairs must have shape (n, 2)")
        if not np.all(np.isfinite(pairs)):
            raise ValueError("coefficient pairs must be finite")
        endpoints = pairs[:, :1] * self._u + pairs[:, 1:] * self._v
        return _readonly_copy(endpoints)
