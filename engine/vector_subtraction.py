"""Renderer-independent vector subtraction built on linear combinations."""

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
    snapshot_method = getattr(model, "snapshot", None)
    if not callable(snapshot_method):
        raise TypeError("LinearCombination must expose snapshot(coefficients)")
    return snapshot_method(coefficients)


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
        and np.allclose(result, expected_result)
    )


@dataclass(frozen=True, slots=True)
class VectorSubtractionSnapshot:
    """Immutable instructional view of ``u - v = u + (-v)``."""

    minuend_vector: tuple[float, ...]
    subtrahend_vector: tuple[float, ...]
    negative_subtrahend: tuple[float, ...]
    result: tuple[float, ...]
    minuend_segment: tuple[tuple[float, ...], tuple[float, ...]]
    negative_segment: tuple[tuple[float, ...], tuple[float, ...]]
    translated_negative_segment: tuple[
        tuple[float, ...],
        tuple[float, ...],
    ]
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
        return self.minuend_segment[1] == self.translated_negative_segment[0]

    @property
    def is_opposite_vector(self) -> bool:
        subtrahend = np.asarray(self.subtrahend_vector, dtype=float)
        negative = np.asarray(self.negative_subtrahend, dtype=float)
        return bool(np.allclose(negative, -subtrahend))

    @property
    def preserves_magnitude(self) -> bool:
        subtrahend = np.asarray(self.subtrahend_vector, dtype=float)
        negative = np.asarray(self.negative_subtrahend, dtype=float)
        return bool(np.isclose(np.linalg.norm(negative), np.linalg.norm(subtrahend)))


class VectorSubtraction:
    """Specialize the linear-combination engine to coefficients ``(1, -1)``."""

    __slots__ = ("_minuend", "_subtrahend", "_model")

    def __init__(
        self,
        minuend_vector: Iterable[float],
        subtrahend_vector: Iterable[float],
    ) -> None:
        minuend = _as_finite_vector(minuend_vector, name="minuend_vector")
        subtrahend = _as_finite_vector(
            subtrahend_vector,
            name="subtrahend_vector",
        )

        if minuend.shape != subtrahend.shape:
            raise ValueError(
                "minuend_vector and subtrahend_vector must have the same dimension"
            )

        vectors = np.vstack((minuend, subtrahend))

        self._minuend = minuend.copy()
        self._subtrahend = subtrahend.copy()
        self._model = LinearCombination(vectors)

    @property
    def dimension(self) -> int:
        return int(self._minuend.size)

    def snapshot(self) -> VectorSubtractionSnapshot:
        coefficients = np.asarray((1.0, -1.0), dtype=float)
        source = _snapshot_from(self._model, coefficients)
        vectors = np.vstack((self._minuend, self._subtrahend))

        if not _snapshot_matches(
            source,
            vectors=vectors,
            coefficients=coefficients,
        ):
            raise ValueError(
                "LinearCombination snapshot no longer matches vector subtraction"
            )

        partial_sums = np.asarray(source.partial_sums, dtype=float)
        result = np.asarray(source.result, dtype=float)
        negative = -self._subtrahend

        origin = tuple(float(value) for value in partial_sums[0])
        minuend_tip = tuple(float(value) for value in partial_sums[1])
        result_tip = tuple(float(value) for value in partial_sums[2])
        negative_tip = tuple(float(value) for value in negative)

        return VectorSubtractionSnapshot(
            minuend_vector=tuple(float(value) for value in self._minuend),
            subtrahend_vector=tuple(float(value) for value in self._subtrahend),
            negative_subtrahend=negative_tip,
            result=tuple(float(value) for value in result),
            minuend_segment=(origin, minuend_tip),
            negative_segment=(origin, negative_tip),
            translated_negative_segment=(minuend_tip, result_tip),
            resultant_segment=(origin, result_tip),
            linear_combination_snapshot=source,
        )
