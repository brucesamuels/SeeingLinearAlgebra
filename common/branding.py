from __future__ import annotations

from pathlib import Path
from manim import *

from common.theme import BACKGROUND, CYAN, GRID, MUTED, TEXT

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SEAL_PATH = PROJECT_ROOT / "assets" / "BTHSseal.jpeg"


class BrooklynTechTitle(Group):
    """Reusable branded title card for Seeing Linear Algebra."""

    def __init__(
        self,
        episode: str,
        title: str,
        subtitle: str = "",
        instructor: str = "Mr. Bruce Samuels",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        seal = ImageMobject(str(SEAL_PATH)).scale_to_fit_height(1.45)
        school = Text(
            "BROOKLYN TECHNICAL HIGH SCHOOL",
            font_size=22,
            color=MUTED,
            weight=BOLD,
        )
        series = Text(
            "SEEING LINEAR ALGEBRA",
            font_size=48,
            color=TEXT,
            weight=BOLD,
        )
        rule = Line(LEFT * 3.6, RIGHT * 3.6, color=GRID, stroke_width=2)
        ep = Text(episode.upper(), font_size=20, color=CYAN, weight=BOLD)
        main = Text(title, font_size=60, color=TEXT, weight=BOLD)
        teacher = Text(instructor, font_size=21, color=MUTED)

        text_items = [school, series, rule, ep, main]
        if subtitle:
            text_items.append(Text(subtitle, font_size=24, color=MUTED))
        text_items.append(teacher)
        text_group = VGroup(*text_items).arrange(DOWN, buff=0.13)

        seal.next_to(text_group, LEFT, buff=0.55)
        self.add(seal, text_group)
        self.move_to(ORIGIN)
        self.seal = seal
        self.text_group = text_group
