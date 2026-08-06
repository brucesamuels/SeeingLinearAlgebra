"""Renderer-independent mathematics for CP128: Why Do We Need Determinants?

The lesson intentionally avoids the coordinate formula ``ad - bc``.  It models
how a linear map changes a reference region and records the geometric outcomes
that motivate the determinant: magnitude of area scaling, orientation, and
collapse.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Sequence

import numpy as np


class AreaBehavior(str, Enum):
    """Qualitative behavior of a planar linear transformation."""

    EXPANDS = "expands"
    CONTRACTS = "contracts"
    PRESERVES = "preserves area"
    REVERSES = "reverses orientation"
    COLLAPSES = "collapses area"


@dataclass(frozen=True)
class TransformationExample:
    """A single geometric example used in the opening determinant lesson."""

    key: str
    matrix: np.ndarray
    caption: str
    signed_scale: float
    behavior: AreaBehavior

    @property
    def magnitude(self) -> float:
        return abs(self.signed_scale)

    @property
    def reverses_orientation(self) -> bool:
        return self.signed_scale < 0

    @property
    def is_collapsed(self) -> bool:
        return np.isclose(self.signed_scale, 0.0)


@dataclass(frozen=True)
class RegionSnapshot:
    """Original and transformed vertices for a polygonal region."""

    original_vertices: np.ndarray
    transformed_vertices: np.ndarray
    original_area: float
    transformed_area: float
    signed_scale: float


UNIT_SQUARE = np.array(
    [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]], dtype=float
)


def signed_polygon_area(vertices: Sequence[Sequence[float]]) -> float:
    """Return the signed shoelace area of a polygon.

    Counterclockwise vertex order gives positive area; clockwise order gives
    negative area.  The function is general-purpose and does not use a
    determinant formula for a matrix.
    """

    points = np.asarray(vertices, dtype=float)
    if points.ndim != 2 or points.shape[1] != 2 or len(points) < 3:
        raise ValueError("vertices must be an array-like object of shape (n, 2), n >= 3")
    x = points[:, 0]
    y = points[:, 1]
    return 0.5 * float(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


def transform_vertices(
    matrix: Sequence[Sequence[float]],
    vertices: Sequence[Sequence[float]] = UNIT_SQUARE,
) -> np.ndarray:
    """Apply a 2 x 2 linear map to row-stored planar vertices."""

    linear_map = np.asarray(matrix, dtype=float)
    points = np.asarray(vertices, dtype=float)
    if linear_map.shape != (2, 2):
        raise ValueError("matrix must have shape (2, 2)")
    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError("vertices must have shape (n, 2)")
    return points @ linear_map.T


def region_snapshot(
    matrix: Sequence[Sequence[float]],
    vertices: Sequence[Sequence[float]] = UNIT_SQUARE,
) -> RegionSnapshot:
    """Compute the signed scale of a transformed polygonal region."""

    original = np.asarray(vertices, dtype=float)
    transformed = transform_vertices(matrix, original)
    original_area = signed_polygon_area(original)
    if np.isclose(original_area, 0.0):
        raise ValueError("the reference region must have nonzero signed area")
    transformed_area = signed_polygon_area(transformed)
    return RegionSnapshot(
        original_vertices=original.copy(),
        transformed_vertices=transformed,
        original_area=original_area,
        transformed_area=transformed_area,
        signed_scale=transformed_area / original_area,
    )


def classify_scale(signed_scale: float, *, tolerance: float = 1e-9) -> AreaBehavior:
    """Classify a signed area scale for the lesson's qualitative language."""

    if abs(signed_scale) <= tolerance:
        return AreaBehavior.COLLAPSES
    if signed_scale < 0:
        return AreaBehavior.REVERSES
    if signed_scale > 1.0 + tolerance:
        return AreaBehavior.EXPANDS
    if signed_scale < 1.0 - tolerance:
        return AreaBehavior.CONTRACTS
    return AreaBehavior.PRESERVES


def build_examples() -> tuple[TransformationExample, ...]:
    """Return the four examples in the approved pedagogical order."""

    raw: Iterable[tuple[str, list[list[float]], str]] = (
        ("expand", [[2.0, 1.0], [0.0, 1.0]], "Area expands"),
        ("contract", [[1.0, 0.0], [0.0, 0.5]], "Area contracts"),
        ("reverse", [[-1.0, 0.0], [0.0, 1.0]], "Orientation reverses"),
        ("collapse", [[1.0, 2.0], [0.0, 0.0]], "Area collapses to zero"),
    )
    examples: list[TransformationExample] = []
    for key, matrix, caption in raw:
        array = np.asarray(matrix, dtype=float)
        snapshot = region_snapshot(array)
        examples.append(
            TransformationExample(
                key=key,
                matrix=array,
                caption=caption,
                signed_scale=snapshot.signed_scale,
                behavior=classify_scale(snapshot.signed_scale),
            )
        )
    return tuple(examples)


def central_question() -> str:
    return "How does a linear transformation change area or volume?"


def determinant_motivation() -> str:
    return (
        "The determinant is the single signed number that records area or volume "
        "scaling, orientation, and collapse."
    )
