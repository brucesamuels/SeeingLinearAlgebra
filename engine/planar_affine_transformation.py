"""Renderer-independent affine transformations for the Linear Transformations chapter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import ArrayLike, NDArray


FloatArray = NDArray[np.float64]


def _vector2(value: ArrayLike, *, name: str) -> FloatArray:
    array = np.asarray(value, dtype=float)
    if array.shape != (2,):
        raise ValueError(f"{name} must have shape (2,), got {array.shape}")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")
    return array.copy()


def _matrix2(value: ArrayLike, *, name: str) -> FloatArray:
    array = np.asarray(value, dtype=float)
    if array.shape != (2, 2):
        raise ValueError(f"{name} must have shape (2, 2), got {array.shape}")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")
    return array.copy()


def _points2(value: ArrayLike, *, name: str) -> FloatArray:
    array = np.asarray(value, dtype=float)
    if array.ndim != 2 or array.shape[1] != 2:
        raise ValueError(f"{name} must have shape (n, 2), got {array.shape}")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")
    return array.copy()


@dataclass(frozen=True)
class PlanarAffineSnapshot:
    """Immutable transformed geometry at one interpolation state."""

    progress: float
    matrix: FloatArray
    offset: FloatArray
    origin: FloatArray
    basis_endpoints: FloatArray
    vector_endpoints: FloatArray
    polygon_vertices: FloatArray
    grid_segments: FloatArray


class PlanarAffineTransformation:
    """The affine map x -> A x + b.

    The abstraction intentionally includes translations so the opening lesson can
    compare linear candidates with a clear non-example.
    """

    def __init__(self, matrix: ArrayLike, offset: ArrayLike = (0.0, 0.0)) -> None:
        self._matrix = _matrix2(matrix, name="matrix")
        self._offset = _vector2(offset, name="offset")

    @property
    def matrix(self) -> FloatArray:
        return self._matrix.copy()

    @property
    def offset(self) -> FloatArray:
        return self._offset.copy()

    @property
    def fixes_origin(self) -> bool:
        return bool(np.allclose(self._offset, 0.0))

    @property
    def is_linear(self) -> bool:
        return self.fixes_origin

    def apply(self, points: ArrayLike) -> FloatArray:
        array = np.asarray(points, dtype=float)
        if array.shape == (2,):
            if not np.all(np.isfinite(array)):
                raise ValueError("points must contain only finite values")
            return self._matrix @ array + self._offset
        checked = _points2(array, name="points")
        return checked @ self._matrix.T + self._offset

    def interpolate(self, progress: float) -> "PlanarAffineTransformation":
        progress = float(progress)
        if not np.isfinite(progress) or not 0.0 <= progress <= 1.0:
            raise ValueError("progress must be finite and lie in [0, 1]")
        identity = np.eye(2)
        matrix = (1.0 - progress) * identity + progress * self._matrix
        offset = progress * self._offset
        return PlanarAffineTransformation(matrix, offset)

    @classmethod
    def rotation(cls, angle: float) -> "PlanarAffineTransformation":
        angle = float(angle)
        if not np.isfinite(angle):
            raise ValueError("angle must be finite")
        cosine, sine = np.cos(angle), np.sin(angle)
        return cls(((cosine, -sine), (sine, cosine)))

    @classmethod
    def reflection(cls, direction: ArrayLike) -> "PlanarAffineTransformation":
        vector = _vector2(direction, name="direction")
        norm = np.linalg.norm(vector)
        if np.isclose(norm, 0.0):
            raise ValueError("direction must be nonzero")
        unit = vector / norm
        return cls(2.0 * np.outer(unit, unit) - np.eye(2))

    @classmethod
    def axial_scaling(cls, x_scale: float, y_scale: float) -> "PlanarAffineTransformation":
        scales = np.asarray((x_scale, y_scale), dtype=float)
        if not np.all(np.isfinite(scales)):
            raise ValueError("scale factors must be finite")
        return cls(np.diag(scales))

    @classmethod
    def shear_x(cls, factor: float) -> "PlanarAffineTransformation":
        factor = float(factor)
        if not np.isfinite(factor):
            raise ValueError("factor must be finite")
        return cls(((1.0, factor), (0.0, 1.0)))

    @classmethod
    def projection(cls, direction: ArrayLike) -> "PlanarAffineTransformation":
        vector = _vector2(direction, name="direction")
        norm = np.linalg.norm(vector)
        if np.isclose(norm, 0.0):
            raise ValueError("direction must be nonzero")
        unit = vector / norm
        return cls(np.outer(unit, unit))

    @classmethod
    def translation(cls, offset: ArrayLike) -> "PlanarAffineTransformation":
        return cls(np.eye(2), offset)


class PlanarTransformationGeometry:
    """Renderer-independent collection transformed as one coherent stage."""

    def __init__(
        self,
        *,
        vector_endpoints: ArrayLike,
        polygon_vertices: ArrayLike,
        grid_extent: int = 4,
        grid_step: float = 1.0,
    ) -> None:
        self._basis_endpoints = np.eye(2)
        self._vector_endpoints = _points2(vector_endpoints, name="vector_endpoints")
        self._polygon_vertices = _points2(polygon_vertices, name="polygon_vertices")
        if not isinstance(grid_extent, int) or grid_extent < 1:
            raise ValueError("grid_extent must be a positive integer")
        grid_step = float(grid_step)
        if not np.isfinite(grid_step) or grid_step <= 0:
            raise ValueError("grid_step must be finite and positive")
        self._grid_extent = grid_extent
        self._grid_step = grid_step
        self._grid_segments = self._build_grid_segments()

    def _build_grid_segments(self) -> FloatArray:
        extent = self._grid_extent * self._grid_step
        coordinates = np.arange(-extent, extent + self._grid_step / 2, self._grid_step)
        segments = []
        for coordinate in coordinates:
            segments.append(((-extent, coordinate), (extent, coordinate)))
            segments.append(((coordinate, -extent), (coordinate, extent)))
        return np.asarray(segments, dtype=float)

    @property
    def grid_segments(self) -> FloatArray:
        return self._grid_segments.copy()

    def snapshot(
        self,
        transformation: PlanarAffineTransformation,
        progress: float = 1.0,
    ) -> PlanarAffineSnapshot:
        current = transformation.interpolate(progress)
        flat_grid = self._grid_segments.reshape(-1, 2)
        transformed_grid = current.apply(flat_grid).reshape(self._grid_segments.shape)
        return PlanarAffineSnapshot(
            progress=float(progress),
            matrix=current.matrix,
            offset=current.offset,
            origin=current.apply((0.0, 0.0)),
            basis_endpoints=current.apply(self._basis_endpoints),
            vector_endpoints=current.apply(self._vector_endpoints),
            polygon_vertices=current.apply(self._polygon_vertices),
            grid_segments=transformed_grid,
        )


ROTATION = PlanarAffineTransformation.rotation(np.pi / 4)
REFLECTION = PlanarAffineTransformation.reflection((1.0, 1.0))
SHEAR = PlanarAffineTransformation.shear_x(0.75)
PROJECTION = PlanarAffineTransformation.projection((1.0, 0.0))
TRANSLATION = PlanarAffineTransformation.translation((1.25, 0.75))

CANDIDATE_TRANSFORMATIONS = (
    ("Rotation", ROTATION),
    ("Reflection", REFLECTION),
    ("Shear", SHEAR),
    ("Projection", PROJECTION),
    ("Translation", TRANSLATION),
)
