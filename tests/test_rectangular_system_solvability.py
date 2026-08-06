from __future__ import annotations

import pytest

from engine.rectangular_system_solvability import RectangularSystemSolvability


def test_snapshot_uses_canonical_overdetermined_example() -> None:
    snapshot = RectangularSystemSolvability.snapshot()
    over = snapshot.overdetermined
    assert over.matrix == ((1, 0), (0, 1), (1, 1))
    assert over.compatible_rhs == (2, -1, 1)
    assert over.incompatible_rhs == (2, -1, 0)
    assert over.compatible_solution == (2, -1)


def test_compatible_overdetermined_solution_is_verified() -> None:
    model = RectangularSystemSolvability
    assert model.matvec(model.OVER_MATRIX, model.OVER_SOLUTION) == model.OVER_COMPATIBLE_RHS


def test_incompatible_overdetermined_rhs_is_not_reached_by_the_candidate() -> None:
    model = RectangularSystemSolvability
    assert model.matvec(model.OVER_MATRIX, model.OVER_SOLUTION) != model.OVER_INCOMPATIBLE_RHS


def test_overdetermined_column_space_condition_matches_both_rhs_vectors() -> None:
    good = RectangularSystemSolvability.OVER_COMPATIBLE_RHS
    bad = RectangularSystemSolvability.OVER_INCOMPATIBLE_RHS
    assert good[2] == good[0] + good[1]
    assert bad[2] != bad[0] + bad[1]


def test_full_column_rank_tall_system_is_unique_when_consistent_but_not_onto() -> None:
    model = RectangularSystemSolvability
    assert model.unique_when_consistent(columns=2, rank=2)
    assert not model.solvable_for_every_rhs(rows=3, rank=2)
    assert model.solution_class(columns=2, rank=2, consistent=True) == "unique"
    assert model.solution_class(columns=2, rank=2, consistent=False) == "none"


def test_snapshot_uses_canonical_underdetermined_example() -> None:
    snapshot = RectangularSystemSolvability.snapshot()
    under = snapshot.underdetermined
    assert under.matrix == ((1, 0, 1), (0, 1, 1))
    assert under.rhs == (2, -1)
    assert under.particular_solution == (2, -1, 0)
    assert under.null_vector == (-1, -1, 1)


def test_underdetermined_particular_solution_and_null_vector_are_verified() -> None:
    model = RectangularSystemSolvability
    assert model.matvec(model.UNDER_MATRIX, model.UNDER_PARTICULAR) == model.UNDER_RHS
    assert model.matvec(model.UNDER_MATRIX, model.UNDER_NULL_VECTOR) == (0, 0)


@pytest.mark.parametrize("parameter", [-3, -1, 0, 2, 5])
def test_entire_affine_solution_family_maps_to_the_same_rhs(parameter: int) -> None:
    model = RectangularSystemSolvability
    vector = tuple(
        particular + parameter * direction
        for particular, direction in zip(model.UNDER_PARTICULAR, model.UNDER_NULL_VECTOR)
    )
    assert model.matvec(model.UNDER_MATRIX, vector) == model.UNDER_RHS


def test_full_row_rank_wide_system_is_onto_but_never_unique() -> None:
    model = RectangularSystemSolvability
    assert model.solvable_for_every_rhs(rows=2, rank=2)
    assert not model.unique_when_consistent(columns=3, rank=2)
    assert model.nullity(columns=3, rank=2) == 1
    assert model.solution_class(columns=3, rank=2, consistent=True) == "infinitely many"


def test_rank_deficient_wide_counterexample_is_inconsistent() -> None:
    model = RectangularSystemSolvability
    assert model.DEFICIENT_WIDE_MATRIX[1] == tuple(2 * value for value in model.DEFICIENT_WIDE_MATRIX[0])
    assert model.DEFICIENT_WIDE_RHS[1] != 2 * model.DEFICIENT_WIDE_RHS[0]


def test_tex_strings_state_column_space_rank_and_complete_solution() -> None:
    snapshot = RectangularSystemSolvability.snapshot()
    assert r"\mathbf{b}\in\operatorname{Col}(A)" in snapshot.common_consistency_tex
    assert r"\operatorname{rank}(A)=\operatorname{rank}([A\mid\mathbf{b}])" == snapshot.augmented_rank_tex
    assert r"\mathbf{x}_p+t\mathbf{v}" in snapshot.underdetermined.complete_solution_tex
    assert r"0&0&-1" in snapshot.overdetermined.incompatible_reduced_tex
    assert r"0&0&0&-2" in snapshot.underdetermined.deficient_reduced_tex


def test_invalid_dimensions_and_ranks_are_rejected() -> None:
    model = RectangularSystemSolvability
    with pytest.raises(ValueError):
        model.nullity(columns=0, rank=0)
    with pytest.raises(ValueError):
        model.nullity(columns=2, rank=3)
    with pytest.raises(ValueError):
        model.unique_when_consistent(columns=3, rank=-1)
    with pytest.raises(ValueError):
        model.solvable_for_every_rhs(rows=True, rank=1)


def test_matvec_validates_shapes() -> None:
    model = RectangularSystemSolvability
    with pytest.raises(ValueError):
        model.matvec((), ())
    with pytest.raises(ValueError):
        model.matvec(((1, 2), (3,)), (1, 2))
    with pytest.raises(ValueError):
        model.matvec(((1, 2),), (1,))
