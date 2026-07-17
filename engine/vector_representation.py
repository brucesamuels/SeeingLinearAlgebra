"""Renderer-independent synchronized representations of one vector."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Iterable

import numpy as np
from numpy.typing import ArrayLike, NDArray


FloatArray = NDArray[np.float64]


def _as_vector(values: ArrayLike) -> FloatArray:
    array = np.asarray(values, dtype=float)

    if array.ndim != 1:
        raise ValueError("vector coordinates must be one-dimensional")
    if array.size == 0:
        raise ValueError("vector must contain at least one coordinate")
    if not np.all(np.isfinite(array)):
        raise ValueError("vector coordinates must be finite")

    result = np.array(array, dtype=float, copy=True)
    result.setflags(write=False)
    return result


@dataclass(frozen=True, slots=True)
class VectorRepresentationSnapshot:
    """Immutable synchronized mathematical views of one vector."""

    coordinates: FloatArray
    row_coordinates: tuple[float, ...]
    column_coordinates: tuple[tuple[float], ...]
    origin: FloatArray
    endpoint: FloatArray
    magnitude: float
    dimension: int
    is_zero: bool

    def __post_init__(self) -> None:
        coordinates = _as_vector(self.coordinates)
        origin = _as_vector(self.origin)
        endpoint = _as_vector(self.endpoint)

        if origin.shape != coordinates.shape:
            raise ValueError("origin shape must match coordinate shape")
        if endpoint.shape != coordinates.shape:
            raise ValueError("endpoint shape must match coordinate shape")
        if not np.allclose(endpoint, origin + coordinates):
            raise ValueError("endpoint must equal origin plus coordinates")
        if self.dimension != coordinates.size:
            raise ValueError("dimension must equal coordinate count")

        expected_row = tuple(float(value) for value in coordinates)
        expected_column = tuple((value,) for value in expected_row)

        if self.row_coordinates != expected_row:
            raise ValueError("row coordinates do not match coordinates")
        if self.column_coordinates != expected_column:
            raise ValueError("column coordinates do not match coordinates")

        expected_magnitude = float(np.linalg.norm(coordinates))
        if not np.isclose(self.magnitude, expected_magnitude):
            raise ValueError("magnitude does not match coordinates")
        if self.is_zero != bool(np.isclose(expected_magnitude, 0.0)):
            raise ValueError("is_zero does not match magnitude")

        object.__setattr__(self, "coordinates", coordinates)
        object.__setattr__(self, "origin", origin)
        object.__setattr__(self, "endpoint", endpoint)


class VectorRepresentation:
    """One vector with synchronized coordinate and geometric views."""

    __slots__ = ("_coordinates", "_origin")

    def __init__(
        self,
        coordinates: ArrayLike,
        *,
        origin: ArrayLike | None = None,
    ) -> None:
        normalized_coordinates = _as_vector(coordinates)

        if origin is None:
            normalized_origin = np.zeros_like(normalized_coordinates)
            normalized_origin.setflags(write=False)
        else:
            normalized_origin = _as_vector(origin)
            if normalized_origin.shape != normalized_coordinates.shape:
                raise ValueError("origin shape must match coordinate shape")

        self._coordinates = normalized_coordinates
        self._origin = normalized_origin

    @property
    def coordinates(self) -> FloatArray:
        return self._coordinates

    @property
    def origin(self) -> FloatArray:
        return self._origin

    @property
    def dimension(self) -> int:
        return int(self._coordinates.size)

    def snapshot(self) -> VectorRepresentationSnapshot:
        endpoint = np.array(
            self._origin + self._coordinates,
            dtype=float,
            copy=True,
        )
        endpoint.setflags(write=False)

        row = tuple(float(value) for value in self._coordinates)
        column = tuple((value,) for value in row)
        magnitude = float(np.linalg.norm(self._coordinates))

        return VectorRepresentationSnapshot(
            coordinates=self._coordinates,
            row_coordinates=row,
            column_coordinates=column,
            origin=self._origin,
            endpoint=endpoint,
            magnitude=magnitude,
            dimension=self.dimension,
            is_zero=bool(np.isclose(magnitude, 0.0)),
        )

    def translated_to(self, origin: ArrayLike) -> "VectorRepresentation":
        """Return the same free vector drawn from a different origin."""
        return VectorRepresentation(self._coordinates, origin=origin)

    def scaled(self, scalar: float) -> "VectorRepresentation":
        """Return a new vector representation scaled by *scalar*."""
        if not np.isscalar(scalar):
            raise TypeError("scalar must be a real number")
        scalar_value = float(scalar)
        if not np.isfinite(scalar_value):
            raise ValueError("scalar must be finite")
        return VectorRepresentation(
            scalar_value * self._coordinates,
            origin=self._origin,
        )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"coordinates={self._coordinates.tolist()!r}, "
            f"origin={self._origin.tolist()!r})"
        )
