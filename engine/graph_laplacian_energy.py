"""Renderer-independent quadratic energy for a graph Laplacian."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from engine.graph_laplacian_operator import GraphLaplacianOperator


class GraphLaplacianEnergy:
    """Compute x^T L x as squared incidence and edge differences."""

    def __init__(self, laplacian: GraphLaplacianOperator | None = None) -> None:
        self.laplacian = GraphLaplacianOperator() if laplacian is None else laplacian
        if not isinstance(self.laplacian, GraphLaplacianOperator):
            raise ValueError("laplacian must be a GraphLaplacianOperator")

    @property
    def vertex_order(self) -> tuple[object, ...]:
        return self.laplacian.vertex_order

    @property
    def oriented_edges(self) -> tuple[tuple[object, object], ...]:
        return self.laplacian.oriented_edges

    def _values(self, values: Iterable[float]) -> np.ndarray:
        vector = np.asarray(tuple(values), dtype=float)
        expected = (len(self.vertex_order),)
        if vector.shape != expected:
            raise ValueError(f"values must have shape {expected}")
        if not np.all(np.isfinite(vector)):
            raise ValueError("values must be finite")
        return vector

    def quadratic_energy(self, values: Iterable[float]) -> float:
        vector = self._values(values)
        return float(vector @ self.laplacian.laplacian_matrix() @ vector)

    def edge_differences(self, values: Iterable[float]) -> np.ndarray:
        vector = self._values(values)
        return self.laplacian.edge_differences(vector)

    def edge_contributions(self, values: Iterable[float]) -> np.ndarray:
        differences = self.edge_differences(values)
        return differences * differences

    def incidence_energy(self, values: Iterable[float]) -> float:
        differences = self.edge_differences(values)
        return float(differences @ differences)

    def graph_edge_energy(self, values: Iterable[float]) -> float:
        vector = self._values(values)
        indices = {vertex: index for index, vertex in enumerate(self.vertex_order)}
        graph = self.laplacian.incidence.encoding.graph
        return float(
            sum(
                (vector[indices[first]] - vector[indices[second]]) ** 2
                for first, second in graph.edges
            )
        )

    def energy_identity(self, values: Iterable[float]) -> tuple[float, float, float]:
        return (
            self.quadratic_energy(values),
            self.incidence_energy(values),
            self.graph_edge_energy(values),
        )

    def with_reversed_edge(self, edge_number: int) -> "GraphLaplacianEnergy":
        return GraphLaplacianEnergy(self.laplacian.with_reversed_edge(edge_number))

