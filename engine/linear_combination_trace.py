"""Renderer-independent traces of sampled linear-combination results.

A ``LinearCombinationGeometrySnapshot`` describes one instantaneous linear
combination.  This module aggregates a finite sequence of those snapshots into
one immutable trace snapshot containing

* the sampled coefficient vectors,
* the sampled resultant tips, and
* the line segments joining consecutive resultant tips.

The module deliberately contains no display projection and no Manim code.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

from .linear_combination_geometry import LinearCombinationGeometrySnapshot


FloatArray = NDArray[np.float64]


def _immutable_float_array(values: object) -> FloatArray:
    """Return an owned, read-only floating-point NumPy array."""

    array = np.array(values, dtype=float, copy=True)
    array.setflags(write=False)
    return array


@dataclass(frozen=True)
class LinearCombinationTraceSnapshot:
    """Immutable sampled trace of a linear-combination coefficient sweep.

    Attributes
    ----------
    coefficients:
        Shape ``(sample_count, coefficient_dimension)``.
    resultant_points:
        Shape ``(sample_count, ambient_dimension)``.  Each row is the tip of
        the corresponding geometry snapshot's ``resultant_segment``.
    resultant_segments:
        Shape ``(max(sample_count - 1, 0), 2, ambient_dimension)``.  Segment
        ``i`` joins ``resultant_points[i]`` to ``resultant_points[i + 1]``.
    """

    coefficients: FloatArray
    resultant_points: FloatArray
    resultant_segments: FloatArray

    @property
    def sample_count(self) -> int:
        """Number of sampled linear combinations in the trace."""

        return int(self.resultant_points.shape[0])

    @property
    def coefficient_dimension(self) -> int:
        """Number of coefficients in each sampled coefficient vector."""

        return int(self.coefficients.shape[1])

    @property
    def ambient_dimension(self) -> int:
        """Dimension of each sampled resultant vector."""

        return int(self.resultant_points.shape[1])


class LinearCombinationTrace:
    """Build an immutable trace from geometry snapshots.

    The class consumes only the established Checkpoint 15 interfaces:

    * ``snapshot.linear_combination_snapshot.coefficients``
    * ``snapshot.resultant_segment``

    It does not construct or alter any existing engine object.
    """

    def __init__(
        self,
        geometry_snapshots: Iterable[LinearCombinationGeometrySnapshot],
    ) -> None:
        snapshots = tuple(geometry_snapshots)
        if not snapshots:
            raise ValueError("geometry_snapshots must contain at least one snapshot")

        coefficient_rows: list[FloatArray] = []
        resultant_points: list[FloatArray] = []
        coefficient_dimension: int | None = None
        ambient_dimension: int | None = None

        for index, geometry_snapshot in enumerate(snapshots):
            try:
                linear_combination_snapshot = (
                    geometry_snapshot.linear_combination_snapshot
                )
                raw_coefficients = linear_combination_snapshot.coefficients
                raw_resultant_segment = geometry_snapshot.resultant_segment
            except AttributeError as exc:
                raise TypeError(
                    "each geometry snapshot must expose "
                    "linear_combination_snapshot.coefficients and "
                    "resultant_segment"
                ) from exc

            coefficients = np.asarray(raw_coefficients, dtype=float)
            if coefficients.ndim != 1 or coefficients.size == 0:
                raise ValueError(
                    f"snapshot {index} coefficients must be a nonempty 1-D array"
                )
            if not np.all(np.isfinite(coefficients)):
                raise ValueError(
                    f"snapshot {index} coefficients must contain only finite values"
                )

            resultant_segment = np.asarray(raw_resultant_segment, dtype=float)
            if (
                resultant_segment.ndim != 2
                or resultant_segment.shape[0] != 2
                or resultant_segment.shape[1] == 0
            ):
                raise ValueError(
                    f"snapshot {index} resultant_segment must have shape (2, dimension)"
                )
            if not np.all(np.isfinite(resultant_segment)):
                raise ValueError(
                    f"snapshot {index} resultant_segment must contain only finite values"
                )

            if coefficient_dimension is None:
                coefficient_dimension = int(coefficients.shape[0])
            elif coefficients.shape[0] != coefficient_dimension:
                raise ValueError(
                    "all snapshots must use the same coefficient dimension"
                )

            current_ambient_dimension = int(resultant_segment.shape[1])
            if ambient_dimension is None:
                ambient_dimension = current_ambient_dimension
            elif current_ambient_dimension != ambient_dimension:
                raise ValueError(
                    "all snapshots must use the same ambient dimension"
                )

            coefficient_rows.append(_immutable_float_array(coefficients))
            resultant_points.append(
                _immutable_float_array(resultant_segment[1])
            )

        coefficients_array = _immutable_float_array(
            np.stack(coefficient_rows, axis=0)
        )
        resultant_points_array = _immutable_float_array(
            np.stack(resultant_points, axis=0)
        )

        assert ambient_dimension is not None
        if len(resultant_points) == 1:
            resultant_segments_array = _immutable_float_array(
                np.empty((0, 2, ambient_dimension), dtype=float)
            )
        else:
            resultant_segments_array = _immutable_float_array(
                np.stack(
                    (
                        resultant_points_array[:-1],
                        resultant_points_array[1:],
                    ),
                    axis=1,
                )
            )

        self._snapshot = LinearCombinationTraceSnapshot(
            coefficients=coefficients_array,
            resultant_points=resultant_points_array,
            resultant_segments=resultant_segments_array,
        )

    def snapshot(self) -> LinearCombinationTraceSnapshot:
        """Return the immutable trace snapshot."""

        return self._snapshot
