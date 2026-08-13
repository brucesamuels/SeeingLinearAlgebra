"""Renderer-independent numerical content for CP153: Projection onto a Vector."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


def _vector(values: Iterable[float], *, name: str) -> FloatArray:
    vector = np.asarray(tuple(values), dtype=float)
    if vector.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional.")
    if vector.size == 0:
        raise ValueError(f"{name} must contain at least one coordinate.")
    if not np.all(np.isfinite(vector)):
        raise ValueError(f"{name} must contain finite coordinates.")
    return vector


def projection_onto(vector: Iterable[float], direction: Iterable[float]) -> FloatArray:
    """Return the orthogonal projection of ``vector`` onto ``span(direction)``."""
    x = _vector(vector, name="vector")
    u = _vector(direction, name="direction")
    if x.shape != u.shape:
        raise ValueError("vector and direction must have the same dimension")
    denominator = float(u @ u)
    if np.isclose(denominator, 0.0):
        raise ValueError("direction must be nonzero")
    return float((x @ u) / denominator) * u


@dataclass(frozen=True)
class ProjectionSnapshot:
    vector: FloatArray
    direction: FloatArray
    coefficient: float
    projection: FloatArray
    residual: FloatArray

    @property
    def residual_dot_direction(self) -> float:
        return float(self.residual @ self.direction)

    @property
    def reconstructs_vector(self) -> bool:
        return bool(np.allclose(self.vector, self.projection + self.residual))


class VectorProjectionLesson:
    GENERAL_FORMULA = (
        r"\operatorname{proj}_{\mathbf{u}}\mathbf{x}="
        r"\frac{\mathbf{x}\cdot\mathbf{u}}{\mathbf{u}\cdot\mathbf{u}}\mathbf{u}"
    )
    UNIT_FORMULA = r"\operatorname{proj}_{\mathbf{q}}\mathbf{x}=(\mathbf{x}\cdot\mathbf{q})\mathbf{q}"
    DECOMPOSITION = (
        r"\mathbf{x}=\operatorname{proj}_{\mathbf{u}}\mathbf{x}+"
        r"\left(\mathbf{x}-\operatorname{proj}_{\mathbf{u}}\mathbf{x}\right)"
    )
    ORTHOGONAL_RESIDUAL = (
        r"\left(\mathbf{x}-\operatorname{proj}_{\mathbf{u}}\mathbf{x}\right)\cdot\mathbf{u}=0"
    )

    def __init__(self) -> None:
        self._vector = np.array((3.0, 3.0), dtype=float)
        self._direction = np.array((4.0, 1.0), dtype=float)

    def example(self) -> ProjectionSnapshot:
        x = self._vector.copy()
        u = self._direction.copy()
        coefficient = float((x @ u) / (u @ u))
        p = coefficient * u
        residual = x - p
        return ProjectionSnapshot(
            vector=x,
            direction=u,
            coefficient=coefficient,
            projection=p,
            residual=residual,
        )
