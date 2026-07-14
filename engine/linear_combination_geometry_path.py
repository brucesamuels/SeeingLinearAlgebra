"""Renderer-independent geometry paths for coefficient sweeps.

This module composes :class:`CoefficientSweepPath` with
:class:`LinearCombinationGeometry`.  It owns no coefficient interpolation and
constructs no segment endpoints itself.
"""

from __future__ import annotations

from .coefficient_sweep_path import CoefficientSweepPath
from .linear_combination import LinearCombination
from .linear_combination_geometry import (
    LinearCombinationGeometry,
    LinearCombinationGeometrySnapshot,
)


class LinearCombinationGeometryPath:
    """Produce linear-combination geometry along a coefficient sweep.

    Parameters
    ----------
    coefficient_sweep_path:
        The renderer-independent path that supplies a
        :class:`LinearCombinationSnapshot` for each progress value.
    geometry:
        The stateless converter that turns each mathematical snapshot into
        tip-to-tail segment geometry.  When omitted, a
        :class:`LinearCombinationGeometry` instance is created.

    Notes
    -----
    This class is intentionally an orchestration layer.  It delegates
    coefficient interpolation to ``coefficient_sweep_path`` and delegates all
    segment construction to ``geometry``.
    """

    def __init__(
        self,
        coefficient_sweep_path: CoefficientSweepPath,
        geometry: LinearCombinationGeometry | None = None,
    ) -> None:
        if not isinstance(coefficient_sweep_path, CoefficientSweepPath):
            raise TypeError(
                "coefficient_sweep_path must be a CoefficientSweepPath"
            )
        if geometry is None:
            geometry = LinearCombinationGeometry()
        if not isinstance(geometry, LinearCombinationGeometry):
            raise TypeError("geometry must be a LinearCombinationGeometry")

        self._coefficient_sweep_path = coefficient_sweep_path
        self._geometry = geometry

    @property
    def coefficient_sweep_path(self) -> CoefficientSweepPath:
        """The exact coefficient path used for every mathematical state."""

        return self._coefficient_sweep_path

    @property
    def geometry(self) -> LinearCombinationGeometry:
        """The exact geometry converter used for every output snapshot."""

        return self._geometry

    @property
    def linear_combination(self) -> LinearCombination:
        """The fixed linear combination owned by the coefficient path."""

        return self._coefficient_sweep_path.linear_combination

    @property
    def vector_count(self) -> int:
        """Number of vectors, coefficients, and tip-to-tail term segments."""

        return self._coefficient_sweep_path.vector_count

    @property
    def dimension(self) -> int:
        """Ambient mathematical dimension of every segment endpoint."""

        return self._coefficient_sweep_path.dimension

    def snapshot(self, progress: float) -> LinearCombinationGeometrySnapshot:
        """Return the complete geometry snapshot at ``progress``."""

        mathematical_snapshot = self._coefficient_sweep_path.snapshot(progress)
        return self._geometry.snapshot(mathematical_snapshot)

    def __call__(self, progress: float) -> LinearCombinationGeometrySnapshot:
        """Shorthand for :meth:`snapshot`."""

        return self.snapshot(progress)
