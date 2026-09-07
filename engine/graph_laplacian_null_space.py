"""Renderer-independent link between Laplacian null spaces and components."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from engine.graph_incidence_encoding import GraphIncidenceEncoding
from engine.graph_laplacian_energy import GraphLaplacianEnergy
from engine.graph_laplacian_operator import GraphLaplacianOperator
from engine.graph_matrix_encoding import GraphMatrixEncoding
from engine.simple_undirected_graph import SimpleUndirectedGraph, triangle_with_tail_graph


class GraphLaplacianNullSpace:
    """Describe null vectors as signals constant on connected components."""

    def __init__(self, graph: SimpleUndirectedGraph | None = None) -> None:
        self.graph = (
            triangle_with_tail_graph().without_edge((3, 4))
            if graph is None
            else graph
        )
        if not isinstance(self.graph, SimpleUndirectedGraph):
            raise ValueError("graph must be a SimpleUndirectedGraph")
        encoding = GraphMatrixEncoding(self.graph)
        incidence = GraphIncidenceEncoding(encoding)
        self.laplacian = GraphLaplacianOperator(incidence)
        self.energy = GraphLaplacianEnergy(self.laplacian)

    @property
    def vertex_order(self) -> tuple[object, ...]:
        return self.laplacian.vertex_order

    @property
    def components(self) -> tuple[tuple[object, ...], ...]:
        return self.graph.connected_components()

    @property
    def nullity(self) -> int:
        """Return the number of component-indicator basis vectors."""

        return len(self.components)

    def _values(self, values: Iterable[float]) -> np.ndarray:
        vector = np.asarray(tuple(values), dtype=float)
        expected = (len(self.vertex_order),)
        if vector.shape != expected:
            raise ValueError(f"values must have shape {expected}")
        if not np.all(np.isfinite(vector)):
            raise ValueError("values must be finite")
        return vector

    def component_indicator(self, component_number: int) -> np.ndarray:
        """Return the indicator of a one-based connected component."""

        if isinstance(component_number, bool) or not isinstance(component_number, int):
            raise ValueError("component_number must be an integer starting at 1")
        if not 1 <= component_number <= self.nullity:
            raise ValueError("component_number is outside the component order")
        component = set(self.components[component_number - 1])
        return np.array(
            [int(vertex in component) for vertex in self.vertex_order],
            dtype=int,
        )

    def component_indicator_matrix(self) -> np.ndarray:
        """Return component indicators as the columns of a matrix."""

        return np.column_stack(
            [self.component_indicator(number) for number in range(1, self.nullity + 1)]
        )

    def component_constant_signal(self, constants: Iterable[float]) -> np.ndarray:
        coefficients = np.asarray(tuple(constants), dtype=float)
        expected = (self.nullity,)
        if coefficients.shape != expected:
            raise ValueError(f"constants must have shape {expected}")
        if not np.all(np.isfinite(coefficients)):
            raise ValueError("constants must be finite")
        return self.component_indicator_matrix() @ coefficients

    def apply(self, values: Iterable[float]) -> np.ndarray:
        return self.laplacian.apply(self._values(values))

    def is_null_vector(self, values: Iterable[float]) -> bool:
        return bool(np.allclose(self.apply(values), 0.0, atol=1e-12, rtol=0.0))

    def is_componentwise_constant(self, values: Iterable[float]) -> bool:
        vector = self._values(values)
        indices = {vertex: index for index, vertex in enumerate(self.vertex_order)}
        return all(
            all(
                np.isclose(
                    vector[indices[vertex]],
                    vector[indices[component[0]]],
                    atol=1e-12,
                    rtol=0.0,
                )
                for vertex in component
            )
            for component in self.components
        )

    def null_space_characterization(self, values: Iterable[float]) -> tuple[bool, bool]:
        """Return both sides of Lx=0 iff x is componentwise constant."""

        vector = self._values(values)
        return self.is_null_vector(vector), self.is_componentwise_constant(vector)
