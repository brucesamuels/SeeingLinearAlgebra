"""CP144 presentation: determinant of a transpose."""
from __future__ import annotations

import numpy as np
from manim import BLUE, FadeIn, FadeOut, GREEN, GREY_B, MathTex, Scene, Text, VGroup, WHITE, YELLOW, Write

from engine.determinant_transpose_rule import (
    big_formula_tex,
    closing_lines,
    conclusion_tex,
    product_rewrite_tex,
    reindex_sum_tex,
    sign_invariance_tex,
    theorem_tex,
    transpose_formula_tex,
)


class DeterminantTransposeRulePresentation(Scene):
    """Prove det(A^T)=det(A) from the permutation formula."""

    def construct(self) -> None:
        banner = Text("Determinant of a Transpose", font_size=38)
        banner.to_edge(np.array([0.0, 1.0, 0.0]), buff=0.24)
        subtitle = MathTex(r"\det(A^T)=\det(A)", font_size=31, color=GREY_B)
        subtitle.next_to(banner, np.array([0.0, -1.0, 0.0]), buff=0.12)
        self.play(Write(banner), FadeIn(subtitle))
        self.wait(0.8)
        self.play(FadeOut(subtitle))

        self.show_theorem(banner)
        self.show_big_formula(banner)
        self.show_apply_to_transpose(banner)
        self.show_rewrite_product(banner)
        self.show_reindex_sum(banner)
        self.show_sign_invariance(banner)
        self.show_conclude(banner)
        self.show_takeaway(banner)

    def stage_title(self, text: str, size: int = 30) -> Text:
        title = Text(text, font_size=size, color=YELLOW)
        title.move_to(np.array([0.0, 2.16, 0.0]))
        return title

    def clear_stage(self, preserve: tuple[object, ...]) -> None:
        self.play(*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve])

    def show_theorem(self, banner: Text) -> None:
        title = self.stage_title("What happens when we transpose?")
        theorem = MathTex(theorem_tex(), font_size=42, color=GREEN)
        theorem.move_to(np.array([0.0, 0.55, 0.0]))
        note = VGroup(
            Text("Transpose swaps rows and columns.", font_size=25, color=WHITE),
            Text("We will prove that the determinant does not change.", font_size=23, color=BLUE),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.24)
        note.move_to(np.array([0.0, -2.10, 0.0]))
        self.play(FadeIn(title), Write(theorem))
        self.play(FadeIn(note))
        self.wait(1.7)
        self.clear_stage((banner,))

    def show_big_formula(self, banner: Text) -> None:
        title = self.stage_title("Start from the Big Formula")
        formula = MathTex(big_formula_tex(), font_size=29, color=WHITE)
        formula.scale_to_fit_width(11.0)
        formula.move_to(np.array([0.0, 0.55, 0.0]))
        note = VGroup(
            Text("This is the permutation formula for det(A).", font_size=23, color=WHITE),
            Text("Now apply the same formula to A^T.", font_size=23, color=GREY_B),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.22)
        note.move_to(np.array([0.0, -1.25, 0.0]))
        self.play(FadeIn(title), Write(formula))
        self.play(FadeIn(note))
        self.wait(1.8)
        self.clear_stage((banner,))

    def show_apply_to_transpose(self, banner: Text) -> None:
        title = MathTex(r"\text{Apply the formula to }A^T", font_size=27, color=YELLOW)
        title.move_to(np.array([0.0, 2.38, 0.0]))
        lines = transpose_formula_tex()
        body = VGroup(
            MathTex(lines[0], font_size=20, color=WHITE),
            MathTex(lines[1], font_size=20, color=BLUE),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.40)
        body.scale_to_fit_width(9.5)
        body.move_to(np.array([0.0, -0.18, 0.0]))
        note = MathTex(
            r"\text{Because }(A^T)_{i,\sigma(i)}=a_{\sigma(i),i}.",
            font_size=22,
            color=GREY_B,
        )
        note.move_to(np.array([0.0, -2.55, 0.0]))
        self.play(FadeIn(title))
        for line in body:
            self.play(Write(line))
        self.play(FadeIn(note))
        self.wait(1.8)
        self.clear_stage((banner,))

    def show_rewrite_product(self, banner: Text) -> None:
        title = self.stage_title("Rewrite the product", size=23)
        lines = product_rewrite_tex()
        formula = MathTex(lines[0], font_size=22, color=GREEN)
        formula.scale_to_fit_width(9.6)
        formula.move_to(np.array([0.0, 0.15, 0.0]))
        note = VGroup(
            MathTex(lines[1], font_size=21, color=WHITE),
            Text("It is the same set of factors, just in a new order.", font_size=19, color=GREY_B),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.26)
        note.move_to(np.array([0.0, -2.10, 0.0]))
        self.play(FadeIn(title), Write(formula))
        self.play(FadeIn(note))
        self.wait(1.8)
        self.clear_stage((banner,))

    def show_reindex_sum(self, banner: Text) -> None:
        title = self.stage_title("Reindex the sum", size=22)
        title.move_to(np.array([0.0, 2.52, 0.0]))
        lines = reindex_sum_tex()
        body = VGroup(
            MathTex(lines[0], font_size=17, color=WHITE),
            MathTex(lines[1], font_size=21, color=YELLOW),
            MathTex(lines[2], font_size=18, color=BLUE),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.34)
        body.scale_to_fit_width(9.4)
        body.move_to(np.array([0.0, -0.62, 0.0]))
        self.play(FadeIn(title))
        for line in body:
            self.play(Write(line))
        self.wait(1.8)
        self.clear_stage((banner,))

    def show_sign_invariance(self, banner: Text) -> None:
        title = self.stage_title("Inverse permutations keep the same sign", size=22)
        title.move_to(np.array([0.0, 2.34, 0.0]))
        lines = sign_invariance_tex()
        formula = MathTex(lines[0], font_size=44, color=GREEN)
        formula.move_to(np.array([0.0, 0.62, 0.0]))
        note = VGroup(
            Text(lines[1], font_size=20, color=WHITE),
            Text("So the sign factor is unchanged after reindexing.", font_size=19, color=BLUE),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.22)
        note.move_to(np.array([0.0, -2.10, 0.0]))
        self.play(FadeIn(title), Write(formula))
        self.play(FadeIn(note))
        self.wait(1.7)
        self.clear_stage((banner,))

    def show_conclude(self, banner: Text) -> None:
        title = self.stage_title("Now recognize the Big Formula again", size=21)
        title.move_to(np.array([0.0, 2.66, 0.0]))
        lines = conclusion_tex()
        body = VGroup(
            MathTex(lines[0], font_size=17, color=WHITE),
            MathTex(lines[1], font_size=28, color=BLUE),
            MathTex(lines[2], font_size=36, color=GREEN),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.34)
        body.scale_to_fit_width(9.6)
        body.move_to(np.array([0.0, -0.72, 0.0]))
        self.play(FadeIn(title))
        for line in body:
            self.play(Write(line))
        self.wait(2.0)
        self.clear_stage((banner,))

    def show_takeaway(self, banner: Text) -> None:
        title = self.stage_title("The big takeaway", size=28)
        theorem = MathTex(theorem_tex(), font_size=48, color=GREEN)
        theorem.move_to(np.array([0.0, 0.95, 0.0]))
        lines = closing_lines()
        notes = VGroup(
            Text(lines[0], font_size=20, color=WHITE),
            Text(lines[1], font_size=20, color=BLUE),
            Text(lines[2], font_size=20, color=GREY_B),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.24)
        notes.scale_to_fit_width(10.8)
        notes.move_to(np.array([0.0, -1.00, 0.0]))
        self.play(FadeIn(title), Write(theorem))
        for line in notes:
            self.play(FadeIn(line))
        self.wait(2.0)
