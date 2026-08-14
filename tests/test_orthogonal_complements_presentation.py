from pathlib import Path

SCENE_PATH = Path("scenes/orthogonal_complements_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_uses_header_and_three_d_scene() -> None:
    source = scene_source()
    assert 'CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"' in source
    assert 'LESSON_TITLE = "Orthogonal Complements"' in source
    assert 'SCENE_REVISION = "cp156_r22_card4_caption_left_and_raise"' in source
    assert "class OrthogonalComplementsPresentation(ThreeDScene)" in source


def test_scene_has_six_cards() -> None:
    source = scene_source()
    for helper in (
        "_residual_motivation_card",
        "_definition_card",
        "_line_example_card",
        "_plane_example_card",
        "_decomposition_card",
        "_bridge_card",
    ):
        assert f"self.{helper}()" in source
        assert f"def {helper}" in source


def test_scene_preserves_approved_residual_geometry() -> None:
    source = scene_source()
    assert "plane = self._square_plane2d().shift(LEFT * 0.10 + DOWN * 0.05)" in source
    assert "def _right_angle_marker" in source
    assert "Create(right_angle)" in source
    assert "plane.c2p(1.55, 2.45)" in source


def test_card4_preserves_camera_scale_and_equation_placement() -> None:
    source = scene_source()
    assert "self.set_camera_orientation(phi=56 * DEGREES, theta=-10 * DEGREES, zoom=0.66)" in source
    assert "x_length=5.05" in source and "y_length=5.05" in source and "z_length=5.00" in source
    assert "zoom=0.66," in source
    assert "move_to(RIGHT * 3.42 + UP * 0.55)" in source


def test_card4_raises_geometry_for_first_frame_clearance() -> None:
    source = scene_source()
    assert "shift(RIGHT * 4.82 + DOWN * 0.22)" in source


def test_card4_moves_bottom_explainer_to_viewer_left_blank_space() -> None:
    source = scene_source()
    assert '"In R^3, the orthogonal complement\\nof a plane is a line normal\\nto the plane."' in source
    assert "font_size=20" in source
    assert "move_to(LEFT * 4.05 + DOWN * 1.76)" in source
    assert ").to_edge(DOWN, buff=0.32)" not in source


def test_card4_preserves_wp_label_behavior() -> None:
    source = scene_source()
    assert "axes.c2p(-0.92, 0.24, 1.14)" in source
    assert "camera_compensation = RIGHT * 0.44 + UP * 1.33" in source
    assert "wp_label_rotated_position = axes.c2p(-1.05, 0.20, 1.18) + camera_compensation" in source
    assert "add_fixed_orientation_mobjects(w_label, wp_label)" in source
    assert "wp_label.animate.move_to(wp_label_rotated_position)" in source
    assert "remove_fixed_orientation_mobjects(w_label, wp_label)" in source


def test_scene_contains_key_math_and_3d_primitives() -> None:
    source = scene_source()
    for token in (
        r"W=\operatorname{span}(1,1)",
        r"W^\perp=\operatorname{span}(1,-1)",
        "self.lesson.DECOMPOSITION",
        "self.lesson.DIMENSION_FACT",
        "ThreeDAxes(",
        "Arrow3D",
        "move_camera",
    ):
        assert token in source


def test_card4_equation_block_restored_to_r18_position() -> None:
    source = scene_source()
    assert "SCENE_REVISION = \"cp156_r22_card4_caption_left_and_raise\"" in source
    assert "move_to(RIGHT * 3.42 + UP * 0.55)" in source
    assert "move_to(LEFT * 4.05 + DOWN * 1.76)" in source


def test_card4_caption_moves_left_and_graphic_raises() -> None:
    source = scene_source()
    assert "SCENE_REVISION = \"cp156_r22_card4_caption_left_and_raise\"" in source
    assert "shift(RIGHT * 4.82 + DOWN * 0.22)" in source
    assert "move_to(LEFT * 4.05 + DOWN * 1.76)" in source
