"""Renderer-independent content for CP154: Orthogonal Decomposition."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

from engine.vector_projection import projection_onto

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


@dataclass(frozen=True)
class OrthogonalDecompositionSnapshot:
    vector: FloatArray
    direction: FloatArray
    parallel: FloatArray
    perpendicular: FloatArray

    @property
    def reconstructs_vector(self) -> bool:
        return bool(np.allclose(self.vector, self.parallel + self.perpendicular))

    @property
    def pieces_are_orthogonal(self) -> bool:
        return bool(np.isclose(self.parallel @ self.perpendicular, 0.0))

    @property
    def pythagorean_holds(self) -> bool:
        lhs = float(self.vector @ self.vector)
        rhs = float(self.parallel @ self.parallel + self.perpendicular @ self.perpendicular)
        return bool(np.isclose(lhs, rhs))

    @property
    def vector_norm_squared(self) -> float:
        return float(self.vector @ self.vector)

    @property
    def parallel_norm_squared(self) -> float:
        return float(self.parallel @ self.parallel)

    @property
    def perpendicular_norm_squared(self) -> float:
        return float(self.perpendicular @ self.perpendicular)


def decompose_along_direction(
    vector: Iterable[float], direction: Iterable[float]
) -> OrthogonalDecompositionSnapshot:
    """Split ``vector`` into components parallel and perpendicular to ``direction``."""
    x = _vector(vector, name="vector")
    u = _vector(direction, name="direction")
    if x.shape != u.shape:
        raise ValueError("vector and direction must have the same dimension")
    parallel = projection_onto(x, u)
    perpendicular = x - parallel
    return OrthogonalDecompositionSnapshot(
        vector=x,
        direction=u,
        parallel=parallel,
        perpendicular=perpendicular,
    )


class OrthogonalDecompositionLesson:
    LINE_DECOMPOSITION = (
        r"\mathbf{x}=\mathbf{p}+\mathbf{r},\qquad "
        r"\mathbf{p}\in W,\quad \mathbf{r}\in W^\perp"
    )
    PROJECTION_IDENTITIES = (
        r"\mathbf{p}=\operatorname{proj}_{W}\mathbf{x},\qquad "
        r"\mathbf{r}=\mathbf{x}-\mathbf{p}"
    )
    PYTHAGOREAN = r"\|\mathbf{x}\|^2=\|\mathbf{p}\|^2+\|\mathbf{r}\|^2"
    GENERAL_SPLIT = (
        r"\mathbb{R}^n=W\oplus W^\perp,\qquad "
        r"\mathbf{x}=\mathbf{p}+\mathbf{r}"
    )

    def __init__(self) -> None:
        self._vector = np.array((4.0, 2.0), dtype=float)
        self._direction = np.array((1.0, 1.0), dtype=float)

    def example(self) -> OrthogonalDecompositionSnapshot:
        return decompose_along_direction(self._vector, self._direction)
