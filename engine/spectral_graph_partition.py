"""Renderer-independent Fiedler-vector partitioning for an undirected graph."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from engine.graph_laplacian_spectrum import GraphLaplacianSpectrum
from engine.simple_undirected_graph import SimpleUndirectedGraph


class SpectralGraphPartition:
    """Turn a Laplacian second mode into candidate two-way graph cuts."""

    def __init__(self, spectrum: GraphLaplacianSpectrum | None = None) -> None:
        self.spectrum = GraphLaplacianSpectrum() if spectrum is None else spectrum
        if not isinstance(self.spectrum, GraphLaplacianSpectrum):
            raise ValueError("spectrum must be a GraphLaplacianSpectrum")
        if len(self.spectrum.vertex_order) < 2:
            raise ValueError("spectral partitioning requires at least two vertices")
        if not self.spectrum.graph.is_connected():
            raise ValueError("spectral partitioning requires a connected graph")

    @property
    def graph(self) -> SimpleUndirectedGraph:
        return self.spectrum.graph

    @property
    def vertex_order(self) -> tuple[object, ...]:
        return self.spectrum.vertex_order

    def fiedler_vector(self) -> np.ndarray:
        vector = self.spectrum.second_mode()
        vector[np.isclose(vector, 0.0, atol=1e-12, rtol=0.0)] = 0.0
        return vector

    def _values(self, values: Iterable[float]) -> np.ndarray:
        vector = np.asarray(tuple(values), dtype=float)
        expected = (len(self.vertex_order),)
        if vector.shape != expected:
            raise ValueError(f"values must have shape {expected}")
        if not np.all(np.isfinite(vector)):
            raise ValueError("values must be finite")
        return vector

    def _partition(self, first_side: Iterable[object]) -> tuple[tuple[object, ...], tuple[object, ...]]:
        supplied = tuple(first_side)
        try:
            supplied_set = set(supplied)
        except TypeError as error:
            raise ValueError("partition vertices must be hashable") from error
        if len(supplied_set) != len(supplied):
            raise ValueError("partition side must not repeat vertices")
        known = set(self.vertex_order)
        if not supplied_set or supplied_set == known:
            raise ValueError("partition must have two nonempty sides")
        if not supplied_set <= known:
            raise ValueError("partition contains an unknown vertex")
        first = tuple(vertex for vertex in self.vertex_order if vertex in supplied_set)
        second = tuple(vertex for vertex in self.vertex_order if vertex not in supplied_set)
        return first, second

    def threshold_partition(
        self,
        values: Iterable[float],
        threshold: float = 0.0,
        *,
        equal_to_upper: bool = True,
    ) -> tuple[tuple[object, ...], tuple[object, ...]]:
        if not np.isfinite(threshold):
            raise ValueError("threshold must be finite")
        vector = self._values(values)
        if equal_to_upper:
            upper = tuple(
                vertex for vertex, value in zip(self.vertex_order, vector) if value >= threshold
            )
        else:
            upper = tuple(
                vertex for vertex, value in zip(self.vertex_order, vector) if value > threshold
            )
        return self._partition(upper)

    def sign_partition(self) -> tuple[tuple[object, ...], tuple[object, ...]]:
        """Put zero coordinates with the nonnegative Fiedler side."""

        return self.threshold_partition(self.fiedler_vector(), 0.0, equal_to_upper=True)

    def cut_edges(self, first_side: Iterable[object]) -> tuple[tuple[object, object], ...]:
        first, _ = self._partition(first_side)
        membership = set(first)
        return tuple(
            edge
            for edge in self.graph.edges
            if (edge[0] in membership) != (edge[1] in membership)
        )

    def cut_size(self, first_side: Iterable[object]) -> int:
        return len(self.cut_edges(first_side))

    def ratio_cut_score(self, first_side: Iterable[object]) -> float:
        first, second = self._partition(first_side)
        return self.cut_size(first) * (1.0 / len(first) + 1.0 / len(second))

    def balanced_partition_signal(self, first_side: Iterable[object]) -> np.ndarray:
        first, second = self._partition(first_side)
        first_set = set(first)
        return np.array(
            [
                1.0 / len(first) if vertex in first_set else -1.0 / len(second)
                for vertex in self.vertex_order
            ]
        )

    def partition_rayleigh_quotient(self, first_side: Iterable[object]) -> float:
        return self.spectrum.rayleigh_quotient(self.balanced_partition_signal(first_side))

    def sweep_partitions(self) -> tuple[tuple[tuple[object, ...], tuple[object, ...]], ...]:
        vector = self.fiedler_vector()
        indices = sorted(range(len(self.vertex_order)), key=lambda index: (vector[index], index))
        ordered = tuple(self.vertex_order[index] for index in indices)
        return tuple(
            self._partition(ordered[:cut])
            for cut in range(1, len(ordered))
            if not np.isclose(
                vector[indices[cut - 1]],
                vector[indices[cut]],
                atol=1e-12,
                rtol=0.0,
            )
        )

    def sweep_scores(self) -> tuple[float, ...]:
        return tuple(self.ratio_cut_score(first) for first, _ in self.sweep_partitions())

    def best_sweep_partition(self) -> tuple[tuple[object, ...], tuple[object, ...]]:
        candidates = self.sweep_partitions()
        return min(candidates, key=lambda partition: self.ratio_cut_score(partition[0]))
