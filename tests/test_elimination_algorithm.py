from __future__ import annotations

import numpy as np
import pytest

from engine.elimination_algorithm import EliminationAlgorithm


def test_default_trace_uses_swap_then_two_replacements() -> None:
    snapshot = EliminationAlgorithm().snapshot()
    assert [action.kind for action in snapshot.actions] == ["swap", "replace", "replace"]
    assert [action.label for action in snapshot.actions] == [
        r"R_1\leftrightarrow R_2",
        r"R_3\leftarrow R_3-2R_1",
        r"R_3\leftarrow R_3-R_2",
    ]


def test_default_trace_reaches_expected_echelon_form() -> None:
    snapshot = EliminationAlgorithm().snapshot()
    np.testing.assert_allclose(
        snapshot.echelon_augmented,
        [
            [1.0, 1.0, 1.0, 3.0],
            [0.0, 1.0, 1.0, 2.0],
            [0.0, 0.0, -2.0, -2.0],
        ],
    )
    assert EliminationAlgorithm().is_row_echelon(snapshot.echelon_augmented)


def test_snapshot_records_pivots_and_active_regions() -> None:
    snapshot = EliminationAlgorithm().snapshot()
    assert snapshot.pivot_positions == ((0, 0), (1, 1), (2, 2))
    assert snapshot.active_regions == ((0, 0), (1, 1), (2, 2))


def test_algorithm_skips_a_column_without_a_pivot() -> None:
    matrix = [
        [0.0, 1.0, 2.0],
        [0.0, 2.0, 4.0],
    ]
    snapshot = EliminationAlgorithm(matrix).snapshot()
    assert snapshot.pivot_positions == ((0, 1),)
    assert snapshot.active_regions == ((0, 1),)


def test_row_replacement_and_swap_do_not_mutate_input() -> None:
    matrix = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    original = matrix.copy()
    swapped = EliminationAlgorithm.swap_rows(matrix, 0, 1)
    replaced = EliminationAlgorithm.replace_row(matrix, target=1, source=0, scalar=-4.0)
    np.testing.assert_allclose(matrix, original)
    np.testing.assert_allclose(swapped, [[4.0, 5.0, 6.0], [1.0, 2.0, 3.0]])
    np.testing.assert_allclose(replaced, [[1.0, 2.0, 3.0], [0.0, -3.0, -6.0]])


def test_invalid_inputs_are_rejected() -> None:
    with pytest.raises(ValueError, match="two-dimensional"):
        EliminationAlgorithm([1.0, 2.0, 3.0])
    with pytest.raises(ValueError, match="finite"):
        EliminationAlgorithm([[1.0, np.nan]])
    with pytest.raises(ValueError, match="atol"):
        EliminationAlgorithm([[1.0, 2.0]], atol=-1.0)
    with pytest.raises(ValueError, match="distinct"):
        EliminationAlgorithm.replace_row(
            np.array([[1.0, 2.0], [3.0, 4.0]]),
            target=0,
            source=0,
            scalar=1.0,
        )
