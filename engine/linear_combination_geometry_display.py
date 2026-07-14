"""Display projection for renderer-independent linear-combination geometry.

This module composes :class:`LinearCombinationGeometryPath` with the existing
:class:`LinearDisplayProjector`.  It projects segment endpoints into display
space while retaining the complete mathematical geometry snapshot.  It has no
Manim or renderer dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
from numbers import Real
from typing import Iterable, TypeAlias

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .linear_combination import LinearCombination, LinearCombinationSnapshot
from .linear_combination_geometry import LinearCombinationGeometrySnapshot
from .linear_combination_geometry_path import LinearCombinationGeometryPath
from .rank_collapse_display import LinearDisplayProjector


FloatArray: TypeAlias = NDArray[np.float64]


def _readonly_float_array(values: ArrayLike, *, ndim: int, name: str) -> FloatArray:
    """Return an owned, finite, read-only float array with the requested rank."""

    array = np.array(values, dtype=float, copy=True)
    if array.ndim != ndim:
        raise ValueError(f"{name} must be a {ndim}-dimensional array")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")
    array.setflags(write=False)
    return array


@dataclass(frozen=True, slots=True)
class LinearCombinationGeometryDisplaySnapshot:
    """Immutable display-space geometry for one coefficient-sweep frame.

    Array conventions
    -----------------
    ``display_term_segments`` has shape
    ``(vector_count, 2, display_dimension)``.

    ``display_resultant_segment`` has shape ``(2, display_dimension)``.

    The original renderer-independent ``geometry_snapshot`` is retained so
    coefficients, scaled terms, partial sums, and mathematical coordinates
    remain available without reverse-projecting display data.
    """

    geometry_snapshot: LinearCombinationGeometrySnapshot
    display_term_segments: FloatArray
    display_resultant_segment: FloatArray
    projection_matrix: FloatArray
    display_offset: FloatArray

    def __post_init__(self) -> None:
        geometry = self.geometry_snapshot
        if not isinstance(geometry, LinearCombinationGeometrySnapshot):
            raise TypeError(
                "geometry_snapshot must be a LinearCombinationGeometrySnapshot"
            )

        display_term_segments = _readonly_float_array(
            self.display_term_segments,
            ndim=3,
            name="display_term_segments",
        )
        display_resultant_segment = _readonly_float_array(
            self.display_resultant_segment,
            ndim=2,
            name="display_resultant_segment",
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

        if projection_matrix.shape[1] != geometry.dimension:
            raise ValueError(
                "projection_matrix input dimension must equal the mathematical "
                "geometry dimension"
            )
        display_dimension = projection_matrix.shape[0]
        if display_dimension < 1:
            raise ValueError("projection_matrix must have a positive display dimension")
        if display_offset.shape != (display_dimension,):
            raise ValueError(
                "display_offset dimension must equal the projection display dimension"
            )
        if display_term_segments.shape != (
            geometry.vector_count,
            2,
            display_dimension,
        ):
            raise ValueError(
                "display_term_segments must have shape "
                "(vector_count, 2, display_dimension)"
            )
        if display_resultant_segment.shape != (2, display_dimension):
            raise ValueError(
                "display_resultant_segment must have shape (2, display_dimension)"
            )

        expected_terms = (
            geometry.term_segments @ projection_matrix.T + display_offset
        )
        expected_resultant = (
            geometry.resultant_segment @ projection_matrix.T + display_offset
        )
        if not np.allclose(display_term_segments, expected_terms):
            raise ValueError(
                "display_term_segments must be the projected mathematical endpoints"
            )
        if not np.allclose(display_resultant_segment, expected_resultant):
            raise ValueError(
                "display_resultant_segment must be the projected resultant endpoints"
            )

        if geometry.vector_count > 1 and not np.allclose(
            display_term_segments[:-1, 1, :],
            display_term_segments[1:, 0, :],
        ):
            raise ValueError("display term segments must remain tip to tail")
        if not np.allclose(
            display_resultant_segment[0],
            display_term_segments[0, 0],
        ):
            raise ValueError(
                "display resultant and first term segment must share their origin"
            )
        if not np.allclose(
            display_resultant_segment[1],
            display_term_segments[-1, 1],
        ):
            raise ValueError(
                "display resultant tip must equal the final term-segment tip"
            )

        object.__setattr__(
            self,
            "display_term_segments",
            display_term_segments,
        )
        object.__setattr__(
            self,
            "display_resultant_segment",
            display_resultant_segment,
        )
        object.__setattr__(self, "projection_matrix", projection_matrix)
        object.__setattr__(self, "display_offset", display_offset)

    @property
    def linear_combination_snapshot(self) -> LinearCombinationSnapshot:
        """Underlying mathematical linear-combination state."""

        return self.geometry_snapshot.linear_combination_snapshot

    @property
    def vector_count(self) -> int:
        """Number of projected tip-to-tail term segments."""

        return self.geometry_snapshot.vector_count

    @property
    def mathematical_dimension(self) -> int:
        """Ambient dimension before display projection."""

        return self.geometry_snapshot.dimension

    @property
    def display_dimension(self) -> int:
        """Ambient dimension after display projection."""

        return int(self.projection_matrix.shape[0])

    @property
    def display_term_starts(self) -> FloatArray:
        """Read-only tails of all projected scaled-term segments."""

        return self.display_term_segments[:, 0, :]

    @property
    def display_term_ends(self) -> FloatArray:
        """Read-only tips of all projected scaled-term segments."""

        return self.display_term_segments[:, 1, :]

    @property
    def display_resultant_start(self) -> FloatArray:
        """Read-only display-space origin of the resultant."""

        return self.display_resultant_segment[0]

    @property
    def display_resultant_end(self) -> FloatArray:
        """Read-only display-space tip of the resultant."""

        return self.display_resultant_segment[1]


class LinearCombinationGeometryDisplayAdapter:
    """Project a linear-combination geometry path into display coordinates.

    The adapter owns no coefficient interpolation and constructs no
    mathematical geometry.  For each progress value it asks ``path`` for a
    :class:`LinearCombinationGeometrySnapshot`, projects every segment
    endpoint with ``projector``, and restores the original segment topology.
    """

    def __init__(
        self,
        path: LinearCombinationGeometryPath,
        projector: LinearDisplayProjector,
    ) -> None:
        if not isinstance(path, LinearCombinationGeometryPath):
            raise TypeError("path must be a LinearCombinationGeometryPath")
        if not isinstance(projector, LinearDisplayProjector):
            raise TypeError("projector must be a LinearDisplayProjector")
        if projector.input_dimension != path.dimension:
            raise ValueError(
                "projector input dimension must equal the path mathematical "
                f"dimension ({path.dimension})"
            )

        self._path = path
        self._projector = projector

    @property
    def path(self) -> LinearCombinationGeometryPath:
        """The exact renderer-independent geometry path being projected."""

        return self._path

    @property
    def projector(self) -> LinearDisplayProjector:
        """The exact affine display projector used for all endpoints."""

        return self._projector

    @property
    def linear_combination(self) -> LinearCombination:
        """The fixed mathematical linear combination owned by the path."""

        return self._path.linear_combination

    @property
    def vector_count(self) -> int:
        """Number of coefficient terms and projected term segments."""

        return self._path.vector_count

    @property
    def dimension(self) -> int:
        """Ambient mathematical dimension before projection."""

        return self._path.dimension

    @property
    def display_dimension(self) -> int:
        """Ambient display dimension after projection."""

        return self._projector.display_dimension

    def snapshot(self, progress: float) -> LinearCombinationGeometryDisplaySnapshot:
        """Return the complete display geometry at ``progress``."""

        geometry_snapshot = self._path.snapshot(progress)

        flattened_term_endpoints = geometry_snapshot.term_segments.reshape(
            -1,
            self.dimension,
        )
        display_term_segments = self._projector.project(
            flattened_term_endpoints
        ).reshape(self.vector_count, 2, self.display_dimension)
        display_resultant_segment = self._projector.project(
            geometry_snapshot.resultant_segment
        )

        return LinearCombinationGeometryDisplaySnapshot(
            geometry_snapshot=geometry_snapshot,
            display_term_segments=display_term_segments,
            display_resultant_segment=display_resultant_segment,
            projection_matrix=self._projector.projection_matrix,
            display_offset=self._projector.offset,
        )

    def snapshots(
        self,
        progress_values: Iterable[Real],
    ) -> tuple[LinearCombinationGeometryDisplaySnapshot, ...]:
        """Return an immutable sequence of projected sampled frames."""

        return tuple(self.snapshot(progress) for progress in progress_values)

    def __call__(self, progress: float) -> LinearCombinationGeometryDisplaySnapshot:
        """Shorthand for :meth:`snapshot`."""

        return self.snapshot(progress)
