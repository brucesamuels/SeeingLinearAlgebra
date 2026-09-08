"""Renderer-independent PageRank model for a finite directed graph."""

from __future__ import annotations

from collections.abc import Hashable, Iterable, Sequence
from numbers import Integral, Real

import numpy as np


class DirectedPageRank:
    """Encode directed links with column probability vectors and teleportation."""

    DEFAULT_VERTICES = (1, 2, 3, 4)
    DEFAULT_EDGES = ((1, 2), (2, 3), (3, 1), (3, 4))

    def __init__(
        self,
        vertices: Iterable[Hashable] = DEFAULT_VERTICES,
        directed_edges: Iterable[Sequence[Hashable]] = DEFAULT_EDGES,
    ) -> None:
        self._vertices = tuple(vertices)
        if not self._vertices:
            raise ValueError("vertices must be nonempty")
        try:
            vertex_set = set(self._vertices)
        except TypeError as error:
            raise ValueError("vertices must be hashable") from error
        if len(vertex_set) != len(self._vertices):
            raise ValueError("vertices must be unique")

        edges = []
        seen = set()
        for directed_edge in directed_edges:
            pair = tuple(directed_edge)
            if len(pair) != 2:
                raise ValueError("each directed edge must have a source and destination")
            source, destination = pair
            try:
                known_endpoints = source in vertex_set and destination in vertex_set
            except TypeError as error:
                raise ValueError("directed edge endpoints must be known vertices") from error
            if not known_endpoints:
                raise ValueError("directed edge endpoints must be known vertices")
            if source == destination:
                raise ValueError("this directed graph does not allow loops")
            if pair in seen:
                raise ValueError("directed edges must be unique")
            seen.add(pair)
            edges.append(pair)

        self._edges = tuple(edges)
        self._index = {vertex: index for index, vertex in enumerate(self._vertices)}

    @property
    def vertices(self) -> tuple[Hashable, ...]:
        return self._vertices

    @property
    def directed_edges(self) -> tuple[tuple[Hashable, Hashable], ...]:
        return self._edges

    def out_neighbors(self, vertex: Hashable) -> tuple[Hashable, ...]:
        self._require_vertex(vertex)
        return tuple(destination for source, destination in self._edges if source == vertex)

    def in_neighbors(self, vertex: Hashable) -> tuple[Hashable, ...]:
        self._require_vertex(vertex)
        return tuple(source for source, destination in self._edges if destination == vertex)

    def out_degree(self, vertex: Hashable) -> int:
        return len(self.out_neighbors(vertex))

    def out_degree_vector(self) -> np.ndarray:
        return np.array([self.out_degree(vertex) for vertex in self._vertices], dtype=int)

    def dangling_vertices(self) -> tuple[Hashable, ...]:
        return tuple(vertex for vertex in self._vertices if self.out_degree(vertex) == 0)

    def adjacency_matrix(self) -> np.ndarray:
        """Return A with A[i,j]=1 when the directed link is j -> i."""

        matrix = np.zeros((len(self._vertices), len(self._vertices)), dtype=int)
        for source, destination in self._edges:
            matrix[self._index[destination], self._index[source]] = 1
        return matrix

    def raw_link_matrix(self) -> np.ndarray:
        """Normalize non-dangling adjacency columns; leave dangling columns zero."""

        matrix = self.adjacency_matrix().astype(float)
        degrees = self.out_degree_vector()
        for column, degree in enumerate(degrees):
            if degree:
                matrix[:, column] /= degree
        return matrix

    def uniform_distribution(self) -> np.ndarray:
        return np.full(len(self._vertices), 1.0 / len(self._vertices))

    def repaired_link_matrix(self) -> np.ndarray:
        """Replace each dangling column by the uniform distribution."""

        matrix = self.raw_link_matrix()
        for vertex in self.dangling_vertices():
            matrix[:, self._index[vertex]] = self.uniform_distribution()
        return matrix

    def teleportation_matrix(self) -> np.ndarray:
        size = len(self._vertices)
        return np.full((size, size), 1.0 / size)

    @staticmethod
    def _damping(value: float) -> float:
        if isinstance(value, bool) or not isinstance(value, Real):
            raise ValueError("damping must be a real number in [0,1)")
        damping = float(value)
        if not np.isfinite(damping) or not 0 <= damping < 1:
            raise ValueError("damping must be a real number in [0,1)")
        return damping

    def google_matrix(self, damping: float = 0.5) -> np.ndarray:
        alpha = self._damping(damping)
        return (
            alpha * self.repaired_link_matrix()
            + (1.0 - alpha) * self.teleportation_matrix()
        )

    def column_sums(self, damping: float = 0.5) -> np.ndarray:
        return self.google_matrix(damping).sum(axis=0)

    def _distribution(self, values: Iterable[float]) -> np.ndarray:
        vector = np.asarray(tuple(values), dtype=float)
        expected = (len(self._vertices),)
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

    def next_distribution(
        self,
        distribution: Iterable[float],
        damping: float = 0.5,
    ) -> np.ndarray:
        return self.google_matrix(damping) @ self._distribution(distribution)

    def trajectory(
        self,
        distribution: Iterable[float],
        steps: int,
        damping: float = 0.5,
    ) -> tuple[np.ndarray, ...]:
        if isinstance(steps, bool) or not isinstance(steps, Integral) or steps < 0:
            raise ValueError("steps must be a nonnegative integer")
        count = int(steps)
        state = self._distribution(distribution)
        states = [state]
        for _ in range(count):
            state = self.next_distribution(state, damping)
            states.append(state)
        return tuple(item.copy() for item in states)

    def page_rank(self, damping: float = 0.5) -> np.ndarray:
        alpha = self._damping(damping)
        size = len(self._vertices)
        right_hand_side = (1.0 - alpha) * self.uniform_distribution()
        rank = np.linalg.solve(
            np.eye(size) - alpha * self.repaired_link_matrix(),
            right_hand_side,
        )
        rank /= rank.sum()
        return rank

    def stationary_residual(self, damping: float = 0.5) -> np.ndarray:
        rank = self.page_rank(damping)
        return self.google_matrix(damping) @ rank - rank

    def rank_order(self, damping: float = 0.5) -> tuple[tuple[Hashable, ...], ...]:
        """Return descending rank groups, preserving vertex order inside ties."""

        rank = self.page_rank(damping)
        remaining = list(range(len(self._vertices)))
        groups = []
        while remaining:
            best = max(rank[index] for index in remaining)
            tied = [index for index in remaining if np.isclose(rank[index], best)]
            groups.append(tuple(self._vertices[index] for index in tied))
            remaining = [index for index in remaining if index not in tied]
        return tuple(groups)

    def total_variation_distance(
        self,
        first: Iterable[float],
        second: Iterable[float],
    ) -> float:
        left = self._distribution(first)
        right = self._distribution(second)
        return 0.5 * float(np.abs(left - right).sum())

    def _require_vertex(self, vertex: Hashable) -> None:
        try:
            present = vertex in self._index
        except TypeError as error:
            raise ValueError("vertex must be hashable") from error
        if not present:
            raise ValueError("unknown vertex")
