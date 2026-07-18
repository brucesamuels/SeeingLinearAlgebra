from __future__ import annotations

import inspect

from engine.vector_addition import VectorAddition, _build_linear_combination


def test_vector_addition_uses_vectors_first_linear_combination_api() -> None:
    source = inspect.getsource(_build_linear_combination)

    assert "model = LinearCombination(vectors)" in source
    assert "_snapshot_from(model, coefficients)" in source
    assert "LinearCombination(vectors, coefficients)" not in source
    assert "LinearCombination(coefficients, vectors)" not in source


def test_vector_addition_evaluates_coefficients_through_snapshot() -> None:
    snapshot = VectorAddition((3.0, 1.0), (1.0, 2.0)).snapshot()

    assert snapshot.coefficients == (1.0, 1.0)
    assert snapshot.result == (4.0, 3.0)
