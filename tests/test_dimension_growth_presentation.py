from pathlib import Path


SCENE_PATH = Path("scenes/dimension_growth_presentation.py")


def test_scene_uses_renderer_independent_dimension_growth_model() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    assert "class DimensionGrowthPresentation(ThreeDScene)" in source
    assert "from engine.dimension_growth import DimensionGrowth" in source
    assert "from engine.manim_dimension_growth import ManimDimensionGrowth" in source


def test_lesson_builds_line_then_plane_then_space() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    line_stage = source.index("line_coefficients = np.linspace")
    plane_stage = source.index("plane_pairs = np.array")
    space_stage = source.index("layer_coefficients = np.linspace")

    assert line_stage < plane_stage < space_stage
    assert "One direction generates a line." in source
    assert "A second independent direction generates a plane." in source
    assert "A direction outside the plane moves the entire plane." in source


def test_prediction_occurs_before_third_vector_and_plane_stack() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    prediction = source.index("self.play(FadeIn(prediction")
    w_reveal = source.index("self.play(Create(display.w_arrow)")
    layers = source.index("layer_coefficients = np.linspace")

    assert prediction < w_reveal < layers
    assert "Will the third vector create a new dimension" in source


def test_space_is_revealed_as_translated_plane_layers() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    assert "model.snapshot(float(coefficient))" in source
    assert "translated_plane_corners" in source
    assert "LaggedStart(*(FadeIn(layer) for layer in layers)" in source
    assert "model.space_points(triples)" in source


def test_formal_span_is_delayed_until_after_camera_rotation() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    rotation = source.index("self.begin_ambient_camera_rotation")
    formal = source.index("self.play(FadeIn(span_label")

    assert rotation < formal
    assert r"\operatorname{span}\{\mathbf u,\mathbf v,\mathbf w\}=\mathbb R^3" in source


def test_text_overlays_are_registered_only_when_needed() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    assert "self.add_fixed_in_frame_mobjects(title)" in source
    assert "self.add_fixed_in_frame_mobjects(line_idea)" in source
    assert "self.add_fixed_in_frame_mobjects(plane_idea)" in source
    assert "self.add_fixed_in_frame_mobjects(prediction)" in source
    assert "self.add_fixed_in_frame_mobjects(space_idea)" in source
    assert "self.add_fixed_in_frame_mobjects(key_idea, span_label)" in source
