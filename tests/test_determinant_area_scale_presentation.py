from __future__ import annotations

import ast
from pathlib import Path

SCENE_PATH = Path("scenes/determinant_area_scale_presentation.py")


def source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_source_is_valid_python() -> None:
    ast.parse(source())


def test_scene_has_expected_class_and_one_stable_axes_object() -> None:
    text = source()
    assert "class DeterminantAreaScalePresentation(Scene):" in text
    assert text.count("axes = Axes(") == 1
    assert "UNIT_SQUARE" in text


def test_scene_maps_basis_vectors_to_matrix_columns() -> None:
    text = source()
    assert "example.columns" in text
    assert r"\mathbf e_1" in text
    assert r"\mathbf e_2" in text
    assert r"\mathbf a_1" in text
    assert r"\mathbf a_2" in text
    assert "ReplacementTransform(e1, a1)" in text
    assert "ReplacementTransform(e2, a2)" in text


def test_scene_transforms_square_in_place_without_persistent_copy() -> None:
    text = source()
    assert "Transform(square, parallelogram)" in text
    assert "square.copy()" not in text


def test_scene_builds_area_from_base_and_height() -> None:
    text = source()
    assert "BraceBetweenPoints" in text
    assert "base_guide" in text
    assert "height_guide" in text
    assert r"=2\cdot2=4" in text


def test_scene_states_absolute_determinant_area_rule() -> None:
    text = source()
    assert r"|\det(A)|=\text{area scale factor}" in text
    assert "The sign comes next" in text


def test_scene_defers_signed_orientation_treatment() -> None:
    text = source()
    assert "negative determinant" not in text.lower()
    assert "clockwise" not in text.lower()
    assert "counterclockwise" not in text.lower()


def test_scene_uses_mathtex_and_standard_manim_arrows() -> None:
    text = source()
    assert "MathTex(" in text
    assert "Arrow(" in text
    assert "Polygon(" in text

def test_scene_fades_heterogeneous_mobjects_individually() -> None:
    text = source()
    assert "*[FadeOut(mob) for mob in list(self.mobjects)]" in text
    assert "VGroup(*self.mobjects)" not in text

