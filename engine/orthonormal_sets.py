"""Renderer-independent numerical content for CP152: Orthonormal Sets."""

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


def normalize(values: Iterable[float]) -> FloatArray:
    vector = _vector(values, name="vector")
    return vector / np.linalg.norm(vector)


@dataclass(frozen=True)
class OrthonormalSetSnapshot:
    vectors: tuple[FloatArray, ...]
    norms: tuple[float, ...]
    gram_matrix: FloatArray

    @property
    def is_orthogonal(self) -> bool:
        off_diagonal = self.gram_matrix - np.diag(np.diag(self.gram_matrix))
        return bool(np.allclose(off_diagonal, 0.0))

    @property
    def is_orthonormal(self) -> bool:
        return bool(np.allclose(self.gram_matrix, np.eye(len(self.vectors))))


class OrthonormalSetExample:
    def __init__(self, vectors: Sequence[Sequence[float]]) -> None:
        if len(vectors) < 2:
            raise ValueError("an orthonormal-set example needs at least two vectors")
        converted = tuple(_vector(vector, name=f"vector_{index}") for index, vector in enumerate(vectors))
        shapes = {vector.shape for vector in converted}
        if len(shapes) != 1:
            raise ValueError("all vectors must have the same dimension")
        self._vectors = converted

    def snapshot(self) -> OrthonormalSetSnapshot:
        matrix = np.column_stack(self._vectors)
        gram = matrix.T @ matrix
        return OrthonormalSetSnapshot(
            vectors=tuple(vector.copy() for vector in self._vectors),
            norms=tuple(float(np.linalg.norm(vector)) for vector in self._vectors),
            gram_matrix=gram,
        )


class OrthonormalSetsLesson:
    DEFINITION = (
        r"\{\mathbf{q}_1,\ldots,\mathbf{q}_k\}\text{ is orthonormal if }"
        r"\mathbf{q}_i\cdot\mathbf{q}_j=0\ (i\ne j)\text{ and }\|\mathbf{q}_i\|=1"
    )
    KRONECKER = r"\mathbf{q}_i\cdot\mathbf{q}_j=\delta_{ij}"
    MATRIX_IDENTITY = r"Q^TQ=I"
    COORDINATE_RULE = r"c_j=\mathbf{q}_j\cdot\mathbf{x}"

    def __init__(self) -> None:
        self._scaled = OrthonormalSetExample(
            (
                (2.0, 0.0, 0.0),
                (0.0, 2.5, 0.0),
                (0.0, 0.0, 1.6),
            )
        )
        self._unit = OrthonormalSetExample(
            (
                (1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0),
            )
        )

    def scaled_orthogonal_example(self) -> OrthonormalSetSnapshot:
        return self._scaled.snapshot()

    def normalized_example(self) -> OrthonormalSetSnapshot:
        return self._unit.snapshot()

    def normalize_scaled_example(self) -> tuple[FloatArray, ...]:
        return tuple(normalize(vector) for vector in self._scaled.snapshot().vectors)
