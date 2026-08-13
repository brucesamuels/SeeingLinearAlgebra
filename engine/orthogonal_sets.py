"""Renderer-independent numerical content for CP151: Orthogonal Sets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


def _vector(values: Iterable[float], *, name: str) -> FloatArray:
    vector = np.asarray(tuple(values), dtype=float)
    if vector.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional.")
    if vector.size == 0:
        raise ValueError(f"{name} must contain at least one coordinate.")
    if not np.all(np.isfinite(vector)):
        raise ValueError(f"{name} must contain finite coordinates.")
    if np.allclose(vector, 0.0):
        raise ValueError(f"{name} must be nonzero.")
    return vector


@dataclass(frozen=True)
class OrthogonalSetSnapshot:
    vectors: tuple[FloatArray, ...]
    pairwise_dots: tuple[tuple[int, int, float], ...]

    @property
    def is_orthogonal(self) -> bool:
        return all(np.isclose(value, 0.0) for _, _, value in self.pairwise_dots)


class OrthogonalSetExample:
    def __init__(self, vectors: Sequence[Sequence[float]]) -> None:
        if len(vectors) < 2:
            raise ValueError("an orthogonal-set example needs at least two vectors")
        converted = tuple(_vector(vector, name=f"vector_{index}") for index, vector in enumerate(vectors))
        lengths = {vector.shape for vector in converted}
        if len(lengths) != 1:
            raise ValueError("all vectors must have the same dimension")
        self._vectors = converted

    def snapshot(self) -> OrthogonalSetSnapshot:
        pairwise_dots: list[tuple[int, int, float]] = []
        for first in range(len(self._vectors)):
            for second in range(first + 1, len(self._vectors)):
                dot = float(np.dot(self._vectors[first], self._vectors[second]))
                pairwise_dots.append((first, second, dot))
        return OrthogonalSetSnapshot(
            vectors=tuple(vector.copy() for vector in self._vectors),
            pairwise_dots=tuple(pairwise_dots),
        )


class OrthogonalSetsLesson:
    DEFINITION = r"\{\mathbf{v}_1,\ldots,\mathbf{v}_k\}\text{ is orthogonal if }\mathbf{v}_i\cdot\mathbf{v}_j=0\text{ whenever }i\ne j"
    THEOREM = r"\text{Orthogonal nonzero vectors are linearly independent.}"

    def __init__(self) -> None:
        self._orthogonal = OrthogonalSetExample(
            (
                (2.0, 0.0, 0.0),
                (0.0, 2.0, 0.0),
                (0.0, 0.0, 2.0),
            )
        )
        self._nonexample = OrthogonalSetExample(
            (
                (2.0, 0.0, 0.0),
                (0.0, 2.0, 0.0),
                (1.5, 0.0, 1.5),
            )
        )

    def orthogonal_example(self) -> OrthogonalSetSnapshot:
        return self._orthogonal.snapshot()

    def nonexample(self) -> OrthogonalSetSnapshot:
        return self._nonexample.snapshot()

    @property
    def bridge_to_orthonormal(self) -> tuple[str, str]:
        return (
            r"\mathbf{v}_i\cdot\mathbf{v}_j=0\quad (i\ne j)",
            r"\|\mathbf{v}_i\|=1",
        )
