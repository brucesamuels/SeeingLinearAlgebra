"""Manim presentation: The Matrix of a Transformation in Another Basis."""
from manim import (
    BLUE_C, GREEN_C, GREY_B, ORANGE, WHITE, YELLOW,
    DOWN, RIGHT, UP,
    Arrow, Create, FadeIn, FadeOut, Line, MathTex, Matrix, NumberPlane,
    ReplacementTransform, Scene, Text, Transform, VGroup, smooth,
)


class TransformationMatrixBasisPresentation(Scene):
    CHAPTER_BANNER = "CHANGE OF BASIS"
    LESSON_TITLE = "The Matrix of a Transformation in Another Basis"

    def _heading(self, text):
        item = Text(text, font_size=27, color=WHITE)
        if item.width > 11.6: item.scale_to_fit_width(11.6)
        return item

    def _chrome(self, heading_text):
        banner = Text(self.CHAPTER_BANNER, font_size=22, color=GREY_B, weight="BOLD").to_edge(UP, buff=0.16)
        title = Text(self.LESSON_TITLE, font_size=31, color=YELLOW, weight="BOLD").next_to(banner, DOWN, buff=0.12)
        heading = self._heading(heading_text).next_to(title, DOWN, buff=0.17)
        return banner, title, heading

    def _replace_heading(self, old, text):
        new = self._heading(text).move_to(old)
        self.play(ReplacementTransform(old, new), run_time=0.6)
        return new

    @staticmethod
    def _fit(group):
        if group.width > 11.2: group.scale_to_fit_width(11.2)
        if group.height > 4.65: group.scale_to_fit_height(4.65)
        group.move_to(DOWN * 0.42)
        return group

    @staticmethod
    def _matrix(entries, scale=0.82):
        return Matrix(entries, v_buff=0.95, h_buff=1.0).scale(scale)

    @staticmethod
    def _basis_grid(plane, first, second, first_color, second_color):
        """Build matching grid lines from two geometric basis vectors."""
        import numpy as np
        first, second = np.asarray(first), np.asarray(second)
        lines = VGroup()
        for fixed_first in range(-2, 8):
            start, end = fixed_first * first - 4 * second, fixed_first * first + 4 * second
            lines.add(Line(
                plane.c2p(*start), plane.c2p(*end), color=second_color,
                stroke_width=3.2 if fixed_first == 0 else 1.8,
                stroke_opacity=1.0 if fixed_first == 0 else 0.82,
            ))
        for fixed_second in range(-4, 5):
            start, end = -2 * first + fixed_second * second, 7 * first + fixed_second * second
            lines.add(Line(
                plane.c2p(*start), plane.c2p(*end), color=first_color,
                stroke_width=3.2 if fixed_second == 0 else 1.8,
                stroke_opacity=1.0 if fixed_second == 0 else 0.82,
            ))
        return lines

    def construct(self):
        banner, title, heading = self._chrome("Does a linear transformation have only one matrix?")
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))
        question = VGroup(
            Text("The transformation is fixed.", font_size=39, color=WHITE),
            Text("How does its matrix change when the coordinate language changes?", font_size=32, color=WHITE),
        ).arrange(DOWN, buff=0.20)
        contrast = MathTex(r"A\quad\longleftrightarrow\quad[A]_{\mathcal B}", font_size=72, color=YELLOW)
        note = Text("Same transformation; different coordinate descriptions.", font_size=32, color=ORANGE)
        opening = self._fit(VGroup(question, contrast, note).arrange(DOWN, buff=0.58))
        self.play(FadeIn(question)); self.play(FadeIn(contrast)); self.play(FadeIn(note)); self.wait(1.7)

        heading = self._replace_heading(heading, "The transformation genuinely moves the vector.")
        self.play(FadeOut(opening))
        plane = NumberPlane(
            x_range=[-1, 7, 1], y_range=[-2, 5, 1], x_length=7.0, y_length=5.8,
            background_line_style={"stroke_color": GREY_B, "stroke_width": 1.8, "stroke_opacity": 0.88},
            axis_config={"stroke_color": WHITE, "stroke_width": 3.0},
        ).shift(DOWN * 0.42)
        standard_grid = self._basis_grid(plane, [1, 0], [0, 1], WHITE, WHITE)
        basis_grid = self._basis_grid(plane, [1, 0], [1, 1], GREEN_C, BLUE_C)
        vector = Arrow(plane.c2p(0, 0), plane.c2p(3, 2), buff=0, color=ORANGE, stroke_width=9)
        transformed_vector = Arrow(plane.c2p(0, 0), plane.c2p(6, 2), buff=0, color=YELLOW, stroke_width=9)
        label_v = MathTex(r"\mathbf v=(3,2)", font_size=38, color=ORANGE).next_to(vector.get_end(), UP, buff=0.10)
        label_av = MathTex(r"A\mathbf v=(6,2)", font_size=38, color=YELLOW).next_to(transformed_vector.get_end(), UP, buff=0.10)
        action = MathTex(r"A:(x,y)\longmapsto(2x,y)", font_size=43, color=WHITE).to_edge(DOWN, buff=0.16)
        self.play(Create(standard_grid), FadeIn(vector), FadeIn(label_v), FadeIn(action)); self.wait(1.0)
        self.play(Transform(vector, transformed_vector), ReplacementTransform(label_v, label_av), run_time=2.2); self.wait(1.5)

        heading = self._replace_heading(heading, "Now describe the same geometric input and output on the B-grid.")
        input_vector = Arrow(plane.c2p(0, 0), plane.c2p(3, 2), buff=0, color=ORANGE, stroke_width=9)
        standard_input_label = MathTex(r"(3,2)_{\mathcal E}", font_size=36, color=ORANGE).next_to(input_vector.get_end(), UP, buff=0.10)
        standard_output_label = MathTex(r"(6,2)_{\mathcal E}", font_size=36, color=YELLOW).move_to(label_av)
        basis_input_label = MathTex(r"(1,2)_{\mathcal B}", font_size=39, color=ORANGE).move_to(standard_input_label)
        basis_output_label = MathTex(r"(4,2)_{\mathcal B}", font_size=39, color=YELLOW).move_to(standard_output_label)
        b1 = Arrow(plane.c2p(0, 0), plane.c2p(1, 0), buff=0, color=GREEN_C, stroke_width=7)
        b2 = Arrow(plane.c2p(0, 0), plane.c2p(1, 1), buff=0, color=BLUE_C, stroke_width=7)
        basis_name = MathTex(r"\mathcal B=\{(1,0),(1,1)\}", font_size=35, color=WHITE).to_edge(DOWN, buff=0.16)
        self.play(FadeOut(action), FadeIn(input_vector), FadeIn(standard_input_label), ReplacementTransform(label_av, standard_output_label))
        self.wait(0.8)
        self.play(
            Transform(standard_grid, basis_grid, rate_func=smooth),
            ReplacementTransform(standard_input_label, basis_input_label),
            ReplacementTransform(standard_output_label, basis_output_label),
            FadeIn(b1), FadeIn(b2), FadeIn(basis_name),
            run_time=4.0,
        )
        same_action = MathTex(
            r"[A]_{\mathcal B}:(1,2)_{\mathcal B}\longmapsto(4,2)_{\mathcal B}",
            font_size=42, color=WHITE,
        ).to_edge(DOWN, buff=0.16)
        self.play(ReplacementTransform(basis_name, same_action)); self.wait(1.8)

        heading = self._replace_heading(heading, "To use B-coordinates, translate in, transform, then translate back.")
        self.play(
            FadeOut(standard_grid), FadeOut(vector), FadeOut(input_vector),
            FadeOut(basis_input_label), FadeOut(basis_output_label),
            FadeOut(b1), FadeOut(b2), FadeOut(same_action),
        )
        route = MathTex(
            r"[\mathbf v]_{\mathcal B}"
            r"\xrightarrow{\quad P_{\mathcal B}\quad}\mathbf v"
            r"\xrightarrow{\quad A\quad}A\mathbf v"
            r"\xrightarrow{\quad P_{\mathcal B}^{-1}\quad}[A\mathbf v]_{\mathcal B}",
            font_size=51, color=WHITE,
        )
        annotations = VGroup(
            Text("decode B-coordinates", font_size=27, color=GREEN_C),
            Text("apply the transformation", font_size=27, color=ORANGE),
            Text("encode the result in B", font_size=27, color=BLUE_C),
        ).arrange(RIGHT, buff=0.75)
        pipeline = self._fit(VGroup(route, annotations).arrange(DOWN, buff=0.62))
        self.play(FadeIn(route)); self.play(FadeIn(annotations)); self.wait(1.8)

        heading = self._replace_heading(heading, "Read the composition from right to left.")
        self.play(FadeOut(pipeline))
        action_on_x = MathTex(
            r"[A\mathbf v]_{\mathcal B}="
            r"P_{\mathcal B}^{-1}AP_{\mathcal B}[\mathbf v]_{\mathcal B}",
            font_size=61, color=WHITE,
        )
        formula = MathTex(r"\boxed{[A]_{\mathcal B}=P_{\mathcal B}^{-1}AP_{\mathcal B}}", font_size=67, color=YELLOW)
        warning = Text("The two basis matrices belong on opposite sides of A.", font_size=31, color=ORANGE)
        derivation = self._fit(VGroup(action_on_x, formula, warning).arrange(DOWN, buff=0.52))
        self.play(FadeIn(action_on_x)); self.play(FadeIn(formula)); self.play(FadeIn(warning)); self.wait(1.8)

        heading = self._replace_heading(heading, "Compute the new matrix with structural matrix objects.")
        self.play(FadeOut(derivation))
        givens = VGroup(
            VGroup(MathTex("A=", font_size=47), self._matrix([["2", "0"], ["0", "1"]])).arrange(RIGHT, buff=0.12),
            VGroup(MathTex(r"P_{\mathcal B}=", font_size=47), self._matrix([["1", "1"], ["0", "1"]])).arrange(RIGHT, buff=0.12),
            VGroup(MathTex(r"P_{\mathcal B}^{-1}=", font_size=47), self._matrix([["1", "-1"], ["0", "1"]])).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.55)
        product = VGroup(
            MathTex(r"[A]_{\mathcal B}=", font_size=47, color=YELLOW),
            self._matrix([["1", "-1"], ["0", "1"]], 0.76),
            self._matrix([["2", "0"], ["0", "1"]], 0.76),
            self._matrix([["1", "1"], ["0", "1"]], 0.76),
            MathTex("=", font_size=48, color=YELLOW),
            self._matrix([["2", "1"], ["0", "1"]], 0.76),
        ).arrange(RIGHT, buff=0.15).set_color(YELLOW)
        computation = self._fit(VGroup(givens, product).arrange(DOWN, buff=0.62))
        self.play(FadeIn(givens)); self.play(FadeIn(product)); self.wait(1.9)

        heading = self._replace_heading(heading, "Verify that both matrices describe the same transformation.")
        self.play(FadeOut(computation))
        b_input = VGroup(MathTex(r"[\mathbf v]_{\mathcal B}=", font_size=48), self._matrix([["1"], ["2"]], 0.80)).arrange(RIGHT, buff=0.12)
        b_calculation = VGroup(
            MathTex(r"[A\mathbf v]_{\mathcal B}=", font_size=46),
            self._matrix([["2", "1"], ["0", "1"]], 0.78),
            self._matrix([["1"], ["2"]], 0.78),
            MathTex("=", font_size=48), self._matrix([["4"], ["2"]], 0.78),
        ).arrange(RIGHT, buff=0.16)
        standard_check = MathTex(r"(1,2)_{\mathcal B}\leftrightarrow(3,2),\qquad(4,2)_{\mathcal B}\leftrightarrow(6,2)", font_size=49, color=ORANGE)
        verification = self._fit(VGroup(b_input, b_calculation, standard_check).arrange(DOWN, buff=0.45))
        self.play(FadeIn(b_input)); self.play(FadeIn(b_calculation)); self.play(FadeIn(standard_check)); self.wait(1.9)

        heading = self._replace_heading(heading, "The matrix changes with the basis; the transformation does not.")
        self.play(FadeOut(verification))
        final = self._fit(VGroup(
            MathTex(r"[\mathbf v]_{\mathcal B}\xrightarrow{\quad[A]_{\mathcal B}\quad}[A\mathbf v]_{\mathcal B}", font_size=61, color=WHITE),
            MathTex(r"\boxed{[A]_{\mathcal B}=P_{\mathcal B}^{-1}AP_{\mathcal B}}", font_size=65, color=YELLOW),
            Text("One geometric action, expressed in a new coordinate language.", font_size=32, color=ORANGE),
        ).arrange(DOWN, buff=0.52))
        self.play(FadeIn(final)); self.wait(2.0)
