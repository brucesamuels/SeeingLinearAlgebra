from manim import *

from common.theme import CYAN, MUTED, TEXT


def chapter_card(number: int, title: str) -> VGroup:
    n = Text(f"{number:02d}", font_size=25, color=CYAN, weight=BOLD)
    t = Text(title, font_size=42, color=TEXT, weight=BOLD)
    line = Line(LEFT * 2.4, RIGHT * 2.4, color=MUTED, stroke_opacity=0.45)
    return VGroup(n, t, line).arrange(DOWN, buff=0.16)


def fade_replace(scene: Scene, old: Mobject, new: Mobject, run_time: float = 0.8) -> None:
    scene.play(FadeOut(old, shift=UP * 0.12), FadeIn(new, shift=UP * 0.12), run_time=run_time)
