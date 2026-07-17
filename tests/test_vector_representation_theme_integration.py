from __future__ import annotations

import inspect

from engine.manim_lesson_layout import LessonLayout
from engine.manim_lesson_theme import LessonTheme
from scenes.vector_representation_presentation import (
    VectorRepresentationPresentation,
)


def test_scene_declares_shared_theme_and_layout() -> None:
    assert isinstance(VectorRepresentationPresentation.THEME, LessonTheme)
    assert isinstance(VectorRepresentationPresentation.LAYOUT, LessonLayout)


def test_scene_uses_themed_text_roles() -> None:
    source = inspect.getsource(VectorRepresentationPresentation.construct)

    assert "ThemedText.lesson_title" in source
    assert "ThemedText.guiding_question" in source
    assert "ThemedText.takeaway" in source
    assert "ThemedText.body" in source


def test_scene_uses_named_timing_presets() -> None:
    source = inspect.getsource(VectorRepresentationPresentation.construct)

    assert "self.THEME.timing.normal" in source
    assert "self.THEME.timing.read" in source
    assert "self.THEME.timing.reflection" in source


def test_scene_preserves_magnitude_derivation() -> None:
    source = inspect.getsource(VectorRepresentationPresentation.construct)

    assert r"\|\mathbf{v}\|=\sqrt{3^2+2^2}" in source
    assert r"\|\mathbf{v}\|=\sqrt{13}" in source
    assert r"\|\mathbf{v}\|\approx 3.6" in source


def test_scene_uses_layout_regions() -> None:
    source = inspect.getsource(VectorRepresentationPresentation.construct)

    assert "self.LAYOUT.place_title(title)" in source
    assert "self.LAYOUT.place_question(prompt)" in source
    assert "self.LAYOUT.place_footer(equivalence)" in source
    assert "self.LAYOUT.place_footer(reflection)" in source
