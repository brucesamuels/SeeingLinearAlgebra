"""Thin Manim adapter for displayed linear-combination geometry.

This module is intentionally renderer-specific.  It consumes an already
projected linear-combination display snapshot and owns only the corresponding
Manim ``Arrow`` mobjects.

All mathematics, coefficient interpolation, tip-to-tail geometry, and display
projection remain upstream of this adapter.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Protocol, TypeAlias

import numpy as np
from manim import Arrow, VGroup


PointLike: TypeAlias = Sequence[float] | np.ndarray
EndpointPair: TypeAlias = tuple[np.ndarray, np.ndarray]


class _ArrowDisplayLike(Protocol):
    """Structural type for one displayed arrow in a snapshot."""

    start: PointLike
    end: PointLike


class _LinearCombinationDisplaySnapshotLike(Protocol):
    """Canonical display-snapshot fields consumed by the Manim adapter."""

    display_term_segments: np.ndarray
    display_resultant_segment: np.ndarray


class ManimLinearCombinationGeometry(VGroup):
    """Own and update Manim arrows for displayed linear-combination geometry.

    Parameters
    ----------
    snapshot
        A ``LinearCombinationGeometryDisplaySnapshot`` produced by the
        renderer-independent display adapter.  Its canonical fields are
        ``display_term_segments`` with shape ``(term_count, 2,
        display_dimension)`` and ``display_resultant_segment`` with shape
        ``(2, display_dimension)``.
    term_arrow_kwargs
        Optional Manim ``Arrow`` style keyword arguments shared by all term
        arrows.  ``buff`` is fixed at zero so displayed endpoints are not
        shortened.
    resultant_arrow_kwargs
        Optional Manim ``Arrow`` style keyword arguments for the resultant.
        ``buff`` is fixed at zero.
    zero_length_epsilon
        A tiny positive display length used when a mathematical arrow has
        coincident endpoints.  This avoids unstable zero-direction arrow-tip
        geometry while keeping the arrow visually collapsed.

    Notes
    -----
    The number of term arrows is structural.  Later snapshots must contain the
    same number of terms, allowing every Manim mobject to be created exactly
    once and then updated in place.
    """

    def __init__(
        self,
        snapshot: _LinearCombinationDisplaySnapshotLike,
        *,
        term_arrow_kwargs: Mapping[str, Any] | None = None,
        resultant_arrow_kwargs: Mapping[str, Any] | None = None,
        zero_length_epsilon: float = 1.0e-8,
    ) -> None:
        if zero_length_epsilon <= 0.0:
            raise ValueError("zero_length_epsilon must be positive")

        self._zero_length_epsilon = float(zero_length_epsilon)
        self._term_arrow_kwargs = _arrow_kwargs(term_arrow_kwargs)
        self._resultant_arrow_kwargs = _arrow_kwargs(resultant_arrow_kwargs)

        term_endpoints, resultant_endpoints = _snapshot_endpoints(snapshot)

        self._term_arrows = tuple(
            self._make_arrow(start, end, self._term_arrow_kwargs)
            for start, end in term_endpoints
        )
        self._resultant_arrow = self._make_arrow(
            resultant_endpoints[0],
            resultant_endpoints[1],
            self._resultant_arrow_kwargs,
        )

        super().__init__(*self._term_arrows, self._resultant_arrow)

    @property
    def mobject(self) -> ManimLinearCombinationGeometry:
        """Return the root Manim mobject represented by this adapter."""

        return self

    @property
    def term_arrows(self) -> tuple[Arrow, ...]:
        """Return the fixed Manim term-arrow objects."""

        return self._term_arrows

    @property
    def resultant_arrow(self) -> Arrow:
        """Return the fixed Manim resultant-arrow object."""

        return self._resultant_arrow

    @property
    def term_count(self) -> int:
        """Return the structural number of linear-combination terms."""

        return len(self._term_arrows)

    def update_from_snapshot(
        self,
        snapshot: _LinearCombinationDisplaySnapshotLike,
    ) -> ManimLinearCombinationGeometry:
        """Update every existing arrow in place from a later display snapshot.

        The complete snapshot is validated before any Manim mobject is
        mutated.  A changed term count raises ``ValueError`` because adding or
        removing arrows would violate the create-once adapter contract.
        """

        term_endpoints, resultant_endpoints = _snapshot_endpoints(snapshot)
        if len(term_endpoints) != self.term_count:
            raise ValueError(
                "term-arrow count changed: "
                f"expected {self.term_count}, received {len(term_endpoints)}"
            )

        rendered_terms = tuple(
            self._renderable_endpoints(start, end)
            for start, end in term_endpoints
        )
        rendered_resultant = self._renderable_endpoints(*resultant_endpoints)

        for arrow, (start, end) in zip(
            self._term_arrows,
            rendered_terms,
            strict=True,
        ):
            arrow.put_start_and_end_on(start, end)

        self._resultant_arrow.put_start_and_end_on(*rendered_resultant)
        return self

    def _make_arrow(
        self,
        start: np.ndarray,
        end: np.ndarray,
        kwargs: Mapping[str, Any],
    ) -> Arrow:
        rendered_start, rendered_end = self._renderable_endpoints(start, end)
        return Arrow(
            start=rendered_start,
            end=rendered_end,
            **kwargs,
        )

    def _renderable_endpoints(
        self,
        start: np.ndarray,
        end: np.ndarray,
    ) -> EndpointPair:
        delta = end - start
        if np.linalg.norm(delta) > self._zero_length_epsilon:
            return start, end

        # A deterministic, visually negligible direction keeps Manim's arrow
        # geometry well-defined at a mathematically zero vector.  The same
        # Arrow instance remains available for a later nonzero update.
        rendered_end = start + np.array(
            [self._zero_length_epsilon, 0.0, 0.0],
            dtype=float,
        )
        return start, rendered_end


def _arrow_kwargs(values: Mapping[str, Any] | None) -> dict[str, Any]:
    kwargs = dict(values or {})

    if "start" in kwargs or "end" in kwargs:
        raise ValueError("Arrow start and end are supplied by the display snapshot")

    if "buff" in kwargs and float(kwargs["buff"]) != 0.0:
        raise ValueError("Arrow buff must be zero to preserve display endpoints")

    kwargs["buff"] = 0.0
    return kwargs


def _snapshot_endpoints(snapshot: object) -> tuple[tuple[EndpointPair, ...], EndpointPair]:
    """Extract endpoints from one projected display snapshot.

    Checkpoint 13's canonical ``LinearCombinationGeometryDisplaySnapshot``
    exposes ``display_term_segments`` and ``display_resultant_segment``.
    Those fields are preferred explicitly.  The endpoint-wrapper fallbacks are
    retained only for compatibility with the focused Checkpoint 14 adapter
    tests and equivalent thin display representations.
    """

    display_terms = _first_attribute(snapshot, ("display_term_segments",))
    display_resultant = _first_attribute(
        snapshot,
        ("display_resultant_segment",),
    )

    if display_terms is not _MISSING and display_resultant is not _MISSING:
        term_segments = np.asarray(display_terms, dtype=float)
        resultant_segment = np.asarray(display_resultant, dtype=float)

        if term_segments.ndim != 3 or term_segments.shape[1] != 2:
            raise ValueError(
                "display_term_segments must have shape "
                "(term_count, 2, display_dimension)"
            )
        if resultant_segment.ndim != 2 or resultant_segment.shape[0] != 2:
            raise ValueError(
                "display_resultant_segment must have shape "
                "(2, display_dimension)"
            )
        if term_segments.shape[2] != resultant_segment.shape[1]:
            raise ValueError(
                "term and resultant display dimensions must agree"
            )

        terms = tuple(_endpoint_pair(segment) for segment in term_segments)
        return terms, _endpoint_pair(resultant_segment)

    term_items = _first_attribute(
        snapshot,
        ("term_arrows", "terms", "term_segments"),
    )
    resultant_item = _first_attribute(
        snapshot,
        ("resultant_arrow", "resultant", "resultant_segment"),
    )

    if term_items is not _MISSING and resultant_item is not _MISSING:
        terms = tuple(_endpoint_pair(item) for item in term_items)
        return terms, _endpoint_pair(resultant_item)

    term_starts = _first_attribute(
        snapshot,
        ("term_starts", "term_start_points", "term_tails"),
    )
    term_ends = _first_attribute(
        snapshot,
        ("term_ends", "term_end_points", "term_tips"),
    )
    resultant_start = _first_attribute(
        snapshot,
        ("resultant_start", "resultant_start_point", "resultant_tail"),
    )
    resultant_end = _first_attribute(
        snapshot,
        ("resultant_end", "resultant_end_point", "resultant_tip"),
    )

    if all(
        value is not _MISSING
        for value in (term_starts, term_ends, resultant_start, resultant_end)
    ):
        starts = tuple(term_starts)
        ends = tuple(term_ends)
        if len(starts) != len(ends):
            raise ValueError(
                "term start/end counts differ: "
                f"received {len(starts)} starts and {len(ends)} ends"
            )
        terms = tuple(
            (_manim_point(start), _manim_point(end))
            for start, end in zip(starts, ends, strict=True)
        )
        return terms, (
            _manim_point(resultant_start),
            _manim_point(resultant_end),
        )

    raise TypeError(
        "snapshot must expose display_term_segments and "
        "display_resultant_segment"
    )

def _endpoint_pair(value: object) -> EndpointPair:
    start = _first_attribute(value, ("start", "start_point", "tail"))
    end = _first_attribute(value, ("end", "end_point", "tip"))

    if start is not _MISSING and end is not _MISSING:
        return _manim_point(start), _manim_point(end)

    if isinstance(value, np.ndarray):
        if value.ndim == 2 and value.shape[0] == 2:
            return _manim_point(value[0]), _manim_point(value[1])

    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        if len(value) == 2:
            return _manim_point(value[0]), _manim_point(value[1])

    raise TypeError("displayed arrow must expose start and end points")


def _manim_point(value: object) -> np.ndarray:
    point = np.asarray(value, dtype=float)
    if point.ndim != 1:
        raise ValueError(f"display point must be one-dimensional, received {point.shape}")

    if point.size == 2:
        point = np.append(point, 0.0)
    elif point.size != 3:
        raise ValueError(
            "Manim display points must have two or three coordinates, "
            f"received {point.size}"
        )

    if not np.all(np.isfinite(point)):
        raise ValueError("Manim display points must contain only finite values")

    return point.astype(float, copy=True)


class _Missing:
    pass


_MISSING = _Missing()


def _first_attribute(value: object, names: Sequence[str]) -> object:
    for name in names:
        if hasattr(value, name):
            return getattr(value, name)
    return _MISSING
