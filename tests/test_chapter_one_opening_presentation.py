from __future__ import annotations

import ast
from pathlib import Path


SCENE_PATH = Path("scenes/chapter_one_opening_presentation.py")


def _source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def _class_definition() -> ast.ClassDef:
    module = ast.parse(_source())
    return next(
        node
        for node in module.body
        if isinstance(node, ast.ClassDef)
        and node.name == "ChapterOneOpeningPresentation"
    )


def test_combined_scene_reuses_the_approved_presentation_classes() -> None:
    source = _source()

    assert "from scenes.why_vectors_presentation import WhyVectorsPresentation" in source
    assert (
        "from scenes.vector_representation_presentation import "
        "VectorRepresentationPresentation"
    ) in source
    assert (
        "from scenes.free_vector_equality_presentation import "
        "FreeVectorEqualityPresentation"
    ) in source


def test_combined_scene_consumes_the_renderer_independent_sequence() -> None:
    source = _source()

    assert (
        "from engine.chapter_one_opening_sequence import "
        "CHAPTER_ONE_OPENING_SEQUENCE"
    ) in source
    assert "CHAPTER_SEQUENCE = CHAPTER_ONE_OPENING_SEQUENCE" in source
    assert "for lesson_index, lesson in enumerate(self.CHAPTER_SEQUENCE):" in source


def test_presentation_registry_matches_the_approved_lesson_keys() -> None:
    source = _source()

    expected_bindings = (
        '"why_vectors": WhyVectorsPresentation',
        '"vector_representation": VectorRepresentationPresentation',
        '"free_vector_equality": FreeVectorEqualityPresentation',
    )

    for binding in expected_bindings:
        assert source.count(binding) == 1


def test_each_lesson_delegates_to_its_existing_construct_method() -> None:
    source = _source()

    assert "presentation_class = self.PRESENTATIONS_BY_KEY[lesson.key]" in source
    assert "presentation_class.construct(self)" in source


def test_combined_scene_creates_named_manim_sections() -> None:
    source = _source()

    assert "self.next_section(lesson.key)" in source


def test_transition_fades_existing_mobjects_and_clears_the_canvas() -> None:
    source = _source()

    assert "current_mobjects = tuple(self.mobjects)" in source
    assert "FadeOut(mobject) for mobject in current_mobjects" in source
    assert "run_time=self.THEME.timing.transition" in source
    assert "self.clear()" in source


def test_combined_scene_does_not_duplicate_lesson_geometry_or_mathematics() -> None:
    source = _source()

    forbidden_fragments = (
        "Arrow(",
        "MathTex(",
        "VectorRepresentation(",
        "FreeVectorEquality(",
        "PerspectivePictogramFactory",
    )

    for fragment in forbidden_fragments:
        assert fragment not in source


def test_combined_scene_remains_a_small_renderer_side_adapter() -> None:
    class_definition = _class_definition()
    method_names = {
        node.name
        for node in class_definition.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert method_names == {"construct", "_transition_between_lessons"}
