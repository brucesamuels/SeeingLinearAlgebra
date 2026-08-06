from __future__ import annotations

import pytest

from engine.rectangular_matrices import RectangularMatrices


def test_snapshot_states_dimension_and_column_space_formulas() -> None:
    snapshot = RectangularMatrices().snapshot()
    assert snapshot.dimension_equation_tex == r"A_{m\times n}\mathbf{x}_{n\times 1}=\mathbf{b}_{m\times 1}"
    assert snapshot.map_tex == r"A:\mathbb{R}^n\longrightarrow\mathbb{R}^m"
    assert r"m\ \text{rows}=m\ \text{equations}" in snapshot.equation_count_tex
    assert snapshot.column_combination_tex == r"A\mathbf{x}=x_1\mathbf{a}_1+\cdots+x_n\mathbf{a}_n=\mathbf{b}"
    assert r"\mathbf{b}\in\operatorname{Col}(A)" in snapshot.consistency_tex


def test_rank_and_nullity_formulas_are_exposed() -> None:
    snapshot = RectangularMatrices().snapshot()
    assert snapshot.rank_bound_tex == r"r=\operatorname{rank}(A)\le \min(m,n)"
    assert snapshot.nullity_tex == r"\dim N(A)=n-r"
    assert snapshot.augmented_rank_tex == r"\operatorname{rank}(A)=\operatorname{rank}([A\mid\mathbf{b}])"


def test_cases_cover_square_tall_and_wide_shapes() -> None:
    cases = RectangularMatrices().cases
    assert tuple(case.name for case in cases) == ("Square", "Tall", "Wide")
    assert [(case.rows, case.columns) for case in cases] == [(2, 2), (3, 2), (2, 3)]
    assert [case.relation_tex for case in cases] == [r"m=n", r"m>n", r"m<n"]


def test_full_rank_square_case_can_be_onto_and_one_to_one() -> None:
    square = RectangularMatrices().cases[0]
    assert square.can_be_onto
    assert square.can_be_one_to_one
    assert square.full_rank_nullity == 0
    assert square.full_rank_tex == r"r=2"


def test_full_rank_tall_case_is_one_to_one_but_not_onto() -> None:
    tall = RectangularMatrices().cases[1]
    assert not tall.can_be_onto
    assert tall.can_be_one_to_one
    assert tall.full_rank_nullity == 0
    assert tall.full_rank_tex == r"r=n=2"
    assert "plane" in tall.full_rank_reachability
    assert "at most one" in tall.full_rank_uniqueness


def test_full_rank_wide_case_is_onto_but_not_one_to_one() -> None:
    wide = RectangularMatrices().cases[2]
    assert wide.can_be_onto
    assert not wide.can_be_one_to_one
    assert wide.full_rank_nullity == 1
    assert wide.full_rank_tex == r"r=m=2"
    assert "Every output" in wide.full_rank_reachability
    assert "infinitely many" in wide.full_rank_uniqueness


def test_dimension_helpers_match_rank_nullity_reasoning() -> None:
    assert RectangularMatrices.maximum_rank(5, 3) == 3
    assert RectangularMatrices.maximum_rank(2, 6) == 2
    assert RectangularMatrices.full_rank_nullity(5, 3) == 0
    assert RectangularMatrices.full_rank_nullity(2, 6) == 4
    assert RectangularMatrices.can_be_one_to_one(5, 3)
    assert not RectangularMatrices.can_be_one_to_one(2, 6)
    assert not RectangularMatrices.can_be_onto(5, 3)
    assert RectangularMatrices.can_be_onto(2, 6)


@pytest.mark.parametrize(
    ("rows", "columns"),
    [(0, 2), (2, 0), (-1, 2), (2, -1), (True, 2), (2, False), (2.5, 3)],
)
def test_invalid_dimensions_are_rejected(rows, columns) -> None:
    with pytest.raises(ValueError):
        RectangularMatrices(rows=rows, columns=columns)
