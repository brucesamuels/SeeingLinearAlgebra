"""Renderer-independent paths through linear-combination coefficient space.

A coefficient sweep changes only the coefficients of a fixed ordered vector
family.  This module owns that interpolation and delegates all resulting
linear-combination mathematics to :class:`LinearCombination`.
"""

from __future__ import annotations

from typing import TypeAlias

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .linear_combination import LinearCombination, LinearCombinationSnapshot


FloatArray: TypeAlias = NDArray[np.float64]


def _validated_progress(progress: float) -> float:
    """Return ``progress`` as a finite scalar in the closed unit interval."""

    array = np.asarray(progress, dtype=float)
    if array.ndim != 0:
        raise ValueError("progress must be a scalar")

    value = float(array)
    if not np.isfinite(value):
        raise ValueError("progress must be finite")
    if value < 0.0 or value > 1.0:
        raise ValueError("progress must lie in the closed interval [0, 1]")
    return value


def _readonly_copy(values: ArrayLike) -> FloatArray:
    """Return an owned read-only float copy."""

    array = np.array(values, dtype=float, copy=True)
    array.setflags(write=False)
    return array


class CoefficientSweepPath:
    """Linearly interpolate coefficients for a fixed linear combination.

    Parameters
    ----------
    linear_combination:
        The fixed ordered vector family and mathematical evaluator.
    start_coefficients, end_coefficients:
        Coefficient vectors defining the endpoints of the sweep.

    Notes
    -----
    For progress ``t`` in ``[0, 1]``, the coefficient vector is

    ``(1 - t) * start_coefficients + t * end_coefficients``.

    The path deliberately does not reproduce scaled-term, partial-sum, or
    resultant calculations.  It passes the interpolated coefficients to the
    supplied :class:`LinearCombination` and returns its snapshot unchanged.
    """

    def __init__(
        self,
        linear_combination: LinearCombination,
        start_coefficients: ArrayLike,
        end_coefficients: ArrayLike,
    ) -> None:
        if not isinstance(linear_combination, LinearCombination):
            raise TypeError("linear_combination must be a LinearCombination")

        start_snapshot = linear_combination.snapshot(start_coefficients)
        end_snapshot = linear_combination.snapshot(end_coefficients)

        self._linear_combination = linear_combination
        self._start_coefficients = start_snapshot.coefficients
        self._end_coefficients = end_snapshot.coefficients
        self._coefficient_delta = _readonly_copy(
            self._end_coefficients - self._start_coefficients
        )

    @property
    def linear_combination(self) -> LinearCombination:
        """The fixed evaluator used to construct every path snapshot."""

        return self._linear_combination

    @property
    def start_coefficients(self) -> FloatArray:
        """Read-only coefficient vector at progress zero."""

        return self._start_coefficients

    @property
    def end_coefficients(self) -> FloatArray:
        """Read-only coefficient vector at progress one."""

        return self._end_coefficients

    @property
    def coefficient_delta(self) -> FloatArray:
        """Read-only change from the start coefficients to the end coefficients."""

        return self._coefficient_delta

    @property
    def vector_count(self) -> int:
        """Number of vectors, and therefore coefficients, in the sweep."""

        return self._linear_combination.vector_count

    @property
    def dimension(self) -> int:
        """Ambient mathematical dimension of the fixed vectors."""

        return self._linear_combination.dimension

    def coefficients_at(self, progress: float) -> FloatArray:
        """Return the interpolated coefficient vector at ``progress``."""

        value = _validated_progress(progress)
        if value == 0.0:
            return _readonly_copy(self._start_coefficients)
        if value == 1.0:
            return _readonly_copy(self._end_coefficients)

        return _readonly_copy(
            self._start_coefficients + value * self._coefficient_delta
        )

    def snapshot(self, progress: float) -> LinearCombinationSnapshot:
        """Return the linear-combination snapshot at ``progress``."""

        return self._linear_combination.snapshot(self.coefficients_at(progress))

    def __call__(self, progress: float) -> LinearCombinationSnapshot:
        """Shorthand for :meth:`snapshot`."""

        return self.snapshot(progress)
