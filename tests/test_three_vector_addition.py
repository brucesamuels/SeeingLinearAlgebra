from __future__ import annotations

import numpy as np
import pytest

from engine.three_vector_addition import ThreeVectorAddition


def test_three_vector_addition_specializes_linear_combination_to_all_ones() -> None:
    snapshot = ThreeVectorAddition(
        (2.0, 0.0, 1.0),
        (0.0, 2.0, 1.0),
        (1.0, 1.0, 2.0),
    ).snapshot()

    assert snapshot.coefficients == (1.0, 1.0, 1.0)
    np.testing.assert_allclose(
        snapshot.linear_combination_snapshot.coefficients,
        [1.0, 1.0, 1.0],
    )


def test_three_vector_addition_computes_successive_segments_and_result() -> None:
    snapshot = ThreeVectorAddition(
        (2.0, 0.0, 1.0),
        (0.0, 2.0, 1.0),
        (1.0, 1.0, 2.0),
    ).snapshot()

    assert snapshot.first_segment == ((0.0, 0.0, 0.0), (2.0, 0.0, 1.0))
    assert snapshot.second_segment == ((2.0, 0.0, 1.0), (2.0, 2.0, 2.0))
    assert snapshot.third_segment == ((2.0, 2.0, 2.0), (3.0, 3.0, 4.0))
    assert snapshot.resultant_segment == ((0.0, 0.0, 0.0), (3.0, 3.0, 4.0))
    assert snapshot.result == (3.0, 3.0, 4.0)
    assert snapshot.is_successive_path


def test_three_vector_addition_exposes_parallelepiped_vertices_and_edges() -> None:
    snapshot = ThreeVectorAddition(
        (2.0, 0.0, 1.0),
        (0.0, 2.0, 1.0),
        (1.0, 1.0, 2.0),
    ).snapshot()

    assert len(snapshot.parallelepiped_vertices) == 8
    assert len(snapshot.parallelepiped_edges) == 12
    assert (3.0, 3.0, 4.0) in snapshot.parallelepiped_vertices
    assert (
        ((2.0, 2.0, 2.0), (3.0, 3.0, 4.0))
        in snapshot.parallelepiped_edges
    )


@pytest.mark.parametrize(
    ('first', 'second', 'third', 'error_type'),
    (
        ((1.0, 2.0), (0.0, 1.0), (1.0, 1.0), ValueError),
        ((1.0, 2.0, 3.0), (1.0, 2.0), (0.0, 1.0, 2.0), ValueError),
        ((1.0, float('nan'), 3.0), (0.0, 1.0, 2.0), (1.0, 1.0, 1.0), ValueError),
        (((1.0, 2.0, 3.0),), ((0.0, 1.0, 2.0),), ((1.0, 1.0, 1.0),), ValueError),
    ),
)
def test_three_vector_addition_validates_vectors(
    first,
    second,
    third,
    error_type,
) -> None:
    with pytest.raises(error_type):
        ThreeVectorAddition(first, second, third)
