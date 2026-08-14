from pathlib import Path

SCENE_PATH = Path("scenes/orthonormalization_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_header_and_revision() -> None:
    source = scene_source()
    assert 'CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"' in source
    assert 'LESSON_TITLE = "From Orthogonal to Orthonormal"' in source
    assert 'SCENE_REVISION = "cp158_r3_grid_on_all_graphic_cards"' in source
    assert "class OrthonormalizationPresentation(Scene)" in source


def test_scene_has_six_cards() -> None:
    source = scene_source()
    for helper in (
        "_recall_orthogonal_pair_card",
        "_normalize_first_card",
        "_normalize_second_card",
        "_unit_circle_card",
        "_orthonormal_summary_card",
        "_bridge_to_qr_card",
    ):
        assert f"self.{helper}()" in source
        assert f"def {helper}" in source


def test_scene_reuses_cp157_pair_and_animates_normalization() -> None:
    source = scene_source()
    for token in (
        r"\mathbf u_1=(1,2)",
        r"\mathbf u_2=(2,-1)",
        "ReplacementTransform(u1_arrow, e1_arrow)",
        "ReplacementTransform(u2_arrow, e2_arrow)",
    ):
        assert token in source


def test_scene_uses_unit_circle_and_right_angle_marker() -> None:
    source = scene_source()
    assert "Circle(radius=radius" in source
    assert "def _right_angle_marker" in source
    assert "Create(right_angle)" in source


def test_scene_states_orthonormal_properties_and_qr_bridge() -> None:
    source = scene_source()
    for token in (
        "self.lesson.UNIT_FACTS",
        "self.lesson.ORTHOGONALITY",
        "self.lesson.SPAN_FACT",
        r"Q^TQ=I",
        r"A=QR",
    ):
        assert token in source


def test_all_graphic_cards_use_emphasized_grid() -> None:
    source = scene_source()
    assert "def _plane(*, wide: bool = True, emphasized_grid: bool = False)" in source
    assert "background_line_style = {\"stroke_opacity\": 0.34, \"stroke_width\": 1.6}" in source
    assert source.count("plane = self._plane(emphasized_grid=True)") >= 3
    assert "plane = self._plane(wide=False, emphasized_grid=True)" in source
