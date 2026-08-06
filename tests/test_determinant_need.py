from __future__ import annotations

import numpy as np
import pytest

from engine.determinant_need import (
    AreaBehavior,
    UNIT_SQUARE,
    build_examples,
    central_question,
    classify_scale,
    determinant_motivation,
    region_snapshot,
    signed_polygon_area,
    transform_vertices,
)


def test_unit_square_has_positive_unit_area() -> None:
    assert signed_polygon_area(UNIT_SQUARE) == pytest.approx(1.0)


def test_transform_vertices_uses_column_action() -> None:
    matrix = np.array([[2.0, 1.0], [0.0, 1.0]])
    transformed = transform_vertices(matrix)
    np.testing.assert_allclose(
        transformed,
        np.array([[0.0, 0.0], [2.0, 0.0], [3.0, 1.0], [1.0, 1.0]]),
    )


def test_region_snapshot_measures_signed_area_scale() -> None:
    snapshot = region_snapshot([[2.0, 1.0], [0.0, 1.0]])
    assert snapshot.original_area == pytest.approx(1.0)
    assert snapshot.transformed_area == pytest.approx(2.0)
    assert snapshot.signed_scale == pytest.approx(2.0)


def test_orientation_reversal_has_negative_signed_scale() -> None:
    snapshot = region_snapshot([[-1.0, 0.0], [0.0, 1.0]])
    assert snapshot.signed_scale == pytest.approx(-1.0)


def test_rank_loss_collapses_area() -> None:
    snapshot = region_snapshot([[1.0, 2.0], [0.0, 0.0]])
    assert snapshot.transformed_area == pytest.approx(0.0)
    assert snapshot.signed_scale == pytest.approx(0.0)


@pytest.mark.parametrize(
    ("scale", "expected"),
    [
        (2.0, AreaBehavior.EXPANDS),
        (0.5, AreaBehavior.CONTRACTS),
        (1.0, AreaBehavior.PRESERVES),
        (-1.0, AreaBehavior.REVERSES),
        (0.0, AreaBehavior.COLLAPSES),
    ],
)
def test_scale_classification(scale: float, expected: AreaBehavior) -> None:
    assert classify_scale(scale) is expected


def test_examples_follow_the_intended_narrative() -> None:
    examples = build_examples()
    assert [example.key for example in examples] == [
        "expand",
        "contract",
        "reverse",
        "collapse",
    ]
    assert [example.signed_scale for example in examples] == pytest.approx([2.0, 0.5, -1.0, 0.0])


def test_lesson_language_states_the_central_question_without_formula() -> None:
    assert central_question() == "How does a linear transformation change area or volume?"
    motivation = determinant_motivation()
    assert "signed number" in motivation
    assert "orientation" in motivation
    assert "ad - bc" not in motivation


def test_invalid_shapes_are_rejected() -> None:
    with pytest.raises(ValueError):
        transform_vertices([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    with pytest.raises(ValueError):
        signed_polygon_area([[0.0, 0.0], [1.0, 0.0]])
