"""Renderer-independent mathematics for CP85.

Reflection across a line through the origin preserves vector addition.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray

Vector = NDArray[np.float64]


@dataclass(frozen=True)
class ReflectionAdditivitySnapshot:
    u: Vector
    v: Vector
    sum_vector: Vector
    reflected_u: Vector
    reflected_v: Vector
    reflected_sum: Vector
    sum_of_reflections: Vector
    residual: Vector
    line_angle: float

    @property
    def endpoints_agree(self) -> bool:
        return bool(np.allclose(self.residual, np.zeros(2), atol=1e-9))


def reflection_matrix(line_angle: float) -> NDArray[np.float64]:
    c = np.cos(2.0 * line_angle)
    s = np.sin(2.0 * line_angle)
    return np.array([[c, s], [s, -c]], dtype=float)


def reflect(vector: Vector, line_angle: float) -> Vector:
    value = np.asarray(vector, dtype=float)
    if value.shape != (2,):
        raise ValueError("vector must be two-dimensional")
    return reflection_matrix(line_angle) @ value


def evaluate_reflection_additivity(
    *,
    u: Vector | None = None,
    v: Vector | None = None,
    line_angle: float = np.deg2rad(24.0),
) -> ReflectionAdditivitySnapshot:
    # CP85.1: use vectors with a substantially wider angular separation so
    # both the original and reflected head-to-tail additions are easy to read.
    u_value = (
        np.array([1.80, -0.50], dtype=float)
        if u is None
        else np.asarray(u, dtype=float)
    )
    v_value = (
        np.array([-0.60, 1.80], dtype=float)
        if v is None
        else np.asarray(v, dtype=float)
    )

    if u_value.shape != (2,) or v_value.shape != (2,):
        raise ValueError("u and v must each be two-dimensional vectors")

    sum_vector = u_value + v_value
    reflected_u = reflect(u_value, line_angle)
    reflected_v = reflect(v_value, line_angle)
    reflected_sum = reflect(sum_vector, line_angle)
    sum_of_reflections = reflected_u + reflected_v

    return ReflectionAdditivitySnapshot(
        u=u_value.copy(),
        v=v_value.copy(),
        sum_vector=sum_vector,
        reflected_u=reflected_u,
        reflected_v=reflected_v,
        reflected_sum=reflected_sum,
        sum_of_reflections=sum_of_reflections,
        residual=reflected_sum - sum_of_reflections,
        line_angle=float(line_angle),
    )
