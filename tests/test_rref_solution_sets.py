from __future__ import annotations

import numpy as np
import pytest

from engine.rref_solution_sets import RREFSolutionSets


def test_three_default_cases_have_expected_classifications() -> None:
    model = RREFSolutionSets()
    cases = model.cases()
    assert [case.classification for case in cases] == ["unique", "none", "infinite"]


def test_unique_case_has_all_pivot_columns_and_no_free_columns() -> None:
    case = RREFSolutionSets().cases()[0]
    assert case.pivot_columns == (0, 1, 2)
    assert case.free_columns == ()
    assert case.contradiction_row is None


def test_no_solution_case_detects_contradiction() -> None:
    case = RREFSolutionSets().cases()[1]
    assert case.contradiction_row == 2
    assert case.classification == "none"


def test_infinite_case_detects_free_variable() -> None:
    case = RREFSolutionSets().cases()[2]
    assert case.pivot_columns == (0, 1)
    assert case.free_columns == (2,)
    assert case.interpretation_tex == (r"z=t", r"x=4-2t", r"y=1+t")


def test_classify_handles_general_consistent_and_inconsistent_rref() -> None:
    model = RREFSolutionSets()
    assert model.classify([[1, 0, 5], [0, 1, 2]]) == "unique"
    assert model.classify([[1, 2, 3], [0, 0, 0]]) == "infinite"
    assert model.classify([[1, 2, 3], [0, 0, 1]]) == "none"


@pytest.mark.parametrize(
    ("matrix", "message"),
    [
        ([1, 2, 3], "two-dimensional"),
        ([[1], [2]], "variables and a right-hand side"),
        ([[1, np.inf]], "finite"),
    ],
)
def test_invalid_augmented_matrices_are_rejected(matrix, message) -> None:
    with pytest.raises(ValueError, match=message):
        RREFSolutionSets().classify(matrix)
