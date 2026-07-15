"""Thin Manim adapter for displayed linear-combination traces.

This renderer-specific module consumes an already projected
``LinearCombinationTraceDisplaySnapshot`` and creates one Manim ``Line`` for
 each consecutive resultant-tip segment.  All coefficient sampling,
mathematical trace construction, and display projection remain upstream.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Protocol, TypeAlias

import numpy as np
from manim import Line, VGroup


PointLike: TypeAlias = Sequence[float] | np.ndarray
EndpointPair: TypeAlias = tuple[np.ndarray, np.ndarray]


class _LinearCombinationTraceDisplaySnapshotLike(Protocol):
    """Canonical display-snapshot field consumed by the Manim adapter."""

    display_resultant_segments: np.ndarray


class ManimLinearCombinationTrace(VGroup):
    """Own fixed Manim lines for one projected resultant trace.

    Parameters
    ----------
    snapshot:
        A ``LinearCombinationTraceDisplaySnapshot`` produced by the
        renderer-independent display adapter.  Its canonical
        ``display_resultant_segments`` field has shape
        ``(segment_count, 2, display_dimension)``.
    segment_kwargs:
        Optional Manim ``Line`` style keyword arguments shared by every trace
        segment.  ``start`` and ``end`` are supplied by the snapshot.  ``buff``
        is fixed at zero so displayed endpoints are preserved exactly.

    Notes
    -----
    This checkpoint intentionally represents a completed trace.  The line
    mobjects are created once and are not updated from later snapshots.
    """

    def __init__(
        self,
        snapshot: _LinearCombinationTraceDisplaySnapshotLike,
        *,
        segment_kwargs: Mapping[str, Any] | None = None,
    ) -> None:
        endpoints = _snapshot_endpoints(snapshot)
        kwargs = _line_kwargs(segment_kwargs)

        self._snapshot = snapshot
        self._segment_lines = tuple(
            Line(start=start, end=end, **kwargs) for start, end in endpoints
        )

        super().__init__(*self._segment_lines)

    @property
    def mobject(self) -> ManimLinearCombinationTrace:
        """Return the root Manim mobject represented by this adapter."""

        return self

    @property
    def snapshot(self) -> _LinearCombinationTraceDisplaySnapshotLike:
        """Return the exact display snapshot used to build the trace."""

        return self._snapshot

    @property
    def segment_lines(self) -> tuple[Line, ...]:
        """Return the fixed Manim line objects in trace order."""

        return self._segment_lines

    @property
    def segment_count(self) -> int:
        """Return the number of consecutive trace segments."""

        return len(self._segment_lines)


def _line_kwargs(values: Mapping[str, Any] | None) -> dict[str, Any]:
    """Validate shared Manim ``Line`` style arguments."""

    kwargs = dict(values or {})
    if "start" in kwargs or "end" in kwargs:
        raise ValueError("Line start and end are supplied by the display snapshot")
    if "buff" in kwargs and float(kwargs["buff"]) != 0.0:
        raise ValueError("Line buff must be zero to preserve display endpoints")
    kwargs["buff"] = 0.0
    return kwargs


def _snapshot_endpoints(snapshot: object) -> tuple[EndpointPair, ...]:
    """Extract canonical display trace segments and convert them for Manim."""

    if not hasattr(snapshot, "display_resultant_segments"):
        raise TypeError("snapshot must expose display_resultant_segments")

    segments = np.asarray(snapshot.display_resultant_segments, dtype=float)
    if segments.ndim != 3 or segments.shape[1] != 2:
        raise ValueError(
            "display_resultant_segments must have shape "
            "(segment_count, 2, display_dimension)"
        )

    display_dimension = int(segments.shape[2])
    if display_dimension < 1 or display_dimension > 3:
        raise ValueError(
            "Manim display segments must have one, two, or three coordinates"
        )
    if not np.all(np.isfinite(segments)):
        raise ValueError(
            "display_resultant_segments must contain only finite values"
        )

    return tuple(
        (_manim_point(segment[0]), _manim_point(segment[1]))
        for segment in segments
    )


def _manim_point(value: PointLike) -> np.ndarray:
    """Return an owned three-coordinate point accepted by Manim."""

    point = np.asarray(value, dtype=float)
    if point.ndim != 1:
        raise ValueError("display points must be one-dimensional")
    if point.size < 1 or point.size > 3:
        raise ValueError(
            "Manim display points must have one, two, or three coordinates"
        )
    if not np.all(np.isfinite(point)):
        raise ValueError("Manim display points must contain only finite values")

    result = np.zeros(3, dtype=float)
    result[: point.size] = point
    return result
