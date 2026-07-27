from pathlib import Path

SCENE = Path("scenes/null_space_presentation.py")


def test_scene_uses_null_space_model() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "from engine.null_space import NullSpace" in source
    assert "class NullSpacePresentation(ThreeDScene)" in source


def test_scene_uses_same_rank_two_matrix_as_column_space_lesson() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "[2.0, -0.5, 1.5]" in source
    assert "[0.5, 1.8, 2.3]" in source
    assert "[0.5, 0.8, 1.3]" in source


def test_scene_contrasts_input_space_and_output_space() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert r"\text{input space }\mathbf x" in source
    assert r"\text{output space }A\mathbf x" in source
    assert "input_axes = ThreeDAxes(" in source
    assert "output_axes = ThreeDAxes(" in source


def test_scene_reveals_null_points_before_the_line() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "self.play(FadeIn(null_dots), run_time=1.6)" in source
    assert "self.play(Create(null_line), null_dots.animate.set_opacity(0.42), run_time=2.4)" in source
    assert "self.wait(0.8)" in source


def test_scene_animates_null_inputs_along_a_line_more_slowly() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "null_samples = model.scalar_multiples" in source
    assert r"A\mathbf n=\mathbf 0" in source
    assert "UpdateFromAlphaFunc(moving_input_dot, sweep_null_input)" in source
    assert "run_time=9.6" in source
    assert "self.wait(1.6)" in source


def test_scene_states_null_space_span_and_rank_nullity() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert r"\operatorname{null}(A)=\operatorname{span}\{\mathbf n\}" in source
    assert r"\dim(\operatorname{null}(A))+\operatorname{rank}(A)=1+2=3" in source


def test_scene_connects_null_space_to_subspace_test() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert r"\operatorname{null}(A)\text{ contains }\mathbf 0" in source
    assert r"\mathbf u,\mathbf v\in\operatorname{null}(A)\Rightarrow A(\mathbf u+\mathbf v)=\mathbf 0" in source
    assert r"c\mathbf u\in\operatorname{null}(A)\Rightarrow A(c\mathbf u)=\mathbf 0" in source


def test_null_sweep_uses_non_degenerate_line_instead_of_arrow() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "moving_input_segment = Line(" in source
    assert "moving_input_arrow" not in source
    assert "safe_scalar = 0.04 if scalar >= 0 else -0.04" in source
