"""Renderer-independent mathematics for the Special Vectors lesson."""

from __future__ import annotations

from dataclasses import dataclass
from math import hypot, isclose
from typing import Final, Iterable


Vector2 = tuple[float, float]

SOURCE_VECTOR: Final[Vector2] = (3.0, 2.0)
ZERO_VECTOR: Final[Vector2] = (0.0, 0.0)


@dataclass(frozen=True)
class SpecialVectorSnapshot:
    """Mathematical facts used by the Special Vectors presentation."""

    source: Vector2
    magnitude: float
    unit: Vector2
    zero: Vector2 = ZERO_VECTOR

    def __post_init__(self) -> None:
        if self.source == ZERO_VECTOR:
            raise ValueError("The source vector for normalization must be nonzero.")
        if not isclose(vector_magnitude(self.unit), 1.0, abs_tol=1.0e-12):
            raise ValueError("The normalized vector must have magnitude one.")
        if not same_direction(self.source, self.unit):
            raise ValueError("Normalization must preserve direction.")


def vector_magnitude(vector: Iterable[float]) -> float:
    """Return the Euclidean magnitude of a two-dimensional vector."""

    x, y = (float(component) for component in vector)
    return hypot(x, y)


def normalize_vector(vector: Iterable[float]) -> Vector2:
    """Return the unit vector in the same direction as ``vector``.

    The zero vector cannot be normalized because it has no direction.
    """

    x, y = (float(component) for component in vector)
    magnitude = vector_magnitude((x, y))
    if isclose(magnitude, 0.0, abs_tol=1.0e-12):
        raise ValueError("The zero vector cannot be normalized.")
    return (x / magnitude, y / magnitude)


def same_direction(first: Iterable[float], second: Iterable[float]) -> bool:
    """Return whether two nonzero vectors point in the same direction."""

    x1, y1 = (float(component) for component in first)
    x2, y2 = (float(component) for component in second)
    cross = x1 * y2 - y1 * x2
    dot = x1 * x2 + y1 * y2
    return isclose(cross, 0.0, abs_tol=1.0e-12) and dot > 0.0


def build_special_vector_snapshot(
    source: Iterable[float] = SOURCE_VECTOR,
) -> SpecialVectorSnapshot:
    """Build the approved mathematical state for the lesson."""

    source_tuple = tuple(float(component) for component in source)
    if len(source_tuple) != 2:
        raise ValueError("Special Vectors currently requires a 2D vector.")
    source_2d: Vector2 = (source_tuple[0], source_tuple[1])
    return SpecialVectorSnapshot(
        source=source_2d,
        magnitude=vector_magnitude(source_2d),
        unit=normalize_vector(source_2d),
    )


SPECIAL_VECTORS_SNAPSHOT: Final[SpecialVectorSnapshot] = (
    build_special_vector_snapshot()
)
