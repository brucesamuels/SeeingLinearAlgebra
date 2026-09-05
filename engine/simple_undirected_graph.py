"""Renderer-independent model for a finite simple undirected graph."""

from __future__ import annotations

from collections.abc import Hashable, Iterable, Sequence


class SimpleUndirectedGraph:
    """Store vertices and unordered edges with introductory graph operations."""

    def __init__(self, vertices: Iterable[Hashable], edges: Iterable[Sequence[Hashable]]):
        self._vertices = tuple(vertices)
        if not self._vertices:
            raise ValueError("vertices must be nonempty")
        try:
            vertex_set = set(self._vertices)
        except TypeError as error:
            raise ValueError("vertices must be hashable") from error
        if len(vertex_set) != len(self._vertices):
            raise ValueError("vertices must be unique")

        order = {vertex: index for index, vertex in enumerate(self._vertices)}
        normalized_edges = []
        seen = set()
        for edge in edges:
            pair = tuple(edge)
            if len(pair) != 2:
                raise ValueError("each edge must have exactly two endpoints")
            first, second = pair
            if first not in vertex_set or second not in vertex_set:
                raise ValueError("edge endpoints must be vertices of the graph")
            if first == second:
                raise ValueError("simple graphs do not allow loops")
            key = frozenset((first, second))
            if key in seen:
                raise ValueError("simple graphs do not allow repeated undirected edges")
            seen.add(key)
            if order[first] > order[second]:
                first, second = second, first
            normalized_edges.append((first, second))

        self._edges = tuple(normalized_edges)
        self._edge_keys = frozenset(seen)
        self._neighbors = {
            vertex: tuple(
                candidate
                for candidate in self._vertices
                if frozenset((vertex, candidate)) in self._edge_keys
            )
            for vertex in self._vertices
        }

    @property
    def vertices(self) -> tuple[Hashable, ...]:
        return self._vertices

    @property
    def edges(self) -> tuple[tuple[Hashable, Hashable], ...]:
        return self._edges

    def neighbors(self, vertex: Hashable) -> tuple[Hashable, ...]:
        self._require_vertex(vertex)
        return self._neighbors[vertex]

    def degree(self, vertex: Hashable) -> int:
        return len(self.neighbors(vertex))

    def degree_sequence(self) -> tuple[int, ...]:
        return tuple(self.degree(vertex) for vertex in self._vertices)

    def is_adjacent(self, first: Hashable, second: Hashable) -> bool:
        self._require_vertex(first)
        self._require_vertex(second)
        return frozenset((first, second)) in self._edge_keys

    def is_walk(self, sequence: Iterable[Hashable]) -> bool:
        route = tuple(sequence)
        if not route or any(vertex not in self._neighbors for vertex in route):
            return False
        return all(self.is_adjacent(first, second) for first, second in zip(route, route[1:]))

    def walk_length(self, sequence: Iterable[Hashable]) -> int:
        route = tuple(sequence)
        if not self.is_walk(route):
            raise ValueError("sequence must be a walk in the graph")
        return len(route) - 1

    def is_path(self, sequence: Iterable[Hashable]) -> bool:
        route = tuple(sequence)
        return self.is_walk(route) and len(route) == len(set(route))

    def connected_components(self) -> tuple[tuple[Hashable, ...], ...]:
        unseen = set(self._vertices)
        components = []
        for start in self._vertices:
            if start not in unseen:
                continue
            unseen.remove(start)
            queue = [start]
            reached = {start}
            while queue:
                vertex = queue.pop(0)
                for neighbor in self._neighbors[vertex]:
                    if neighbor in unseen:
                        unseen.remove(neighbor)
                        reached.add(neighbor)
                        queue.append(neighbor)
            components.append(tuple(vertex for vertex in self._vertices if vertex in reached))
        return tuple(components)

    def is_connected(self) -> bool:
        return len(self.connected_components()) == 1

    def without_edge(self, edge: Sequence[Hashable]) -> "SimpleUndirectedGraph":
        pair = tuple(edge)
        if len(pair) != 2:
            raise ValueError("edge must have exactly two endpoints")
        key = frozenset(pair)
        if key not in self._edge_keys:
            raise ValueError("edge is not present in the graph")
        remaining = [candidate for candidate in self._edges if frozenset(candidate) != key]
        return SimpleUndirectedGraph(self._vertices, remaining)

    def _require_vertex(self, vertex: Hashable) -> None:
        try:
            present = vertex in self._neighbors
        except TypeError as error:
            raise ValueError("vertex must be hashable") from error
        if not present:
            raise ValueError("unknown vertex")


def triangle_with_tail_graph() -> SimpleUndirectedGraph:
    """Return the four-vertex numerical spine for the graph chapter."""

    return SimpleUndirectedGraph(
        vertices=(1, 2, 3, 4),
        edges=((1, 2), (2, 3), (1, 3), (3, 4)),
    )
