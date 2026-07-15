"""Reusable Manim labels for displayed linear-combination geometry.

This renderer-specific adapter owns fixed ``MathTex`` labels for the displayed
term segments and resultant segment of one already projected linear-combination
geometry snapshot.  It moves those labels in place as later compatible display
snapshots arrive.

No coefficient interpolation, vector arithmetic, tip-to-tail construction,
display projection, scene timing, or pedagogical sequencing is performed here.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Protocol, TypeAlias

import numpy as np
from manim import MathTex, VGroup


PointLike: TypeAlias = Sequence[float] | np.ndarray


class _LinearCombinationDisplaySnapshotLike(Protocol):
    """Canonical display fields consumed by the labels adapter."""

    display_term_segments: np.ndarray
    display_resultant_segment: np.ndarray


class ManimLinearCombinationLabels(VGroup):
    """Own fixed mathematical labels tied to displayed segment positions.

    Parameters
    ----------
    snapshot:
        One canonical ``LinearCombinationGeometryDisplaySnapshot``.  Its
        projected term and resultant segments determine the initial label
        anchors.
    term_labels:
        Optional TeX strings for the term labels.  When omitted, labels are
        generated as ``c_i\\mathbf{v}_i`` in term order.
    resultant_label:
        TeX string for the resultant label.
    term_label_offset:
        Constant two- or three-dimensional display-space offset from each term
        segment midpoint.
    resultant_label_offset:
        Constant two- or three-dimensional display-space offset from the
        resultant segment midpoint.
    label_kwargs:
        Optional keyword arguments copied and forwarded to every ``MathTex``
        label.

    Notes
    -----
    Label text, term count, and display dimension are structural.  Later
    snapshots must preserve the term count and display dimension so every
    existing ``MathTex`` mobject can be moved in place.
    """

    def __init__(
        self,
        snapshot: _LinearCombinationDisplaySnapshotLike,
        *,
        term_labels: Sequence[str] | None = None,
        resultant_label: str = r"\mathbf{r}",
        term_label_offset: PointLike = (0.0, 0.25, 0.0),
        resultant_label_offset: PointLike = (0.0, -0.25, 0.0),
        label_kwargs: Mapping[str, Any] | None = None,
    ) -> None:
        term_anchors, resultant_anchor, display_dimension = _snapshot_anchors(
            snapshot
        )
        term_label_sources = _term_label_sources(
            term_labels,
            term_count=len(term_anchors),
        )
        resultant_label_source = _label_source(
            resultant_label,
            name="resultant_label",
        )
        term_offset = _manim_offset(term_label_offset, name="term_label_offset")
        resultant_offset = _manim_offset(
            resultant_label_offset,
            name="resultant_label_offset",
        )
        options = _label_options(label_kwargs)

        term_label_mobjects = tuple(
            MathTex(source, **dict(options)) for source in term_label_sources
        )
        resultant_label_mobject = MathTex(
            resultant_label_source,
            **dict(options),
        )

        super().__init__(*term_label_mobjects, resultant_label_mobject)

        self._term_label_mobjects = term_label_mobjects
        self._resultant_label_mobject = resultant_label_mobject
        self._term_label_sources = term_label_sources
        self._resultant_label_source = resultant_label_source
        self._term_label_offset = term_offset
        self._resultant_label_offset = resultant_offset
        self._term_count = len(term_anchors)
        self._display_dimension = display_dimension
        self._snapshot = snapshot

        self._move_labels(term_anchors, resultant_anchor)

    @property
    def mobject(self) -> VGroup:
        """Return this adapter's root Manim group."""

        return self

    @property
    def snapshot(self) -> _LinearCombinationDisplaySnapshotLike:
        """Return the exact display snapshot currently represented."""

        return self._snapshot

    @property
    def term_label_mobjects(self) -> tuple[MathTex, ...]:
        """Return the fixed term-label mobjects in term order."""

        return self._term_label_mobjects

    @property
    def resultant_label_mobject(self) -> MathTex:
        """Return the fixed resultant-label mobject."""

        return self._resultant_label_mobject

    @property
    def term_label_sources(self) -> tuple[str, ...]:
        """Return the immutable TeX sources for the term labels."""

        return self._term_label_sources

    @property
    def resultant_label_source(self) -> str:
        """Return the immutable TeX source for the resultant label."""

        return self._resultant_label_source

    @property
    def term_count(self) -> int:
        """Return the structural number of displayed terms."""

        return self._term_count

    @property
    def display_dimension(self) -> int:
        """Return the structural projected display dimension."""

        return self._display_dimension

    @property
    def term_label_offset(self) -> np.ndarray:
        """Return a copy of the three-dimensional term-label offset."""

        return self._term_label_offset.copy()

    @property
    def resultant_label_offset(self) -> np.ndarray:
        """Return a copy of the three-dimensional resultant-label offset."""

        return self._resultant_label_offset.copy()

    def update_from_snapshot(
        self,
        snapshot: _LinearCombinationDisplaySnapshotLike,
    ) -> ManimLinearCombinationLabels:
        """Move all labels to a compatible display snapshot in place.

        The complete incoming display structure and every coordinate are
        validated before any Manim mobject is mutated.
        """

        term_anchors, resultant_anchor, display_dimension = _snapshot_anchors(
            snapshot
        )

        if len(term_anchors) != self._term_count:
            raise ValueError(
                "snapshot term count does not match the labels adapter: "
                f"expected {self._term_count}, received {len(term_anchors)}"
            )
        if display_dimension != self._display_dimension:
            raise ValueError(
                "snapshot display dimension does not match the labels adapter: "
                f"expected {self._display_dimension}, received {display_dimension}"
            )

        self._move_labels(term_anchors, resultant_anchor)
        self._snapshot = snapshot
        return self

    def _move_labels(
        self,
        term_anchors: tuple[np.ndarray, ...],
        resultant_anchor: np.ndarray,
    ) -> None:
        term_positions = tuple(
            anchor + self._term_label_offset for anchor in term_anchors
        )
        resultant_position = resultant_anchor + self._resultant_label_offset

        for label, position in zip(
            self._term_label_mobjects,
            term_positions,
            strict=True,
        ):
            label.move_to(position)
        self._resultant_label_mobject.move_to(resultant_position)


def _snapshot_anchors(
    snapshot: _LinearCombinationDisplaySnapshotLike,
) -> tuple[tuple[np.ndarray, ...], np.ndarray, int]:
    """Return validated Manim-space midpoint anchors for one display snapshot."""

    try:
        term_segments = np.asarray(snapshot.display_term_segments, dtype=float)
        resultant_segment = np.asarray(
            snapshot.display_resultant_segment,
            dtype=float,
        )
    except AttributeError as exc:
        raise TypeError(
            "snapshot must expose display_term_segments and "
            "display_resultant_segment"
        ) from exc
    except (TypeError, ValueError) as exc:
        raise TypeError("snapshot display segments must be numeric") from exc

    if term_segments.ndim != 3 or term_segments.shape[1] != 2:
        raise ValueError(
            "display_term_segments must have shape (term_count, 2, dimension)"
        )
    if term_segments.shape[0] < 1:
        raise ValueError("display_term_segments must contain at least one term")

    display_dimension = int(term_segments.shape[2])
    if display_dimension not in (2, 3):
        raise ValueError("display dimension must be 2 or 3")
    if resultant_segment.shape != (2, display_dimension):
        raise ValueError(
            "display_resultant_segment must have shape "
            f"(2, {display_dimension})"
        )
    if not np.isfinite(term_segments).all():
        raise ValueError("display_term_segments must contain only finite values")
    if not np.isfinite(resultant_segment).all():
        raise ValueError(
            "display_resultant_segment must contain only finite values"
        )

    term_midpoints = np.mean(term_segments, axis=1)
    resultant_midpoint = np.mean(resultant_segment, axis=0)

    term_anchors = tuple(_manim_point(point) for point in term_midpoints)
    resultant_anchor = _manim_point(resultant_midpoint)
    return term_anchors, resultant_anchor, display_dimension


def _manim_point(point: np.ndarray) -> np.ndarray:
    """Embed one validated two- or three-dimensional point in Manim space."""

    result = np.zeros(3, dtype=float)
    result[: point.size] = point
    return result


def _manim_offset(value: PointLike, *, name: str) -> np.ndarray:
    """Validate and embed one user-supplied label offset in Manim space."""

    try:
        offset = np.asarray(value, dtype=float)
    except (TypeError, ValueError) as exc:
        raise TypeError(f"{name} must be a numeric point") from exc

    if offset.ndim != 1 or offset.size not in (2, 3):
        raise ValueError(f"{name} must contain exactly 2 or 3 coordinates")
    if not np.isfinite(offset).all():
        raise ValueError(f"{name} must contain only finite values")

    return _manim_point(offset)


def _term_label_sources(
    values: Sequence[str] | None,
    *,
    term_count: int,
) -> tuple[str, ...]:
    """Return validated term-label TeX sources in term order."""

    if values is None:
        return tuple(
            rf"c_{{{index}}}\mathbf{{v}}_{{{index}}}"
            for index in range(1, term_count + 1)
        )
    if isinstance(values, (str, bytes)):
        raise TypeError("term_labels must be a sequence of label strings")

    sources = tuple(values)
    if len(sources) != term_count:
        raise ValueError(
            "term_labels length must match the display term count: "
            f"expected {term_count}, received {len(sources)}"
        )
    return tuple(
        _label_source(source, name=f"term_labels[{index}]")
        for index, source in enumerate(sources)
    )


def _label_source(value: str, *, name: str) -> str:
    """Validate one immutable TeX label source."""

    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value.strip():
        raise ValueError(f"{name} must not be empty")
    return value


def _label_options(
    values: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Copy and validate options forwarded to every ``MathTex`` label."""

    if values is None:
        return {}
    if not isinstance(values, Mapping):
        raise TypeError("label_kwargs must be a mapping")

    options = dict(values)
    if "tex_strings" in options:
        raise ValueError(
            "label_kwargs cannot override the adapter-owned label text"
        )
    return options
