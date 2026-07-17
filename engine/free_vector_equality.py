"""Renderer-independent equality data for translated copies of a free vector."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import ArrayLike, NDArray

from engine.vector_representation import (
    VectorRepresentation,
    VectorRepresentationSnapshot,
)


FloatArray = NDArray[np.float64]


def _readonly_origin(origin: ArrayLike, *, dimension: int) -> FloatArray:
    array = np.asarray(origin, dtype=float)
    if array.ndim != 1:
        raise ValueError("translation origin must be one-dimensional")
    if array.size != dimension:
        raise ValueError("translation origin dimension must match vector dimension")
    if not np.all(np.isfinite(array)):
        raise ValueError("translation origin must contain finite values")
    result = np.array(array, dtype=float, copy=True)
    result.setflags(write=False)
    return result


@dataclass(frozen=True, slots=True)
class FreeVectorEqualitySnapshot:
    """One base vector and translated copies that represent the same vector."""

    base: VectorRepresentationSnapshot
    copies: tuple[VectorRepresentationSnapshot, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.base, VectorRepresentationSnapshot):
            raise TypeError("base must be a VectorRepresentationSnapshot")
        if not self.copies:
            raise ValueError("free-vector equality requires at least one copy")
        for copy in self.copies:
            if not isinstance(copy, VectorRepresentationSnapshot):
                raise TypeError(
                    "copies must contain VectorRepresentationSnapshot values"
                )
            if copy.dimension != self.base.dimension:
                raise ValueError("all copies must have the same dimension")
            if not np.allclose(copy.coordinates, self.base.coordinates):
                raise ValueError("all copies must have the same coordinates")
            if not np.isclose(copy.magnitude, self.base.magnitude):
                raise ValueError("all copies must have the same magnitude")

    @property
    def copy_count(self) -> int:
        return len(self.copies)

    @property
    def all_equal_as_free_vectors(self) -> bool:
        return all(
            np.allclose(copy.coordinates, self.base.coordinates)
            and np.isclose(copy.magnitude, self.base.magnitude)
            for copy in self.copies
        )

    @property
    def distinct_origins(self) -> bool:
        origins = {
            tuple(float(value) for value in copy.origin)
            for copy in self.copies
        }
        return len(origins) == len(self.copies)


class FreeVectorEquality:
    """Build translated copies of one free vector."""

    __slots__ = ("_base", "_origins")

    def __init__(
        self,
        coordinates: ArrayLike,
        origins: Iterable[ArrayLike],
    ) -> None:
        base = VectorRepresentation(coordinates)
        normalized_origins = tuple(
            _readonly_origin(origin, dimension=base.dimension)
            for origin in origins
        )
        if not normalized_origins:
            raise ValueError("at least one translated origin is required")
        self._base = base
        self._origins = normalized_origins

    def snapshot(self) -> FreeVectorEqualitySnapshot:
        return FreeVectorEqualitySnapshot(
            base=self._base.snapshot(),
            copies=tuple(
                self._base.translated_to(origin).snapshot()
                for origin in self._origins
            ),
        )
