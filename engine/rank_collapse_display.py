"""Display-projection helpers for rank-collapse animations.

This module remains independent of Manim.  It takes the codomain outputs of a
:class:`RankCollapsePath` object and projects them into a lower-dimensional
*display space* such as 2D or 3D.  A renderer can then convert those display
coordinates into its own scene objects.
"""

from __future__ import annotations

from dataclasses import dataclass
from numbers import Real
from typing import Iterable, Sequence

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .rank_collapse_path import RankCollapsePath


FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class RankCollapseDisplaySnapshot:
    """Projected geometry and collapse data for one animation frame."""

    progress: float
    matrix: FloatArray
    singular_values: FloatArray
    rank: int
    nullity: int
    input_points: FloatArray
    output_points: FloatArray
    basis_images: FloatArray
    display_points: FloatArray
    display_basis_images: FloatArray
    projection_matrix: FloatArray
    display_offset: FloatArray
    display_dimension: int


class LinearDisplayProjector:
    """Project vectors from one Euclidean space into a display space.

    The projector is affine:

        x -> P x + b

    where ``P`` is a real matrix of shape
    ``(display_dimension, input_dimension)`` and ``b`` is an optional offset in
    the display space.

    Collections of row-stored vectors are transformed row-wise.
    """

    def __init__(
        self,
        projection_matrix: ArrayLike,
        *,
        offset: ArrayLike | None = None,
    ) -> None:
        matrix = np.asarray(projection_matrix, dtype=float)

        if matrix.ndim != 2:
            raise ValueError("projection_matrix must be two-dimensional")
        if matrix.shape[0] == 0 or matrix.shape[1] == 0:
            raise ValueError("projection_matrix must be nonempty")
        if not np.all(np.isfinite(matrix)):
            raise ValueError("projection_matrix entries must be finite")

        if offset is None:
            offset_array = np.zeros(matrix.shape[0], dtype=float)
        else:
            offset_array = np.asarray(offset, dtype=float)
            if offset_array.ndim != 1:
                raise ValueError("offset must be one-dimensional")
            if offset_array.size != matrix.shape[0]:
                raise ValueError(
                    "offset dimension must equal the display dimension "
                    f"({matrix.shape[0]})"
                )
            if not np.all(np.isfinite(offset_array)):
                raise ValueError("offset entries must be finite")

        self._projection_matrix = matrix.copy()
        self._offset = offset_array.copy()

    @classmethod
    def from_axis_selector(
        cls,
        input_dimension: int,
        axis_indices: Sequence[int],
        *,
        scales: Sequence[Real] | None = None,
        offset: ArrayLike | None = None,
    ) -> "LinearDisplayProjector":
        """Build a projector by selecting and scaling chosen coordinates.

        Examples
        --------
        ``from_axis_selector(4, [0, 2])`` projects ``R^4`` to ``R^2`` using the
        first and third coordinates.
        """

        if isinstance(input_dimension, bool) or not isinstance(input_dimension, (int, np.integer)):
            raise TypeError("input_dimension must be a positive integer")
        input_dim = int(input_dimension)
        if input_dim <= 0:
            raise ValueError("input_dimension must be positive")

        if len(axis_indices) == 0:
            raise ValueError("axis_indices must contain at least one axis")

        normalized_indices: list[int] = []
        for index in axis_indices:
            if isinstance(index, bool) or not isinstance(index, (int, np.integer)):
                raise TypeError("axis indices must be integers")
            value = int(index)
            if not 0 <= value < input_dim:
                raise ValueError(
                    f"axis index {value} is out of range for input dimension {input_dim}"
                )
            normalized_indices.append(value)

        if len(set(normalized_indices)) != len(normalized_indices):
            raise ValueError("axis_indices must not repeat axes")

        if scales is None:
            scale_values = np.ones(len(normalized_indices), dtype=float)
        else:
            scale_values = np.asarray(scales, dtype=float)
            if scale_values.ndim != 1:
                raise ValueError("scales must be one-dimensional")
            if scale_values.size != len(normalized_indices):
                raise ValueError(
                    "scales length must equal the number of selected axes"
                )
            if not np.all(np.isfinite(scale_values)):
                raise ValueError("scales must be finite")

        matrix = np.zeros((len(normalized_indices), input_dim), dtype=float)
        for row, (axis, scale) in enumerate(zip(normalized_indices, scale_values, strict=True)):
            matrix[row, axis] = float(scale)

        return cls(matrix, offset=offset)

    @property
    def input_dimension(self) -> int:
        return self._projection_matrix.shape[1]

    @property
    def display_dimension(self) -> int:
        return self._projection_matrix.shape[0]

    @property
    def projection_matrix(self) -> FloatArray:
        return self._projection_matrix.copy()

    @property
    def offset(self) -> FloatArray:
        return self._offset.copy()

    def project(self, vectors: ArrayLike) -> FloatArray:
        """Project one vector or a row-stored collection of vectors."""

        array = np.asarray(vectors, dtype=float)

        if array.ndim == 1:
            if array.size != self.input_dimension:
                raise ValueError(
                    "vector dimension must equal the projector input dimension "
                    f"({self.input_dimension})"
                )
            if not np.all(np.isfinite(array)):
                raise ValueError("vector coordinates must be finite")
            return self._projection_matrix @ array + self._offset

        if array.ndim == 2:
            if array.shape[1] != self.input_dimension:
                raise ValueError(
                    "each vector dimension must equal the projector input dimension "
                    f"({self.input_dimension})"
                )
            if not np.all(np.isfinite(array)):
                raise ValueError("vector coordinates must be finite")
            return array @ self._projection_matrix.T + self._offset

        raise ValueError("vectors must be one- or two-dimensional")


class RankCollapseDisplayAdapter:
    """Project rank-collapse geometry into a chosen display space."""

    def __init__(
        self,
        path: RankCollapsePath,
        projector: LinearDisplayProjector,
    ) -> None:
        if not isinstance(path, RankCollapsePath):
            raise TypeError("path must be a RankCollapsePath instance")
        if not isinstance(projector, LinearDisplayProjector):
            raise TypeError("projector must be a LinearDisplayProjector instance")
        if projector.input_dimension != path.codomain_dimension:
            raise ValueError(
                "projector input dimension must equal the path codomain dimension "
                f"({path.codomain_dimension})"
            )

        self._path = path
        self._projector = projector

    @property
    def path(self) -> RankCollapsePath:
        return self._path

    @property
    def projector(self) -> LinearDisplayProjector:
        return self._projector

    @property
    def display_dimension(self) -> int:
        return self._projector.display_dimension

    @property
    def point_count(self) -> int:
        return self._path.point_count

    @property
    def domain_dimension(self) -> int:
        return self._path.domain_dimension

    @property
    def codomain_dimension(self) -> int:
        return self._path.codomain_dimension

    def display_points_at(self, progress: float) -> FloatArray:
        """Project all transformed points at one progress value."""

        return self._projector.project(self._path.points_at(progress))

    def display_basis_images_at(self, progress: float) -> FloatArray:
        """Project images of the domain basis vectors at one progress value."""

        return self._projector.project(self._path.basis_images_at(progress))

    def display_trajectory(
        self,
        point: ArrayLike,
        progress_values: Iterable[Real],
    ) -> FloatArray:
        """Project one point's sampled trajectory into display space."""

        return self._projector.project(self._path.trajectory(point, progress_values))

    def snapshot(self, progress: float) -> RankCollapseDisplaySnapshot:
        """Return projected frame data for one progress value."""

        path_snapshot = self._path.snapshot(progress)
        display_points = self._projector.project(path_snapshot.output_points)
        display_basis_images = self._projector.project(path_snapshot.basis_images)

        return RankCollapseDisplaySnapshot(
            progress=path_snapshot.progress,
            matrix=path_snapshot.matrix.copy(),
            singular_values=path_snapshot.singular_values.copy(),
            rank=path_snapshot.rank,
            nullity=path_snapshot.nullity,
            input_points=path_snapshot.input_points.copy(),
            output_points=path_snapshot.output_points.copy(),
            basis_images=path_snapshot.basis_images.copy(),
            display_points=display_points,
            display_basis_images=display_basis_images,
            projection_matrix=self._projector.projection_matrix,
            display_offset=self._projector.offset,
            display_dimension=self.display_dimension,
        )

    def snapshots(
        self,
        progress_values: Iterable[Real],
    ) -> tuple[RankCollapseDisplaySnapshot, ...]:
        """Return an immutable sequence of projected sampled frames."""

        return tuple(self.snapshot(progress) for progress in progress_values)
