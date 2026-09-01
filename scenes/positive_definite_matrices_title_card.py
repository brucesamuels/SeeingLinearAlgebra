"""Opening title card for the Positive Definite Matrices preview chapter."""
from manim import (
    DOWN, FadeIn, GREEN_C, GREY_B, MathTex, Matrix, ORANGE, RIGHT, Scene,
    TEAL_C, Text, UP, VGroup, WHITE, YELLOW,
)


class PositiveDefiniteMatricesTitleCard(Scene):
    """Introduce the chapter through its central equivalent statements."""

    def construct(self):
        eyebrow = Text(
            "SEEING LINEAR ALGEBRA", font_size=24, color=GREY_B, weight="BOLD"
        )
        title = Text(
            "POSITIVE DEFINITE MATRICES", font_size=53, color=YELLOW, weight="BOLD"
        )
        subtitle = Text(
            "Energy, structure, and unique minima.", font_size=32, color=WHITE
        )
        headings = VGroup(eyebrow, title, subtitle).arrange(DOWN, buff=0.24)
        headings.move_to(UP * 1.85)

        matrix = Matrix([["2", "1"], ["1", "2"]], h_buff=0.92, v_buff=0.80).scale(0.72)
        center = VGroup(MathTex(r"A=", font_size=39), matrix).arrange(RIGHT, buff=0.13)

        statements = VGroup(
            MathTex(r"x^TAx>0", font_size=39, color=TEAL_C),
            MathTex(r"\lambda_i>0", font_size=39, color=ORANGE),
            MathTex(r"A=R^TR", font_size=39, color=GREEN_C),
        ).arrange(RIGHT, buff=1.05)
        body = VGroup(center, statements).arrange(DOWN, buff=0.52).move_to(DOWN * 0.28)

        question = Text(
            "How can one property appear in so many forms?",
            font_size=29,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.38)

        self.play(FadeIn(headings), run_time=0.9)
        self.play(FadeIn(center), run_time=0.8)
        self.play(FadeIn(statements), run_time=0.9)
        self.play(FadeIn(question), run_time=0.6)
        self.wait(2.0)
