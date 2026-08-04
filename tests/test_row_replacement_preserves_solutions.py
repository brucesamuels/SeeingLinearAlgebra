from __future__ import annotations

import numpy as np
import pytest

from engine.row_replacement_preserves_solutions import (
    RowReplacementPreservesSolutions,
)


def test_default_snapshot_contains_expected_systems() -> None:
    model = RowReplacementPreservesSolutions()
    snapshot = model.snapshot()

    np.testing.assert_allclose(
        snapshot.original_augmented,
        np.array([[1.0, 1.0, 2.0], [2.0, -1.0, 1.0]]),
    )
    np.testing.assert_allclose(
        snapshot.transformed_augmented,
        np.array([[1.0, 1.0, 2.0], [0.0, -3.0, -3.0]]),
    )
    np.testing.assert_allclose(snapshot.recovered_augmented, snapshot.original_augmented)


def test_default_solution_satisfies_both_systems() -> None:
    model = RowReplacementPreservesSolutions()
    snapshot = model.snapshot()

    np.testing.assert_allclose(snapshot.solution, np.array([1.0, 1.0]))
    assert model.satisfies(snapshot.original_augmented, snapshot.solution)
    assert model.satisfies(snapshot.transformed_augmented, snapshot.solution)


def test_snapshot_records_matching_left_and_right_values() -> None:
    snapshot = RowReplacementPreservesSolutions().snapshot()

    np.testing.assert_allclose(snapshot.original_left_values, snapshot.original_right_values)
    np.testing.assert_allclose(
        snapshot.transformed_left_values,
        snapshot.transformed_right_values,
    )


def test_replace_row_returns_a_fresh_array() -> None:
    original = np.array([[1.0, 1.0, 2.0], [2.0, -1.0, 1.0]])
    transformed = RowReplacementPreservesSolutions.replace_row(
        original,
        target=1,
        source=0,
        scalar=-2.0,
    )

    np.testing.assert_allclose(original, np.array([[1.0, 1.0, 2.0], [2.0, -1.0, 1.0]]))
    np.testing.assert_allclose(transformed[1], np.array([0.0, -3.0, -3.0]))
    assert transformed is not original


def test_inverse_replacement_recovers_original() -> None:
    model = RowReplacementPreservesSolutions()
    transformed = model.transformed_augmented()
    recovered = model.replace_row(transformed, target=1, source=0, scalar=2.0)
    np.testing.assert_allclose(recovered, model.augmented_matrix)


def test_invalid_row_replacement_is_rejected() -> None:
    model = RowReplacementPreservesSolutions()
    with pytest.raises(ValueError, match="distinct"):
        model.replace_row(model.augmented_matrix, target=0, source=0, scalar=2.0)
    with pytest.raises(IndexError):
        model.replace_row(model.augmented_matrix, target=5, source=0, scalar=2.0)
    with pytest.raises(ValueError, match="finite"):
        model.replace_row(model.augmented_matrix, target=1, source=0, scalar=np.inf)


def test_candidate_shape_is_validated() -> None:
    model = RowReplacementPreservesSolutions()
    with pytest.raises(ValueError, match="candidate length"):
        model.evaluate(model.augmented_matrix, [1.0, 1.0, 1.0])
