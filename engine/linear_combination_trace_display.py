"""Display projection for renderer-independent linear-combination traces.

This module composes :class:`LinearCombinationTrace` with the existing
:class:`LinearDisplayProjector`.  It projects sampled resultant-tip points and
trace-segment endpoints into display space while retaining the complete
renderer-independent trace snapshot.  It has no Manim or renderer
dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .linear_combination_trace import (
    LinearCombinationTrace,
    LinearCombinationTraceSnapshot,
)
from .rank_collapse_display import LinearDisplayProjector


FloatArray: TypeAlias = NDArray[np.float64]


def _readonly_float_array(
    values: ArrayLike,
    *,
    ndim: int,
    name: str,
) -> FloatArray:
    """Return an owned, finite, read-only float array of the requested rank."""

    array = np.array(values, dtype=float, copy=True)
    if array.ndim != ndim:
        raise ValueError(f"{name} must be a {ndim}-dimensional array")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")
    array.setflags(write=False)
    return array


@dataclass(frozen=True, slots=True)
class LinearCombinationTraceDisplaySnapshot:
    """Immutable display-space representation of one sampled trace.

    Array conventions
    -----------------
    ``display_resultant_points`` has shape
    ``(sample_count, display_dimension)``.

    ``display_resultant_segments`` has shape
    ``(max(sample_count - 1, 0), 2, display_dimension)``.

    The original renderer-independent ``trace_snapshot`` is retained so
    coefficient samples and mathematical coordinates remain available without
    reverse-projecting display data.
    """

    trace_snapshot: LinearCombinationTraceSnapshot
    display_resultant_points: FloatArray
    display_resultant_segments: FloatArray
    projection_matrix: FloatArray
    display_offset: FloatArray

    def __post_init__(self) -> None:
        trace = self.trace_snapshot
        if not isinstance(trace, LinearCombinationTraceSnapshot):
            raise TypeError(
                "trace_snapshot must be a LinearCombinationTraceSnapshot"
            )

        display_points = _readonly_float_array(
            self.display_resultant_points,
            ndim=2,
            name="display_resultant_points",
        )
        display_segments = _readonly_float_array(
            self.display_resultant_segments,
            ndim=3,
            name="display_resultant_segments",
        )
        projection_matrix = _readonly_float_array(
            self.projection_matrix,
            ndim=2,
            name="projection_matrix",
        )
        display_offset = _readonly_float_array(
            self.display_offset,
            ndim=1,
            name="display_offset",
        )

        if projection_matrix.shape[1] != trace.ambient_dimension:
            raise ValueError(
                "projection_matrix input dimension must equal the mathematical "
                "trace dimension"
            )

        display_dimension = int(projection_matrix.shape[0])
        if display_dimension < 1:
            raise ValueError(
                "projection_matrix must have a positive display dimension"
            )
        if display_offset.shape != (display_dimension,):
            raise ValueError(
                "display_offset dimension must equal the projection display "
                "dimension"
            )

        if display_points.shape != (trace.sample_count, display_dimension):
            raise ValueError(
                "display_resultant_points must have shape "
                "(sample_count, display_dimension)"
            )

        expected_segment_count = max(trace.sample_count - 1, 0)
        if display_segments.shape != (
            expected_segment_count,
            2,
            display_dimension,
        ):
            raise ValueError(
                "display_resultant_segments must have shape "
                "(max(sample_count - 1, 0), 2, display_dimension)"
            )

        expected_points = (
            trace.resultant_points @ projection_matrix.T + display_offset
        )
        expected_segments = (
            trace.resultant_segments @ projection_matrix.T + display_offset
        )
        if not np.allclose(display_points, expected_points):
            raise ValueError(
                "display_resultant_points must be the projected mathematical "
                "trace points"
            )
        if not np.allclose(display_segments, expected_segments):
            raise ValueError(
                "display_resultant_segments must be the projected mathematical "
                "trace segments"
            )

        if trace.sample_count > 1:
            if not np.allclose(
                display_segments[:, 0, :],
                display_points[:-1],
            ):
                raise ValueError(
                    "display segment starts must equal preceding display points"
                )
            if not np.allclose(
                display_segments[:, 1, :],
                display_points[1:],
            ):
                raise ValueError(
                    "display segment ends must equal following display points"
                )

        object.__setattr__(
            self,
            "display_resultant_points",
            display_points,
        )
        object.__setattr__(
            self,
            "display_resultant_segments",
            display_segments,
        )
        object.__setattr__(self, "projection_matrix", projection_matrix)
        object.__setattr__(self, "display_offset", display_offset)

    @property
    def coefficients(self) -> FloatArray:
        """Read-only sampled coefficient vectors from the mathematical trace."""

        return self.trace_snapshot.coefficients

    @property
    def sample_count(self) -> int:
        """Number of sampled resultant-tip points."""

        return self.trace_snapshot.sample_count

    @property
    def coefficient_dimension(self) -> int:
        """Number of coefficients in each sampled coefficient vector."""

        return self.trace_snapshot.coefficient_dimension

    @property
    def mathematical_dimension(self) -> int:
        """Ambient dimension before display projection."""

        return self.trace_snapshot.ambient_dimension

    @property
    def display_dimension(self) -> int:
        """Ambient dimension after display projection."""

        return int(self.projection_matrix.shape[0])

    @property
    def display_resultant_starts(self) -> FloatArray:
        """Read-only starts of the projected trace segments."""

        return self.display_resultant_segments[:, 0, :]

    @property
    def display_resultant_ends(self) -> FloatArray:
        """Read-only ends of the projected trace segments."""

        return self.display_resultant_segments[:, 1, :]


class LinearCombinationTraceDisplayAdapter:
    """Project a sampled linear-combination trace into display coordinates.

    The adapter owns no coefficient interpolation, mathematical geometry, or
    trace construction.  It asks ``trace`` for its established immutable
    snapshot, projects all points and segment endpoints with ``projector``, and
    returns a display snapshot retaining the exact mathematical trace.
    """

    __slots__ = ("_trace", "_projector")

    def __init__(
        self,
        trace: LinearCombinationTrace,
        projector: LinearDisplayProjector,
    ) -> None:
        if not isinstance(trace, LinearCombinationTrace):
            raise TypeError("trace must be a LinearCombinationTrace")
        if not isinstance(projector, LinearDisplayProjector):
            raise TypeError("projector must be a LinearDisplayProjector")

        trace_snapshot = trace.snapshot()
        if projector.input_dimension != trace_snapshot.ambient_dimension:
            raise ValueError(
                "projector input dimension must equal the trace mathematical "
                f"dimension ({trace_snapshot.ambient_dimension})"
            )

        self._trace = trace
        self._projector = projector

    @property
    def trace(self) -> LinearCombinationTrace:
        """The exact renderer-independent trace being projected."""

        return self._trace

    @property
    def projector(self) -> LinearDisplayProjector:
        """The exact affine display projector used for every point."""

        return self._projector

    @property
    def sample_count(self) -> int:
        """Number of sampled resultant-tip points."""

        return self._trace.snapshot().sample_count

    @property
    def coefficient_dimension(self) -> int:
        """Number of coefficients in each sampled coefficient vector."""

        return self._trace.snapshot().coefficient_dimension

    @property
    def mathematical_dimension(self) -> int:
        """Ambient dimension before display projection."""

        return self._trace.snapshot().ambient_dimension

    @property
    def display_dimension(self) -> int:
        """Ambient dimension after display projection."""

        return self._projector.display_dimension

    def snapshot(self) -> LinearCombinationTraceDisplaySnapshot:
        """Return the complete projected trace geometry."""

        trace_snapshot = self._trace.snapshot()
        display_points = self._projector.project(
            trace_snapshot.resultant_points
        )

        flattened_endpoints = trace_snapshot.resultant_segments.reshape(
            -1,
            trace_snapshot.ambient_dimension,
        )
        display_segments = self._projector.project(
            flattened_endpoints
        ).reshape(
            max(trace_snapshot.sample_count - 1, 0),
            2,
            self._projector.display_dimension,
        )

        return LinearCombinationTraceDisplaySnapshot(
            trace_snapshot=trace_snapshot,
            display_resultant_points=display_points,
            display_resultant_segments=display_segments,
            projection_matrix=self._projector.projection_matrix,
            display_offset=self._projector.offset,
        )

    def __call__(self) -> LinearCombinationTraceDisplaySnapshot:
        """Shorthand for :meth:`snapshot`."""

        return self.snapshot()
