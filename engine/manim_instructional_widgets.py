"""Reusable themed instructional text widgets."""

from __future__ import annotations

from manim import RoundedRectangle, Text, VGroup

from engine.manim_lesson_theme import LessonTheme, SEEING_LINEAR_ALGEBRA_THEME


class ThemedText:
    """Factory for semantic text roles."""

    @staticmethod
    def lesson_title(
        text: str,
        *,
        theme: LessonTheme = SEEING_LINEAR_ALGEBRA_THEME,
    ) -> Text:
        return Text(text).scale(theme.typography.lesson_title_scale)

    @staticmethod
    def guiding_question(
        text: str,
        *,
        theme: LessonTheme = SEEING_LINEAR_ALGEBRA_THEME,
    ) -> Text:
        return Text(text).scale(
            theme.typography.guiding_question_scale
        ).set_color(theme.colors.prediction)

    @staticmethod
    def perspective_title(
        text: str,
        *,
        theme: LessonTheme = SEEING_LINEAR_ALGEBRA_THEME,
    ) -> Text:
        return Text(text).scale(
            theme.typography.perspective_title_scale
        ).set_color(theme.colors.application)

    @staticmethod
    def body(
        text: str,
        *,
        theme: LessonTheme = SEEING_LINEAR_ALGEBRA_THEME,
    ) -> Text:
        return Text(text).scale(theme.typography.body_scale)

    @staticmethod
    def takeaway(
        text: str,
        *,
        theme: LessonTheme = SEEING_LINEAR_ALGEBRA_THEME,
    ) -> Text:
        return Text(text).scale(
            theme.typography.takeaway_scale
        ).set_color(theme.colors.reflection)

    @staticmethod
    def footer(
        text: str,
        *,
        theme: LessonTheme = SEEING_LINEAR_ALGEBRA_THEME,
    ) -> Text:
        return Text(text).scale(
            theme.typography.footer_scale
        ).set_color(theme.colors.narration)


class KeyIdeaBanner(VGroup):
    """Simple themed banner for one important statement."""

    def __init__(
        self,
        text: str,
        *,
        theme: LessonTheme = SEEING_LINEAR_ALGEBRA_THEME,
    ) -> None:
        label = ThemedText.takeaway(text, theme=theme)
        box = RoundedRectangle(
            width=label.width + 0.5,
            height=label.height + 0.3,
            corner_radius=0.08,
        ).set_color(theme.colors.definition)
        super().__init__(box, label)
