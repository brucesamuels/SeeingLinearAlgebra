import numpy as np
import pytest

from engine.rank_pivots_consistency import RankPivotsConsistency


def test_unique_case_has_full_coefficient_rank() -> None:
    case = RankPivotsConsistency().case("unique")
    assert case.coefficient_rank == 3
    assert case.augmented_rank == 3
    assert case.pivot_columns == (0, 1, 2)
    assert case.free_columns == ()
    assert case.is_consistent
    assert case.solution_type == "unique"


def test_infinite_case_has_equal_ranks_and_one_free_column() -> None:
    case = RankPivotsConsistency().case("infinite")
    assert case.coefficient_rank == 2
    assert case.augmented_rank == 2
    assert case.pivot_columns == (0, 1)
    assert case.free_columns == (2,)
    assert case.is_consistent
    assert case.solution_type == "infinite"


def test_inconsistent_case_gains_augmented_rank() -> None:
    case = RankPivotsConsistency().case("inconsistent")
    assert case.coefficient_rank == 2
    assert case.augmented_rank == 3
    assert not case.is_consistent
    assert case.solution_type == "none"
    assert "additional pivot" in case.reason


def test_default_examples_are_returned_as_copies() -> None:
    model = RankPivotsConsistency()
    first = model.case("unique")
    first.rref_augmented[0, 0] = 99
    second = model.case("unique")
    assert second.rref_augmented[0, 0] == 1


def test_unknown_case_is_rejected() -> None:
    with pytest.raises(KeyError):
        RankPivotsConsistency().case("missing")


def test_case_dictionary_must_have_all_three_names() -> None:
    with pytest.raises(ValueError, match="unique, infinite, and inconsistent"):
        RankPivotsConsistency(cases={"unique": np.zeros((3, 4))})


def test_each_augmented_matrix_must_have_shape_three_by_four() -> None:
    bad = {
        "unique": np.zeros((2, 4)),
        "infinite": np.zeros((3, 4)),
        "inconsistent": np.zeros((3, 4)),
    }
    with pytest.raises(ValueError, match="shape"):
        RankPivotsConsistency(cases=bad)


def test_nonfinite_entries_are_rejected() -> None:
    bad = {name: matrix.copy() for name, matrix in RankPivotsConsistency.DEFAULT_CASES.items()}
    bad["unique"][0, 0] = np.nan
    with pytest.raises(ValueError, match="finite"):
        RankPivotsConsistency(cases=bad)


def test_tolerance_must_be_positive_and_finite() -> None:
    for value in (0, -1, np.inf, np.nan):
        with pytest.raises(ValueError, match="positive finite"):
            RankPivotsConsistency(atol=value)


def test_snapshot_contains_rank_theorem_and_all_cases() -> None:
    snapshot = RankPivotsConsistency().snapshot()
    assert snapshot.unique.solution_type == "unique"
    assert snapshot.infinite.solution_type == "infinite"
    assert snapshot.inconsistent.solution_type == "none"
    assert r"\operatorname{rank}(A)=\operatorname{rank}([A\mid\mathbf{b}])" in snapshot.consistency_theorem_tex
    assert r"\operatorname{rank}(A)=n\ \Longrightarrow\ \text{unique solution}" in snapshot.classification_tex
