"""Renderer-independent walk counting with powers of an adjacency matrix."""

from __future__ import annotations

from numbers import Integral

import numpy as np

from engine.graph_matrix_encoding import GraphMatrixEncoding


class GraphWalkCounting:
    """Connect adjacency-matrix powers to fixed-length walks in a graph."""

    def __init__(self, encoding: GraphMatrixEncoding | None = None) -> None:
        self.encoding = GraphMatrixEncoding() if encoding is None else encoding
        if not isinstance(self.encoding, GraphMatrixEncoding):
            raise ValueError("encoding must be a GraphMatrixEncoding")

    @property
    def vertex_order(self) -> tuple[object, ...]:
        return self.encoding.vertex_order

    def _validate_vertex(self, vertex: object) -> None:
        if vertex not in self.vertex_order:
            raise ValueError("walk counting requires known vertices")

    @staticmethod
    def _validate_length(length: int) -> int:
        if isinstance(length, bool) or not isinstance(length, Integral) or length < 0:
            raise ValueError("walk length must be a nonnegative integer")
        return int(length)

    def matrix_power(self, length: int) -> np.ndarray:
        """Return A raised to ``length``, including A^0 = I."""

        exponent = self._validate_length(length)
        return np.linalg.matrix_power(self.encoding.adjacency_matrix(), exponent)

    def walk_count(self, start: object, end: object, length: int) -> int:
        """Count walks with the requested endpoints and exact edge length."""

        self._validate_vertex(start)
        self._validate_vertex(end)
        power = self.matrix_power(length)
        row = self.vertex_order.index(start)
        column = self.vertex_order.index(end)
        return int(power[row, column])

    def endpoint_counts(self, start: object, length: int) -> np.ndarray:
        """Count exact-length walks from ``start`` to every ordered endpoint."""

        self._validate_vertex(start)
        power = self.matrix_power(length)
        row = self.vertex_order.index(start)
        return power[row].copy()

    def walks(self, start: object, end: object, length: int) -> tuple[tuple[object, ...], ...]:
        """Enumerate walks for small teaching examples in vertex-order order."""

        self._validate_vertex(start)
        self._validate_vertex(end)
        steps = self._validate_length(length)
        routes: list[tuple[object, ...]] = []

        def extend(route: tuple[object, ...], remaining: int) -> None:
            if remaining == 0:
                if route[-1] == end:
                    routes.append(route)
                return
            current = route[-1]
            for candidate in self.vertex_order:
                if self.encoding.graph.is_adjacent(current, candidate):
                    extend(route + (candidate,), remaining - 1)

        extend((start,), steps)
        return tuple(routes)

