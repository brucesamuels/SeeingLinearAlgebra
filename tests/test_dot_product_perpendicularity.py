import numpy as np
import pytest

from engine.dot_product_perpendicularity import (
    DotProductExample,
    DotProductPerpendicularityLesson,
)


def test_examples_have_expected_dot_product_signs() -> None:
    lesson = DotProductPerpendicularityLesson()
    assert lesson.acute_example().dot_product == pytest.approx(4.0)
    assert lesson.right_example().dot_product == pytest.approx(0.0)
    assert lesson.obtuse_example().dot_product == pytest.approx(-1.0)


def test_right_example_is_perpendicular() -> None:
    right = DotProductPerpendicularityLesson().right_example()
    assert right.is_perpendicular
    assert right.angle_degrees == pytest.approx(90.0)
    assert right.sign_label == "zero"


def test_sign_summary_tracks_geometric_cases() -> None:
    assert DotProductPerpendicularityLesson().sign_summary == (
        ("acute angle", r"\mathbf{u}\cdot\mathbf{v}>0"),
        ("right angle", r"\mathbf{u}\cdot\mathbf{v}=0"),
        ("obtuse angle", r"\mathbf{u}\cdot\mathbf{v}<0"),
    )


def test_dot_product_example_rejects_zero_vector() -> None:
    with pytest.raises(ValueError, match="nonzero"):
        DotProductExample((0, 0), (1, 2))


def test_coordinate_and_angle_views_agree_on_cosine() -> None:
    bridge = DotProductPerpendicularityLesson().bridge_example()
    expected = bridge.dot_product / (bridge.norm_first * bridge.norm_second)
    assert bridge.cosine_between == pytest.approx(expected)
    assert 0.0 < bridge.angle_degrees < 90.0


def test_final_statement_matches_lesson_goal() -> None:
    assert (
        DotProductPerpendicularityLesson().FINAL_STATEMENT
        == r"\mathbf{u}\perp\mathbf{v}\iff\mathbf{u}\cdot\mathbf{v}=0"
    )
