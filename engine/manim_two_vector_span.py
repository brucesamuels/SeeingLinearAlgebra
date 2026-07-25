"""Thin Manim adapters for :mod:`engine.two_vector_span`."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

import numpy as np
from manim import Arrow, Dot, Line, VGroup

from engine.two_vector_span import FixedCoefficientLineSnapshot, TwoVectorSpanSnapshot


PointMapper = Callable[[np.ndarray], np.ndarray]


class ManimTwoVectorCombination:
    """Identity-preserving resultant arrow and endpoint marker."""

    ZERO_EPSILON = 1.0e-7

    def __init__(
        self,
        snapshot: TwoVectorSpanSnapshot,
        point_mapper: PointMapper,
        *,
        arrow_kwargs: Mapping[str, Any] | None = None,
        dot_kwargs: Mapping[str, Any] | None = None,
    ) -> None:
        if not callable(point_mapper):
            raise TypeError("point_mapper must be callable")
        self._point_mapper = point_mapper
        self._dimension = snapshot.dimension
        origin = self._map(np.zeros(self._dimension, dtype=float))
        endpoint = self._map(snapshot.endpoint)
        self.arrow = Arrow(
            origin,
            self._safe_endpoint(origin, endpoint),
            buff=0.0,
            **dict(arrow_kwargs or {}),
        )
        self.endpoint_dot = Dot(endpoint, **dict(dot_kwargs or {}))
        self.mobject = VGroup(self.arrow, self.endpoint_dot)
        self._snapshot = snapshot
        self.update_from_snapshot(snapshot)

    @property
    def snapshot(self) -> TwoVectorSpanSnapshot:
        return self._snapshot

    def update_from_snapshot(self, snapshot: TwoVectorSpanSnapshot) -> None:
        if snapshot.dimension != self._dimension:
            raise ValueError("snapshot dimension cannot change during an update")
        origin = self._map(np.zeros(self._dimension, dtype=float))
        endpoint = self._map(snapshot.endpoint)
        distance = float(np.linalg.norm(endpoint - origin))
        self.arrow.put_start_and_end_on(origin, self._safe_endpoint(origin, endpoint))
        self.arrow.set_opacity(0.0 if distance <= self.ZERO_EPSILON else 1.0)
        self.endpoint_dot.move_to(endpoint)
        self._snapshot = snapshot

    def _map(self, coordinates: np.ndarray) -> np.ndarray:
        point = np.asarray(self._point_mapper(coordinates.copy()), dtype=float)
        if point.shape != (3,) or not np.all(np.isfinite(point)):
            raise ValueError("point_mapper must return one finite three-coordinate point")
        return point

    @classmethod
    def _safe_endpoint(cls, origin: np.ndarray, endpoint: np.ndarray) -> np.ndarray:
        if float(np.linalg.norm(endpoint - origin)) > cls.ZERO_EPSILON:
            return endpoint
        return origin + np.array([cls.ZERO_EPSILON, 0.0, 0.0])


class ManimFixedCoefficientLine:
    """Identity-preserving line adapter for fixed ``a`` and varying ``b``."""

    def __init__(
        self,
        snapshot: FixedCoefficientLineSnapshot,
        point_mapper: PointMapper,
        *,
        line_kwargs: Mapping[str, Any] | None = None,
    ) -> None:
        if not callable(point_mapper):
            raise TypeError("point_mapper must be callable")
        self._point_mapper = point_mapper
        self.line = Line(
            self._map(snapshot.start),
            self._map(snapshot.end),
            **dict(line_kwargs or {}),
        )
        self._snapshot = snapshot

    @property
    def snapshot(self) -> FixedCoefficientLineSnapshot:
        return self._snapshot

    def update_from_snapshot(self, snapshot: FixedCoefficientLineSnapshot) -> None:
        self.line.put_start_and_end_on(self._map(snapshot.start), self._map(snapshot.end))
        self._snapshot = snapshot

    def _map(self, coordinates: np.ndarray) -> np.ndarray:
        point = np.asarray(self._point_mapper(coordinates.copy()), dtype=float)
        if point.shape != (3,) or not np.all(np.isfinite(point)):
            raise ValueError("point_mapper must return one finite three-coordinate point")
        return point
