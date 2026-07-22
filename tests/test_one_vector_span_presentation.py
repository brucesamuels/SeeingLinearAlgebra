from pathlib import Path


SCENE_PATH = Path("scenes/one_vector_span_presentation.py")


def test_scene_is_additive_and_uses_the_renderer_independent_model() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    assert "class OneVectorSpanPresentation(Scene)" in source
    assert "from engine.one_vector_span import OneVectorSpan" in source
    assert "from engine.manim_one_vector_span import ManimOneVectorSpan" in source
    assert "chapter_one" not in source.lower()


def test_chapter_two_opens_with_the_approved_inquiry() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    assert "What should we call the collection" in source
    assert "of all vectors we can create?" in source
    assert 'CHAPTER_TITLE = "Vector Spaces and Subspaces"' in source


def test_span_is_revealed_by_continuous_motion_before_the_definition() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    assert "ValueTracker" in source
    assert "TracedPath" in source
    assert "rate_func=linear" in source
    assert "Continuous motion makes the span appear before it is named." in source
    assert r"\operatorname{span}\{\mathbf v\}" in source

    sweep_index = source.index("coefficient.animate.set_value(COEFFICIENT_EXTENT)")
    definition_index = source.index("definition = MathTex(SPAN_DEFINITION")
    assert sweep_index < definition_index


def test_prediction_and_reflection_are_both_present() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    assert 'PREDICTION_PROMPT = "As t takes every real value' in source
    assert 'REFLECTION_PROMPT = "Why must the line pass through the origin?"' in source
    assert "PAUSE AND PREDICT" in source


def test_zero_length_arrow_is_handled_by_the_thin_adapter() -> None:
    source = Path("engine/manim_one_vector_span.py").read_text(encoding="utf-8")

    assert "ZERO_EPSILON" in source
    assert "put_start_and_end_on" in source
    assert "set_opacity(0.0 if distance <= self.ZERO_EPSILON else 1.0)" in source
