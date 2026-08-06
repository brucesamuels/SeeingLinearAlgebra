"""Opening title card for Chapter 4: Solving Linear Systems."""

from __future__ import annotations

from manim import DOWN, FadeIn, FadeOut, MathTex, Scene, Text, UP, VGroup, Write, YELLOW


class ChapterFourTitleCard(Scene):
    """Introduce the assembled chapter without crowding the frame."""

    def construct(self) -> None:
        chapter = Text("CHAPTER 4", font_size=28, color=YELLOW)
        title = Text("Solving Linear Systems", font_size=52)
        equation = MathTex(
            r"A\mathbf{x}=\mathbf{b}",
            font_size=64,
            color=YELLOW,
        )
        subtitle = Text(
            "Elimination, solution sets, inverses, and factorization",
            font_size=24,
        )
        series = Text("Seeing Linear Algebra", font_size=21)

        main_group = VGroup(chapter, title, equation, subtitle).arrange(DOWN, buff=0.28)
        self._fit_down_only(main_group, 11.4)
        main_group.move_to(UP * 0.18)
        series.to_edge(DOWN, buff=0.42)

        self.play(FadeIn(chapter), run_time=1.0)
        self.play(Write(title), run_time=1.8)
        self.play(FadeIn(equation), run_time=1.25)
        self.play(FadeIn(subtitle), FadeIn(series), run_time=1.25)
        self.wait(3.2)
        self.play(FadeOut(main_group), FadeOut(series), run_time=1.5)

    @staticmethod
    def _fit_down_only(mobject, maximum_width: float):
        if mobject.width > maximum_width:
            mobject.scale_to_fit_width(maximum_width)
        return mobject
