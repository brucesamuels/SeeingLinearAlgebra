"""CP141 presentation: derive and apply Cramer's Rule."""
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

from engine.determinant_cramers_rule import (
    closing_lines,
    column_equation_tex,
    derivation_lines_tex,
    determinant_a,
    example_ratios_tex,
    example_system_tex,
    replacement_definition_tex,
    replacement_determinants,
    replacement_matrices,
    solution_vector,
    theorem_condition_tex,
    theorem_tex,
)


class DeterminantCramersRulePresentation(Scene):
    """Derive Cramer's Rule from column linearity and apply it numerically."""

    TITLE_Y = 2.05

    def construct(self) -> None:
        banner = Text("Solving with Determinants", font_size=38)
        banner.to_edge(np.array([0.0, 1.0, 0.0]), buff=0.24)
        subtitle = Text("Cramer's Rule", font_size=28, color=GREY_B)
        subtitle.next_to(banner, np.array([0.0, -1.0, 0.0]), buff=0.12)
        self.play(Write(banner), FadeIn(subtitle))
        self.wait(0.8)
        self.play(FadeOut(subtitle))

        self.show_column_view(banner)
        self.show_derivation(banner)
        self.show_theorem(banner)
        self.show_example_setup(banner)
        self.show_replacement_determinants(banner)
        self.show_solution(banner)

    def stage_title(self, text: str, *, size: int = 29) -> Text:
        title = Text(text, font_size=size, color=YELLOW)
        title.move_to(np.array([0.0, self.TITLE_Y, 0.0]))
        return title

    def show_column_view(self, banner: Text) -> None:
        title = self.stage_title("Begin with Ax = b, written by columns")
        matrix_form = MathTex(r"A\mathbf x=\mathbf b", font_size=40, color=BLUE)
        matrix_form.move_to(np.array([0.0, 0.85, 0.0]))

        column_form = MathTex(column_equation_tex(), font_size=34, color=WHITE)
        column_form.scale_to_fit_width(10.8)
        column_form.move_to(np.array([0.0, -0.45, 0.0]))

        self.play(FadeIn(title))
        self.play(Write(matrix_form))
        self.play(Write(column_form))
        self.wait(1.0)
        self.play(FadeOut(matrix_form), FadeOut(column_form))

        cue = Text("Replace one column of A by b.", font_size=27, color=GREEN)
        cue.move_to(np.array([0.0, 0.55, 0.0]))
        replaced = MathTex(replacement_definition_tex(), font_size=30, color=GREEN)
        replaced.scale_to_fit_width(10.6)
        replaced.move_to(np.array([0.0, -0.75, 0.0]))
        self.play(FadeIn(cue))
        self.play(Write(replaced))
        self.wait(1.5)
        self.clear_stage((banner,))

    def show_derivation(self, banner: Text) -> None:
        title = self.stage_title("Why the replacement isolates x_k")
        title.move_to(np.array([0.0, 1.80, 0.0]))
        lines = derivation_lines_tex()
        self.play(FadeIn(title))

        first = MathTex(lines[0], font_size=28, color=WHITE)
        first.scale_to_fit_width(10.2)
        second = MathTex(lines[1], font_size=27, color=BLUE)
        second.scale_to_fit_width(10.2)
        key = MathTex(lines[2], font_size=28, color=GREEN)
        key.scale(first.height / key.height)

        equations = VGroup(first, second, key).arrange(np.array([0.0, -1.0, 0.0]), buff=0.30)
        equations.move_to(np.array([0.0, 0.35, 0.0]))
        equations.scale_to_fit_height(2.25)

        explanation = VGroup(
            Text("Use linearity in the replaced column.", font_size=23, color=GREY_B),
            MathTex(r"\text{Only the }x_k\text{ term keeps distinct columns.}", font_size=24, color=WHITE),
            Text("All other terms repeat a column, so their determinants are zero.", font_size=22, color=GREY_B),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.20)
        explanation.scale_to_fit_width(10.2)
        explanation.move_to(np.array([0.0, -2.05, 0.0]))

        self.play(Write(first))
        self.play(Write(second))
        self.play(Write(key))
        for line in explanation:
            self.play(FadeIn(line))
        self.wait(1.6)
        self.clear_stage((banner,))

    def show_theorem(self, banner: Text) -> None:
        title = self.stage_title("Cramer's Rule", size=31)
        condition = MathTex(theorem_condition_tex(), font_size=38, color=GREEN)
        condition.move_to(np.array([0.0, 0.75, 0.0]))
        statement = MathTex(theorem_tex(), font_size=40, color=BLUE)
        statement.scale_to_fit_width(10.2)
        statement.move_to(np.array([0.0, -0.55, 0.0]))

        self.play(FadeIn(title))
        self.play(Write(condition))
        self.play(Write(statement))
        self.wait(1.2)
        self.play(FadeOut(condition), FadeOut(statement))

        definition = MathTex(
            r"A_k\text{ is obtained from }A\text{ by replacing column }k\text{ with }\mathbf b.",
            font_size=31,
            color=WHITE,
        )
        definition.scale_to_fit_width(9.8)
        definition.move_to(np.array([0.0, 0.25, 0.0]))
        interpretation = Text(
            "Each component of the solution is a ratio of determinants.",
            font_size=24,
            color=GREY_B,
        )
        interpretation.scale_to_fit_width(9.8)
        interpretation.move_to(np.array([0.0, -1.05, 0.0]))
        self.play(FadeIn(definition))
        self.play(FadeIn(interpretation))
        self.wait(1.5)
        self.clear_stage((banner,))

    def show_example_setup(self, banner: Text) -> None:
        title = self.stage_title("A 3 x 3 example", size=31)
        title.move_to(np.array([0.0, 1.92, 0.0]))
        system = MathTex(example_system_tex(), font_size=30, color=WHITE)
        system.scale_to_fit_width(7.9)
        system.move_to(np.array([0.0, -0.05, 0.0]))
        det_line = MathTex(rf"\det(A)={determinant_a()}\neq0", font_size=37, color=GREEN)
        det_line.move_to(np.array([0.0, -1.78, 0.0]))
        cue = Text(
            "The system has a unique solution, so Cramer's Rule applies.",
            font_size=23,
            color=GREY_B,
        )
        cue.scale_to_fit_width(9.8)
        cue.move_to(np.array([0.0, -2.55, 0.0]))

        self.play(FadeIn(title))
        self.play(Write(system))
        self.play(Write(det_line))
        self.play(FadeIn(cue))
        self.wait(1.6)
        self.clear_stage((banner,))

    def show_replacement_determinants(self, banner: Text) -> None:
        title = self.stage_title("Replace one column at a time", size=30)
        mats = replacement_matrices()
        dets = replacement_determinants()
        cards = VGroup()
        for idx, (mat, det) in enumerate(zip(mats, dets), start=1):
            matrix = Matrix(
                [[str(x) for x in row] for row in mat],
                element_to_mobject_config={"font_size": 25},
                h_buff=0.62,
                v_buff=0.48,
            )
            label = MathTex(rf"A_{idx}", font_size=28, color=BLUE)
            value = MathTex(rf"\det(A_{idx})={det}", font_size=29, color=GREEN if det >= 0 else RED)
            card = VGroup(label, matrix, value).arrange(np.array([0.0, -1.0, 0.0]), buff=0.18)
            cards.add(card)

        cards.arrange(np.array([1.0, 0.0, 0.0]), buff=0.65)
        cards.scale_to_fit_width(10.9)
        cards.move_to(np.array([0.0, -0.35, 0.0]))

        self.play(FadeIn(title))
        for card in cards:
            self.play(FadeIn(card))
        self.wait(1.8)
        self.clear_stage((banner,))

    def show_solution(self, banner: Text) -> None:
        title = self.stage_title("Divide by det(A)", size=30)
        ratios = example_ratios_tex()
        self.play(FadeIn(title))

        work = VGroup(
            *[MathTex(tex, font_size=29, color=color) for tex, color in zip(ratios, (GREEN, RED, GREEN))]
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.34)
        work.move_to(np.array([0.0, 0.15, 0.0]))
        work.scale_to_fit_height(2.75)
        for line in work:
            self.play(Write(line))
        self.wait(1.0)
        self.play(FadeOut(work))

        sol = solution_vector()
        answer = MathTex(
            rf"\mathbf x=\begin{{bmatrix}}{sol[0]}\\{sol[1]}\\{sol[2]}\end{{bmatrix}}",
            font_size=42,
            color=BLUE,
        )
        answer.move_to(np.array([0.0, 0.35, 0.0]))
        self.play(Write(answer))
        self.wait(1.0)
        self.play(FadeOut(answer))

        lines = closing_lines()
        footer = VGroup(
            Text(lines[0], font_size=22, color=WHITE),
            Text(lines[1], font_size=21, color=GREY_B),
            Text(lines[2], font_size=21, color=GREY_B),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.26)
        footer.scale_to_fit_width(10.2)
        footer.move_to(np.array([0.0, -0.35, 0.0]))
        for line in footer:
            self.play(FadeIn(line))
        self.wait(1.8)

    def clear_stage(self, preserve: tuple[object, ...]) -> None:
        self.play(*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve])
