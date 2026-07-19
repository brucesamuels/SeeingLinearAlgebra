from __future__ import annotations

import inspect

from manim import Scene

from engine.manim_lesson_layout import LessonLayout
from engine.manim_lesson_theme import LessonTheme
from engine.vector_subtraction_lesson import VECTOR_SUBTRACTION_LESSON_SEQUENCE
from scenes.vector_subtraction_presentation import (
    MINUEND_VECTOR,
    SUBTRAHEND_VECTOR,
    VectorSubtractionPresentation,
)


def test_scene_declares_sequence_theme_and_layout() -> None:
    assert issubclass(VectorSubtractionPresentation, Scene)
    assert (
        VectorSubtractionPresentation.LESSON_SEQUENCE
        is VECTOR_SUBTRACTION_LESSON_SEQUENCE
    )
    assert isinstance(VectorSubtractionPresentation.THEME, LessonTheme)
    assert isinstance(VectorSubtractionPresentation.LAYOUT, LessonLayout)


def test_scene_reuses_vector_addition_example_vectors() -> None:
    assert MINUEND_VECTOR == (3.0, 1.0)
    assert SUBTRAHEND_VECTOR == (1.0, 2.0)


def test_scene_uses_renderer_independent_subtraction_snapshot() -> None:
    source = inspect.getsource(VectorSubtractionPresentation.construct)

    assert "snapshot = VectorSubtraction(" in source
    assert "assert snapshot.result == (2.0, -1.0)" in source
    assert "assert snapshot.coefficients == (1.0, -1.0)" in source
    assert "assert snapshot.is_opposite_vector" in source
    assert "assert snapshot.preserves_magnitude" in source


def test_scene_reverses_v_through_origin_before_translating_it() -> None:
    source = inspect.getsource(VectorSubtractionPresentation.construct)

    rotate_index = source.index(
        "Rotate(v_arrow, angle=PI, about_point=origin)"
    )
    translate_index = source.index(
        "Transform(moving_negative_v, translated_negative_target)"
    )

    assert rotate_index < translate_index
    assert "negative_v_target = Arrow(" in source
    assert "translated_negative_target = Arrow(" in source


def test_scene_computes_subtraction_in_successive_forms() -> None:
    source = inspect.getsource(VectorSubtractionPresentation.construct)

    assert r"\mathbf{u}-\mathbf{v}" in source
    assert r"\mathbf{u}+(-\mathbf{v})" in source
    assert r"(3,1)+(-1,-2)" in source
    assert r"\mathbf{u}-\mathbf{v}=(2,-1)" in source
    assert "ReplacementTransform(symbolic_subtraction, addition_form)" in source
    assert "ReplacementTransform(addition_form, substituted_form)" in source
    assert "ReplacementTransform(substituted_form, exact_result)" in source


def test_scene_emphasizes_same_magnitude_and_opposite_direction() -> None:
    source = inspect.getsource(VectorSubtractionPresentation.construct)

    assert r"-\mathbf{v}=(-1,-2)" in source
    assert r"\|-\mathbf{v}\|=\|\mathbf{v}\|" in source
    assert "Reverse v without changing its length." in source
    assert "The opposite has the same magnitude and reverse direction." in source


def test_scene_states_subtraction_as_adding_the_opposite() -> None:
    source = inspect.getsource(VectorSubtractionPresentation.construct)

    assert "To subtract a vector, add its opposite" in source
    assert "How can subtraction be drawn using only vector addition?" in source


def test_scene_uses_shared_visual_identity_and_pacing() -> None:
    source = inspect.getsource(VectorSubtractionPresentation.construct)

    assert "ThemedText.lesson_title" in source
    assert "ThemedText.guiding_question" in source
    assert "ThemedText.body" in source
    assert "ThemedText.takeaway" in source
    assert "self.THEME.timing.normal" in source
    assert "self.THEME.timing.read" in source
    assert "self.THEME.timing.reflection" in source
