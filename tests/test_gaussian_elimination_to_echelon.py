from __future__ import annotations

import numpy as np
import pytest

from engine.gaussian_elimination_to_echelon import GaussianEliminationToEchelon


def test_default_system_and_solution() -> None:
    model = GaussianEliminationToEchelon()
    np.testing.assert_allclose(
        model.augmented_matrix,
        np.array(
            [
                [1.0, 1.0, 1.0, 3.0],
                [2.0, -1.0, 1.0, 2.0],
                [1.0, 2.0, -1.0, 2.0],
            ]
        ),
    )
    np.testing.assert_allclose(model.solution(), np.array([1.0, 1.0, 1.0]))


def test_elimination_has_four_operations_and_five_stages() -> None:
    snapshot = GaussianEliminationToEchelon().snapshot()
    assert len(snapshot.operations) == 4
    assert len(snapshot.stages) == 5


def test_first_replacement_clears_row_two_column_one() -> None:
    stages = GaussianEliminationToEchelon().stages()
    np.testing.assert_allclose(stages[1][1], np.array([0.0, -3.0, -1.0, -4.0]))


def test_second_replacement_clears_row_three_column_one() -> None:
    stages = GaussianEliminationToEchelon().stages()
    np.testing.assert_allclose(stages[2][2], np.array([0.0, 1.0, -2.0, -1.0]))


def test_row_swap_places_unit_second_pivot() -> None:
    stages = GaussianEliminationToEchelon().stages()
    np.testing.assert_allclose(stages[3][1], np.array([0.0, 1.0, -2.0, -1.0]))
    np.testing.assert_allclose(stages[3][2], np.array([0.0, -3.0, -1.0, -4.0]))


def test_final_replacement_reaches_expected_echelon_form() -> None:
    model = GaussianEliminationToEchelon()
    expected = np.array(
        [
            [1.0, 1.0, 1.0, 3.0],
            [0.0, 1.0, -2.0, -1.0],
            [0.0, 0.0, -7.0, -7.0],
        ]
    )
    np.testing.assert_allclose(model.echelon_augmented(), expected)
    assert model.is_row_echelon(expected)


def test_pivots_form_a_staircase() -> None:
    snapshot = GaussianEliminationToEchelon().snapshot()
    assert snapshot.pivot_positions == ((0, 0), (1, 1), (2, 2))


def test_every_stage_has_the_same_unique_solution() -> None:
    snapshot = GaussianEliminationToEchelon().snapshot()
    for stage in snapshot.stages:
        solution = np.linalg.solve(stage[:, :-1], stage[:, -1])
        np.testing.assert_allclose(solution, snapshot.solution)


def test_replace_row_and_swap_rows_do_not_mutate_input() -> None:
    original = GaussianEliminationToEchelon.DEFAULT_AUGMENTED.copy()
    replaced = GaussianEliminationToEchelon.replace_row(
        original,
        target=1,
        source=0,
        scalar=-2,
    )
    swapped = GaussianEliminationToEchelon.swap_rows(original, first=1, second=2)
    np.testing.assert_allclose(original, GaussianEliminationToEchelon.DEFAULT_AUGMENTED)
    assert replaced is not original
    assert swapped is not original


def test_invalid_operations_are_rejected() -> None:
    original = GaussianEliminationToEchelon.DEFAULT_AUGMENTED
    with pytest.raises(ValueError, match="distinct"):
        GaussianEliminationToEchelon.replace_row(
            original,
            target=0,
            source=0,
            scalar=1,
        )
    with pytest.raises(ValueError, match="distinct"):
        GaussianEliminationToEchelon.swap_rows(original, first=1, second=1)
    with pytest.raises(IndexError):
        GaussianEliminationToEchelon.swap_rows(original, first=0, second=8)


def test_constructor_requires_full_rank_three_by_three_system() -> None:
    with pytest.raises(ValueError, match="3 by 4"):
        GaussianEliminationToEchelon([[1, 2, 3], [4, 5, 6]])
    with pytest.raises(ValueError, match="full-rank"):
        GaussianEliminationToEchelon(
            [[1, 1, 1, 3], [2, 2, 2, 6], [3, 3, 3, 9]]
        )
