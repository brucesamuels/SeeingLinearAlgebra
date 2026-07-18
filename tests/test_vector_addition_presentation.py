from __future__ import annotations

import inspect

from manim import Scene

from engine.manim_lesson_layout import LessonLayout
from engine.manim_lesson_theme import LessonTheme
from engine.vector_addition_lesson import VECTOR_ADDITION_LESSON_SEQUENCE
from scenes.vector_addition_presentation import (
    FIRST_VECTOR,
    SECOND_VECTOR,
    VectorAdditionPresentation,
)


def test_scene_declares_sequence_theme_and_layout() -> None:
    assert issubclass(VectorAdditionPresentation, Scene)
    assert (
        VectorAdditionPresentation.LESSON_SEQUENCE
        is VECTOR_ADDITION_LESSON_SEQUENCE
    )
    assert isinstance(VectorAdditionPresentation.THEME, LessonTheme)
    assert isinstance(VectorAdditionPresentation.LAYOUT, LessonLayout)


def test_scene_uses_the_requested_vectors() -> None:
    assert FIRST_VECTOR == (3.0, 1.0)
    assert SECOND_VECTOR == (1.0, 2.0)


def test_scene_reuses_renderer_independent_vector_addition_model() -> None:
    source = inspect.getsource(VectorAdditionPresentation.construct)

    assert "VectorAddition(" in source
    assert ").snapshot()" in source
    assert "snapshot.coefficients == (1.0, 1.0)" in source
    assert "snapshot.is_tip_to_tail" in source


def test_scene_establishes_both_vectors_in_standard_position() -> None:
    source = inspect.getsource(VectorAdditionPresentation.construct)

    assert "first_arrow = Arrow(" in source
    assert "second_arrow = Arrow(" in source
    assert "origin,\n            first_tip," in source
    assert "origin,\n            second_tip," in source


def test_scene_translates_second_vector_head_to_tail() -> None:
    source = inspect.getsource(VectorAdditionPresentation.construct)

    assert "translated_second_arrow = Arrow(" in source
    assert "first_tip,\n            result_tip," in source
    assert "ReplacementTransform(\n                second_arrow," in source
    assert "translated_second_arrow" in source


def test_scene_synchronizes_translation_with_coordinate_substitution() -> None:
    source = inspect.getsource(VectorAdditionPresentation.construct)

    assert r"\mathbf{u}+\mathbf{v}=(3,1)+(1,2)" in source
    assert "ReplacementTransform(\n                symbolic_sum," in source
    assert "substituted_sum" in source


def test_scene_draws_resultant_and_exact_sum_together() -> None:
    source = inspect.getsource(VectorAdditionPresentation.construct)

    assert r"\mathbf{u}+\mathbf{v}=(4,3)" in source
    assert "Create(resultant_arrow)" in source
    assert "FadeIn(resultant_label)" in source
    assert "ReplacementTransform(\n                substituted_sum," in source


def test_scene_delays_parallelogram_until_after_resultant() -> None:
    source = inspect.getsource(VectorAdditionPresentation.construct)

    resultant_index = source.index("Create(resultant_arrow)")
    parallelogram_index = source.index("Create(alternate_second)")
    assert resultant_index < parallelogram_index


def test_scene_uses_shared_visual_identity_and_conclusion() -> None:
    source = inspect.getsource(VectorAdditionPresentation.construct)

    assert "ThemedText.lesson_title" in source
    assert "ThemedText.guiding_question" in source
    assert "ThemedText.body" in source
    assert "ThemedText.takeaway" in source
    assert "Vector addition combines successive displacements" in source
    assert "self.THEME.timing.normal" in source
    assert "self.THEME.timing.read" in source
    assert "self.THEME.timing.reflection" in source
