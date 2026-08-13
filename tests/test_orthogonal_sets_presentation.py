from pathlib import Path

SCENE_PATH = Path("scenes/orthogonal_sets_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_uses_chapter_header_and_3d_scene() -> None:
    source = scene_source()
    assert 'CHAPTER_BANNER = "ORTHOGONALITY AND PROJECTION"' in source
    assert 'LESSON_TITLE = "Orthogonal Sets"' in source
    assert "class OrthogonalSetsPresentation(ThreeDScene)" in source
    assert 'SCENE_REVISION = "cp151_r14_expanded_3d_rotation"' in source


def test_scene_has_six_cards() -> None:
    source = scene_source()
    for helper in (
        "_transition_to_collections",
        "_definition_card",
        "_orthogonal_example_card",
        "_nonexample_card",
        "_independence_card",
        "_bridge_card",
    ):
        assert f"self.{helper}()" in source
        assert f"def {helper}" in source


def test_scene_uses_fixed_in_frame_header_and_3d_primitives() -> None:
    source = scene_source()
    assert "add_fixed_in_frame_mobjects" in source
    assert "ThreeDAxes(" in source
    assert "Arrow3D" in source
    assert "set_camera_orientation" in source
    assert "move_camera" in source


def test_scene_contains_definition_example_nonexample_and_theorem() -> None:
    source = scene_source()
    assert "self.lesson.DEFINITION" in source
    assert "An orthogonal set in R^3" in source
    assert "One good pair is not enough" in source
    assert "self.lesson.THEOREM" in source


def test_scene_nonexample_is_explicitly_pairwise() -> None:
    source = scene_source()
    assert r"\mathbf{w}_1\cdot\mathbf{w}_3\neq 0" in source
    assert "every distinct pair" in source


def test_scene_bridges_to_orthonormal_sets() -> None:
    source = scene_source()
    assert "What if the vectors are also unit length?" in source
    assert "self.lesson.bridge_to_orthonormal" in source


def test_scene_does_not_reference_checkpoint_numbers_to_students() -> None:
    source = scene_source()
    assert "CP150" not in source
    assert "cp150" not in source.lower()


def test_3d_cards_are_larger_lower_and_shifted_screen_right() -> None:
    source = scene_source()
    assert source.count("x_length=3.9") == 2
    assert source.count("y_length=3.9") == 2
    assert source.count("z_length=3.9") == 2
    assert source.count("shift(RIGHT * 2.60 + DOWN * 2.45)") == 2


def test_final_yellow_question_is_raised_for_balance() -> None:
    source = scene_source()
    assert '"What if the vectors are also unit length?"' in source
    assert ").move_to(UP * 0.88)" in source




def test_camera_starts_at_minus_15_and_rotates_farther_for_depth() -> None:
    source = scene_source()
    assert "theta=-15 * DEGREES" in source
    assert "zoom=0.90" in source
    assert source.count("shift(RIGHT * 2.60 + DOWN * 2.45)") == 2
    assert "theta=28 * DEGREES" in source
    assert "theta=25 * DEGREES" in source
    assert source.count("run_time=2.6") == 2
