"""Renderer-independent vector addition built on the linear-combination engine."""

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
    """Evaluate the established model at one coefficient vector."""
    snapshot_method = getattr(model, "snapshot", None)
    if not callable(snapshot_method):
        raise TypeError("LinearCombination must expose snapshot(coefficients)")

    try:
        return snapshot_method(coefficients)
    except TypeError:
        # Retain compatibility with a model whose constructor already owns a
        # fixed coefficient vector, while preferring the actual project API.
        return snapshot_method()


def _snapshot_matches(
    snapshot: Any,
    *,
    vectors: np.ndarray,
    coefficients: np.ndarray,
) -> bool:
    required_fields = ("coefficients", "terms", "partial_sums", "result")
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
        and partial_sums.shape
        == (vectors.shape[0] + 1, vectors.shape[1])
        and result.shape == (vectors.shape[1],)
        and np.allclose(snapshot_coefficients, coefficients)
        and np.allclose(terms, expected_terms)
        and np.allclose(partial_sums[0], np.zeros(vectors.shape[1]))
        and np.allclose(partial_sums[1:], np.cumsum(expected_terms, axis=0))
        and np.allclose(partial_sums[-1], expected_result)
        and np.allclose(result, expected_result)
    )


def _build_linear_combination(vectors: np.ndarray) -> LinearCombination:
    """Construct the established vectors-first mathematical model."""
    coefficients = np.ones(vectors.shape[0], dtype=float)
    model = LinearCombination(vectors)
    snapshot = _snapshot_from(model, coefficients)

    if not _snapshot_matches(
        snapshot,
        vectors=vectors,
        coefficients=coefficients,
    ):
        raise ValueError(
            "LinearCombination snapshot does not match coefficient-one "
            "vector addition"
        )

    return model


@dataclass(frozen=True, slots=True)
class VectorAdditionSnapshot:
    """Immutable instructional view of one vector sum."""

    first_vector: tuple[float, ...]
    second_vector: tuple[float, ...]
    result: tuple[float, ...]
    first_segment: tuple[tuple[float, ...], tuple[float, ...]]
    second_segment: tuple[tuple[float, ...], tuple[float, ...]]
    resultant_segment: tuple[tuple[float, ...], tuple[float, ...]]
    linear_combination_snapshot: Any

    @property
    def dimension(self) -> int:
        return len(self.result)

    @property
    def coefficients(self) -> tuple[float, float]:
        source = np.asarray(
            self.linear_combination_snapshot.coefficients,
            dtype=float,
        )
        return tuple(float(value) for value in source)

    @property
    def is_tip_to_tail(self) -> bool:
        return self.first_segment[1] == self.second_segment[0]


class VectorAddition:
    """Specialize the linear-combination engine to coefficients ``(1, 1)``."""

    __slots__ = ("_first_vector", "_second_vector", "_model")

    def __init__(
        self,
        first_vector: Iterable[float],
        second_vector: Iterable[float],
    ) -> None:
        first = _as_finite_vector(first_vector, name="first_vector")
        second = _as_finite_vector(second_vector, name="second_vector")

        if first.shape != second.shape:
            raise ValueError(
                "first_vector and second_vector must have the same dimension"
            )

        vectors = np.vstack((first, second))

        self._first_vector = first.copy()
        self._second_vector = second.copy()
        self._model = _build_linear_combination(vectors)

    @property
    def dimension(self) -> int:
        return int(self._first_vector.size)

    def snapshot(self) -> VectorAdditionSnapshot:
        coefficients = np.ones(2, dtype=float)
        source = _snapshot_from(self._model, coefficients)
        vectors = np.vstack((self._first_vector, self._second_vector))

        if not _snapshot_matches(
            source,
            vectors=vectors,
            coefficients=coefficients,
        ):
            raise ValueError(
                "LinearCombination snapshot no longer matches this vector sum"
            )

        partial_sums = np.asarray(source.partial_sums, dtype=float)
        result = np.asarray(source.result, dtype=float)

        origin = tuple(float(value) for value in partial_sums[0])
        first_tip = tuple(float(value) for value in partial_sums[1])
        result_tip = tuple(float(value) for value in partial_sums[2])

        return VectorAdditionSnapshot(
            first_vector=tuple(float(value) for value in self._first_vector),
            second_vector=tuple(float(value) for value in self._second_vector),
            result=tuple(float(value) for value in result),
            first_segment=(origin, first_tip),
            second_segment=(first_tip, result_tip),
            resultant_segment=(origin, result_tip),
            linear_combination_snapshot=source,
        )
