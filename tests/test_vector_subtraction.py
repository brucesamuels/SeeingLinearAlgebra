from __future__ import annotations

import inspect

import numpy as np
import pytest

from engine.vector_subtraction import VectorSubtraction, VectorSubtractionSnapshot


def test_vector_subtraction_computes_u_minus_v() -> None:
    snapshot = VectorSubtraction((3, 1), (1, 2)).snapshot()

    assert isinstance(snapshot, VectorSubtractionSnapshot)
    assert snapshot.minuend_vector == (3.0, 1.0)
    assert snapshot.subtrahend_vector == (1.0, 2.0)
    assert snapshot.negative_subtrahend == (-1.0, -2.0)
    assert snapshot.result == (2.0, -1.0)
    assert snapshot.coefficients == (1.0, -1.0)


def test_vector_subtraction_exposes_head_to_tail_geometry() -> None:
    snapshot = VectorSubtraction((3, 1), (1, 2)).snapshot()

    assert snapshot.minuend_segment == ((0.0, 0.0), (3.0, 1.0))
    assert snapshot.negative_segment == ((0.0, 0.0), (-1.0, -2.0))
    assert snapshot.translated_negative_segment == (
        (3.0, 1.0),
        (2.0, -1.0),
    )
    assert snapshot.resultant_segment == ((0.0, 0.0), (2.0, -1.0))
    assert snapshot.is_tip_to_tail


def test_negative_vector_preserves_magnitude_and_reverses_direction() -> None:
    snapshot = VectorSubtraction((3, 1), (1, 2)).snapshot()

    assert snapshot.is_opposite_vector
    assert snapshot.preserves_magnitude
    assert np.isclose(
        np.linalg.norm(snapshot.subtrahend_vector),
        np.linalg.norm(snapshot.negative_subtrahend),
    )


def test_vector_subtraction_accepts_any_matching_dimension() -> None:
    snapshot = VectorSubtraction((2, -1, 4), (5, 3, -2)).snapshot()

    assert snapshot.dimension == 3
    assert snapshot.result == (-3.0, -4.0, 6.0)


def test_vector_subtraction_rejects_dimension_mismatch() -> None:
    with pytest.raises(ValueError, match="same dimension"):
        VectorSubtraction((1, 2), (1, 2, 3))


def test_vector_subtraction_rejects_empty_or_nonfinite_vectors() -> None:
    with pytest.raises(ValueError, match="at least one component"):
        VectorSubtraction((), ())

    with pytest.raises(ValueError, match="finite"):
        VectorSubtraction((1, np.inf), (2, 3))


def test_vector_subtraction_uses_linear_combination_coefficients() -> None:
    source = inspect.getsource(VectorSubtraction)

    assert "LinearCombination(vectors)" in source
    assert "(1.0, -1.0)" in source
    assert "_snapshot_from(self._model, coefficients)" in source


def test_vector_subtraction_module_has_no_manim_dependency() -> None:
    import engine.vector_subtraction as module

    source = inspect.getsource(module)
    assert "manim" not in source.lower()
