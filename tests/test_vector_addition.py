from __future__ import annotations

import numpy as np
import pytest

from engine.vector_addition import VectorAddition


def test_vector_addition_specializes_linear_combination_to_coefficients_one() -> None:
    snapshot = VectorAddition((3.0, 1.0), (1.0, 2.0)).snapshot()

    assert snapshot.coefficients == (1.0, 1.0)
    np.testing.assert_allclose(
        snapshot.linear_combination_snapshot.coefficients,
        [1.0, 1.0],
    )


def test_vector_addition_computes_the_requested_sum() -> None:
    snapshot = VectorAddition((3.0, 1.0), (1.0, 2.0)).snapshot()

    assert snapshot.first_vector == (3.0, 1.0)
    assert snapshot.second_vector == (1.0, 2.0)
    assert snapshot.result == (4.0, 3.0)


def test_vector_addition_exposes_tip_to_tail_geometry() -> None:
    snapshot = VectorAddition((3.0, 1.0), (1.0, 2.0)).snapshot()

    assert snapshot.first_segment == ((0.0, 0.0), (3.0, 1.0))
    assert snapshot.second_segment == ((3.0, 1.0), (4.0, 3.0))
    assert snapshot.resultant_segment == ((0.0, 0.0), (4.0, 3.0))
    assert snapshot.is_tip_to_tail


def test_vector_addition_remains_dimension_independent() -> None:
    snapshot = VectorAddition(
        (1.0, -2.0, 3.0),
        (4.0, 1.0, -1.0),
    ).snapshot()

    assert snapshot.dimension == 3
    assert snapshot.result == (5.0, -1.0, 2.0)
    assert snapshot.second_segment == (
        (1.0, -2.0, 3.0),
        (5.0, -1.0, 2.0),
    )


@pytest.mark.parametrize(
    ("first", "second", "error_type"),
    (
        ((), (), ValueError),
        ((1.0, 2.0), (1.0,), ValueError),
        ((1.0, float("nan")), (1.0, 2.0), ValueError),
        (((1.0, 2.0),), ((3.0, 4.0),), ValueError),
    ),
)
def test_vector_addition_validates_vectors(
    first,
    second,
    error_type,
) -> None:
    with pytest.raises(error_type):
        VectorAddition(first, second)
