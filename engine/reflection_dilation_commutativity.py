"""Renderer-independent mathematics for CP84.

Reflection across a line through the origin commutes with dilation
centered at the origin.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray

Vector = NDArray[np.float64]


@dataclass(frozen=True)
class ReflectionDilationSnapshot:
    vector: Vector
    line_angle: float
    scalar: float
    reflected: Vector
    dilated: Vector
    reflect_then_dilate: Vector
    dilate_then_reflect: Vector
    residual: Vector

    @property
    def endpoints_agree(self) -> bool:
        return bool(np.allclose(self.residual, np.zeros(2), atol=1e-9))


def reflection_matrix(line_angle: float) -> NDArray[np.float64]:
    """Return the 2D reflection matrix across a line through the origin."""
    c = np.cos(2.0 * line_angle)
    s = np.sin(2.0 * line_angle)
    return np.array([[c, s], [s, -c]], dtype=float)


def reflect(vector: Vector, line_angle: float) -> Vector:
    value = np.asarray(vector, dtype=float)
    if value.shape != (2,):
        raise ValueError("vector must be two-dimensional")
    return reflection_matrix(line_angle) @ value


def dilate(vector: Vector, scalar: float) -> Vector:
    value = np.asarray(vector, dtype=float)
    if value.shape != (2,):
        raise ValueError("vector must be two-dimensional")
    return float(scalar) * value


def evaluate_reflection_dilation(
    *,
    vector: Vector | None = None,
    line_angle: float = np.deg2rad(28.0),
    scalar: float = 1.65,
) -> ReflectionDilationSnapshot:
    """Evaluate both orders of reflection and dilation."""
    # CP84.1: move the initial vector farther from the mirror line so the
    # reflection is visually unmistakable.
    v = (
        np.array([0.85, 1.75], dtype=float)
        if vector is None
        else np.asarray(vector, dtype=float)
    )

    if v.shape != (2,):
        raise ValueError("vector must be two-dimensional")

    reflected = reflect(v, line_angle)
    dilated = dilate(v, scalar)
    reflect_then_dilate = dilate(reflected, scalar)
    dilate_then_reflect = reflect(dilated, line_angle)

    return ReflectionDilationSnapshot(
        vector=v.copy(),
        line_angle=float(line_angle),
        scalar=float(scalar),
        reflected=reflected,
        dilated=dilated,
        reflect_then_dilate=reflect_then_dilate,
        dilate_then_reflect=dilate_then_reflect,
        residual=reflect_then_dilate - dilate_then_reflect,
    )
