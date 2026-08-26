"""Opening title card for the Change of Basis preview chapter."""
from manim import (
    BLUE_C, GREEN_C, GREY_B, ORANGE, PURPLE_C, TEAL_C, WHITE, YELLOW,
    DOWN, LEFT, RIGHT, UP,
    Arrow, FadeIn, FadeOut, Line, MathTex, Scene, Text, VGroup,
)


class ChangeOfBasisTitleCard(Scene):
    def construct(self):
        eyebrow = Text("SEEING LINEAR ALGEBRA", font_size=24, color=GREY_B, weight="BOLD")
        eyebrow.to_edge(UP, buff=0.42)
        title = Text("CHANGE OF BASIS", font_size=64, color=YELLOW, weight="BOLD")
        subtitle = Text("One object. Many coordinate languages.", font_size=34, color=WHITE)
        headings = VGroup(eyebrow, title, subtitle).arrange(DOWN, buff=0.27)
        headings.move_to(UP * 1.55)

        origin = DOWN * 1.48
        fixed_vector = Arrow(origin, origin + RIGHT * 3.0 + UP * 1.45, buff=0, color=ORANGE, stroke_width=9)
        fixed_label = MathTex(r"\mathbf v", font_size=42, color=ORANGE).next_to(fixed_vector.get_end(), UP, buff=0.08)

        standard_axes = VGroup(
            Arrow(origin, origin + RIGHT * 2.15, buff=0, color=GREEN_C, stroke_width=6),
            Arrow(origin, origin + UP * 1.85, buff=0, color=BLUE_C, stroke_width=6),
        )
        changed_axes = VGroup(
            Arrow(origin, origin + RIGHT * 1.55 + UP * 1.05, buff=0, color=TEAL_C, stroke_width=6),
            Arrow(origin, origin + RIGHT * 1.60 + DOWN * 1.05, buff=0, color=PURPLE_C, stroke_width=6),
        )

        standard_grid = VGroup()
        for offset in range(-3, 5):
            standard_grid.add(Line(origin + RIGHT * offset + DOWN * 1.2, origin + RIGHT * offset + UP * 2.0, color=GREY_B, stroke_width=1.2, stroke_opacity=0.35))
        for offset in range(-1, 3):
            standard_grid.add(Line(origin + LEFT * 3.4 + UP * offset, origin + RIGHT * 4.0 + UP * offset, color=GREY_B, stroke_width=1.2, stroke_opacity=0.35))

        changed_grid = standard_grid.copy()
        changed_grid.apply_matrix([[1.0, 0.85], [0.55, -0.55]], about_point=origin)
        changed_grid.set_color(TEAL_C).set_stroke(opacity=0.35)

        question = Text("What changes—and what stays the same?", font_size=31, color=YELLOW)
        question.to_edge(DOWN, buff=0.28)

        self.play(FadeIn(headings), run_time=1.0)
        self.play(FadeIn(standard_grid), FadeIn(standard_axes), FadeIn(fixed_vector), FadeIn(fixed_label), run_time=1.2)
        self.wait(0.7)
        self.play(FadeOut(standard_grid), FadeOut(standard_axes), FadeIn(changed_grid), FadeIn(changed_axes), run_time=1.6)
        self.play(FadeIn(question))
        self.wait(1.8)

