"""Renderer-independent geometry for CP149: Why Orthogonality?

The lesson opens Chapter 6 by comparing coordinate directions without yet
introducing the dot-product criterion for orthogonality.  It provides stable
2D examples for the Manim presentation and keeps all numerical geometry out of
the scene layer.
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
    return vector


@dataclass(frozen=True)
class BasisSnapshot:
    first: FloatArray
    second: FloatArray
    coefficients: FloatArray
    target: FloatArray
    determinant: float
    cosine_between: float

    @property
    def is_independent(self) -> bool:
        return not np.isclose(self.determinant, 0.0)

    @property
    def is_perpendicular(self) -> bool:
        return np.isclose(self.cosine_between, 0.0)


class BasisExample:
    """A validated 2D basis together with one coordinate decomposition."""

    def __init__(
        self,
        first: Sequence[float],
        second: Sequence[float],
        coefficients: Sequence[float],
    ) -> None:
        self._first = _vec2(first, name="first")
        self._second = _vec2(second, name="second")
        self._coefficients = _vec2(coefficients, name="coefficients")

        matrix = np.column_stack((self._first, self._second))
        determinant = float(np.linalg.det(matrix))
        if np.isclose(determinant, 0.0):
            raise ValueError("basis vectors must be linearly independent.")

    def snapshot(self) -> BasisSnapshot:
        matrix = np.column_stack((self._first, self._second))
        target = matrix @ self._coefficients
        determinant = float(np.linalg.det(matrix))
        denominator = float(np.linalg.norm(self._first) * np.linalg.norm(self._second))
        cosine_between = float(np.dot(self._first, self._second) / denominator)
        return BasisSnapshot(
            first=self._first.copy(),
            second=self._second.copy(),
            coefficients=self._coefficients.copy(),
            target=target,
            determinant=determinant,
            cosine_between=cosine_between,
        )


@dataclass(frozen=True)
class DeterminantBridgeSnapshot:
    matrix: FloatArray
    reference_square: FloatArray
    transformed_region: FloatArray
    area_scale: float


class WhyOrthogonalityLesson:
    """Stable numerical content for the CP149 opening lesson."""

    PREVIEW_TOPICS = (
        "Projection",
        "Orthogonal decomposition",
        "Gram-Schmidt",
        "QR factorization",
        "Least squares",
    )

    def __init__(self) -> None:
        # This echoes the determinant chapter with an uncomplicated shear/scale.
        self._bridge_matrix = np.array([[2.0, 1.0], [0.0, 1.0]])
        self._reference_square = np.array(
            [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]],
            dtype=float,
        )

        # Both bases span R^2 and reconstruct the same target x=(2,1).
        self._skew = BasisExample(
            first=(1.0, 0.0),
            second=(1.0, 1.0),
            coefficients=(1.0, 1.0),
        )
        self._orthogonal = BasisExample(
            first=(1.0, 0.0),
            second=(0.0, 1.0),
            coefficients=(2.0, 1.0),
        )

    def determinant_bridge(self) -> DeterminantBridgeSnapshot:
        transformed = self._reference_square @ self._bridge_matrix.T
        return DeterminantBridgeSnapshot(
            matrix=self._bridge_matrix.copy(),
            reference_square=self._reference_square.copy(),
            transformed_region=transformed,
            area_scale=abs(float(np.linalg.det(self._bridge_matrix))),
        )

    def skew_basis(self) -> BasisSnapshot:
        return self._skew.snapshot()

    def orthogonal_basis(self) -> BasisSnapshot:
        return self._orthogonal.snapshot()

    @property
    def preview_topics(self) -> tuple[str, ...]:
        return self.PREVIEW_TOPICS
