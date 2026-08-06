"""Renderer-independent mathematics for CP129: determinant as area scale factor in R^2."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np

UNIT_SQUARE = np.array(
    [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]],
    dtype=float,
)


@dataclass(frozen=True)
class AreaScaleExample:
    """Mathematical data for one area-scale transformation."""

    matrix: np.ndarray
    source_vertices: np.ndarray
    image_vertices: np.ndarray
    source_area: float
    image_area: float
    area_scale: float

    @property
    def columns(self) -> tuple[np.ndarray, np.ndarray]:
        return self.matrix[:, 0].copy(), self.matrix[:, 1].copy()


def as_matrix_2x2(values: Sequence[Sequence[float]] | np.ndarray) -> np.ndarray:
    matrix = np.asarray(values, dtype=float)
    if matrix.shape != (2, 2):
        raise ValueError("matrix must have shape (2, 2)")
    if not np.isfinite(matrix).all():
        raise ValueError("matrix entries must be finite")
    return matrix


def polygon_area(vertices: Sequence[Sequence[float]] | np.ndarray) -> float:
    points = np.asarray(vertices, dtype=float)
    if points.ndim != 2 or points.shape[1] != 2 or len(points) < 3:
        raise ValueError("vertices must be an array of at least three 2D points")
    x = points[:, 0]
    y = points[:, 1]
    return float(abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1))) / 2.0)


def transform_vertices(
    matrix: Sequence[Sequence[float]] | np.ndarray,
    vertices: Sequence[Sequence[float]] | np.ndarray = UNIT_SQUARE,
) -> np.ndarray:
    linear_map = as_matrix_2x2(matrix)
    points = np.asarray(vertices, dtype=float)
    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError("vertices must have shape (n, 2)")
    return points @ linear_map.T


def build_area_scale_example() -> AreaScaleExample:
    """Return the visually clear CP129 example A=[[2,1],[0,2]]."""

    matrix = np.array([[2.0, 1.0], [0.0, 2.0]], dtype=float)
    image = transform_vertices(matrix)
    source_area = polygon_area(UNIT_SQUARE)
    image_area = polygon_area(image)
    return AreaScaleExample(
        matrix=matrix,
        source_vertices=UNIT_SQUARE.copy(),
        image_vertices=image,
        source_area=source_area,
        image_area=image_area,
        area_scale=image_area / source_area,
    )


def area_scale_statement() -> str:
    return "The magnitude of the determinant is the area scale factor."
