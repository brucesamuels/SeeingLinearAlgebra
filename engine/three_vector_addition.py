"""Renderer-independent addition of three vectors in 3-space."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

import numpy as np

from engine.linear_combination import LinearCombination


def _as_finite_vector(values: Iterable[float], *, name: str) -> np.ndarray:
    try:
        vector = np.asarray(tuple(values), dtype=float)
    except (TypeError, ValueError) as exc:
        raise TypeError(f"{name} must be an iterable of real numbers") from exc

    if vector.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    if vector.size == 0:
        raise ValueError(f"{name} must contain at least one component")
    if not np.all(np.isfinite(vector)):
        raise ValueError(f"{name} must contain only finite values")

    return vector


def _snapshot_from(model: Any, coefficients: np.ndarray) -> Any:
    snapshot_method = getattr(model, 'snapshot', None)
    if not callable(snapshot_method):
        raise TypeError('LinearCombination must expose snapshot(coefficients)')

    try:
        return snapshot_method(coefficients)
    except TypeError:
        return snapshot_method()


def _snapshot_matches(
    snapshot: Any,
    *,
    vectors: np.ndarray,
    coefficients: np.ndarray,
) -> bool:
    required_fields = ('coefficients', 'terms', 'partial_sums', 'result')
    if any(not hasattr(snapshot, field) for field in required_fields):
        return False

    try:
        snapshot_coefficients = np.asarray(snapshot.coefficients, dtype=float)
        terms = np.asarray(snapshot.terms, dtype=float)
        partial_sums = np.asarray(snapshot.partial_sums, dtype=float)
        result = np.asarray(snapshot.result, dtype=float)
    except (TypeError, ValueError):
        return False

    expected_terms = coefficients[:, None] * vectors
    expected_result = coefficients @ vectors

    return (
        snapshot_coefficients.shape == coefficients.shape
        and terms.shape == vectors.shape
        and partial_sums.shape == (vectors.shape[0] + 1, vectors.shape[1])
        and result.shape == (vectors.shape[1],)
        and np.allclose(snapshot_coefficients, coefficients)
        and np.allclose(terms, expected_terms)
        and np.allclose(partial_sums[0], np.zeros(vectors.shape[1]))
        and np.allclose(partial_sums[1:], np.cumsum(expected_terms, axis=0))
        and np.allclose(partial_sums[-1], expected_result)
        and np.allclose(result, expected_result)
    )


def _build_linear_combination(vectors: np.ndarray) -> LinearCombination:
    coefficients = np.ones(vectors.shape[0], dtype=float)
    model = LinearCombination(vectors)
    snapshot = _snapshot_from(model, coefficients)

    if not _snapshot_matches(
        snapshot,
        vectors=vectors,
        coefficients=coefficients,
    ):
        raise ValueError(
            'LinearCombination snapshot does not match coefficient-one '
            'three-vector addition'
        )

    return model


@dataclass(frozen=True, slots=True)
class ThreeVectorAdditionSnapshot:
    """Immutable instructional view of one three-vector sum."""

    first_vector: tuple[float, float, float]
    second_vector: tuple[float, float, float]
    third_vector: tuple[float, float, float]
    result: tuple[float, float, float]
    first_segment: tuple[tuple[float, float, float], tuple[float, float, float]]
    second_segment: tuple[tuple[float, float, float], tuple[float, float, float]]
    third_segment: tuple[tuple[float, float, float], tuple[float, float, float]]
    resultant_segment: tuple[tuple[float, float, float], tuple[float, float, float]]
    parallelepiped_vertices: tuple[tuple[float, float, float], ...]
    parallelepiped_edges: tuple[
        tuple[tuple[float, float, float], tuple[float, float, float]], ...
    ]
    linear_combination_snapshot: Any

    @property
    def dimension(self) -> int:
        return len(self.result)

    @property
    def coefficients(self) -> tuple[float, float, float]:
        source = np.asarray(
            self.linear_combination_snapshot.coefficients,
            dtype=float,
        )
        return tuple(float(value) for value in source)

    @property
    def is_successive_path(self) -> bool:
        return (
            self.first_segment[1] == self.second_segment[0]
            and self.second_segment[1] == self.third_segment[0]
        )


class ThreeVectorAddition:
    """Specialize the linear-combination engine to coefficients ``(1, 1, 1)``."""

    __slots__ = ('_first_vector', '_second_vector', '_third_vector', '_model')

    def __init__(
        self,
        first_vector: Iterable[float],
        second_vector: Iterable[float],
        third_vector: Iterable[float],
    ) -> None:
        first = _as_finite_vector(first_vector, name='first_vector')
        second = _as_finite_vector(second_vector, name='second_vector')
        third = _as_finite_vector(third_vector, name='third_vector')

        if first.shape != second.shape or first.shape != third.shape:
            raise ValueError('all three vectors must have the same dimension')
        if first.size != 3:
            raise ValueError('three-vector addition lesson requires 3D vectors')

        vectors = np.vstack((first, second, third))
        self._first_vector = first.copy()
        self._second_vector = second.copy()
        self._third_vector = third.copy()
        self._model = _build_linear_combination(vectors)

    @property
    def dimension(self) -> int:
        return int(self._first_vector.size)

    def snapshot(self) -> ThreeVectorAdditionSnapshot:
        coefficients = np.ones(3, dtype=float)
        source = _snapshot_from(self._model, coefficients)
        vectors = np.vstack(
            (self._first_vector, self._second_vector, self._third_vector)
        )

        if not _snapshot_matches(
            source,
            vectors=vectors,
            coefficients=coefficients,
        ):
            raise ValueError(
                'LinearCombination snapshot no longer matches this three-vector sum'
            )

        partial_sums = np.asarray(source.partial_sums, dtype=float)
        result = np.asarray(source.result, dtype=float)

        origin = tuple(float(value) for value in partial_sums[0])
        first_tip = tuple(float(value) for value in partial_sums[1])
        second_tip = tuple(float(value) for value in partial_sums[2])
        result_tip = tuple(float(value) for value in partial_sums[3])

        first = tuple(float(value) for value in self._first_vector)
        second = tuple(float(value) for value in self._second_vector)
        third = tuple(float(value) for value in self._third_vector)
        result_tuple = tuple(float(value) for value in result)

        zero = np.zeros(3, dtype=float)
        u = self._first_vector
        v = self._second_vector
        w = self._third_vector

        vertices = tuple(
            tuple(float(value) for value in point)
            for point in (
                zero,
                u,
                v,
                w,
                u + v,
                u + w,
                v + w,
                u + v + w,
            )
        )

        edges = tuple(
            (vertices[start], vertices[end])
            for start, end in (
                (0, 1), (0, 2), (0, 3),
                (1, 4), (1, 5),
                (2, 4), (2, 6),
                (3, 5), (3, 6),
                (4, 7), (5, 7), (6, 7),
            )
        )

        return ThreeVectorAdditionSnapshot(
            first_vector=first,
            second_vector=second,
            third_vector=third,
            result=result_tuple,
            first_segment=(origin, first_tip),
            second_segment=(first_tip, second_tip),
            third_segment=(second_tip, result_tip),
            resultant_segment=(origin, result_tip),
            parallelepiped_vertices=vertices,
            parallelepiped_edges=edges,
            linear_combination_snapshot=source,
        )
