"""Thin Manim geometry adapter for :mod:`engine.one_vector_span`."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

import numpy as np
from manim import Arrow, Dot, VGroup

from engine.one_vector_span import OneVectorSpanSnapshot


PointMapper = Callable[[np.ndarray], np.ndarray]


class ManimOneVectorSpan:
    """Own one identity-preserving arrow and endpoint marker.

    The adapter consumes already-computed snapshots.  It does not multiply the
    generator, choose coefficients, control animation timing, or introduce the
    mathematical term ``span``.
    """

    ZERO_EPSILON = 1.0e-7

    def __init__(
        self,
        snapshot: OneVectorSpanSnapshot,
        point_mapper: PointMapper,
        *,
        arrow_kwargs: Mapping[str, Any] | None = None,
        dot_kwargs: Mapping[str, Any] | None = None,
    ) -> None:
        if not callable(point_mapper):
            raise TypeError("point_mapper must be callable")
        self._point_mapper = point_mapper
        self._dimension = snapshot.dimension
        self._arrow_kwargs = dict(arrow_kwargs or {})
        self._dot_kwargs = dict(dot_kwargs or {})

        origin = self._map(np.zeros(self._dimension, dtype=float))
        endpoint = self._map(snapshot.endpoint)
        safe_endpoint = self._safe_endpoint(origin, endpoint)

        self.arrow = Arrow(origin, safe_endpoint, buff=0.0, **self._arrow_kwargs)
        self.endpoint_dot = Dot(endpoint, **self._dot_kwargs)
        self.mobject = VGroup(self.arrow, self.endpoint_dot)
        self._snapshot = snapshot
        self.update_from_snapshot(snapshot)

    @property
    def snapshot(self) -> OneVectorSpanSnapshot:
        return self._snapshot

    @property
    def dimension(self) -> int:
        return self._dimension

    def update_from_snapshot(self, snapshot: OneVectorSpanSnapshot) -> None:
        if snapshot.dimension != self._dimension:
            raise ValueError("snapshot dimension cannot change during an update")

        origin = self._map(np.zeros(self._dimension, dtype=float))
        endpoint = self._map(snapshot.endpoint)
        distance = float(np.linalg.norm(endpoint - origin))
        safe_endpoint = self._safe_endpoint(origin, endpoint)

        self.arrow.put_start_and_end_on(origin, safe_endpoint)
        self.arrow.set_opacity(0.0 if distance <= self.ZERO_EPSILON else 1.0)
        self.endpoint_dot.move_to(endpoint)
        self._snapshot = snapshot

    def _map(self, coordinates: np.ndarray) -> np.ndarray:
        point = np.asarray(self._point_mapper(coordinates.copy()), dtype=float)
        if point.shape != (3,):
            raise ValueError("point_mapper must return one three-coordinate point")
        if not np.all(np.isfinite(point)):
            raise ValueError("point_mapper returned a nonfinite point")
        return point

    @classmethod
    def _safe_endpoint(cls, origin: np.ndarray, endpoint: np.ndarray) -> np.ndarray:
        if float(np.linalg.norm(endpoint - origin)) > cls.ZERO_EPSILON:
            return endpoint
        return origin + np.array([cls.ZERO_EPSILON, 0.0, 0.0])
