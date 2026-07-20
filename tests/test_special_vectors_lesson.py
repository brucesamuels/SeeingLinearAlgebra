from __future__ import annotations

from math import isclose, sqrt

import pytest

from engine.special_vectors_lesson import (
    SOURCE_VECTOR,
    SPECIAL_VECTORS_SNAPSHOT,
    ZERO_VECTOR,
    build_special_vector_snapshot,
    normalize_vector,
    same_direction,
    vector_magnitude,
)


def test_approved_source_vector_and_magnitude() -> None:
    assert SOURCE_VECTOR == (3.0, 2.0)
    assert isclose(vector_magnitude(SOURCE_VECTOR), sqrt(13.0))


def test_normalization_produces_expected_unit_vector() -> None:
    unit = normalize_vector(SOURCE_VECTOR)

    assert isclose(unit[0], 3.0 / sqrt(13.0))
    assert isclose(unit[1], 2.0 / sqrt(13.0))
    assert isclose(vector_magnitude(unit), 1.0)


def test_normalization_preserves_direction() -> None:
    assert same_direction(SOURCE_VECTOR, SPECIAL_VECTORS_SNAPSHOT.unit)


def test_zero_vector_is_distinguished_and_cannot_be_normalized() -> None:
    assert ZERO_VECTOR == (0.0, 0.0)
    assert vector_magnitude(ZERO_VECTOR) == 0.0

    with pytest.raises(ValueError, match="cannot be normalized"):
        normalize_vector(ZERO_VECTOR)


def test_snapshot_contains_renderer_independent_lesson_facts() -> None:
    snapshot = build_special_vector_snapshot()

    assert snapshot.source == SOURCE_VECTOR
    assert snapshot.zero == ZERO_VECTOR
    assert isclose(snapshot.magnitude, sqrt(13.0))
    assert isclose(vector_magnitude(snapshot.unit), 1.0)


def test_snapshot_rejects_non_two_dimensional_input() -> None:
    with pytest.raises(ValueError, match="requires a 2D vector"):
        build_special_vector_snapshot((1.0, 2.0, 3.0))
