from pathlib import Path


SCENE_PATH = Path("scenes/two_vector_span_presentation.py")


def test_scene_is_additive_and_uses_renderer_independent_mathematics() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    assert "class TwoVectorSpanPresentation(ThreeDScene)" in source
    assert "from engine.two_vector_span import TwoVectorSpan" in source
    assert "from engine.manim_two_vector_span import" in source
    assert "chapter_one" not in source.lower()


def test_lesson_asks_the_approved_second_direction_question() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    assert 'LESSON_QUESTION = "What changes when we add a second direction?"' in source
    assert "leave gaps" in source
    assert "form a grid" in source
    assert "fill the plane" in source


def test_text_is_registered_as_fixed_in_frame_only_when_needed() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    assert "self.add_fixed_in_frame_mobjects(title)" in source
    assert "self.add_fixed_in_frame_mobjects(prediction)" in source
    assert "self.add_fixed_in_frame_mobjects(readout)" in source
    assert "self.add_fixed_in_frame_mobjects(first_discovery)" in source
    assert "self.add_fixed_in_frame_mobjects(second_discovery)" in source
    assert "self.add_fixed_in_frame_mobjects(definition, key_idea)" in source


def test_one_line_is_traced_before_the_family_sweeps_the_plane() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    first_sweep = source.index("coefficient_b.animate.set_value(B_EXTENT)")
    family_sweep = source.index("sample_values = np.linspace")
    definition = source.index("self.play(FadeIn(definition")

    assert first_sweep < family_sweep < definition
    assert "fixed_u_line" in source
    assert "moving a translates the entire b-line" in source
    assert "rate_func=linear" in source


def test_formal_span_and_reflection_are_delayed_until_after_motion() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    assert r"\operatorname{span}\{\mathbf u,\mathbf v\}" in source
    assert "Two independent directions generate the entire plane." in source
    assert "Why does every point in the plane have a recipe" in source


def test_manim_adapters_update_existing_objects_in_place() -> None:
    source = Path("engine/manim_two_vector_span.py").read_text(encoding="utf-8")

    assert "put_start_and_end_on" in source
    assert "class ManimTwoVectorCombination" in source
    assert "class ManimFixedCoefficientLine" in source
    assert "self.line.put_start_and_end_on" in source


def test_final_sweep_resolves_into_sampled_vector_endpoints() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    family_sweep = source.index("sample_values = np.linspace")
    sparse_reveal = source.index("coefficient_a_values = np.linspace")
    dense_reveal = source.index("dense_endpoint_field = VGroup")
    definition = source.index("self.play(FadeIn(definition")

    assert family_sweep < sparse_reveal < dense_reveal < definition
    assert "model.endpoints_for(pairs)" in source
    assert "model.endpoints_for(dense_pairs)" in source
    assert "LaggedStart" in source
    assert "FadeOut(retained_lines)" in source


def test_endpoint_sampling_extends_beyond_the_visible_frame() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    assert "np.linspace(-4.60, 4.60, 31)" in source
    assert "np.linspace(-4.60, 4.60, 41)" in source


def test_completed_b_line_is_removed_before_camera_tilt() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    solid_reveal = source.index("FadeIn(solid_span_plane)")
    line_removal = source.index("FadeOut(moving_line.line)")
    camera_reveal = source.index("self.move_camera(phi=72 * DEGREES, theta=-58 * DEGREES, zoom=0.95, run_time=2.8)")

    assert solid_reveal <= line_removal < camera_reveal


def test_scene_uses_3d_camera_reveal_without_adding_a_third_axis() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    assert "self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0)" in source
    assert "self.move_camera(phi=72 * DEGREES, theta=-58 * DEGREES, zoom=0.95, run_time=2.8)" in source
    assert "ThreeDAxes" not in source
    assert "z_axis" not in source.lower()


def test_final_definition_layout_uses_separate_bottom_rows() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    assert "definition = MathTex(SPAN_DEFINITION, font_size=34, color=TEXT).to_edge(DOWN, buff=0.30)" in source
    assert "key_idea = Text(KEY_IDEA, font_size=24, color=MUTED).next_to(definition, UP, buff=0.32)" in source


def test_cp69_7_preserves_dense_sampling_and_more_retained_lines() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    assert "sample_values = np.linspace(-A_EXTENT, A_EXTENT, 17)" in source
    assert "run_time=0.30" in source
    assert "dense_endpoint_field.animate.set_opacity(0.14)" in source
