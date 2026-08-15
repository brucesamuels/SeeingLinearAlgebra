from pathlib import Path

SCENE_PATH = Path("scenes/gram_schmidt_three_vectors_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_header_and_revision() -> None:
    source = scene_source()
    assert 'LESSON_TITLE = "Gram-Schmidt in R^3"' in source
    assert 'SCENE_REVISION = "cp159_r6_card5_pairwise_views"' in source
    assert 'class GramSchmidtThreeVectorsPresentation(ThreeDScene)' in source


def test_scene_has_six_cards() -> None:
    source = scene_source()
    for helper in (
        '_starting_triple_card',
        '_build_u1_u2_card',
        '_remove_u1_component_from_v3_card',
        '_remove_u2_component_from_v3_card',
        '_orthogonal_frame_card',
        '_synthesis_card',
    ):
        assert f'self.{helper}()' in source
        assert f'def {helper}' in source


def test_scene_uses_3d_axes_and_camera_motion() -> None:
    source = scene_source()
    assert 'ThreeDAxes(' in source
    assert 'Arrow3D(' in source
    assert 'self.set_camera_orientation(phi=65 * DEGREES, theta=-40 * DEGREES, zoom=0.84)' in source
    assert 'self.move_camera(phi=55 * DEGREES, theta=135 * DEGREES, zoom=0.88, run_time=1.8)' in source
    assert 'self.move_camera(phi=37 * DEGREES, theta=-45 * DEGREES, zoom=0.88, run_time=1.8)' in source
    assert 'self.move_camera(phi=88 * DEGREES, theta=45 * DEGREES, zoom=0.88, run_time=1.8)' in source
    assert 'self.move_camera(phi=65 * DEGREES, theta=-40 * DEGREES, zoom=0.84, run_time=1.2)' in source


def test_scene_contains_clean_three_vector_example() -> None:
    source = scene_source()
    for token in (
        r'\mathbf v_1=(2,2,0)',
        r'\mathbf v_2=(2,0,2)',
        r'\mathbf v_3=(3,-1,1)',
        r'\operatorname{proj}_{\mathbf u_1}\mathbf v_3=(1,1,0)',
        r'\operatorname{proj}_{\mathbf u_2}\mathbf v_3=(1,-1,2)',
        r'=(1,-1,-1)',
    ):
        assert token in source


def test_scene_states_general_recipe_and_normalization_note() -> None:
    source = scene_source()
    assert 'self.lesson.GENERAL_STEP' in source
    assert 'self.lesson.NORMALIZE_NOTE' in source
    assert 'self.lesson.closing_prompt' in source
    assert 'add_fixed_orientation_mobjects' in source
    assert 'Looking nearly along one vector makes the other two reveal a right angle.' in source


def test_scene_uses_runtime_safe_fixed_registration_and_lower_larger_axes() -> None:
    source = scene_source()
    assert "def _prepare_fixed_orientation" not in source
    assert "def _prepare_fixed_in_frame" not in source
    assert "self.add_fixed_orientation_mobjects(v1_label, v2_label, v3_label)" in source
    assert "self.add_fixed_in_frame_mobjects(heading)" in source
    assert "self.remove_fixed_orientation_mobjects" in source
    assert "x_length=5.35" in source
    assert "y_length=6.15" in source
    assert "z_length=5.35" in source
    assert ".shift(LEFT * 2.2 + DOWN * 2.45)" in source
    assert "run_time=0.01" not in source
    assert "self.set_camera_orientation(phi=65 * DEGREES, theta=-40 * DEGREES, zoom=0.84)" in source


def test_scene_uses_farther_label_offsets() -> None:
    source = scene_source()
    assert "np.array([-0.62, 0.48, 0.0])" in source
    assert "np.array([0.52, -0.40, 0.0])" in source
    assert "np.array([0.66, 0.38, 0.0])" in source
    assert "np.array([-0.40, 0.52, 0.0])" in source
    assert "np.array([0.56, 0.40, 0.0])" in source
    assert "np.array([0.48, -0.42, 0.0])" in source


def test_card5_reveals_pairwise_orthogonality_sequentially() -> None:
    source = scene_source()
    assert "self.add_fixed_in_frame_mobjects(equations[0], caption)" in source
    assert "self.add_fixed_in_frame_mobjects(equations[1])" in source
    assert "self.add_fixed_in_frame_mobjects(equations[2])" in source
    assert "self.wait(0.8)" in source
    assert "Rotate(" not in source
    assert "Z_AXIS" not in source
