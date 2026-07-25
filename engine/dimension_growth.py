"""Renderer-independent mathematics for line, plane, and space generation."""
from __future__ import annotations

from dataclasses import dataclass
from numbers import Real
import numpy as np
from numpy.typing import ArrayLike, NDArray

FloatArray = NDArray[np.float64]


def _readonly(values: ArrayLike) -> FloatArray:
    array = np.asarray(values, dtype=float).copy()
    array.setflags(write=False)
    return array


def _finite_vector(values: ArrayLike, *, name: str) -> FloatArray:
    vector = np.asarray(values, dtype=float)
    if vector.shape != (3,):
        raise ValueError(f"{name} must be a 3D vector")
    if not np.all(np.isfinite(vector)):
        raise ValueError(f"{name} must contain finite coordinates")
    if np.linalg.norm(vector) == 0:
        raise ValueError(f"{name} must be nonzero")
    return _readonly(vector)


def _real(value: Real, *, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be real")
    number = float(value)
    if not np.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


@dataclass(frozen=True)
class DimensionGrowthSnapshot:
    generator_u: FloatArray
    generator_v: FloatArray
    generator_w: FloatArray
    plane_corners: FloatArray
    translated_plane_corners: FloatArray
    translation_coefficient: float
    rank_uv: int
    rank_uvw: int
    volume: float


class DimensionGrowth:
    """Describe how one, two, and three independent 3D generators grow span."""

    def __init__(self, generator_u: ArrayLike, generator_v: ArrayLike, generator_w: ArrayLike) -> None:
        self._u = _finite_vector(generator_u, name="generator_u")
        self._v = _finite_vector(generator_v, name="generator_v")
        self._w = _finite_vector(generator_w, name="generator_w")

        uv = np.column_stack((self._u, self._v))
        uvw = np.column_stack((self._u, self._v, self._w))
        if np.linalg.matrix_rank(uv) != 2:
            raise ValueError("generator_u and generator_v must be independent")
        if np.linalg.matrix_rank(uvw) != 3:
            raise ValueError("generator_w must lie outside span{u, v}")

    @property
    def generator_u(self) -> FloatArray:
        return self._u

    @property
    def generator_v(self) -> FloatArray:
        return self._v

    @property
    def generator_w(self) -> FloatArray:
        return self._w

    def snapshot(self, translation_coefficient: Real, *, plane_extent: Real = 2.25) -> DimensionGrowthSnapshot:
        c = _real(translation_coefficient, name="translation_coefficient")
        extent = _real(plane_extent, name="plane_extent")
        if extent <= 0:
            raise ValueError("plane_extent must be positive")

        plane_corners = np.array(
            [
                -extent * self._u - extent * self._v,
                extent * self._u - extent * self._v,
                extent * self._u + extent * self._v,
                -extent * self._u + extent * self._v,
            ],
            dtype=float,
        )
        translated = plane_corners + c * self._w
        volume = abs(float(np.linalg.det(np.column_stack((self._u, self._v, self._w)))))
        return DimensionGrowthSnapshot(
            generator_u=_readonly(self._u),
            generator_v=_readonly(self._v),
            generator_w=_readonly(self._w),
            plane_corners=_readonly(plane_corners),
            translated_plane_corners=_readonly(translated),
            translation_coefficient=c,
            rank_uv=2,
            rank_uvw=3,
            volume=volume,
        )

    def line_points(self, coefficients: ArrayLike) -> FloatArray:
        values = np.asarray(coefficients, dtype=float)
        if values.ndim != 1 or not np.all(np.isfinite(values)):
            raise ValueError("coefficients must be a finite one-dimensional array")
        return _readonly(values[:, None] * self._u)

    def plane_points(self, coefficient_pairs: ArrayLike) -> FloatArray:
        pairs = np.asarray(coefficient_pairs, dtype=float)
        if pairs.ndim != 2 or pairs.shape[1] != 2 or not np.all(np.isfinite(pairs)):
            raise ValueError("coefficient_pairs must have shape (n, 2) with finite entries")
        return _readonly(pairs[:, :1] * self._u + pairs[:, 1:] * self._v)

    def space_points(self, coefficient_triples: ArrayLike) -> FloatArray:
        triples = np.asarray(coefficient_triples, dtype=float)
        if triples.ndim != 2 or triples.shape[1] != 3 or not np.all(np.isfinite(triples)):
            raise ValueError("coefficient_triples must have shape (n, 3) with finite entries")
        return _readonly(
            triples[:, :1] * self._u
            + triples[:, 1:2] * self._v
            + triples[:, 2:] * self._w
        )
