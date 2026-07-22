"""Renderer-independent mathematics for the span of one vector.

Checkpoint 68 begins Chapter 2 by shifting attention from one scaled vector to
all vectors obtainable from the same generator.  This module owns only the
mathematics of ``t * v``.  It has no Manim dependency and makes no decisions
about pacing, layout, labels, or rendering.
"""

from __future__ import annotations

from dataclasses import dataclass
from numbers import Real

import numpy as np
from numpy.typing import ArrayLike, NDArray


FloatArray = NDArray[np.float64]


def _readonly_copy(values: ArrayLike) -> FloatArray:
    array = np.asarray(values, dtype=float).copy()
    array.setflags(write=False)
    return array


@dataclass(frozen=True)
class OneVectorSpanSnapshot:
    """One exact scalar multiple of a fixed generator."""

    coefficient: float
    generator: FloatArray
    endpoint: FloatArray

    @property
    def dimension(self) -> int:
        return int(self.generator.size)

    @property
    def is_zero_vector(self) -> bool:
        return bool(np.allclose(self.endpoint, 0.0, atol=1.0e-12, rtol=0.0))


class OneVectorSpan:
    """Compute scalar multiples of one fixed finite-dimensional vector."""

    def __init__(self, generator: ArrayLike) -> None:
        vector = np.asarray(generator, dtype=float)
        if vector.ndim != 1:
            raise ValueError("generator must be a one-dimensional vector")
        if vector.size == 0:
            raise ValueError("generator must contain at least one coordinate")
        if not np.all(np.isfinite(vector)):
            raise ValueError("generator coordinates must be finite")
        self._generator = _readonly_copy(vector)

    @property
    def generator(self) -> FloatArray:
        """Return a defensive, read-only copy of the generator."""

        return _readonly_copy(self._generator)

    @property
    def dimension(self) -> int:
        return int(self._generator.size)

    @property
    def is_zero_generator(self) -> bool:
        return bool(np.allclose(self._generator, 0.0, atol=1.0e-12, rtol=0.0))

    def snapshot(self, coefficient: Real) -> OneVectorSpanSnapshot:
        """Return the exact vector ``coefficient * generator``."""

        if isinstance(coefficient, bool) or not isinstance(coefficient, Real):
            raise TypeError("coefficient must be a real number")
        value = float(coefficient)
        if not np.isfinite(value):
            raise ValueError("coefficient must be finite")
        endpoint = value * self._generator
        return OneVectorSpanSnapshot(
            coefficient=value,
            generator=_readonly_copy(self._generator),
            endpoint=_readonly_copy(endpoint),
        )

    def endpoints_for(self, coefficients: ArrayLike) -> FloatArray:
        """Return one endpoint row for each finite scalar coefficient."""

        values = np.asarray(coefficients, dtype=float)
        if values.ndim != 1:
            raise ValueError("coefficients must be one-dimensional")
        if not np.all(np.isfinite(values)):
            raise ValueError("coefficients must be finite")
        endpoints = values[:, np.newaxis] * self._generator[np.newaxis, :]
        return _readonly_copy(endpoints)
