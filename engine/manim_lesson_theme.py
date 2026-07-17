"""Semantic visual identity for Seeing Linear Algebra lesson scenes."""

from __future__ import annotations

from dataclasses import dataclass

from manim import BLUE, GOLD, GREEN, GREY_B, ORANGE, PURPLE, RED, TEAL, WHITE


@dataclass(frozen=True, slots=True)
class LessonColors:
    geometry: str = BLUE
    application: str = GREEN
    definition: str = GOLD
    reflection: str = PURPLE
    prediction: str = TEAL
    mathematics: str = WHITE
    example: str = ORANGE
    warning: str = RED
    narration: str = GREY_B


@dataclass(frozen=True, slots=True)
class LessonTypography:
    chapter_title_scale: float = 0.92
    lesson_title_scale: float = 0.82
    guiding_question_scale: float = 0.58
    perspective_title_scale: float = 0.66
    body_scale: float = 0.40
    takeaway_scale: float = 0.46
    footer_scale: float = 0.46

    def __post_init__(self) -> None:
        for name in self.__dataclass_fields__:
            if getattr(self, name) <= 0:
                raise ValueError(f"{name} must be positive")


@dataclass(frozen=True, slots=True)
class LessonTiming:
    quick: float = 0.35
    normal: float = 0.65
    read: float = 1.20
    reflection: float = 1.40
    transition: float = 0.80

    def __post_init__(self) -> None:
        for name in self.__dataclass_fields__:
            if getattr(self, name) <= 0:
                raise ValueError(f"{name} must be positive")


@dataclass(frozen=True, slots=True)
class LessonTheme:
    colors: LessonColors = LessonColors()
    typography: LessonTypography = LessonTypography()
    timing: LessonTiming = LessonTiming()


SEEING_LINEAR_ALGEBRA_THEME = LessonTheme()
