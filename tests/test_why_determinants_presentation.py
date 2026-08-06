from __future__ import annotations

import ast
from pathlib import Path


SCENE_PATH = Path("scenes/why_determinants_presentation.py")


def source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_source_is_valid_python() -> None:
    ast.parse(source())


def test_scene_has_expected_class_and_stable_axes() -> None:
    text = source()
    assert "class WhyDeterminantsPresentation(Scene):" in text
    assert text.count("axes = Axes(") == 1
    assert "UNIT_SQUARE" in text


def test_scene_includes_four_geometric_behaviors() -> None:
    text = source()
    for key in ("expand", "contract", "reverse", "collapse"):
        assert f'"{key}"' in text
    assert "Area expands" in text or "example.caption" in text
    assert "signed scale" in text


def test_scene_ends_with_the_chapter_question() -> None:
    text = source()
    assert "central_question()" in text
    assert "Chapter 5: Determinants" in text


def test_scene_does_not_reveal_the_two_by_two_formula() -> None:
    text = source()
    forbidden = ("ad-bc", "ad - bc", "a d - b c", r"ad\,-\,bc")
    assert not any(item in text for item in forbidden)


def test_independent_highlights_are_explicitly_removed() -> None:
    text = source()
    assert "FadeOut(current_caption)" in text
    assert "FadeOut(current_scale)" in text


def test_math_uses_mathtex_and_standard_arrow() -> None:
    text = source()
    assert "MathTex(" in text
    assert "Arrow(" in text
    assert "Polygon(" in text

def test_reference_square_is_transformed_in_place() -> None:
    text = source()
    assert "current_polygon = original" in text
    assert "current_polygon = original.copy()" not in text

