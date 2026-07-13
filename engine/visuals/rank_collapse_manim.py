"""Thin Manim-facing adapter for dimension-independent rank-collapse data.

The mathematical and projection work remains in ``RankCollapse``,
``RankCollapsePath``, and ``RankCollapseDisplayAdapter``.  This module only:

1. converts 1D, 2D, or 3D display coordinates to Manim's three-coordinate
   scene convention;
2. creates a stable point-cloud mobject; and
3. moves those existing point mobjects as animation progress changes.

Manim is imported lazily so the coordinate and update logic can be tested
without requiring a rendering installation.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

import numpy as np
from numpy.typing import ArrayLike, NDArray

from ..rank_collapse_display import RankCollapseDisplayAdapter


FloatArray = NDArray[np.float64]
PointFactory = Callable[..., Any]
GroupFactory = Callable[..., Any]


def to_manim_coordinates(coordinates: ArrayLike) -> FloatArray:
    """Convert one or more display vectors to Manim scene coordinates.

    Manim positions are represented by three coordinates.  Display vectors in
    ``R`` or ``R^2`` are padded with trailing zeros.  Vectors already in
    ``R^3`` are copied unchanged.  Display dimensions above three cannot be
    rendered directly and must first be projected by
    :class:`LinearDisplayProjector`.

    The input may be a single vector of shape ``(d,)`` or a row-stored
    collection with shape ``(count, d)``.  The returned shape mirrors the input:
    ``(3,)`` for one vector and ``(count, 3)`` for a collection.
    """

    array = np.asarray(coordinates, dtype=float)

    if array.ndim not in (1, 2):
        raise ValueError("coordinates must be one- or two-dimensional")
    if array.shape[-1] == 0:
        raise ValueError("coordinates must have positive dimension")
    if array.shape[-1] > 3:
        raise ValueError(
            "display coordinates above dimension 3 must be projected before "
            "conversion to Manim coordinates"
        )
    if not np.all(np.isfinite(array)):
        raise ValueError("coordinate entries must be finite")

    pad_width = 3 - array.shape[-1]
    if array.ndim == 1:
        return np.pad(array, (0, pad_width)).astype(float, copy=False)

    return np.pad(array, ((0, 0), (0, pad_width))).astype(float, copy=False)


class ManimRankCollapsePointCloud:
    """Render a projected rank-collapse path as a stable Manim point cloud.

    Parameters
    ----------
    display_adapter:
        A fully configured :class:`RankCollapseDisplayAdapter`.  Its display
        dimension must be 1, 2, or 3.

    Notes
    -----
    The class intentionally does not subclass ``Scene`` or ``Mobject``.  It is
    a small bridge that creates and updates mobjects owned by the caller's
    scene.  Custom factories may be supplied for testing or for alternate
    point styles.
    """

    def __init__(self, display_adapter: RankCollapseDisplayAdapter) -> None:
        if not isinstance(display_adapter, RankCollapseDisplayAdapter):
            raise TypeError(
                "display_adapter must be a RankCollapseDisplayAdapter instance"
            )
        if display_adapter.display_dimension > 3:
            raise ValueError(
                "Manim point clouds require display dimension 1, 2, or 3"
            )

        self._display_adapter = display_adapter

    @property
    def display_adapter(self) -> RankCollapseDisplayAdapter:
        return self._display_adapter

    @property
    def display_dimension(self) -> int:
        return self._display_adapter.display_dimension

    @property
    def point_count(self) -> int:
        return self._display_adapter.point_count

    def scene_points_at(self, progress: float) -> FloatArray:
        """Return all projected points as Manim-compatible coordinates."""

        return to_manim_coordinates(
            self._display_adapter.display_points_at(progress)
        )

    def scene_basis_images_at(self, progress: float) -> FloatArray:
        """Return projected basis-image endpoints in Manim coordinates."""

        return to_manim_coordinates(
            self._display_adapter.display_basis_images_at(progress)
        )

    def build_point_cloud(
        self,
        progress: float = 0.0,
        *,
        point_factory: PointFactory | None = None,
        group_factory: GroupFactory | None = None,
        point_kwargs: dict[str, Any] | None = None,
    ) -> Any:
        """Create one point mobject per transformed input point.

        When factories are omitted, the method lazily imports ``Dot`` or
        ``Dot3D`` and ``VGroup`` from Manim.  ``Dot3D`` is selected only for a
        three-dimensional display; 1D and 2D displays use ``Dot``.
        """

        if point_factory is None or group_factory is None:
            default_point_factory, default_group_factory = self._manim_factories()
            if point_factory is None:
                point_factory = default_point_factory
            if group_factory is None:
                group_factory = default_group_factory

        kwargs = {} if point_kwargs is None else dict(point_kwargs)
        points = [
            point_factory(point=coordinate.copy(), **kwargs)
            for coordinate in self.scene_points_at(progress)
        ]
        return group_factory(*points)

    def update_point_cloud(self, point_cloud: Any, progress: float) -> Any:
        """Move existing point mobjects to their positions at ``progress``.

        The point objects are not replaced, preserving object identity and
        allowing Manim to animate efficiently with an updater.
        """

        scene_points = self.scene_points_at(progress)
        mobjects = list(point_cloud)

        if len(mobjects) != len(scene_points):
            raise ValueError(
                "point_cloud size must equal the adapter point count "
                f"({len(scene_points)})"
            )

        for mobject, coordinate in zip(mobjects, scene_points, strict=True):
            move_to = getattr(mobject, "move_to", None)
            if not callable(move_to):
                raise TypeError("every point-cloud element must provide move_to")
            move_to(coordinate.copy())

        return point_cloud

    def bind_to_tracker(self, point_cloud: Any, tracker: Any) -> Any:
        """Attach a Manim updater driven by a ValueTracker-like object."""

        add_updater = getattr(point_cloud, "add_updater", None)
        if not callable(add_updater):
            raise TypeError("point_cloud must provide add_updater")

        get_value = getattr(tracker, "get_value", None)
        if not callable(get_value):
            raise TypeError("tracker must provide get_value")

        def updater(group: Any) -> None:
            self.update_point_cloud(group, get_value())

        add_updater(updater)
        return point_cloud

    def sampled_scene_frames(
        self,
        progress_values: Iterable[float],
    ) -> tuple[FloatArray, ...]:
        """Return sampled Manim-coordinate point clouds without mobjects."""

        return tuple(self.scene_points_at(progress) for progress in progress_values)

    def _manim_factories(self) -> tuple[PointFactory, GroupFactory]:
        try:
            from manim import Dot, Dot3D, VGroup
        except ModuleNotFoundError as exc:
            raise ModuleNotFoundError(
                "Manim is required when point_factory and group_factory are "
                "not supplied"
            ) from exc

        point_factory: PointFactory = Dot3D if self.display_dimension == 3 else Dot
        return point_factory, VGroup
