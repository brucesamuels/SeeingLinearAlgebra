"""CP143 presentation: determinants of products."""
from __future__ import annotations

import numpy as np
from manim import BLUE, FadeIn, FadeOut, GREEN, GREY_B, MathTex, Scene, Text, VGroup, WHITE, YELLOW, Write

from engine.determinant_product_rule import (
    closing_lines,
    elementary_cases,
    elementary_conclusion_tex,
    factorization_tex,
    invertible_chain_tex,
    inverse_consequence_tex,
    many_factors_tex,
    power_consequence_tex,
    product_factorization_tex,
    singular_case_tex,
    theorem_tex,
)


class DeterminantProductRulePresentation(Scene):
    """Prove det(AB)=det(A)det(B) from elementary row operations."""

    def construct(self) -> None:
        banner = Text("Determinants of Products", font_size=38)
        banner.to_edge(np.array([0.0, 1.0, 0.0]), buff=0.24)
        subtitle = MathTex(r"\det(AB)=\det(A)\det(B)", font_size=31, color=GREY_B)
        subtitle.next_to(banner, np.array([0.0, -1.0, 0.0]), buff=0.12)
        self.play(Write(banner), FadeIn(subtitle))
        self.wait(0.8)
        self.play(FadeOut(subtitle))

        self.show_theorem(banner)
        self.show_elementary_cases(banner)
        self.show_invertible_setup(banner)
        self.show_invertible_peel_off(banner)
        self.show_invertible_recognition(banner)
        self.show_singular_case(banner)
        self.show_consequences(banner)
        self.show_takeaway(banner)

    def stage_title(self, text: str, size: int = 30) -> Text:
        title = Text(text, font_size=size, color=YELLOW)
        title.move_to(np.array([0.0, 2.00, 0.0]))
        return title

    def clear_stage(self, preserve: tuple[object, ...]) -> None:
        self.play(*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve])

    def show_theorem(self, banner: Text) -> None:
        title = self.stage_title("What is det(AB)?")
        question = MathTex(r"\det(AB)\overset{?}{=}\det(A)\det(B)", font_size=48, color=WHITE)
        question.move_to(np.array([0.0, 0.45, 0.0]))
        note = VGroup(
            Text("We will not compute AB first.", font_size=27, color=BLUE),
            Text("We will prove why the determinant factors multiply.", font_size=25, color=GREY_B),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.28)
        note.move_to(np.array([0.0, -1.35, 0.0]))
        self.play(FadeIn(title), Write(question))
        self.play(FadeIn(note))
        self.wait(1.7)
        self.clear_stage((banner,))

    def show_elementary_cases(self, banner: Text) -> None:
        title = self.stage_title("First let the left factor E be elementary", size=28)
        intro = MathTex(r"B\ \xrightarrow{\text{one row operation}}\ EB", font_size=34, color=WHITE)
        intro.move_to(np.array([0.0, 1.18, 0.0]))
        self.play(FadeIn(title), Write(intro))

        rows = VGroup()
        for operation, det_e, det_eb in elementary_cases():
            row = VGroup(
                MathTex(operation, font_size=24, color=WHITE),
                MathTex(det_e, font_size=24, color=BLUE),
                MathTex(det_eb, font_size=24, color=GREEN),
            ).arrange(np.array([1.0, 0.0, 0.0]), buff=0.50)
            rows.add(row)
        rows.arrange(np.array([0.0, -1.0, 0.0]), buff=0.28, aligned_edge=np.array([-1.0, 0.0, 0.0]))
        rows.scale_to_fit_width(10.3)
        rows.move_to(np.array([0.0, -0.55, 0.0]))
        for row in rows:
            self.play(FadeIn(row))

        conclusion = MathTex(elementary_conclusion_tex(), font_size=34, color=YELLOW)
        conclusion.move_to(np.array([0.0, -2.28, 0.0]))
        self.play(Write(conclusion))
        self.wait(2.0)
        self.clear_stage((banner,))

    def show_invertible_setup(self, banner: Text) -> None:
        title = self.stage_title("Now suppose A is invertible", size=26)
        title.move_to(np.array([0.0, 2.32, 0.0]))
        factorization = MathTex(factorization_tex(), font_size=34, color=WHITE)
        product_line = MathTex(product_factorization_tex(), font_size=34, color=BLUE)
        formulas = VGroup(factorization, product_line).arrange(np.array([0.0, -1.0, 0.0]), buff=0.34)
        formulas.scale_to_fit_width(10.4)
        formulas.move_to(np.array([0.0, 0.75, 0.0]))

        note = VGroup(
            Text("Each E_i is one elementary row operation.", font_size=23, color=WHITE),
            Text("So we can apply det(EX)=det(E)det(X) one step at a time.", font_size=21, color=GREY_B),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.22)
        note.move_to(np.array([0.0, -1.35, 0.0]))

        self.play(FadeIn(title))
        self.play(Write(factorization))
        self.play(Write(product_line))
        self.play(FadeIn(note))
        self.wait(1.8)
        self.clear_stage((banner,))

    def show_invertible_peel_off(self, banner: Text) -> None:
        title = self.stage_title("Peel off the elementary matrices", size=26)
        lines = VGroup(
            MathTex(r"\det(AB)=\det(E_mE_{m-1}\cdots E_1B)", font_size=29, color=WHITE),
            MathTex(r"=\det(E_m)\det(E_{m-1}\cdots E_1B)", font_size=29, color=BLUE),
            MathTex(r"=\det(E_m)\det(E_{m-1})\cdots\det(E_1)\det(B)", font_size=27, color=GREEN),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.34)
        lines.scale_to_fit_width(10.6)
        lines.move_to(np.array([0.0, -0.10, 0.0]))

        self.play(FadeIn(title))
        for line in lines:
            self.play(Write(line))
        self.wait(1.8)
        self.clear_stage((banner,))

    def show_invertible_recognition(self, banner: Text) -> None:
        title = self.stage_title("Recognize the product as det(A)", size=26)
        lines = invertible_chain_tex()
        body = VGroup(
            MathTex(lines[1], font_size=29, color=WHITE),
            MathTex(r"\det(AB)=\bigl(\det(E_m)\cdots\det(E_1)\bigr)\det(B)", font_size=27, color=BLUE),
            MathTex(lines[2], font_size=38, color=GREEN),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.34)
        body.scale_to_fit_width(10.4)
        body.move_to(np.array([0.0, -0.15, 0.0]))

        self.play(FadeIn(title))
        for line in body:
            self.play(Write(line))
        self.wait(2.0)
        self.clear_stage((banner,))

    def show_singular_case(self, banner: Text) -> None:
        title = self.stage_title("What if A is singular?", size=26)
        lines = singular_case_tex()
        body = VGroup(
            MathTex(lines[0], font_size=27, color=WHITE),
            MathTex(lines[1], font_size=27, color=BLUE),
            MathTex(lines[2], font_size=27, color=WHITE),
            MathTex(lines[3], font_size=31, color=GREEN),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.28)
        body.scale_to_fit_width(9.9)
        body.move_to(np.array([0.0, -0.45, 0.0]))
        self.play(FadeIn(title))
        for line in body:
            self.play(Write(line))
        self.wait(1.9)
        self.clear_stage((banner,))

    def show_consequences(self, banner: Text) -> None:
        title = self.stage_title("Consequences of multiplicativity", size=26)
        inv = inverse_consequence_tex()
        inverse_block = VGroup(
            Text("Inverse", font_size=22, color=YELLOW),
            MathTex(inv[0], font_size=25, color=WHITE),
            MathTex(inv[1], font_size=25, color=BLUE),
            MathTex(inv[2], font_size=29, color=GREEN),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.16)
        inverse_block.move_to(np.array([0.0, 0.88, 0.0]))

        powers_block = VGroup(
            Text("Powers", font_size=22, color=YELLOW),
            MathTex(power_consequence_tex(), font_size=28, color=GREEN),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.18)
        powers_block.move_to(np.array([0.0, -0.42, 0.0]))

        many_block = VGroup(
            Text("Many factors", font_size=22, color=YELLOW),
            MathTex(many_factors_tex(), font_size=22, color=WHITE),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.18)
        many_block.scale_to_fit_width(10.0)
        many_block.move_to(np.array([0.0, -1.95, 0.0]))

        self.play(FadeIn(title))
        self.play(FadeIn(inverse_block))
        self.play(FadeIn(powers_block))
        self.play(FadeIn(many_block))
        self.wait(2.0)
        self.clear_stage((banner,))

    def show_takeaway(self, banner: Text) -> None:
        title = self.stage_title("The big takeaway", size=28)
        theorem = MathTex(theorem_tex(), font_size=42, color=GREEN)
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
