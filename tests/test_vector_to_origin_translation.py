from __future__ import annotations

import numpy as np
import pytest

from engine.vector_to_origin_translation import VectorToOriginTranslation


def test_translation_computes_vector_as_terminal_minus_initial() -> None:
    path = VectorToOriginTranslation([2.0, 1.0], [5.0, 3.0])

    assert np.allclose(path.vector_coordinates, [3.0, 2.0])
    assert np.allclose(path.required_translation, [-2.0, -1.0])
    assert path.dimension == 2


def test_zero_progress_preserves_original_endpoints() -> None:
    snapshot = VectorToOriginTranslation([2.0, 1.0], [5.0, 3.0]).snapshot(0.0)

    assert np.allclose(snapshot.current_initial_point, [2.0, 1.0])
    assert np.allclose(snapshot.current_terminal_point, [5.0, 3.0])
    assert np.allclose(snapshot.translation, [0.0, 0.0])
    assert not snapshot.is_at_origin


def test_half_progress_translates_both_endpoints_equally() -> None:
    snapshot = VectorToOriginTranslation([2.0, 1.0], [5.0, 3.0]).snapshot(0.5)

    assert np.allclose(snapshot.translation, [-1.0, -0.5])
    assert np.allclose(snapshot.current_initial_point, [1.0, 0.5])
    assert np.allclose(snapshot.current_terminal_point, [4.0, 2.5])
    assert snapshot.subtraction_is_invariant


def test_full_progress_places_tail_at_origin() -> None:
    snapshot = VectorToOriginTranslation([2.0, 1.0], [5.0, 3.0]).snapshot(1.0)

    assert snapshot.is_at_origin
    assert np.allclose(snapshot.current_initial_point, [0.0, 0.0])
    assert np.allclose(snapshot.current_terminal_point, [3.0, 2.0])
    assert np.allclose(snapshot.vector_coordinates, [3.0, 2.0])


def test_translation_is_dimension_independent() -> None:
    snapshot = VectorToOriginTranslation(
        [1.0, -2.0, 3.0],
        [4.0, 2.0, 5.0],
    ).snapshot(1.0)

    assert snapshot.current.dimension == 3
    assert np.allclose(snapshot.current_initial_point, [0.0, 0.0, 0.0])
    assert np.allclose(snapshot.current_terminal_point, [3.0, 4.0, 2.0])


@pytest.mark.parametrize("progress", [-0.1, 1.1, np.inf, np.nan])
def test_invalid_progress_is_rejected(progress: float) -> None:
    path = VectorToOriginTranslation([2.0, 1.0], [5.0, 3.0])

    with pytest.raises(ValueError):
        path.snapshot(progress)


def test_point_dimensions_must_match() -> None:
    with pytest.raises(ValueError):
        VectorToOriginTranslation([2.0, 1.0], [5.0, 3.0, 4.0])


def test_input_arrays_are_copied_and_read_only() -> None:
    initial = np.array([2.0, 1.0])
    terminal = np.array([5.0, 3.0])
    path = VectorToOriginTranslation(initial, terminal)
    initial[:] = 99.0
    terminal[:] = 99.0

    assert np.allclose(path.initial_point, [2.0, 1.0])
    assert np.allclose(path.terminal_point, [5.0, 3.0])
    assert not path.initial_point.flags.writeable
    assert not path.terminal_point.flags.writeable
