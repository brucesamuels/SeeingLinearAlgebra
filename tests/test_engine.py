"""Minimal render test for engine v0.1."""

from manim import Create, FadeIn, FadeOut, NumberPlane
from engine.branding import BrooklynTechIntro
from engine.scene_tools import SeeingScene, chapter_title
from engine.theme import AXIS, GRID

class EngineSmokeTest(SeeingScene):
    def construct(self):
        intro = BrooklynTechIntro(episode_number=0, episode_title="Engine Test")
        self.play(FadeIn(intro))
        self.wait(0.5)
        self.clear_all()

        plane = NumberPlane(
            background_line_style={
                "stroke_color": GRID,
                "stroke_width": 1,
                "stroke_opacity": 0.55,
            },
            axis_config={"color": AXIS},
        )
        heading = chapter_title("Engine v0.1")
        self.play(Create(plane), FadeIn(heading))
        self.wait(0.5)
        self.play(FadeOut(plane), FadeOut(heading))
