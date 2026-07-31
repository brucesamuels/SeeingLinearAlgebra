"""Renderer-independent mathematics for real Euclidean inner products."""
from __future__ import annotations
from dataclasses import dataclass
import math
import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]

@dataclass(frozen=True)
class InnerProductSnapshot:
    vector_u: FloatArray
    vector_v: FloatArray
    value: float
    norm_u: float
    norm_v: float
    cosine: float
    angle_radians: float
    angle_degrees: float
    classification: str
    projection_scalar: float
    projection_vector: FloatArray

class InnerProduct:
    """Compute the standard Euclidean inner product and related geometry."""
    def __init__(self, vector_u=None, vector_v=None, *, zero_tolerance: float = 1e-9) -> None:
        self.vector_u = np.asarray(vector_u if vector_u is not None else [3.0, 0.0], dtype=float)
        self.vector_v = np.asarray(vector_v if vector_v is not None else [2.0, 2.0], dtype=float)
        self.zero_tolerance = float(zero_tolerance)
        if self.vector_u.ndim != 1 or self.vector_v.ndim != 1:
            raise ValueError('vector_u and vector_v must be one-dimensional.')
        if self.vector_u.shape != self.vector_v.shape:
            raise ValueError('vector_u and vector_v must have the same dimension.')
        if self.vector_u.size == 0:
            raise ValueError('vectors must contain at least one coordinate.')
        if self.zero_tolerance <= 0:
            raise ValueError('zero_tolerance must be positive.')

    def snapshot(self) -> InnerProductSnapshot:
        norm_u = float(np.linalg.norm(self.vector_u))
        norm_v = float(np.linalg.norm(self.vector_v))
        if norm_u <= self.zero_tolerance or norm_v <= self.zero_tolerance:
            raise ValueError('the angle is undefined when either vector is zero.')
        value = float(np.dot(self.vector_u, self.vector_v))
        cosine = float(np.clip(value / (norm_u * norm_v), -1.0, 1.0))
        angle_radians = float(math.acos(cosine))
        if value > self.zero_tolerance:
            classification = 'acute'
        elif value < -self.zero_tolerance:
            classification = 'obtuse'
        else:
            classification = 'right'
        projection_scalar = value / (norm_u * norm_u)
        return InnerProductSnapshot(
            self.vector_u.copy(), self.vector_v.copy(), value, norm_u, norm_v,
            cosine, angle_radians, float(math.degrees(angle_radians)),
            classification, float(projection_scalar),
            np.asarray(projection_scalar * self.vector_u, dtype=float),
        )

    @staticmethod
    def dot(vector_u, vector_v) -> float:
        u = np.asarray(vector_u, dtype=float)
        v = np.asarray(vector_v, dtype=float)
        if u.ndim != 1 or v.ndim != 1:
            raise ValueError('vectors must be one-dimensional.')
        if u.shape != v.shape:
            raise ValueError('vectors must have the same dimension.')
        return float(np.dot(u, v))
