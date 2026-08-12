from pathlib import Path

SCENE_PATH = Path("scenes/why_orthogonality_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_uses_established_header_hierarchy_and_2d_geometry() -> None:
    source = scene_source()
    assert 'CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"' in source
    assert 'LESSON_TITLE = "Why Orthogonality?"' in source
    assert "NumberPlane(" in source
    assert "RightAngle(" in source
    assert "ThreeDScene" not in source
    assert "ambient_camera" not in source


def test_scene_has_five_distinct_pedagogical_cards() -> None:
    source = scene_source()
    for helper in (
        "_determinant_bridge",
        "_compare_bases",
        "_skew_coordinates",
        "_orthogonal_coordinates",
        "_chapter_question",
    ):
        assert f"self.{helper}()" in source
        assert f"def {helper}" in source


def test_scene_asks_the_opening_questions_and_previews_projection_spine() -> None:
    source = scene_source()
    assert "Are some bases better than others?" in source
    assert "What becomes possible" in source
    assert "when our directions are orthogonal?" in source
    assert "self.lesson.preview_topics" in source


def test_scene_does_not_preempt_cp150_or_projection_formula() -> None:
    source = scene_source()
    forbidden = (
        r"\mathbf{u}\cdot\mathbf{v}=0",
        r"\operatorname{proj}",
        "u dot v = 0",
        "projection formula",
    )
    for item in forbidden:
        assert item not in source


def test_scene_keeps_math_and_explanatory_prose_in_separate_zones() -> None:
    source = scene_source()
    assert ".next_to(self.lesson_title_mobject, DOWN" in source
    assert ".to_edge(DOWN, buff=0.38)" in source
    assert "scale_to_fit_width(12.4)" in source


def test_scene_uses_standard_manim_arrows_and_mathtex() -> None:
    source = scene_source()
    assert "Arrow(" in source
    assert "MathTex(" in source
    assert "Polygon(" in source
    assert "homemade" not in source.lower()
