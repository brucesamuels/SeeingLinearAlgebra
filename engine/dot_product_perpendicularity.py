"""Renderer-independent geometry for CP150: Dot Product and Perpendicularity.

This lesson answers the question raised in CP149 by connecting the coordinate
formula for the dot product to its geometric interpretation via the angle
between two vectors.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


def _vec2(values: Iterable[float], *, name: str) -> FloatArray:
    vector = np.asarray(tuple(values), dtype=float)
    if vector.shape != (2,):
        raise ValueError(f"{name} must contain exactly two coordinates.")
    if not np.all(np.isfinite(vector)):
        raise ValueError(f"{name} must contain finite coordinates.")
    if np.allclose(vector, 0.0):
        raise ValueError(f"{name} must be nonzero.")
    return vector


@dataclass(frozen=True)
class DotProductSnapshot:
    first: FloatArray
    second: FloatArray
    dot_product: float
    norm_first: float
    norm_second: float
    cosine_between: float
    angle_degrees: float

    @property
    def sign_label(self) -> str:
        if np.isclose(self.dot_product, 0.0):
            return "zero"
        if self.dot_product > 0:
            return "positive"
        return "negative"

    @property
    def is_perpendicular(self) -> bool:
        return np.isclose(self.dot_product, 0.0)


class DotProductExample:
    """A validated pair of 2D nonzero vectors."""

    def __init__(self, first: Sequence[float], second: Sequence[float]) -> None:
        self._first = _vec2(first, name="first")
        self._second = _vec2(second, name="second")

    def snapshot(self) -> DotProductSnapshot:
        dot = float(np.dot(self._first, self._second))
        norm_first = float(np.linalg.norm(self._first))
        norm_second = float(np.linalg.norm(self._second))
        cosine = dot / (norm_first * norm_second)
        cosine = float(np.clip(cosine, -1.0, 1.0))
        angle = float(np.degrees(np.arccos(cosine)))
        return DotProductSnapshot(
            first=self._first.copy(),
            second=self._second.copy(),
            dot_product=dot,
            norm_first=norm_first,
            norm_second=norm_second,
            cosine_between=cosine,
            angle_degrees=angle,
        )


class DotProductPerpendicularityLesson:
    """Stable numerical content for the CP150 lesson."""

    FINAL_STATEMENT = r"\mathbf{u}\perp\mathbf{v}\iff\mathbf{u}\cdot\mathbf{v}=0"

    def __init__(self) -> None:
        self._acute = DotProductExample((2.0, 1.0), (1.0, 2.0))
        self._right = DotProductExample((2.0, 0.0), (0.0, 3.0))
        self._obtuse = DotProductExample((2.0, 1.0), (-1.0, 1.0))
        self._bridge = DotProductExample((3.0, 0.0), (1.5, 2.0))

    def bridge_example(self) -> DotProductSnapshot:
        return self._bridge.snapshot()

    def acute_example(self) -> DotProductSnapshot:
        return self._acute.snapshot()

    def right_example(self) -> DotProductSnapshot:
        return self._right.snapshot()

    def obtuse_example(self) -> DotProductSnapshot:
        return self._obtuse.snapshot()

    @property
    def sign_summary(self) -> tuple[tuple[str, str], ...]:
        return (
            ("acute angle", r"\mathbf{u}\cdot\mathbf{v}>0"),
            ("right angle", r"\mathbf{u}\cdot\mathbf{v}=0"),
            ("obtuse angle", r"\mathbf{u}\cdot\mathbf{v}<0"),
        )
