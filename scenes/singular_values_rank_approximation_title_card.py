"""Opening title card for Singular Values, Rank, and Approximation."""

from manim import (
    DOWN,
    FadeIn,
    GREEN_C,
    GREY_B,
    MathTex,
    ORANGE,
    RIGHT,
    Scene,
    SurroundingRectangle,
    TEAL_C,
    Text,
    UP,
    VGroup,
    WHITE,
    YELLOW,
)


class SingularValuesRankApproximationTitleCard(Scene):
    """Introduce the chapter through the information in the SVD."""

    @staticmethod
    def _card(label, formula, note, color):
        body = VGroup(
            Text(label, font_size=22, color=color, weight="BOLD"),
            MathTex(formula, font_size=41, color=WHITE),
            Text(note, font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.16)
        border = SurroundingRectangle(body, color=color, buff=0.17, stroke_width=2.0)
        return VGroup(border, body)

    def construct(self):
        eyebrow = Text(
            "SEEING LINEAR ALGEBRA", font_size=24, color=GREY_B, weight="BOLD"
        )
        title = Text(
            "SINGULAR VALUES, RANK, AND APPROXIMATION",
            font_size=45,
            color=YELLOW,
            weight="BOLD",
        )
        if title.width > 12.2:
            title.scale_to_fit_width(12.2)
        subtitle = Text(
            "What matrices preserve, lose, amplify, and approximate.",
            font_size=30,
            color=WHITE,
        )
        headings = VGroup(eyebrow, title, subtitle).arrange(DOWN, buff=0.23).move_to(UP * 2.12)

        formula = MathTex(r"A=U\Sigma V^T", font_size=55, color=YELLOW)
        roles = VGroup(
            self._card("INPUT", r"V^T", "preferred directions", TEAL_C),
            self._card("STRETCH", r"\Sigma", "singular values", ORANGE),
            self._card("OUTPUT", r"U", "images of directions", GREEN_C),
        ).arrange(RIGHT, buff=0.52)
        body = VGroup(formula, roles).arrange(DOWN, buff=0.39).move_to(DOWN * 0.35)

        question = Text(
            "What does each singular value tell us?",
            font_size=28,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.33)

        self.play(FadeIn(headings), run_time=0.9)
        self.play(FadeIn(formula), run_time=0.8)
        self.play(FadeIn(roles), run_time=0.9)
        self.play(FadeIn(question), run_time=0.6)
        self.wait(2.5)
