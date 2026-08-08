"""CP142 presentation: the adjugate and the determinant formula for A^{-1}."""
from __future__ import annotations

import numpy as np
from manim import (
    BLUE,
    FadeIn,
    FadeOut,
    GREEN,
    GREY_B,
    MathTex,
    Matrix,
    RED,
    Scene,
    Text,
    VGroup,
    WHITE,
    YELLOW,
    Write,
)

from engine.determinant_adjugate_inverse import (
    adjugate_definition_tex,
    closing_lines,
    cofactor_signs,
    cramer_connection_tex,
    diagonal_entry_tex,
    example_adjugate,
    example_cofactor_matrix,
    example_inverse_formula_tex,
    example_matrix,
    example_product_tex,
    identity_tex,
    inverse_formula_tex,
    off_diagonal_entry_tex,
)


class DeterminantAdjugateInversePresentation(Scene):
    """Show how cofactors assemble into the inverse formula."""

    def construct(self) -> None:
        banner = Text("From Cofactors to the Inverse", font_size=38)
        banner.to_edge(np.array([0.0, 1.0, 0.0]), buff=0.24)
        subtitle = MathTex(r"\text{The Adjugate and }A^{-1}", font_size=28, color=GREY_B)
        subtitle.next_to(banner, np.array([0.0, -1.0, 0.0]), buff=0.12)
        self.play(Write(banner), FadeIn(subtitle))
        self.wait(0.8)
        self.play(FadeOut(subtitle))

        self.show_cofactor_to_adjugate(banner)
        self.show_identity_card(banner)
        self.show_inverse_formula(banner)
        self.show_two_by_two_example(banner)
        self.show_cramers_connection(banner)
        self.show_summary(banner)

    def stage_title(self, text: str, size: int = 30) -> Text:
        title = Text(text, font_size=size, color=YELLOW)
        title.move_to(np.array([0.0, 1.85, 0.0]))
        return title

    def show_cofactor_to_adjugate(self, banner: Text) -> None:
        title = self.stage_title("Build the adjugate from cofactors")
        sign_grid = VGroup(*[
            VGroup(*[MathTex(sign, font_size=34, color=GREEN if sign == "+" else RED) for sign in row]).arrange(np.array([1.0, 0.0, 0.0]), buff=0.55)
            for row in cofactor_signs()
        ]).arrange(np.array([0.0, -1.0, 0.0]), buff=0.38)
        sign_grid.move_to(np.array([-4.0, 0.15, 0.0]))

        labels = VGroup(
            Text("checkerboard signs", font_size=22, color=GREY_B),
            MathTex(r"C=[C_{ij}]", font_size=36, color=BLUE),
            MathTex(adjugate_definition_tex(), font_size=34, color=WHITE),
        ).arrange(np.array([0.0, -1.0, 0.0]), aligned_edge=np.array([-1.0, 0.0, 0.0]), buff=0.28)
        labels.scale_to_fit_width(7.4)
        labels.move_to(np.array([1.8, 0.10, 0.0]))

        self.play(FadeIn(title), FadeIn(sign_grid))
        for item in labels:
            self.play(FadeIn(item))
        self.wait(1.8)
        self.clear_stage((banner,))

    def show_identity_card(self, banner: Text) -> None:
        title = self.stage_title("Why A adj(A) becomes det(A) I")
        identity = MathTex(identity_tex(), font_size=44, color=GREEN)
        identity.move_to(np.array([0.0, 0.95, 0.0]))

        middle = VGroup(
            MathTex(diagonal_entry_tex(), font_size=28, color=WHITE),
            MathTex(off_diagonal_entry_tex(), font_size=26, color=BLUE),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.38)
        middle.scale_to_fit_width(10.7)
        middle.move_to(np.array([0.0, -0.15, 0.0]))

        emphasis = VGroup(
            Text("Diagonal entries: each is a cofactor expansion of det(A).", font_size=23, color=GREY_B),
            Text("Off-diagonal entries: the corresponding determinant has two equal rows.", font_size=22, color=GREY_B),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.24)
        emphasis.scale_to_fit_width(11.0)
        emphasis.move_to(np.array([0.0, -1.95, 0.0]))

        self.play(FadeIn(title))
        self.play(Write(identity))
        self.play(FadeIn(middle[0]))
        self.play(FadeIn(middle[1]))
        self.play(FadeIn(emphasis[0]), FadeIn(emphasis[1]))
        self.wait(2.0)
        self.clear_stage((banner,))

    def show_inverse_formula(self, banner: Text) -> None:
        title = self.stage_title("When det(A) is nonzero, divide both sides")
        start = MathTex(identity_tex(), font_size=40, color=WHITE)
        start.move_to(np.array([0.0, 0.90, 0.0]))
        arrow = MathTex(r"\det(A)\neq0", font_size=32, color=BLUE)
        arrow.move_to(np.array([0.0, 0.00, 0.0]))
        formula = MathTex(inverse_formula_tex(), font_size=40, color=GREEN)
        formula.scale_to_fit_width(10.2)
        formula.move_to(np.array([0.0, -1.00, 0.0]))
        cue = Text("So the adjugate is 'almost' the inverse: divide by det(A).", font_size=23, color=GREY_B)
        cue.scale_to_fit_width(10.7)
        cue.move_to(np.array([0.0, -2.30, 0.0]))

        self.play(FadeIn(title))
        self.play(Write(start))
        self.play(FadeIn(arrow))
        self.play(Write(formula))
        self.play(FadeIn(cue))
        self.wait(1.8)
        self.clear_stage((banner,))

    def show_two_by_two_example(self, banner: Text) -> None:
        title = self.stage_title("A 2 x 2 example recovers the familiar inverse formula", size=28)
        title.move_to(np.array([0.0, 2.32, 0.0]))

        A = Matrix([[str(x) for x in row] for row in example_matrix()], element_to_mobject_config={"font_size": 28}, h_buff=0.72, v_buff=0.55)
        C = Matrix([[str(x) for x in row] for row in example_cofactor_matrix()], element_to_mobject_config={"font_size": 28}, h_buff=0.72, v_buff=0.55)
        Adj = Matrix([[str(x) for x in row] for row in example_adjugate()], element_to_mobject_config={"font_size": 28}, h_buff=0.72, v_buff=0.55)
        trio = VGroup(
            VGroup(Text("A", font_size=23, color=WHITE), A).arrange(np.array([0.0, -1.0, 0.0]), buff=0.16),
            VGroup(Text("cofactor matrix", font_size=20, color=BLUE), C).arrange(np.array([0.0, -1.0, 0.0]), buff=0.16),
            VGroup(Text("adj(A)", font_size=23, color=GREEN), Adj).arrange(np.array([0.0, -1.0, 0.0]), buff=0.16),
        ).arrange(np.array([1.0, 0.0, 0.0]), buff=0.62)
        trio.scale_to_fit_width(8.8)
        trio.move_to(np.array([0.0, 1.00, 0.0]))

        formula = MathTex(example_inverse_formula_tex(), font_size=27, color=GREEN)
        formula.scale_to_fit_width(9.4)
        formula.move_to(np.array([0.0, -0.95, 0.0]))
        product = MathTex(example_product_tex(), font_size=25, color=WHITE)
        product.scale_to_fit_width(5.9)
        product.move_to(np.array([0.0, -2.15, 0.0]))

        self.play(FadeIn(title))
        self.play(FadeIn(trio))
        self.play(Write(formula))
        self.play(Write(product))
        self.wait(2.0)
        self.clear_stage((banner,))

    def show_cramers_connection(self, banner: Text) -> None:
        title = self.stage_title("This also explains Cramer's Rule")
        lines = cramer_connection_tex()
        display = VGroup(
            MathTex(lines[0], font_size=40, color=WHITE),
            MathTex(lines[1], font_size=38, color=GREEN),
            MathTex(lines[2], font_size=28, color=BLUE),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.42)
        display.scale_to_fit_width(10.8)
        display.move_to(np.array([0.0, -0.25, 0.0]))

        self.play(FadeIn(title))
        for line in display:
            self.play(Write(line) if isinstance(line, MathTex) else FadeIn(line))
        self.wait(1.9)
        self.clear_stage((banner,))

    def show_summary(self, banner: Text) -> None:
        title = self.stage_title("The big takeaway")
        title.move_to(np.array([0.0, 2.38, 0.0]))
        lines = closing_lines()
        summary = VGroup(
            Text(lines[0], font_size=27, color=WHITE),
            MathTex(identity_tex(), font_size=38, color=BLUE),
            MathTex(inverse_formula_tex(), font_size=38, color=GREEN),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.42)
        summary.scale_to_fit_width(10.9)
        summary.move_to(np.array([0.0, 0.10, 0.0]))
        foot = Text(lines[2], font_size=22, color=GREY_B)
        foot.scale_to_fit_width(10.8)
        foot.move_to(np.array([0.0, -2.20, 0.0]))

        self.play(FadeIn(title))
        for line in summary:
            self.play(FadeIn(line) if isinstance(line, Text) else Write(line))
        self.play(FadeIn(foot))
        self.wait(2.0)

    def clear_stage(self, preserve: tuple[object, ...]) -> None:
        self.play(*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve])
