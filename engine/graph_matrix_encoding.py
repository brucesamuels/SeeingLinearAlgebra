"""Renderer-independent adjacency and degree matrix encoding for a graph."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from engine.simple_undirected_graph import SimpleUndirectedGraph, triangle_with_tail_graph


class GraphMatrixEncoding:
    """Encode a simple undirected graph after choosing a vertex order."""

    def __init__(
        self,
        graph: SimpleUndirectedGraph | None = None,
        vertex_order: Iterable[object] | None = None,
    ) -> None:
        self.graph = triangle_with_tail_graph() if graph is None else graph
        if not isinstance(self.graph, SimpleUndirectedGraph):
            raise ValueError("graph must be a SimpleUndirectedGraph")
        order = self.graph.vertices if vertex_order is None else tuple(vertex_order)
        if len(order) != len(self.graph.vertices) or set(order) != set(self.graph.vertices):
            raise ValueError("vertex_order must contain every graph vertex exactly once")
        self._vertex_order = tuple(order)

    @property
    def vertex_order(self) -> tuple[object, ...]:
        return self._vertex_order

    def adjacency_matrix(self) -> np.ndarray:
        size = len(self._vertex_order)
        matrix = np.zeros((size, size), dtype=int)
        for row, first in enumerate(self._vertex_order):
            for column, second in enumerate(self._vertex_order):
                if first != second and self.graph.is_adjacent(first, second):
                    matrix[row, column] = 1
        return matrix

    def adjacency_entry(self, first: object, second: object) -> int:
        if first not in self._vertex_order or second not in self._vertex_order:
            raise ValueError("adjacency entry requires known vertices")
        return int(self.graph.is_adjacent(first, second))

    def degree_vector(self) -> np.ndarray:
        return np.array(
            [self.graph.degree(vertex) for vertex in self._vertex_order],
            dtype=int,
        )

    def degree_matrix(self) -> np.ndarray:
        return np.diag(self.degree_vector())

    def row_sums(self) -> np.ndarray:
        return self.adjacency_matrix().sum(axis=1)

    def neighbor_sums(self, values: Iterable[float]) -> np.ndarray:
        vector = np.asarray(tuple(values), dtype=float)
        expected = (len(self._vertex_order),)
        if vector.shape != expected:
            raise ValueError(f"values must have shape {expected}")
        if not np.all(np.isfinite(vector)):
            raise ValueError("values must be finite")
        return self.adjacency_matrix() @ vector
