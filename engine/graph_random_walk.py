"""Renderer-independent simple random walk on an undirected graph."""

from __future__ import annotations

from collections.abc import Iterable
from numbers import Integral

import numpy as np

from engine.graph_incidence_encoding import GraphIncidenceEncoding
from engine.graph_laplacian_operator import GraphLaplacianOperator
from engine.graph_matrix_encoding import GraphMatrixEncoding
from engine.simple_undirected_graph import SimpleUndirectedGraph, triangle_with_tail_graph


class GraphRandomWalk:
    """Evolve column probability vectors with P = A D^{-1}."""

    def __init__(self, graph: SimpleUndirectedGraph | None = None) -> None:
        self.graph = triangle_with_tail_graph() if graph is None else graph
        if not isinstance(self.graph, SimpleUndirectedGraph):
            raise ValueError("graph must be a SimpleUndirectedGraph")
        if any(self.graph.degree(vertex) == 0 for vertex in self.graph.vertices):
            raise ValueError("random walk graph must have no isolated vertices")
        self.encoding = GraphMatrixEncoding(self.graph)
        self.laplacian = GraphLaplacianOperator(GraphIncidenceEncoding(self.encoding))

    @property
    def vertex_order(self) -> tuple[object, ...]:
        return self.encoding.vertex_order

    def transition_matrix(self) -> np.ndarray:
        """Return the column-stochastic matrix whose column j leaves vertex j."""

        adjacency = self.encoding.adjacency_matrix().astype(float)
        inverse_degrees = np.diag(1.0 / self.encoding.degree_vector())
        return adjacency @ inverse_degrees

    def column_sums(self) -> np.ndarray:
        return self.transition_matrix().sum(axis=0)

    def _distribution(self, values: Iterable[float]) -> np.ndarray:
        vector = np.asarray(tuple(values), dtype=float)
        expected = (len(self.vertex_order),)
        if vector.shape != expected:
            raise ValueError(f"distribution must have shape {expected}")
        if not np.all(np.isfinite(vector)):
            raise ValueError("distribution must be finite")
        if np.any(vector < -1e-12):
            raise ValueError("distribution entries must be nonnegative")
        if not np.isclose(vector.sum(), 1.0, atol=1e-12, rtol=0.0):
            raise ValueError("distribution entries must sum to one")
        vector[np.isclose(vector, 0.0, atol=1e-12, rtol=0.0)] = 0.0
        return vector

    @staticmethod
    def _steps(steps: int) -> int:
        if isinstance(steps, bool) or not isinstance(steps, Integral) or steps < 0:
            raise ValueError("steps must be a nonnegative integer")
        return int(steps)

    def point_mass(self, vertex: object) -> np.ndarray:
        if vertex not in self.vertex_order:
            raise ValueError("point mass requires a known vertex")
        vector = np.zeros(len(self.vertex_order), dtype=float)
        vector[self.vertex_order.index(vertex)] = 1.0
        return vector

    def next_distribution(self, distribution: Iterable[float]) -> np.ndarray:
        return self.transition_matrix() @ self._distribution(distribution)

    def evolve(self, distribution: Iterable[float], steps: int) -> np.ndarray:
        vector = self._distribution(distribution)
        return np.linalg.matrix_power(self.transition_matrix(), self._steps(steps)) @ vector

    def trajectory(
        self,
        distribution: Iterable[float],
        steps: int,
    ) -> tuple[np.ndarray, ...]:
        count = self._steps(steps)
        states = [self._distribution(distribution)]
        for _ in range(count):
            states.append(self.next_distribution(states[-1]))
        return tuple(state.copy() for state in states)

    def stationary_distribution(self) -> np.ndarray:
        degrees = self.encoding.degree_vector().astype(float)
        return degrees / degrees.sum()

    def is_stationary(self, distribution: Iterable[float]) -> bool:
        vector = self._distribution(distribution)
        return bool(
            np.allclose(
                self.next_distribution(vector),
                vector,
                atol=1e-12,
                rtol=0.0,
            )
        )

    def stationary_laplacian_vector(self) -> np.ndarray:
        """Return D^{-1} pi, which lies in the Laplacian null space."""

        return self.stationary_distribution() / self.encoding.degree_vector()

    def stationary_laplacian_residual(self) -> np.ndarray:
        return self.laplacian.apply(self.stationary_laplacian_vector())

    def total_variation_distance(
        self,
        first: Iterable[float],
        second: Iterable[float],
    ) -> float:
        left = self._distribution(first)
        right = self._distribution(second)
        return 0.5 * float(np.abs(left - right).sum())
