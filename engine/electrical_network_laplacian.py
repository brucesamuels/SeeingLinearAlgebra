"""Renderer-independent unit-resistance electrical network on a graph."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from engine.graph_incidence_encoding import GraphIncidenceEncoding
from engine.graph_laplacian_energy import GraphLaplacianEnergy
from engine.graph_laplacian_operator import GraphLaplacianOperator
from engine.graph_matrix_encoding import GraphMatrixEncoding
from engine.simple_undirected_graph import SimpleUndirectedGraph, triangle_with_tail_graph


class ElectricalNetworkLaplacian:
    """Solve Kirchhoff equations when every graph edge has resistance one."""

    def __init__(self, graph: SimpleUndirectedGraph | None = None) -> None:
        self.graph = triangle_with_tail_graph() if graph is None else graph
        if not isinstance(self.graph, SimpleUndirectedGraph):
            raise ValueError("graph must be a SimpleUndirectedGraph")
        if not self.graph.is_connected():
            raise ValueError("electrical network graph must be connected")
        encoding = GraphMatrixEncoding(self.graph)
        incidence = GraphIncidenceEncoding(encoding)
        self.laplacian = GraphLaplacianOperator(incidence)
        self.energy = GraphLaplacianEnergy(self.laplacian)

    @property
    def vertex_order(self) -> tuple[object, ...]:
        return self.laplacian.vertex_order

    @property
    def oriented_edges(self) -> tuple[tuple[object, object], ...]:
        return self.laplacian.oriented_edges

    def _vertex_vector(self, values: Iterable[float], name: str) -> np.ndarray:
        vector = np.asarray(tuple(values), dtype=float)
        expected = (len(self.vertex_order),)
        if vector.shape != expected:
            raise ValueError(f"{name} must have shape {expected}")
        if not np.all(np.isfinite(vector)):
            raise ValueError(f"{name} must be finite")
        return vector

    def potentials(self, values: Iterable[float]) -> np.ndarray:
        return self._vertex_vector(values, "potentials")

    def injections(self, values: Iterable[float]) -> np.ndarray:
        return self._vertex_vector(values, "injections")

    def oriented_currents(self, potentials: Iterable[float]) -> np.ndarray:
        """Return signed current from each stored tail to its stored head."""

        voltage = self.potentials(potentials)
        return -self.laplacian.edge_differences(voltage)

    def current_on_edge(
        self,
        first: object,
        second: object,
        potentials: Iterable[float],
    ) -> float:
        """Return signed current from first to second for a unit resistor."""

        if first not in self.vertex_order or second not in self.vertex_order:
            raise ValueError("current requires known vertices")
        if not self.graph.is_adjacent(first, second):
            raise ValueError("current requires an edge")
        voltage = self.potentials(potentials)
        indices = {vertex: index for index, vertex in enumerate(self.vertex_order)}
        return float(voltage[indices[first]] - voltage[indices[second]])

    def net_outflow(self, potentials: Iterable[float]) -> np.ndarray:
        """Return the sum of outward edge currents at each vertex."""

        return self.laplacian.apply(self.potentials(potentials))

    def compatible_injections(self, injections: Iterable[float]) -> bool:
        current = self.injections(injections)
        return bool(np.isclose(current.sum(), 0.0, atol=1e-12, rtol=0.0))

    def is_kirchhoff_solution(
        self,
        potentials: Iterable[float],
        injections: Iterable[float],
    ) -> bool:
        voltage = self.potentials(potentials)
        current = self.injections(injections)
        return bool(np.allclose(self.net_outflow(voltage), current, atol=1e-10, rtol=0.0))

    def solve_potentials(
        self,
        injections: Iterable[float],
        *,
        reference_vertex: object,
        reference_potential: float = 0.0,
    ) -> np.ndarray:
        current = self.injections(injections)
        if not self.compatible_injections(current):
            raise ValueError("injections must sum to zero")
        if reference_vertex not in self.vertex_order:
            raise ValueError("reference_vertex must be a known vertex")
        if not np.isfinite(reference_potential):
            raise ValueError("reference_potential must be finite")

        reference = self.vertex_order.index(reference_vertex)
        keep = [index for index in range(len(self.vertex_order)) if index != reference]
        matrix = self.laplacian.laplacian_matrix().astype(float)
        reduced = matrix[np.ix_(keep, keep)]
        right_side = current[keep] - matrix[keep, reference] * float(reference_potential)
        voltage = np.empty(len(self.vertex_order), dtype=float)
        voltage[reference] = float(reference_potential)
        voltage[keep] = np.linalg.solve(reduced, right_side)
        return voltage

    def source_sink_injections(
        self,
        source: object,
        sink: object,
        current: float = 1.0,
    ) -> np.ndarray:
        if source not in self.vertex_order or sink not in self.vertex_order:
            raise ValueError("source and sink must be known vertices")
        if source == sink:
            raise ValueError("source and sink must be distinct")
        if not np.isfinite(current) or current <= 0:
            raise ValueError("current must be positive and finite")
        injections = np.zeros(len(self.vertex_order), dtype=float)
        injections[self.vertex_order.index(source)] = float(current)
        injections[self.vertex_order.index(sink)] = -float(current)
        return injections

    def solve_source_sink(
        self,
        source: object,
        sink: object,
        current: float = 1.0,
        *,
        reference_potential: float = 0.0,
    ) -> np.ndarray:
        injections = self.source_sink_injections(source, sink, current)
        return self.solve_potentials(
            injections,
            reference_vertex=sink,
            reference_potential=reference_potential,
        )

    def gauge_shift(self, potentials: Iterable[float], shift: float) -> np.ndarray:
        if not np.isfinite(shift):
            raise ValueError("shift must be finite")
        return self.potentials(potentials) + float(shift)

    def dissipated_power(self, potentials: Iterable[float]) -> float:
        currents = self.oriented_currents(potentials)
        return float(currents @ currents)

    def supplied_power(
        self,
        potentials: Iterable[float],
        injections: Iterable[float],
    ) -> float:
        voltage = self.potentials(potentials)
        current = self.injections(injections)
        return float(current @ voltage)

    def energy_balance(
        self,
        potentials: Iterable[float],
        injections: Iterable[float],
    ) -> tuple[float, float, float]:
        voltage = self.potentials(potentials)
        current = self.injections(injections)
        return (
            self.energy.quadratic_energy(voltage),
            self.dissipated_power(voltage),
            self.supplied_power(voltage, current),
        )

    def effective_resistance(self, source: object, sink: object) -> float:
        voltage = self.solve_source_sink(source, sink, 1.0)
        indices = {vertex: index for index, vertex in enumerate(self.vertex_order)}
        return float(voltage[indices[source]] - voltage[indices[sink]])
