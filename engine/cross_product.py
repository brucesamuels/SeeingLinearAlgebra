"""Renderer-independent mathematics for the three-dimensional cross product."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
from numpy.typing import NDArray


FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class CrossProductSnapshot:
    vector_u: FloatArray
    vector_v: FloatArray
    cross_uv: FloatArray
    cross_vu: FloatArray
    norm_u: float
    norm_v: float
    magnitude: float
    cosine: float
    sine: float
    angle_radians: float
    angle_degrees: float
    parallelogram_area: float
    dot_u_cross: float
    dot_v_cross: float
    is_degenerate: bool


class CrossProduct:
    """Compute the 3D cross product and related geometry."""

    def __init__(
        self,
        vector_u=None,
        vector_v=None,
        *,
        zero_tolerance: float = 1e-9,
    ) -> None:
        self.vector_u = np.asarray(
            vector_u if vector_u is not None else [3.0, 0.0, 0.0],
            dtype=float,
        )
        self.vector_v = np.asarray(
            vector_v if vector_v is not None else [1.0, 2.0, 0.0],
            dtype=float,
        )
        self.zero_tolerance = float(zero_tolerance)

        if self.vector_u.shape != (3,):
            raise ValueError("vector_u must contain exactly three coordinates.")
        if self.vector_v.shape != (3,):
            raise ValueError("vector_v must contain exactly three coordinates.")
        if self.zero_tolerance <= 0:
            raise ValueError("zero_tolerance must be positive.")

    def snapshot(self) -> CrossProductSnapshot:
        norm_u = float(np.linalg.norm(self.vector_u))
        norm_v = float(np.linalg.norm(self.vector_v))

        if norm_u <= self.zero_tolerance or norm_v <= self.zero_tolerance:
            raise ValueError("both vectors must be nonzero.")

        cross_uv = np.cross(self.vector_u, self.vector_v)
        cross_vu = np.cross(self.vector_v, self.vector_u)
        magnitude = float(np.linalg.norm(cross_uv))

        cosine = float(
            np.dot(self.vector_u, self.vector_v) / (norm_u * norm_v)
        )
        cosine = float(np.clip(cosine, -1.0, 1.0))
        angle_radians = float(math.acos(cosine))
        angle_degrees = float(math.degrees(angle_radians))
        sine = float(math.sin(angle_radians))

        return CrossProductSnapshot(
            vector_u=self.vector_u.copy(),
            vector_v=self.vector_v.copy(),
            cross_uv=np.asarray(cross_uv, dtype=float),
            cross_vu=np.asarray(cross_vu, dtype=float),
            norm_u=norm_u,
            norm_v=norm_v,
            magnitude=magnitude,
            cosine=cosine,
            sine=sine,
            angle_radians=angle_radians,
            angle_degrees=angle_degrees,
            parallelogram_area=magnitude,
            dot_u_cross=float(np.dot(self.vector_u, cross_uv)),
            dot_v_cross=float(np.dot(self.vector_v, cross_uv)),
            is_degenerate=magnitude <= self.zero_tolerance,
        )

    @staticmethod
    def cross(vector_u, vector_v) -> FloatArray:
        u = np.asarray(vector_u, dtype=float)
        v = np.asarray(vector_v, dtype=float)

        if u.shape != (3,) or v.shape != (3,):
            raise ValueError("cross product inputs must both be 3D vectors.")
        return np.asarray(np.cross(u, v), dtype=float)
