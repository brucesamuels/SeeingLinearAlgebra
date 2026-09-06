"""Renderer-independent oriented incidence encoding for an undirected graph."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

import numpy as np

from engine.graph_matrix_encoding import GraphMatrixEncoding


class GraphIncidenceEncoding:
    """Choose edge orientations and build an edge-by-vertex incidence matrix."""

    def __init__(
        self,
        encoding: GraphMatrixEncoding | None = None,
        oriented_edges: Iterable[Sequence[object]] | None = None,
    ) -> None:
        self.encoding = GraphMatrixEncoding() if encoding is None else encoding
        if not isinstance(self.encoding, GraphMatrixEncoding):
            raise ValueError("encoding must be a GraphMatrixEncoding")

        choices = self.encoding.graph.edges if oriented_edges is None else oriented_edges
        orientation = tuple(tuple(edge) for edge in choices)
        self._validate_orientation(orientation)
        self._oriented_edges = orientation

    @property
    def vertex_order(self) -> tuple[object, ...]:
        return self.encoding.vertex_order

    @property
    def oriented_edges(self) -> tuple[tuple[object, object], ...]:
        return self._oriented_edges

    @property
    def shape(self) -> tuple[int, int]:
        return len(self._oriented_edges), len(self.vertex_order)

    def _validate_orientation(self, orientation: tuple[tuple[object, ...], ...]) -> None:
        graph = self.encoding.graph
        if len(orientation) != len(graph.edges):
            raise ValueError("oriented_edges must orient every graph edge exactly once")

        expected = {frozenset(edge) for edge in graph.edges}
        seen: set[frozenset[object]] = set()
        for edge in orientation:
            if len(edge) != 2:
                raise ValueError("each oriented edge must have tail and head")
            tail, head = edge
            if tail == head or tail not in self.vertex_order or head not in self.vertex_order:
                raise ValueError("each oriented edge must use two known endpoints")
            key = frozenset((tail, head))
            if key not in expected:
                raise ValueError("oriented_edges may only use graph edges")
            if key in seen:
                raise ValueError("oriented_edges must orient every graph edge exactly once")
            seen.add(key)
        if seen != expected:
            raise ValueError("oriented_edges must orient every graph edge exactly once")

    def incidence_matrix(self) -> np.ndarray:
        matrix = np.zeros(self.shape, dtype=int)
        vertex_indices = {vertex: index for index, vertex in enumerate(self.vertex_order)}
        for row, (tail, head) in enumerate(self._oriented_edges):
            matrix[row, vertex_indices[tail]] = -1
            matrix[row, vertex_indices[head]] = 1
        return matrix

    def row_for_edge(self, edge_number: int) -> np.ndarray:
        if isinstance(edge_number, bool) or not isinstance(edge_number, int):
            raise ValueError("edge_number must be an integer starting at 1")
        if not 1 <= edge_number <= len(self._oriented_edges):
            raise ValueError("edge_number is outside the oriented edge order")
        return self.incidence_matrix()[edge_number - 1].copy()

    def edge_differences(self, values: Iterable[float]) -> np.ndarray:
        vector = np.asarray(tuple(values), dtype=float)
        expected = (len(self.vertex_order),)
        if vector.shape != expected:
            raise ValueError(f"values must have shape {expected}")
        if not np.all(np.isfinite(vector)):
            raise ValueError("values must be finite")
        return self.incidence_matrix() @ vector

    def reverse_edge(self, edge_number: int) -> "GraphIncidenceEncoding":
        self.row_for_edge(edge_number)
        reversed_edges = list(self._oriented_edges)
        tail, head = reversed_edges[edge_number - 1]
        reversed_edges[edge_number - 1] = (head, tail)
        return GraphIncidenceEncoding(self.encoding, reversed_edges)

