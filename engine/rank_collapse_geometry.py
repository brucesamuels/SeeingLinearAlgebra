"""Renderer-independent topology for rank-collapse geometry.

This module deliberately does not depend on Manim or on a display dimension.
It stores source vertices and connectivity, then creates snapshots from any
transformed vertex array with the same number of vertices.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, TypeAlias

import numpy as np
from numpy.typing import ArrayLike, NDArray


Edge: TypeAlias = tuple[int, int]
Polyline: TypeAlias = tuple[int, ...]
FloatArray: TypeAlias = NDArray[np.float64]


def _readonly_vertex_array(vertices: ArrayLike, *, name: str) -> FloatArray:
    """Return a finite, two-dimensional, read-only float array."""

    try:
        array = np.asarray(vertices, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a rectangular numeric array") from exc

    if array.ndim != 2:
        raise ValueError(
            f"{name} must have shape (vertex_count, dimension); "
            f"received an array with {array.ndim} dimensions"
        )
    if array.shape[0] == 0:
        raise ValueError(f"{name} must contain at least one vertex")
    if array.shape[1] == 0:
        raise ValueError(f"{name} vertices must have at least one coordinate")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")

    result = np.array(array, dtype=float, copy=True)
    result.setflags(write=False)
    return result


def _normalize_vertex_index(
    value: object,
    *,
    vertex_count: int,
    location: str,
) -> int:
    """Validate and normalize one connectivity index."""

    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
        raise TypeError(f"{location} must be an integer vertex index")

    index = int(value)
    if index < 0 or index >= vertex_count:
        raise IndexError(
            f"{location}={index} is outside the valid range "
            f"0 through {vertex_count - 1}"
        )
    return index


def _normalize_edges(
    edges: Iterable[Iterable[int]],
    *,
    vertex_count: int,
) -> tuple[Edge, ...]:
    normalized: list[Edge] = []

    for edge_number, edge in enumerate(edges):
        try:
            values = tuple(edge)
        except TypeError as exc:
            raise TypeError(f"edge {edge_number} must be an iterable of two indices") from exc

        if len(values) != 2:
            raise ValueError(
                f"edge {edge_number} must contain exactly two vertex indices"
            )

        start = _normalize_vertex_index(
            values[0],
            vertex_count=vertex_count,
            location=f"edge {edge_number} start",
        )
        end = _normalize_vertex_index(
            values[1],
            vertex_count=vertex_count,
            location=f"edge {edge_number} end",
        )
        normalized.append((start, end))

    return tuple(normalized)


def _normalize_polylines(
    polylines: Iterable[Iterable[int]],
    *,
    vertex_count: int,
) -> tuple[Polyline, ...]:
    normalized: list[Polyline] = []

    for polyline_number, polyline in enumerate(polylines):
        try:
            values = tuple(polyline)
        except TypeError as exc:
            raise TypeError(
                f"polyline {polyline_number} must be an iterable of vertex indices"
            ) from exc

        if len(values) < 2:
            raise ValueError(
                f"polyline {polyline_number} must contain at least two vertex indices"
            )

        normalized.append(
            tuple(
                _normalize_vertex_index(
                    value,
                    vertex_count=vertex_count,
                    location=f"polyline {polyline_number} index {position}",
                )
                for position, value in enumerate(values)
            )
        )

    return tuple(normalized)


@dataclass(frozen=True, slots=True)
class RankCollapseGeometrySnapshot:
    """Vertex positions and unchanged topology at one path parameter."""

    t: float
    vertices: FloatArray
    edges: tuple[Edge, ...]
    polylines: tuple[Polyline, ...]

    def __post_init__(self) -> None:
        parameter = float(self.t)
        if not np.isfinite(parameter):
            raise ValueError("t must be finite")

        vertices = _readonly_vertex_array(self.vertices, name="vertices")
        edges = _normalize_edges(self.edges, vertex_count=vertices.shape[0])
        polylines = _normalize_polylines(
            self.polylines,
            vertex_count=vertices.shape[0],
        )

        object.__setattr__(self, "t", parameter)
        object.__setattr__(self, "vertices", vertices)
        object.__setattr__(self, "edges", edges)
        object.__setattr__(self, "polylines", polylines)

    @property
    def vertex_count(self) -> int:
        return int(self.vertices.shape[0])

    @property
    def ambient_dimension(self) -> int:
        return int(self.vertices.shape[1])

    def edge_segments(self) -> tuple[FloatArray, ...]:
        """Return one read-only 2-by-d coordinate array per edge."""

        return tuple(_readonly_vertex_array(self.vertices[list(edge)], name="edge") for edge in self.edges)

    def polyline_vertices(self) -> tuple[FloatArray, ...]:
        """Return one read-only k-by-d coordinate array per polyline."""

        return tuple(
            _readonly_vertex_array(self.vertices[list(polyline)], name="polyline")
            for polyline in self.polylines
        )


class RankCollapseGeometry:
    """Static vertices and topology for a rank-collapse animation.

    The source vertices may live in any positive dimension. A snapshot may live
    in a different positive dimension, provided it contains the same number of
    vertices. This supports general maps from R^n to R^m without renderer logic.
    """

    def __init__(
        self,
        vertices: ArrayLike,
        *,
        edges: Iterable[Iterable[int]] = (),
        polylines: Iterable[Iterable[int]] = (),
    ) -> None:
        source_vertices = _readonly_vertex_array(vertices, name="vertices")
        vertex_count = int(source_vertices.shape[0])

        self._vertices = source_vertices
        self._edges = _normalize_edges(edges, vertex_count=vertex_count)
        self._polylines = _normalize_polylines(
            polylines,
            vertex_count=vertex_count,
        )

    @property
    def vertices(self) -> FloatArray:
        """Read-only source vertex array with shape (N, n)."""

        return self._vertices

    @property
    def edges(self) -> tuple[Edge, ...]:
        return self._edges

    @property
    def polylines(self) -> tuple[Polyline, ...]:
        return self._polylines

    @property
    def vertex_count(self) -> int:
        return int(self._vertices.shape[0])

    @property
    def ambient_dimension(self) -> int:
        return int(self._vertices.shape[1])

    def source_snapshot(self, *, t: float = 0.0) -> RankCollapseGeometrySnapshot:
        """Return a snapshot using the original source vertices."""

        return self.snapshot(self._vertices, t=t)

    def snapshot(
        self,
        transformed_vertices: ArrayLike,
        *,
        t: float,
    ) -> RankCollapseGeometrySnapshot:
        """Attach this topology to transformed vertices at parameter ``t``.

        Only the vertex count is fixed. The transformed ambient dimension may
        differ from the source ambient dimension.
        """

        vertices = _readonly_vertex_array(
            transformed_vertices,
            name="transformed_vertices",
        )
        if vertices.shape[0] != self.vertex_count:
            raise ValueError(
                "transformed_vertices must contain exactly "
                f"{self.vertex_count} vertices; received {vertices.shape[0]}"
            )

        return RankCollapseGeometrySnapshot(
            t=t,
            vertices=vertices,
            edges=self._edges,
            polylines=self._polylines,
        )
