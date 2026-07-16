"""Thin native-3D Manim adapter for displayed linear-combination geometry.

The adapter consumes the canonical projected display snapshot and owns stable
``Arrow3D`` objects.  Native cylindrical arrows are rebuilt internally and
copied into the existing owning objects with ``become`` because transforming an
existing ``Arrow3D`` with ``put_start_and_end_on`` does not reliably synchronize
its stored start/end attributes.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Protocol

import numpy as np
from manim import Arrow3D, VGroup

from engine.manim_linear_combination_geometry import _snapshot_endpoints


class _LinearCombinationDisplaySnapshotLike(Protocol):
    display_term_segments: np.ndarray
    display_resultant_segment: np.ndarray


class ManimLinearCombinationGeometry3D(VGroup):
    """Own and update native Manim ``Arrow3D`` objects."""

    def __init__(
        self,
        snapshot: _LinearCombinationDisplaySnapshotLike,
        *,
        term_arrow_kwargs: (
            Mapping[str, Any]
            | Sequence[Mapping[str, Any]]
            | None
        ) = None,
        resultant_arrow_kwargs: Mapping[str, Any] | None = None,
        zero_length_epsilon: float = 1.0e-8,
    ) -> None:
        if zero_length_epsilon <= 0.0:
            raise ValueError("zero_length_epsilon must be positive")

        self._zero_length_epsilon = float(zero_length_epsilon)

        term_endpoints, resultant_endpoints = _snapshot_endpoints(snapshot)
        self._term_arrow_kwargs = _term_arrow3d_kwargs(
            term_arrow_kwargs,
            len(term_endpoints),
        )
        self._resultant_arrow_kwargs = _arrow3d_kwargs(
            resultant_arrow_kwargs,
        )
        _require_three_dimensions(term_endpoints, resultant_endpoints)

        self._term_arrows = tuple(
            self._make_arrow(start, end, kwargs)
            for (start, end), kwargs in zip(
                term_endpoints,
                self._term_arrow_kwargs,
                strict=True,
            )
        )
        self._resultant_arrow = self._make_arrow(
            resultant_endpoints[0],
            resultant_endpoints[1],
            self._resultant_arrow_kwargs,
        )

        super().__init__(*self._term_arrows, self._resultant_arrow)

    @property
    def mobject(self) -> "ManimLinearCombinationGeometry3D":
        return self

    @property
    def term_arrows(self) -> tuple[Arrow3D, ...]:
        return self._term_arrows

    @property
    def resultant_arrow(self) -> Arrow3D:
        return self._resultant_arrow

    @property
    def term_count(self) -> int:
        return len(self._term_arrows)

    def update_from_snapshot(
        self,
        snapshot: _LinearCombinationDisplaySnapshotLike,
    ) -> "ManimLinearCombinationGeometry3D":
        term_endpoints, resultant_endpoints = _snapshot_endpoints(snapshot)
        _require_three_dimensions(term_endpoints, resultant_endpoints)

        if len(term_endpoints) != self.term_count:
            raise ValueError(
                "term-arrow count changed: "
                f"expected {self.term_count}, received {len(term_endpoints)}"
            )

        rendered_terms = tuple(
            self._renderable_endpoints(start, end)
            for start, end in term_endpoints
        )
        rendered_resultant = self._renderable_endpoints(
            *resultant_endpoints,
        )

        replacements = tuple(
            self._replacement_arrow(
                start,
                end,
                kwargs,
            )
            for (start, end), kwargs in zip(
                rendered_terms,
                self._term_arrow_kwargs,
                strict=True,
            )
        )
        replacement_resultant = self._replacement_arrow(
            rendered_resultant[0],
            rendered_resultant[1],
            self._resultant_arrow_kwargs,
        )

        # All replacements are constructed successfully before any owner mutates.
        for arrow, replacement, (start, end) in zip(
            self._term_arrows,
            replacements,
            rendered_terms,
            strict=True,
        ):
            arrow.become(replacement)
            arrow.set_start_and_end_attrs(start, end)

        self._resultant_arrow.become(replacement_resultant)
        self._resultant_arrow.set_start_and_end_attrs(
            rendered_resultant[0],
            rendered_resultant[1],
        )
        return self

    def _make_arrow(
        self,
        start: np.ndarray,
        end: np.ndarray,
        kwargs: Mapping[str, Any],
    ) -> Arrow3D:
        rendered_start, rendered_end = self._renderable_endpoints(start, end)
        return Arrow3D(
            start=rendered_start,
            end=rendered_end,
            **kwargs,
        )

    def _replacement_arrow(
        self,
        start: np.ndarray,
        end: np.ndarray,
        kwargs: Mapping[str, Any],
    ) -> Arrow3D:
        return Arrow3D(start=start, end=end, **kwargs)

    def _renderable_endpoints(
        self,
        start: np.ndarray,
        end: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        if np.linalg.norm(end - start) > self._zero_length_epsilon:
            return start, end

        rendered_end = start + np.array(
            [self._zero_length_epsilon, 0.0, 0.0],
            dtype=float,
        )
        return start, rendered_end



def _term_arrow3d_kwargs(
    values: Mapping[str, Any] | Sequence[Mapping[str, Any]] | None,
    term_count: int,
) -> tuple[dict[str, Any], ...]:
    if values is None or isinstance(values, Mapping):
        shared = _arrow3d_kwargs(values)
        return tuple(dict(shared) for _ in range(term_count))

    options = tuple(_arrow3d_kwargs(value) for value in values)
    if len(options) != term_count:
        raise ValueError(
            "term_arrow_kwargs count changed: "
            f"expected {term_count}, received {len(options)}"
        )
    return options


def _arrow3d_kwargs(values: Mapping[str, Any] | None) -> dict[str, Any]:
    kwargs = dict(values or {})
    if "start" in kwargs or "end" in kwargs:
        raise ValueError(
            "Arrow3D start and end are supplied by the display snapshot"
        )
    return kwargs


def _require_three_dimensions(
    term_endpoints: tuple[tuple[np.ndarray, np.ndarray], ...],
    resultant_endpoints: tuple[np.ndarray, np.ndarray],
) -> None:
    endpoints = [
        point
        for segment in (*term_endpoints, resultant_endpoints)
        for point in segment
    ]
    if any(point.shape != (3,) for point in endpoints):
        raise ValueError(
            "native 3D geometry requires three-coordinate display points"
        )
