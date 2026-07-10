from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from manim import *

from common.theme import (
    BLUE_VEC,
    BODY_FONT_SIZE,
    CYAN,
    GRID,
    LABEL_FONT_SIZE,
    MUTED,
    PURPLE,
    TEXT,
    TITLE_FONT_SIZE,
    YELLOW,
)


class GlowArrow(VGroup):
    """A vector arrow with a subtle layered glow."""

    def __init__(
        self,
        end: np.ndarray,
        start: np.ndarray = ORIGIN,
        color: ManimColor = BLUE_VEC,
        label: str | None = None,
        label_direction: np.ndarray = UR,
        buff: float = 0.0,
        stroke_width: float = 7,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        glow_outer = Arrow(
            start,
            end,
            buff=buff,
            color=color,
            stroke_width=20,
            max_tip_length_to_length_ratio=0.12,
        ).set_opacity(0.08)
        glow_inner = Arrow(
            start,
            end,
            buff=buff,
            color=color,
            stroke_width=12,
            max_tip_length_to_length_ratio=0.12,
        ).set_opacity(0.16)
        arrow = Arrow(
            start,
            end,
            buff=buff,
            color=color,
            stroke_width=stroke_width,
            max_tip_length_to_length_ratio=0.12,
        )
        self.arrow = arrow
        self.add(glow_outer, glow_inner, arrow)
        if label:
            tex = MathTex(label, color=color, font_size=LABEL_FONT_SIZE)
            tex.next_to(arrow.get_end(), label_direction, buff=0.12)
            self.label = tex
            self.add(tex)


class CornerCaption(VGroup):
    def __init__(self, heading: str, body: str | None = None, **kwargs) -> None:
        super().__init__(**kwargs)
        h = Text(heading, font_size=26, color=TEXT, weight=BOLD)
        items = [h]
        if body:
            b = Text(body, font_size=20, color=MUTED, line_spacing=0.85)
            b.next_to(h, DOWN, aligned_edge=LEFT, buff=0.12)
            items.append(b)
        self.add(*items)
        self.to_corner(UL, buff=0.35)


class SeriesTitle(VGroup):
    def __init__(self, episode: str, title: str, subtitle: str = "", **kwargs) -> None:
        super().__init__(**kwargs)
        brand = Text("SEEING LINEAR ALGEBRA", font_size=22, color=CYAN, weight=BOLD)
        rule = Line(LEFT * 3.4, RIGHT * 3.4, color=GRID, stroke_width=2)
        ep = Text(episode.upper(), font_size=20, color=MUTED)
        main = Text(title, font_size=TITLE_FONT_SIZE, color=TEXT, weight=BOLD)
        parts = [brand, rule, ep, main]
        if subtitle:
            sub = Text(subtitle, font_size=25, color=MUTED)
            parts.append(sub)
        self.add(*parts)
        self.arrange(DOWN, buff=0.18)


class DimensionBadge(VGroup):
    def __init__(self, dimension: int, label: str, **kwargs) -> None:
        super().__init__(**kwargs)
        number = Integer(dimension, font_size=48, color=YELLOW)
        word = Text("DIMENSION", font_size=17, color=MUTED, weight=BOLD)
        desc = Text(label, font_size=21, color=TEXT)
        number.next_to(word, DOWN, buff=0.05)
        desc.next_to(number, DOWN, buff=0.08)
        box = RoundedRectangle(
            corner_radius=0.16,
            width=2.2,
            height=1.65,
            stroke_color=PURPLE,
            stroke_opacity=0.7,
            fill_color="#111A2D",
            fill_opacity=0.82,
        )
        self.add(box, word, number, desc)
        VGroup(word, number, desc).move_to(box)


@dataclass(frozen=True)
class NarrationCue:
    key: str
    seconds: float


def equation_panel(*lines: Mobject, width: float = 4.6) -> VGroup:
    content = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    panel = RoundedRectangle(
        width=max(width, content.width + 0.5),
        height=content.height + 0.45,
        corner_radius=0.14,
        stroke_color=GRID,
        stroke_opacity=0.8,
        fill_color="#10182A",
        fill_opacity=0.9,
    )
    content.move_to(panel)
    return VGroup(panel, content)
