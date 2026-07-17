from __future__ import annotations

from manim import Text, VGroup

from engine.manim_instructional_widgets import (
    KeyIdeaBanner,
    ThemedText,
)
from engine.manim_lesson_theme import SEEING_LINEAR_ALGEBRA_THEME


def test_themed_text_factories_return_text() -> None:
    theme = SEEING_LINEAR_ALGEBRA_THEME

    assert isinstance(ThemedText.lesson_title("Lesson", theme=theme), Text)
    assert isinstance(ThemedText.guiding_question("Why?", theme=theme), Text)
    assert isinstance(ThemedText.perspective_title("Physics", theme=theme), Text)
    assert isinstance(ThemedText.body("Body", theme=theme), Text)
    assert isinstance(ThemedText.takeaway("Idea", theme=theme), Text)
    assert isinstance(ThemedText.footer("Footer", theme=theme), Text)


def test_key_idea_banner_is_group() -> None:
    banner = KeyIdeaBanner("One important idea")

    assert isinstance(banner, VGroup)
    assert len(banner) == 2
