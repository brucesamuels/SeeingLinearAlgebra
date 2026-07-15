"""Reusable Manim composition for moving linear-combination presentation.

This renderer-specific module combines the established
:class:`ManimLinearCombinationGeometry` and
:class:`ManimLinearCombinationReadout` adapters behind one synchronized
``update_from_snapshot`` interface.  It consumes one already projected
linear-combination geometry display snapshot per frame.

No coefficient interpolation, vector arithmetic, tip-to-tail construction,
display projection, trace construction, or scene timing is performed here.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol

import numpy as np
from manim import VGroup

from .manim_linear_combination_geometry import ManimLinearCombinationGeometry
from .manim_linear_combination_readout import ManimLinearCombinationReadout


class _LinearCombinationSnapshotLike(Protocol):
    """Canonical mathematical fields retained by a display snapshot."""

    coefficients: np.ndarray
    result: np.ndarray


class _LinearCombinationDisplaySnapshotLike(Protocol):
    """Canonical display fields consumed by the composite adapter."""

    display_term_segments: np.ndarray
    display_resultant_segment: np.ndarray
    linear_combination_snapshot: _LinearCombinationSnapshotLike


class ManimLinearCombinationPresentation(VGroup):
    """Own synchronized moving arrows and coefficient/result readout.

    Parameters
    ----------
    snapshot:
        One canonical ``LinearCombinationGeometryDisplaySnapshot``.  Its
        projected segment fields initialize the arrow adapter, while its
        retained ``linear_combination_snapshot`` initializes the readout.
    geometry_kwargs:
        Optional keyword arguments copied and forwarded to
        :class:`ManimLinearCombinationGeometry`.
    readout_kwargs:
        Optional keyword arguments copied and forwarded to
        :class:`ManimLinearCombinationReadout`.

    Notes
    -----
    The two child adapters are added to this root ``VGroup`` without imposing
    a layout between them.  A scene may position the readout independently
    while preserving mathematical display coordinates for the arrows.

    The number of terms, display dimension, coefficient count, and result
    dimension are structural.  Later snapshots must preserve all four so the
    complete presentation can update existing mobjects in place.
    """

    def __init__(
        self,
        snapshot: _LinearCombinationDisplaySnapshotLike,
        *,
        geometry_kwargs: Mapping[str, Any] | None = None,
        readout_kwargs: Mapping[str, Any] | None = None,
    ) -> None:
        structure = _snapshot_structure(snapshot)
        geometry_options = _component_kwargs(
            geometry_kwargs,
            name="geometry_kwargs",
        )
        readout_options = _component_kwargs(
            readout_kwargs,
            name="readout_kwargs",
        )

        self._geometry = ManimLinearCombinationGeometry(
            snapshot,
            **geometry_options,
        )
        self._readout = ManimLinearCombinationReadout(
            snapshot.linear_combination_snapshot,
            **readout_options,
        )

        super().__init__(self._geometry, self._readout)

        self._snapshot = snapshot
        (
            self._vector_count,
            self._display_dimension,
            self._coefficient_count,
            self._result_dimension,
        ) = structure

    @property
    def mobject(self) -> ManimLinearCombinationPresentation:
        """Return the root Manim mobject represented by this adapter."""

        return self

    @property
    def snapshot(self) -> _LinearCombinationDisplaySnapshotLike:
        """Return the exact display snapshot currently represented."""

        return self._snapshot

    @property
    def geometry(self) -> ManimLinearCombinationGeometry:
        """Return the fixed moving-arrow adapter."""

        return self._geometry

    @property
    def readout(self) -> ManimLinearCombinationReadout:
        """Return the fixed coefficient/result readout adapter."""

        return self._readout

    @property
    def vector_count(self) -> int:
        """Return the structural number of term arrows."""

        return self._vector_count

    @property
    def display_dimension(self) -> int:
        """Return the structural projected display dimension."""

        return self._display_dimension

    @property
    def coefficient_count(self) -> int:
        """Return the structural number of displayed coefficients."""

        return self._coefficient_count

    @property
    def result_dimension(self) -> int:
        """Return the structural mathematical result dimension."""

        return self._result_dimension

    def update_from_snapshot(
        self,
        snapshot: _LinearCombinationDisplaySnapshotLike,
    ) -> ManimLinearCombinationPresentation:
        """Update both child adapters from one shared display snapshot.

        The complete incoming snapshot is validated before either child is
        mutated.  This preserves the create-once/update-in-place contract for
        the whole composite presentation.
        """

        structure = _snapshot_structure(snapshot)
        expected = (
            self.vector_count,
            self.display_dimension,
            self.coefficient_count,
            self.result_dimension,
        )
        if structure != expected:
            _raise_structure_change(expected, structure)

        self._geometry.update_from_snapshot(snapshot)
        self._readout.update_from_snapshot(
            snapshot.linear_combination_snapshot
        )
        self._snapshot = snapshot
        return self


def _component_kwargs(
    values: Mapping[str, Any] | None,
    *,
    name: str,
) -> dict[str, Any]:
    kwargs = dict(values or {})
    if "snapshot" in kwargs:
        raise ValueError(f"{name} cannot override adapter-owned snapshot")
    return kwargs


def _snapshot_structure(
    snapshot: object,
) -> tuple[int, int, int, int]:
    required = (
        "display_term_segments",
        "display_resultant_segment",
        "linear_combination_snapshot",
    )
    if not all(hasattr(snapshot, name) for name in required):
        raise TypeError(
            "snapshot must expose display_term_segments, "
            "display_resultant_segment, and linear_combination_snapshot"
        )

    term_segments = np.asarray(
        getattr(snapshot, "display_term_segments"),
        dtype=float,
    )
    resultant_segment = np.asarray(
        getattr(snapshot, "display_resultant_segment"),
        dtype=float,
    )

    if term_segments.ndim != 3 or term_segments.shape[1] != 2:
        raise ValueError(
            "display_term_segments must have shape "
            "(term_count, 2, display_dimension)"
        )
    if term_segments.shape[0] < 1:
        raise ValueError("display_term_segments must contain at least one term")
    if resultant_segment.ndim != 2 or resultant_segment.shape[0] != 2:
        raise ValueError(
            "display_resultant_segment must have shape "
            "(2, display_dimension)"
        )
    if term_segments.shape[2] != resultant_segment.shape[1]:
        raise ValueError("term and resultant display dimensions must agree")

    display_dimension = int(term_segments.shape[2])
    if display_dimension not in (2, 3):
        raise ValueError("Manim display dimension must be two or three")
    if not np.all(np.isfinite(term_segments)):
        raise ValueError("display_term_segments must contain only finite values")
    if not np.all(np.isfinite(resultant_segment)):
        raise ValueError(
            "display_resultant_segment must contain only finite values"
        )

    mathematical = getattr(snapshot, "linear_combination_snapshot")
    if not hasattr(mathematical, "coefficients") or not hasattr(
        mathematical,
        "result",
    ):
        raise TypeError(
            "linear_combination_snapshot must expose coefficients and result"
        )

    coefficients = np.asarray(getattr(mathematical, "coefficients"), dtype=float)
    result = np.asarray(getattr(mathematical, "result"), dtype=float)
    if coefficients.ndim != 1:
        raise ValueError("coefficients must be a one-dimensional array")
    if result.ndim != 1:
        raise ValueError("result must be a one-dimensional array")
    if coefficients.size < 1:
        raise ValueError("coefficients must contain at least one value")
    if result.size < 1:
        raise ValueError("result must contain at least one value")
    if not np.all(np.isfinite(coefficients)):
        raise ValueError("coefficients must contain only finite values")
    if not np.all(np.isfinite(result)):
        raise ValueError("result must contain only finite values")

    vector_count = int(term_segments.shape[0])
    coefficient_count = int(coefficients.size)
    if vector_count != coefficient_count:
        raise ValueError(
            "term-arrow count must equal coefficient count: "
            f"received {vector_count} terms and {coefficient_count} coefficients"
        )

    return (
        vector_count,
        display_dimension,
        coefficient_count,
        int(result.size),
    )


def _raise_structure_change(
    expected: tuple[int, int, int, int],
    received: tuple[int, int, int, int],
) -> None:
    names = (
        "term-arrow count",
        "display dimension",
        "coefficient count",
        "result dimension",
    )
    for name, expected_value, received_value in zip(
        names,
        expected,
        received,
        strict=True,
    ):
        if expected_value != received_value:
            raise ValueError(
                f"{name} changed: expected {expected_value}, "
                f"received {received_value}"
            )
    raise RuntimeError("unreachable presentation structure comparison")
