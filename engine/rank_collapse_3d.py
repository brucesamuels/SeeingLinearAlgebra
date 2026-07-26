"""Renderer-independent mathematics for rank 3 -> rank 2 -> rank 1 collapse."""
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
    if np.linalg.norm(vector) == 0:
        raise ValueError(f"{name} must be nonzero")
    return _readonly(vector)


def _unit_interval(value: Real, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be real")
    number = float(value)
    if not np.isfinite(number) or not 0.0 <= number <= 1.0:
        raise ValueError(f"{name} must lie in [0, 1]")
    return number


def _slerp_vectors(start: FloatArray, end: FloatArray, progress: float) -> FloatArray:
    """Interpolate directions on the sphere while blending magnitudes linearly."""
    t = float(progress)
    start_norm = float(np.linalg.norm(start))
    end_norm = float(np.linalg.norm(end))
    start_unit = start / start_norm
    end_unit = end / end_norm
    dot = float(np.clip(np.dot(start_unit, end_unit), -1.0, 1.0))

    if abs(dot) > 0.9995:
        direction = (1.0 - t) * start_unit + t * end_unit
        direction_norm = float(np.linalg.norm(direction))
        if direction_norm == 0.0:
            direction = end_unit
        else:
            direction = direction / direction_norm
    else:
        theta = float(np.arccos(dot))
        sin_theta = float(np.sin(theta))
        weight_start = np.sin((1.0 - t) * theta) / sin_theta
        weight_end = np.sin(t * theta) / sin_theta
        direction = weight_start * start_unit + weight_end * end_unit
    magnitude = (1.0 - t) * start_norm + t * end_norm
    return _readonly(magnitude * direction)


@dataclass(frozen=True)
class RankCollapse3DSnapshot:
    generator_u: FloatArray
    generator_v: FloatArray
    generator_w: FloatArray
    endpoints: FloatArray
    parallelepiped_corners: FloatArray
    determinant: float
    rank: int


class RankCollapse3D:
    """Produce continuous generator states for rank collapse in R^3."""

    def __init__(
        self,
        generator_u: ArrayLike,
        generator_v: ArrayLike,
        generator_w: ArrayLike,
        coefficient_triples: ArrayLike,
    ) -> None:
        self._u = _vector(generator_u, "generator_u")
        self._v = _vector(generator_v, "generator_v")
        self._w = _vector(generator_w, "generator_w")
        triples = np.asarray(coefficient_triples, dtype=float)
        if triples.ndim != 2 or triples.shape[1] != 3 or not np.all(np.isfinite(triples)):
            raise ValueError("coefficient_triples must have shape (n, 3)")
        if np.linalg.matrix_rank(np.column_stack((self._u, self._v, self._w))) != 3:
            raise ValueError("initial generators must have rank 3")
        self._triples = _readonly(triples)
        self._rank2_w = _readonly(0.72 * self._u - 0.58 * self._v)
        self._rank1_v = _readonly(0.78 * self._u)
        self._rank1_w = _readonly(-0.62 * self._u)

    def space_to_plane(self, progress: Real) -> RankCollapse3DSnapshot:
        t = _unit_interval(progress, "progress")
        w = _slerp_vectors(self._w, self._rank2_w, t)
        return self._snapshot(self._u, self._v, w)

    def plane_to_line(self, progress: Real) -> RankCollapse3DSnapshot:
        t = _unit_interval(progress, "progress")
        v = _slerp_vectors(self._v, self._rank1_v, t)
        w = _slerp_vectors(self._rank2_w, self._rank1_w, t)
        return self._snapshot(self._u, v, w)

    def _snapshot(self, u: FloatArray, v: FloatArray, w: FloatArray) -> RankCollapse3DSnapshot:
        matrix = np.column_stack((u, v, w))
        endpoints = self._triples @ matrix.T
        corners = np.array(
            [
                np.zeros(3), u, v, w,
                u + v, u + w, v + w, u + v + w,
            ],
            dtype=float,
        )
        return RankCollapse3DSnapshot(
            generator_u=_readonly(u),
            generator_v=_readonly(v),
            generator_w=_readonly(w),
            endpoints=_readonly(endpoints),
            parallelepiped_corners=_readonly(corners),
            determinant=float(np.linalg.det(matrix)),
            rank=int(np.linalg.matrix_rank(matrix, tol=1e-9)),
        )
