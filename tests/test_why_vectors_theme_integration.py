from __future__ import annotations

import inspect

from engine.manim_lesson_theme import LessonTheme
from scenes.why_vectors_presentation import WhyVectorsPresentation


def test_scene_declares_shared_theme() -> None:
    assert isinstance(WhyVectorsPresentation.THEME, LessonTheme)


def test_scene_uses_named_timing_presets() -> None:
    source = inspect.getsource(WhyVectorsPresentation.construct)

    assert "self.THEME.timing.quick" in source
    assert "self.THEME.timing.normal" in source
    assert "self.THEME.timing.reflection" in source


def test_scene_uses_themed_text_factories() -> None:
    construct_source = inspect.getsource(
        WhyVectorsPresentation.construct
    )
    parts_source = inspect.getsource(
        WhyVectorsPresentation._perspective_parts
    )

    assert "ThemedText.lesson_title" in construct_source
    assert "ThemedText.guiding_question" in construct_source
    assert "ThemedText.perspective_title" in parts_source
    assert "ThemedText.takeaway" in parts_source
