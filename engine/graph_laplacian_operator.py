"""Renderer-independent graph Laplacian built from incidence and adjacency data."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from engine.graph_incidence_encoding import GraphIncidenceEncoding


class GraphLaplacianOperator:
    """Represent the vertex-to-edge-to-vertex operator L = B^T B = D - A."""

    def __init__(self, incidence: GraphIncidenceEncoding | None = None) -> None:
        self.incidence = GraphIncidenceEncoding() if incidence is None else incidence
        if not isinstance(self.incidence, GraphIncidenceEncoding):
            raise ValueError("incidence must be a GraphIncidenceEncoding")

    @property
    def vertex_order(self) -> tuple[object, ...]:
        return self.incidence.vertex_order

    @property
    def oriented_edges(self) -> tuple[tuple[object, object], ...]:
        return self.incidence.oriented_edges

    def _vertex_values(self, values: Iterable[float]) -> np.ndarray:
        vector = np.asarray(tuple(values), dtype=float)
        expected = (len(self.vertex_order),)
        if vector.shape != expected:
            raise ValueError(f"vertex values must have shape {expected}")
        if not np.all(np.isfinite(vector)):
            raise ValueError("vertex values must be finite")
        return vector

    def _edge_values(self, values: Iterable[float]) -> np.ndarray:
        vector = np.asarray(tuple(values), dtype=float)
        expected = (len(self.oriented_edges),)
        if vector.shape != expected:
            raise ValueError(f"edge values must have shape {expected}")
        if not np.all(np.isfinite(vector)):
            raise ValueError("edge values must be finite")
        return vector

    def laplacian_from_incidence(self) -> np.ndarray:
        incidence = self.incidence.incidence_matrix()
        return incidence.T @ incidence

    def laplacian_from_degree_adjacency(self) -> np.ndarray:
        encoding = self.incidence.encoding
        return encoding.degree_matrix() - encoding.adjacency_matrix()

    def laplacian_matrix(self) -> np.ndarray:
        from_incidence = self.laplacian_from_incidence()
        from_graph = self.laplacian_from_degree_adjacency()
        if not np.array_equal(from_incidence, from_graph):
            raise RuntimeError("incidence and graph formulas disagree")
        return from_incidence

    def edge_differences(self, values: Iterable[float]) -> np.ndarray:
        vector = self._vertex_values(values)
        return self.incidence.incidence_matrix() @ vector

    def return_to_vertices(self, edge_values: Iterable[float]) -> np.ndarray:
        vector = self._edge_values(edge_values)
        return self.incidence.incidence_matrix().T @ vector

    def apply(self, values: Iterable[float]) -> np.ndarray:
        vector = self._vertex_values(values)
        return self.laplacian_matrix() @ vector

    def local_difference_sum(self, vertex: object, values: Iterable[float]) -> float:
        if vertex not in self.vertex_order:
            raise ValueError("local difference requires a known vertex")
        vector = self._vertex_values(values)
        index = self.vertex_order.index(vertex)
        graph = self.incidence.encoding.graph
        indices = {item: position for position, item in enumerate(self.vertex_order)}
        return float(
            sum(vector[index] - vector[indices[neighbor]] for neighbor in graph.neighbors(vertex))
        )

    def with_reversed_edge(self, edge_number: int) -> "GraphLaplacianOperator":
        return GraphLaplacianOperator(self.incidence.reverse_edge(edge_number))

