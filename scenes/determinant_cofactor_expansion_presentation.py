"""CP137 presentation: derive cofactor expansion from the six-term determinant formula."""
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

from engine.determinant_cofactor_expansion import (
    bridge_lines,
    checkerboard_signs,
    cofactor_definition_tex,
    first_row_cofactor_tex,
    general_column_expansion_tex,
    general_row_expansion_tex,
    grouped_by_first_row_tex,
    minor_definition_tex,
    row_one_expansion_tex,
    sign_origin_tex,
    row_one_minor_determinants_tex,
    six_term_formula_lines,
)


class DeterminantCofactorExpansionPresentation(Scene):
    """Show that cofactor expansion is the six-term determinant formula reorganized."""

    def construct(self) -> None:
        banner = Text("Methods of Computation", font_size=38)
        banner.to_edge(np.array([0.0, 1.0, 0.0]), buff=0.24)
        subtitle = Text("Cofactor Expansion", font_size=28, color=GREY_B)
        subtitle.next_to(banner, np.array([0.0, -1.0, 0.0]), buff=0.12)
        self.play(Write(banner), FadeIn(subtitle))
        self.wait(0.8)
        self.play(FadeOut(subtitle))

        self.show_cp136_bridge(banner)
        self.show_grouping(banner)
        self.show_minor_determinants(banner)
        self.show_minors_and_cofactors(banner)
        self.show_general_expansion(banner)

    def show_cp136_bridge(self, banner: Text) -> None:
        title = Text("Start with the six-term determinant formula", font_size=29, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))

        line1_tex, line2_tex = six_term_formula_lines()
        line1 = MathTex(line1_tex, font_size=35, color=GREEN)
        line2 = MathTex(line2_tex, font_size=35, color=RED)
        max_width = max(line1.width, line2.width)
        if max_width > 11.2:
            scale_factor = 11.2 / max_width
            line1.scale(scale_factor)
            line2.scale(scale_factor)
        formulas = VGroup(line1, line2).arrange(np.array([0.0, -1.0, 0.0]), buff=0.22)
        formulas.move_to(np.array([0.0, 0.65, 0.0]))

        lines = bridge_lines()
        explanation = VGroup(
            Text(lines[0], font_size=23, color=WHITE),
            Text(lines[1], font_size=23, color=WHITE),
            Text(lines[2], font_size=23, color=BLUE),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.23)
        explanation.move_to(np.array([0.0, -1.75, 0.0]))

        self.play(FadeIn(title))
        self.play(Write(line1), Write(line2))
        for line in explanation:
            self.play(FadeIn(line))
        self.wait(1.5)
        self.clear_stage((banner,))

    def show_grouping(self, banner: Text) -> None:
        title = Text("Group by the entries in the first row", font_size=30, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))

        matrix = self.symbolic_matrix(font_size=27)
        matrix.move_to(np.array([0.0, 0.95, 0.0]))
        first_row = VGroup(*matrix.get_rows()[0])
        first_row.set_color(BLUE)

        grouped = MathTex(grouped_by_first_row_tex(), font_size=32, color=WHITE)
        grouped.scale_to_fit_width(12.0)
        grouped.move_to(np.array([0.0, -1.0, 0.0]))

        cue = Text(
            "The alternating + - + pattern is already present in the six-term formula.",
            font_size=22,
            color=GREY_B,
        )
        cue.scale_to_fit_width(11.5)
        cue.move_to(np.array([0.0, -2.65, 0.0]))

        self.play(FadeIn(title), FadeIn(matrix))
        self.play(FadeIn(first_row))
        self.play(Write(grouped))
        self.play(FadeIn(cue))
        self.wait(1.6)
        self.clear_stage((banner,))

    def show_minor_determinants(self, banner: Text) -> None:
        title = Text("Each parenthesis is a 2x2 determinant", font_size=30, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))

        expansion = MathTex(row_one_expansion_tex(), font_size=31, color=BLUE)
        expansion.scale_to_fit_width(12.0)
        expansion.move_to(np.array([0.0, 0.95, 0.0]))

        m11, m12, m13 = row_one_minor_determinants_tex()
        cards = VGroup(
            self.minor_card(r"a_{11}", r"M_{11}", m11, GREEN),
            self.minor_card(r"a_{12}", r"M_{12}", m12, RED),
            self.minor_card(r"a_{13}", r"M_{13}", m13, GREEN),
        ).arrange(np.array([1.0, 0.0, 0.0]), buff=0.75)
        cards.move_to(np.array([0.0, -1.25, 0.0]))

        instruction = Text(
            "For a first-row entry: delete row 1 and that entry's column.",
            font_size=23,
            color=GREY_B,
        )
        instruction.move_to(np.array([0.0, -2.95, 0.0]))

        self.play(FadeIn(title))
        self.play(Write(expansion))
        for card in cards:
            self.play(FadeIn(card))
        self.play(FadeIn(instruction))
        self.wait(1.7)
        self.clear_stage((banner,))

    def show_minors_and_cofactors(self, banner: Text) -> None:
        title = Text("Minors become cofactors when we attach the sign", font_size=29, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))

        signs = Matrix(
            checkerboard_signs(),
            element_to_mobject_config={"font_size": 34},
            h_buff=0.75,
            v_buff=0.55,
        )
        signs.move_to(np.array([-4.5, 0.15, 0.0]))
        sign_label = Text("checkerboard signs", font_size=22, color=GREY_B)
        sign_label.next_to(signs, np.array([0.0, -1.0, 0.0]), buff=0.25)

        definitions = VGroup(
            MathTex(minor_definition_tex(), font_size=30, color=WHITE),
            MathTex(cofactor_definition_tex(), font_size=36, color=BLUE),
            MathTex(sign_origin_tex(), font_size=29, color=GREY_B),
            MathTex(r"\text{These signs are inherited from the permutation signs.}", font_size=27, color=GREY_B),
            MathTex(r"C_{11}=+M_{11},\quad C_{12}=-M_{12},\quad C_{13}=+M_{13}", font_size=31, color=WHITE),
        ).arrange(np.array([0.0, -1.0, 0.0]), aligned_edge=np.array([-1.0, 0.0, 0.0]), buff=0.24)
        definitions.move_to(np.array([2.1, 0.02, 0.0]))
        definitions.scale_to_fit_width(7.2)

        self.play(FadeIn(title))
        self.play(FadeIn(signs), FadeIn(sign_label))
        for definition in definitions:
            self.play(Write(definition))
        self.wait(1.7)
        self.clear_stage((banner,))

    def show_general_expansion(self, banner: Text) -> None:
        title = Text("Cofactor expansion", font_size=31, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))

        row_one = MathTex(first_row_cofactor_tex(), font_size=36, color=BLUE)
        row_one.move_to(np.array([0.0, 1.15, 0.0]))

        row_general = MathTex(general_row_expansion_tex(), font_size=35, color=GREEN)
        col_general = MathTex(general_column_expansion_tex(), font_size=35, color=GREEN)
        general = VGroup(row_general, col_general).arrange(np.array([0.0, -1.0, 0.0]), buff=0.42)
        general.move_to(np.array([0.0, -0.45, 0.0]))

        labels = VGroup(
            Text("expand along row i", font_size=21, color=GREY_B),
            Text("expand along column j", font_size=21, color=GREY_B),
        )
        labels[0].next_to(row_general, np.array([0.0, -1.0, 0.0]), buff=0.10)
        labels[1].next_to(col_general, np.array([0.0, -1.0, 0.0]), buff=0.10)

        insight = Text(
            "Cofactor expansion is the Big Formula reorganized - and it works along any row or column.",
            font_size=23,
            color=WHITE,
        )
        insight.scale_to_fit_width(11.6)
        insight.move_to(np.array([0.0, -2.75, 0.0]))

        self.play(FadeIn(title))
        self.play(Write(row_one))
        self.play(Write(row_general), FadeIn(labels[0]))
        self.play(Write(col_general), FadeIn(labels[1]))
        self.play(FadeIn(insight))
        self.wait(2.0)

    @staticmethod
    def symbolic_matrix(font_size: int) -> Matrix:
        return Matrix(
            [
                [r"a_{11}", r"a_{12}", r"a_{13}"],
                [r"a_{21}", r"a_{22}", r"a_{23}"],
                [r"a_{31}", r"a_{32}", r"a_{33}"],
            ],
            element_to_mobject_config={"font_size": font_size},
            h_buff=0.8,
            v_buff=0.6,
        )

    @staticmethod
    def minor_card(entry_tex: str, minor_name_tex: str, minor_tex: str, color) -> VGroup:
        entry = MathTex(entry_tex, font_size=31, color=color)
        arrow = MathTex(r"\longrightarrow", font_size=27, color=GREY_B)
        minor = MathTex(minor_name_tex + "=" + minor_tex, font_size=27, color=color)
        return VGroup(entry, arrow, minor).arrange(np.array([0.0, -1.0, 0.0]), buff=0.18)

    def clear_stage(self, preserve: tuple[object, ...]) -> None:
        self.play(*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve])
