"""Renderer-independent geometry for linear-combination snapshots.

This module converts mathematical linear-combination state into explicit
arrow segments in the same ambient mathematical coordinate space.  It has no
display-projection or renderer dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .linear_combination import LinearCombinationSnapshot


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
class LinearCombinationGeometrySnapshot:
    """Immutable arrow geometry for one linear-combination state.

    Array conventions
    -----------------
    ``term_segments`` has shape ``(vector_count, 2, dimension)``.  For each
    term, index zero is the segment tail and index one is the segment tip.
    Consecutive term segments are placed tip to tail.

    ``resultant_segment`` has shape ``(2, dimension)`` and runs from the
    origin to the final sum.
    """

    linear_combination_snapshot: LinearCombinationSnapshot
    term_segments: FloatArray
    resultant_segment: FloatArray

    def __post_init__(self) -> None:
        mathematical = self.linear_combination_snapshot
        if not isinstance(mathematical, LinearCombinationSnapshot):
            raise TypeError(
                "linear_combination_snapshot must be a LinearCombinationSnapshot"
            )

        term_segments = _readonly_float_array(
            self.term_segments, ndim=3, name="term_segments"
        )
        resultant_segment = _readonly_float_array(
            self.resultant_segment, ndim=2, name="resultant_segment"
        )

        expected_term_shape = (
            mathematical.vector_count,
            2,
            mathematical.dimension,
        )
        if term_segments.shape != expected_term_shape:
            raise ValueError(
                "term_segments must have shape "
                "(vector_count, 2, mathematical dimension)"
            )
        if resultant_segment.shape != (2, mathematical.dimension):
            raise ValueError(
                "resultant_segment must have shape (2, mathematical dimension)"
            )

        if not np.allclose(term_segments[:, 0, :], mathematical.partial_sums[:-1]):
            raise ValueError("term segment tails must equal preceding partial sums")
        if not np.allclose(term_segments[:, 1, :], mathematical.partial_sums[1:]):
            raise ValueError("term segment tips must equal following partial sums")
        if not np.allclose(
            term_segments[:, 1, :] - term_segments[:, 0, :],
            mathematical.terms,
        ):
            raise ValueError("term segment displacements must equal scaled terms")

        origin = np.zeros(mathematical.dimension, dtype=float)
        if not np.allclose(resultant_segment[0], origin):
            raise ValueError("resultant segment must start at the origin")
        if not np.allclose(resultant_segment[1], mathematical.result):
            raise ValueError("resultant segment must end at the final sum")

        object.__setattr__(self, "term_segments", term_segments)
        object.__setattr__(self, "resultant_segment", resultant_segment)

    @property
    def vector_count(self) -> int:
        """Number of tip-to-tail term segments."""

        return self.linear_combination_snapshot.vector_count

    @property
    def dimension(self) -> int:
        """Ambient mathematical dimension of every segment endpoint."""

        return self.linear_combination_snapshot.dimension

    @property
    def term_starts(self) -> FloatArray:
        """Read-only tails of the scaled-term segments."""

        return self.term_segments[:, 0, :]

    @property
    def term_ends(self) -> FloatArray:
        """Read-only tips of the scaled-term segments."""

        return self.term_segments[:, 1, :]

    @property
    def resultant_start(self) -> FloatArray:
        """Read-only origin of the resultant segment."""

        return self.resultant_segment[0]

    @property
    def resultant_end(self) -> FloatArray:
        """Read-only tip of the resultant segment."""

        return self.resultant_segment[1]


class LinearCombinationGeometry:
    """Convert mathematical linear-combination snapshots into arrow geometry.

    The converter is intentionally stateless.  It does not recompute the
    linear combination and does not know about coefficient paths, display
    projection, styling, animation timing, or any renderer.
    """

    def snapshot(
        self,
        linear_combination_snapshot: LinearCombinationSnapshot,
    ) -> LinearCombinationGeometrySnapshot:
        """Return tip-to-tail term segments and the origin-based resultant."""

        if not isinstance(linear_combination_snapshot, LinearCombinationSnapshot):
            raise TypeError(
                "linear_combination_snapshot must be a LinearCombinationSnapshot"
            )

        partial_sums = linear_combination_snapshot.partial_sums
        term_segments = np.stack(
            (partial_sums[:-1], partial_sums[1:]),
            axis=1,
        )
        resultant_segment = np.stack(
            (
                np.zeros(linear_combination_snapshot.dimension, dtype=float),
                linear_combination_snapshot.result,
            ),
            axis=0,
        )

        return LinearCombinationGeometrySnapshot(
            linear_combination_snapshot=linear_combination_snapshot,
            term_segments=term_segments,
            resultant_segment=resultant_segment,
        )

    def __call__(
        self,
        linear_combination_snapshot: LinearCombinationSnapshot,
    ) -> LinearCombinationGeometrySnapshot:
        """Shorthand for :meth:`snapshot`."""

        return self.snapshot(linear_combination_snapshot)
