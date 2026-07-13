"""Dimension-independent geometry paths for rank-collapse animations.

This module contains no Manim code.  It transforms arbitrary collections of
points or vectors in the domain of a :class:`RankCollapse` model and returns
frame data in the matrix codomain.  A renderer may later project that data into
2D or 3D display coordinates without duplicating the linear-algebra logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from numbers import Real
from typing import Iterable

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .rank_collapse import RankCollapse


FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class RankCollapsePathSnapshot:
    """All geometry data needed to render one rank-collapse frame.

    Arrays follow a row-vector convention for collections of geometry:

    - ``input_points`` has shape ``(point_count, domain_dimension)``.
    - ``output_points`` has shape ``(point_count, codomain_dimension)``.
    - ``basis_images`` has shape
      ``(domain_dimension, codomain_dimension)``; row ``i`` is the image of
      the domain standard basis vector ``e_i``.
    """

    progress: float
    matrix: FloatArray
    singular_values: FloatArray
    rank: int
    nullity: int
    input_points: FloatArray
    output_points: FloatArray
    basis_images: FloatArray


class RankCollapsePath:
    """Transform arbitrary-dimensional geometry through a rank collapse.

    Parameters
    ----------
    collapse:
        The dimension-independent :class:`RankCollapse` mathematical model.
    points:
        One point/vector of length ``domain_dimension`` or a two-dimensional
        array whose rows are points/vectors in the domain.

    Notes
    -----
    The class deliberately does not decide how an output in ``R^m`` should be
    displayed.  A 2D or 3D renderer is responsible only for choosing a display
    projection and converting the returned numerical arrays into mobjects.
    """

    def __init__(self, collapse: RankCollapse, points: ArrayLike) -> None:
        if not isinstance(collapse, RankCollapse):
            raise TypeError("collapse must be a RankCollapse instance")

        self._collapse = collapse
        self._input_points = self._normalize_points(points)

    @property
    def collapse(self) -> RankCollapse:
        return self._collapse

    @property
    def domain_dimension(self) -> int:
        return self._collapse.domain_dimension

    @property
    def codomain_dimension(self) -> int:
        return self._collapse.codomain_dimension

    @property
    def point_count(self) -> int:
        return self._input_points.shape[0]

    @property
    def input_points(self) -> FloatArray:
        return self._input_points.copy()

    def points_at(self, progress: float) -> FloatArray:
        """Return every transformed point at one progress value.

        Rows are transformed by ``x -> A(progress) x``.  With row-stored input
        points, this is computed as ``points @ A(progress).T``.
        """

        matrix = self._collapse.matrix_at(progress)
        return self._input_points @ matrix.T

    def basis_images_at(self, progress: float) -> FloatArray:
        """Return images of the domain standard basis vectors as rows."""

        return self._collapse.matrix_at(progress).T.copy()

    def trajectory(
        self,
        point: ArrayLike,
        progress_values: Iterable[Real],
    ) -> FloatArray:
        """Return one point's complete trajectory through sampled progress.

        The returned array has shape
        ``(number_of_progress_values, codomain_dimension)``.
        """

        normalized = self._normalize_single_point(point)
        matrices = [self._collapse.matrix_at(p) for p in progress_values]

        if not matrices:
            return np.empty((0, self.codomain_dimension), dtype=float)

        return np.vstack([matrix @ normalized for matrix in matrices])

    def snapshot(self, progress: float) -> RankCollapsePathSnapshot:
        """Return all mathematical and geometry data for one frame."""

        collapse_snapshot = self._collapse.snapshot(progress)
        matrix = collapse_snapshot.matrix

        return RankCollapsePathSnapshot(
            progress=collapse_snapshot.progress,
            matrix=matrix.copy(),
            singular_values=collapse_snapshot.singular_values.copy(),
            rank=collapse_snapshot.rank,
            nullity=collapse_snapshot.nullity,
            input_points=self._input_points.copy(),
            output_points=self._input_points @ matrix.T,
            basis_images=matrix.T.copy(),
        )

    def snapshots(
        self,
        progress_values: Iterable[Real],
    ) -> tuple[RankCollapsePathSnapshot, ...]:
        """Return an immutable sequence of sampled animation frames."""

        return tuple(self.snapshot(progress) for progress in progress_values)

    def _normalize_points(self, points: ArrayLike) -> FloatArray:
        array = np.asarray(points, dtype=float)

        if array.ndim == 1:
            array = array.reshape(1, -1)
        elif array.ndim != 2:
            raise ValueError("points must be one- or two-dimensional")

        if array.shape[0] == 0:
            raise ValueError("points must contain at least one point")
        if array.shape[1] != self.domain_dimension:
            raise ValueError(
                "each point dimension must equal the matrix domain dimension "
                f"({self.domain_dimension})"
            )
        if not np.all(np.isfinite(array)):
            raise ValueError("point coordinates must be finite")

        return array.copy()

    def _normalize_single_point(self, point: ArrayLike) -> FloatArray:
        array = np.asarray(point, dtype=float)

        if array.ndim != 1:
            raise ValueError("point must be one-dimensional")
        if array.size != self.domain_dimension:
            raise ValueError(
                "point dimension must equal the matrix domain dimension "
                f"({self.domain_dimension})"
            )
        if not np.all(np.isfinite(array)):
            raise ValueError("point coordinates must be finite")

        return array.copy()
