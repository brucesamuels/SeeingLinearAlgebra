"""Renderer-independent mathematics for the geometric subspace test."""
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


def _vector(values: ArrayLike, name: str) -> FloatArray:
    vector = np.asarray(values, dtype=float)
    if vector.shape != (3,) or not np.all(np.isfinite(vector)):
        raise ValueError(f"{name} must be a finite 3D vector")
    return _readonly(vector)


def _scalar(value: Real, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be real")
    number = float(value)
    if not np.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


@dataclass(frozen=True)
class SubspaceTestSnapshot:
    offset: FloatArray
    point_u: FloatArray
    point_v: FloatArray
    sum_point: FloatArray
    scaled_point: FloatArray
    contains_origin: bool
    closed_under_addition: bool
    closed_under_scaling: bool

    @property
    def is_subspace(self) -> bool:
        return self.contains_origin and self.closed_under_addition and self.closed_under_scaling


class SubspaceTest:
    """Compare a plane through the origin with a parallel shifted plane."""

    def __init__(
        self,
        direction_u: ArrayLike = (1.8, 0.4, 0.0),
        direction_v: ArrayLike = (-0.5, 1.5, 0.0),
        shifted_offset: ArrayLike = (0.0, 0.0, 1.2),
    ) -> None:
        self._u = _vector(direction_u, "direction_u")
        self._v = _vector(direction_v, "direction_v")
        self._shift = _vector(shifted_offset, "shifted_offset")
        if np.linalg.matrix_rank(np.column_stack((self._u, self._v))) != 2:
            raise ValueError("direction_u and direction_v must be independent")
        normal = np.cross(self._u, self._v)
        if abs(float(np.dot(normal, self._shift))) < 1e-9:
            raise ValueError("shifted_offset must move the plane off itself")
        self._normal = _readonly(normal)

    def through_origin(self, scale: Real = 1.7) -> SubspaceTestSnapshot:
        return self._snapshot(np.zeros(3), _scalar(scale, "scale"))

    def shifted(self, scale: Real = 1.7) -> SubspaceTestSnapshot:
        return self._snapshot(self._shift, _scalar(scale, "scale"))

    def _snapshot(self, offset: FloatArray, scale: float) -> SubspaceTestSnapshot:
        point_u = offset + self._u
        point_v = offset + self._v
        sum_point = point_u + point_v
        scaled_point = scale * point_u
        contains_origin = self._on_plane(np.zeros(3), offset)
        closed_under_addition = self._on_plane(sum_point, offset)
        closed_under_scaling = self._on_plane(scaled_point, offset)
        return SubspaceTestSnapshot(
            offset=_readonly(offset),
            point_u=_readonly(point_u),
            point_v=_readonly(point_v),
            sum_point=_readonly(sum_point),
            scaled_point=_readonly(scaled_point),
            contains_origin=contains_origin,
            closed_under_addition=closed_under_addition,
            closed_under_scaling=closed_under_scaling,
        )

    def plane_corners(self, offset: ArrayLike, extent: Real = 2.5) -> FloatArray:
        offset_vector = _vector(offset, "offset")
        amount = _scalar(extent, "extent")
        if amount <= 0:
            raise ValueError("extent must be positive")
        u = self._u / np.linalg.norm(self._u)
        v = self._v - np.dot(self._v, u) * u
        v = v / np.linalg.norm(v)
        corners = np.array([
            offset_vector - amount * u - amount * v,
            offset_vector + amount * u - amount * v,
            offset_vector + amount * u + amount * v,
            offset_vector - amount * u + amount * v,
        ])
        return _readonly(corners)

    def _on_plane(self, point: FloatArray, offset: FloatArray) -> bool:
        return bool(abs(float(np.dot(self._normal, point - offset))) < 1e-9)
