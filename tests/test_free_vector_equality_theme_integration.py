from __future__ import annotations

import inspect

from engine.manim_lesson_layout import LessonLayout
from engine.manim_lesson_theme import LessonTheme
from scenes.free_vector_equality_presentation import (
    FreeVectorEqualityPresentation,
)


def test_scene_declares_shared_theme_and_layout() -> None:
    assert isinstance(FreeVectorEqualityPresentation.THEME, LessonTheme)
    assert isinstance(FreeVectorEqualityPresentation.LAYOUT, LessonLayout)


def test_scene_uses_themed_text_roles() -> None:
    source = inspect.getsource(FreeVectorEqualityPresentation.construct)

    assert "ThemedText.lesson_title" in source
    assert "ThemedText.guiding_question" in source
    assert "ThemedText.body" in source
    assert "ThemedText.takeaway" in source


def test_scene_uses_named_timing_presets() -> None:
    source = inspect.getsource(FreeVectorEqualityPresentation.construct)

    assert "self.THEME.timing.quick" in source
    assert "self.THEME.timing.normal" in source
    assert "self.THEME.timing.read" in source
    assert "self.THEME.timing.reflection" in source


def test_scene_uses_layout_regions() -> None:
    source = inspect.getsource(FreeVectorEqualityPresentation.construct)

    assert "self.LAYOUT.place_title(title)" in source
    assert "self.LAYOUT.place_question(prompt)" in source
    assert "self.LAYOUT.place_footer(coordinate_label)" in source
    assert "self.LAYOUT.place_footer(definition)" in source


def test_scene_uses_semantic_theme_colors() -> None:
    source = inspect.getsource(FreeVectorEqualityPresentation.construct)

    assert "self.THEME.colors.geometry" in source
    assert "self.THEME.colors.mathematics" in source
    assert "self.THEME.colors.definition" in source
    assert "self.THEME.colors.example" in source


def test_scene_preserves_free_vector_translation_sequence() -> None:
    source = inspect.getsource(FreeVectorEqualityPresentation.construct)

    assert "FreeVectorEquality(" in source
    assert "for target in arrows[1:]" in source
    assert "ReplacementTransform(moving_arrow, next_arrow)" in source
    assert "self.play(*[FadeIn(arrow) for arrow in arrows])" in source
