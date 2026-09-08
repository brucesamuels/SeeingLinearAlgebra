"""Renderer-independent fundamental subspaces of graph incidence matrices."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from engine.graph_incidence_encoding import GraphIncidenceEncoding
from engine.graph_laplacian_operator import GraphLaplacianOperator
from engine.graph_matrix_encoding import GraphMatrixEncoding


class GraphFundamentalSubspaces:
    """Connect the four subspaces of B to components, gradients, and cycles."""

    CYCLE_FLOW = np.array([1, 1, -1, 0], dtype=float)

    def __init__(self, incidence: GraphIncidenceEncoding | None = None) -> None:
        self.incidence = GraphIncidenceEncoding() if incidence is None else incidence
        if not isinstance(self.incidence, GraphIncidenceEncoding):
            raise ValueError("incidence must be a GraphIncidenceEncoding")
        self.laplacian = GraphLaplacianOperator(self.incidence)

    @property
    def vertex_count(self) -> int:
        return len(self.incidence.vertex_order)

    @property
    def edge_count(self) -> int:
        return len(self.incidence.oriented_edges)

    @property
    def rank(self) -> int:
        return int(np.linalg.matrix_rank(self.incidence_matrix()))

    @property
    def nullity(self) -> int:
        return self.vertex_count - self.rank

    @property
    def left_nullity(self) -> int:
        return self.edge_count - self.rank

    @property
    def component_count(self) -> int:
        return len(self.incidence.encoding.graph.connected_components())

    @property
    def cycle_rank(self) -> int:
        return self.edge_count - self.vertex_count + self.component_count

    def incidence_matrix(self) -> np.ndarray:
        return self.incidence.incidence_matrix().copy()

    def laplacian_matrix(self) -> np.ndarray:
        return self.laplacian.laplacian_matrix().copy()

    @staticmethod
    def _vector(values: Iterable[float], size: int, name: str) -> np.ndarray:
        vector = np.asarray(tuple(values), dtype=float)
        if vector.shape != (size,):
            raise ValueError(f"{name} must have shape ({size},)")
        if not np.all(np.isfinite(vector)):
            raise ValueError(f"{name} must be finite")
        return vector

    def vertex_values(self, values: Iterable[float]) -> np.ndarray:
        return self._vector(values, self.vertex_count, "vertex values")

    def edge_values(self, values: Iterable[float]) -> np.ndarray:
        return self._vector(values, self.edge_count, "edge values")

    def edge_differences(self, values: Iterable[float]) -> np.ndarray:
        return self.incidence_matrix() @ self.vertex_values(values)

    def vertex_accumulation(self, values: Iterable[float]) -> np.ndarray:
        return self.incidence_matrix().T @ self.edge_values(values)

    def component_indicators(self) -> tuple[np.ndarray, ...]:
        order = self.incidence.vertex_order
        indicators = []
        for component in self.incidence.encoding.graph.connected_components():
            members = set(component)
            indicators.append(np.array([1.0 if vertex in members else 0.0 for vertex in order]))
        return tuple(indicator.copy() for indicator in indicators)

    def is_componentwise_constant(self, values: Iterable[float]) -> bool:
        vector = self.vertex_values(values)
        return bool(np.allclose(self.edge_differences(vector), np.zeros(self.edge_count)))

    def is_balanced_on_components(self, values: Iterable[float]) -> bool:
        vector = self.vertex_values(values)
        return all(np.isclose(indicator @ vector, 0.0) for indicator in self.component_indicators())

    def cycle_flow(self) -> np.ndarray:
        if self.incidence_matrix().shape != (4, 4):
            raise ValueError("canonical cycle flow belongs to the recurring graph")
        return self.CYCLE_FLOW.copy()

    def cycle_sum(self, values: Iterable[float]) -> float:
        vector = self.edge_values(values)
        cycle = self.cycle_flow()
        return float(cycle @ vector)

    def is_compatible_edge_difference(self, values: Iterable[float]) -> bool:
        vector = self.edge_values(values)
        coefficients, *_ = np.linalg.lstsq(self.incidence_matrix(), vector, rcond=None)
        return bool(np.allclose(self.incidence_matrix() @ coefficients, vector))

    def gradient_component(self, values: Iterable[float]) -> np.ndarray:
        vector = self.edge_values(values)
        return self.incidence_matrix() @ (np.linalg.pinv(self.incidence_matrix()) @ vector)

    def circulation_component(self, values: Iterable[float]) -> np.ndarray:
        vector = self.edge_values(values)
        return vector - self.gradient_component(vector)

    def laplacian_output_is_reachable(self, values: Iterable[float]) -> bool:
        return self.is_balanced_on_components(values)

    @classmethod
    def without_edge(cls, edge: tuple[int, int]) -> "GraphFundamentalSubspaces":
        base = GraphMatrixEncoding()
        graph = base.graph.without_edge(edge)
        encoding = GraphMatrixEncoding(graph, base.vertex_order)
        oriented_edges = tuple(
            candidate
            for candidate in ((1, 2), (2, 3), (1, 3), (3, 4))
            if frozenset(candidate) != frozenset(edge)
        )
        return cls(GraphIncidenceEncoding(encoding, oriented_edges))
