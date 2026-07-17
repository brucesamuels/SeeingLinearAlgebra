"""Reusable screen regions for Manim lesson scenes."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from manim import DOWN, LEFT, Mobject, UP


@dataclass(frozen=True, slots=True)
class LessonLayout:
    """Renderer-side anchors and safe-area helpers for lesson composition."""

    title_y: float = 3.25
    question_y: float = 2.55
    content_top_y: float = 1.75
    content_left_x: float = -4.9
    content_max_height: float = 4.25
    footer_y: float = -3.15
    title_scale: float = 0.82
    question_scale: float = 0.58
    footer_scale: float = 0.46

    def __post_init__(self) -> None:
        if not self.title_y > self.question_y > self.content_top_y:
            raise ValueError(
                "layout vertical anchors must satisfy "
                "title_y > question_y > content_top_y"
            )
        if self.content_max_height <= 0:
            raise ValueError("content_max_height must be positive")
        for name in ("title_scale", "question_scale", "footer_scale"):
            if getattr(self, name) <= 0:
                raise ValueError(f"{name} must be positive")

    @property
    def title_anchor(self) -> np.ndarray:
        return np.array([0.0, self.title_y, 0.0])

    @property
    def question_anchor(self) -> np.ndarray:
        return np.array([0.0, self.question_y, 0.0])

    @property
    def content_anchor(self) -> np.ndarray:
        return np.array([self.content_left_x, self.content_top_y, 0.0])

    @property
    def footer_anchor(self) -> np.ndarray:
        return np.array([0.0, self.footer_y, 0.0])

    def place_title(self, mobject: Mobject) -> Mobject:
        return mobject.move_to(self.title_anchor)

    def place_question(self, mobject: Mobject) -> Mobject:
        return mobject.move_to(self.question_anchor)

    def place_content(self, mobject: Mobject) -> Mobject:
        """Place a left-aligned content block within the instructional region."""
        mobject.align_to(self.content_anchor, LEFT)
        mobject.align_to(self.content_anchor, UP)
        if mobject.height > self.content_max_height:
            mobject.scale_to_fit_height(self.content_max_height)
            mobject.align_to(self.content_anchor, LEFT)
            mobject.align_to(self.content_anchor, UP)
        return mobject

    def place_footer(self, mobject: Mobject) -> Mobject:
        return mobject.move_to(self.footer_anchor)
