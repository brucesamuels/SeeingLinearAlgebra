"""Manim presentation: Why a Good Basis Matters."""
from manim import (
    BLUE_C, GREEN_C, GREY_B, ORANGE, WHITE, YELLOW,
    DOWN, RIGHT, UP,
    Arrow, Create, FadeIn, FadeOut, Line, MathTex, Matrix, NumberPlane,
    ReplacementTransform, Scene, Text, Transform, VGroup, smooth,
)


class GoodBasisPresentation(Scene):
    CHAPTER_BANNER = "CHANGE OF BASIS"
    LESSON_TITLE = "Why a Good Basis Matters"

    def _heading(self, text):
        item = Text(text, font_size=27, color=WHITE)
        if item.width > 11.6: item.scale_to_fit_width(11.6)
        return item

    def _chrome(self, heading_text):
        banner = Text(self.CHAPTER_BANNER, font_size=22, color=GREY_B, weight="BOLD").to_edge(UP, buff=0.16)
        title = Text(self.LESSON_TITLE, font_size=32, color=YELLOW, weight="BOLD").next_to(banner, DOWN, buff=0.12)
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
    def _matrix(entries, scale=0.80):
        return Matrix(entries, v_buff=0.95, h_buff=1.0).scale(scale)

    @staticmethod
    def _grid(plane, first, second, first_color, second_color):
        import numpy as np
        first, second = np.asarray(first), np.asarray(second)
        lines = VGroup()
        for fixed_first in range(-4, 5):
            start, end = fixed_first * first - 4 * second, fixed_first * first + 4 * second
            lines.add(Line(
                plane.c2p(*start), plane.c2p(*end), color=second_color,
                stroke_width=3.2 if fixed_first == 0 else 1.8,
                stroke_opacity=1.0 if fixed_first == 0 else 0.78,
            ))
        for fixed_second in range(-4, 5):
            start, end = -4 * first + fixed_second * second, 4 * first + fixed_second * second
            lines.add(Line(
                plane.c2p(*start), plane.c2p(*end), color=first_color,
                stroke_width=3.2 if fixed_second == 0 else 1.8,
                stroke_opacity=1.0 if fixed_second == 0 else 0.78,
            ))
        return lines

    def construct(self):
        banner, title, heading = self._chrome("Can a better coordinate system reveal hidden simplicity?")
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))
        opening = self._fit(VGroup(
            Text("In the standard basis, the coordinates are mixed together.", font_size=34, color=WHITE),
            VGroup(MathTex("A=", font_size=52), self._matrix([["3", "1"], ["1", "3"]], 0.88)).arrange(RIGHT, buff=0.15),
            Text("Could another basis make the action easier to see?", font_size=34, color=ORANGE),
        ).arrange(DOWN, buff=0.48))
        self.play(FadeIn(opening[0])); self.play(FadeIn(opening[1])); self.play(FadeIn(opening[2])); self.wait(1.7)

        heading = self._replace_heading(heading, "On the standard grid, both coordinate directions turn and mix.")
        self.play(FadeOut(opening))
        plane = NumberPlane(x_range=[-6, 7, 1], y_range=[-6, 7, 1], x_length=6.2, y_length=5.9).shift(DOWN * 0.40)
        standard_grid = self._grid(plane, [1, 0], [0, 1], WHITE, WHITE)
        mixed_grid = self._grid(plane, [3, 1], [1, 3], YELLOW, ORANGE)
        e1 = Arrow(plane.c2p(0, 0), plane.c2p(1, 0), buff=0, color=GREEN_C, stroke_width=8)
        e2 = Arrow(plane.c2p(0, 0), plane.c2p(0, 1), buff=0, color=BLUE_C, stroke_width=8)
        ae1 = Arrow(plane.c2p(0, 0), plane.c2p(3, 1), buff=0, color=GREEN_C, stroke_width=8)
        ae2 = Arrow(plane.c2p(0, 0), plane.c2p(1, 3), buff=0, color=BLUE_C, stroke_width=8)
        standard_caption = MathTex(r"A\mathbf e_1=(3,1),\qquad A\mathbf e_2=(1,3)", font_size=42, color=WHITE).to_edge(DOWN, buff=0.16)
        self.play(Create(standard_grid), FadeIn(e1), FadeIn(e2)); self.wait(0.8)
        self.play(
            Transform(standard_grid, mixed_grid, rate_func=smooth),
            Transform(e1, ae1), Transform(e2, ae2), FadeIn(standard_caption), run_time=3.2,
        )
        self.wait(1.7)

        heading = self._replace_heading(heading, "Now align the coordinate grid with two special diagonal directions.")
        self.play(FadeOut(standard_grid), FadeOut(e1), FadeOut(e2), FadeOut(standard_caption))
        basis_grid = self._grid(plane, [1, 1], [1, -1], GREEN_C, BLUE_C)
        scaled_basis_grid = self._grid(plane, [4, 4], [2, -2], GREEN_C, BLUE_C)
        b1 = Arrow(plane.c2p(0, 0), plane.c2p(1, 1), buff=0, color=GREEN_C, stroke_width=8)
        b2 = Arrow(plane.c2p(0, 0), plane.c2p(1, -1), buff=0, color=BLUE_C, stroke_width=8)
        ab1 = Arrow(plane.c2p(0, 0), plane.c2p(4, 4), buff=0, color=GREEN_C, stroke_width=8)
        ab2 = Arrow(plane.c2p(0, 0), plane.c2p(2, -2), buff=0, color=BLUE_C, stroke_width=8)
        basis_name = MathTex(r"\mathcal B=\{\mathbf b_1=(1,1),\ \mathbf b_2=(1,-1)\}", font_size=37, color=WHITE).to_edge(DOWN, buff=0.16)
        self.play(Create(basis_grid), FadeIn(b1), FadeIn(b2), FadeIn(basis_name)); self.wait(1.0)

        heading = self._replace_heading(heading, "In this basis, each coordinate direction only scales—neither one turns.")
        scaling_caption = MathTex(r"A\mathbf b_1=4\mathbf b_1,\qquad A\mathbf b_2=2\mathbf b_2", font_size=45, color=YELLOW).move_to(basis_name)
        self.play(
            Transform(basis_grid, scaled_basis_grid, rate_func=smooth),
            Transform(b1, ab1), Transform(b2, ab2),
            ReplacementTransform(basis_name, scaling_caption), run_time=3.2,
        )
        self.wait(1.8)

        heading = self._replace_heading(heading, "The change-of-basis calculation exposes the independent scalings.")
        self.play(FadeOut(basis_grid), FadeOut(b1), FadeOut(b2), FadeOut(scaling_caption))
        givens = VGroup(
            VGroup(MathTex("A=", font_size=47), self._matrix([["3", "1"], ["1", "3"]])).arrange(RIGHT, buff=0.12),
            VGroup(MathTex(r"P_{\mathcal B}=", font_size=47), self._matrix([["1", "1"], ["1", "-1"]])).arrange(RIGHT, buff=0.12),
            VGroup(MathTex(r"P_{\mathcal B}^{-1}=", font_size=47), self._matrix([[r"\tfrac12", r"\tfrac12"], [r"\tfrac12", r"-\tfrac12"]], 0.76)).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.48)
        product = VGroup(
            MathTex(r"[A]_{\mathcal B}=P_{\mathcal B}^{-1}AP_{\mathcal B}=", font_size=45, color=YELLOW),
            self._matrix([["4", "0"], ["0", "2"]], 0.88),
        ).arrange(RIGHT, buff=0.18)
        algebra = self._fit(VGroup(givens, product).arrange(DOWN, buff=0.62))
        self.play(FadeIn(givens)); self.play(FadeIn(product)); self.wait(1.8)

        heading = self._replace_heading(heading, "A diagonal matrix means there is no coordinate mixing.")
        self.play(FadeOut(algebra))
        columns = VGroup(
            VGroup(self._matrix([["4", "0"], ["0", "2"]], 0.90), MathTex(r"\mathbf e_1", font_size=48), MathTex("=", font_size=48), self._matrix([["4"], ["0"]], 0.86)).arrange(RIGHT, buff=0.18),
            VGroup(self._matrix([["4", "0"], ["0", "2"]], 0.90), MathTex(r"\mathbf e_2", font_size=48), MathTex("=", font_size=48), self._matrix([["0"], ["2"]], 0.86)).arrange(RIGHT, buff=0.18),
        ).arrange(DOWN, buff=0.48)
        column_note = Text("Each coordinate axis stays independent of the other.", font_size=32, color=ORANGE)
        no_mixing = self._fit(VGroup(columns, column_note).arrange(DOWN, buff=0.48))
        self.play(FadeIn(columns)); self.play(FadeIn(column_note)); self.wait(1.8)

        heading = self._replace_heading(heading, "The simpler matrix makes every vector calculation transparent.")
        self.play(FadeOut(no_mixing))
        example = VGroup(
            MathTex(r"[\mathbf v]_{\mathcal B}=", font_size=48), self._matrix([["2"], ["1"]], 0.82),
            MathTex(r"\quad\longmapsto\quad", font_size=48), self._matrix([["8"], ["2"]], 0.82),
        ).arrange(RIGHT, buff=0.18)
        standard_check = MathTex(r"(2,1)_{\mathcal B}\leftrightarrow(3,1),\qquad(8,2)_{\mathcal B}\leftrightarrow(10,6)", font_size=47, color=ORANGE)
        explanation = Text("Scale the first basis coordinate by 4 and the second by 2.", font_size=31, color=WHITE)
        worked = self._fit(VGroup(example, standard_check, explanation).arrange(DOWN, buff=0.48))
        self.play(FadeIn(example)); self.play(FadeIn(standard_check)); self.play(FadeIn(explanation)); self.wait(1.9)

        heading = self._replace_heading(heading, "A good basis reveals the transformation's natural structure.")
        self.play(FadeOut(worked))
        comparison = VGroup(
            VGroup(MathTex("A=", font_size=48), self._matrix([["3", "1"], ["1", "3"]], 0.88)).arrange(RIGHT, buff=0.12),
            MathTex(r"\quad\longleftrightarrow\quad", font_size=50, color=WHITE),
            VGroup(MathTex(r"[A]_{\mathcal B}=", font_size=48), self._matrix([["4", "0"], ["0", "2"]], 0.88)).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.30)
        final_message = Text("Same transformation. A coordinate system that reveals what it really does.", font_size=31, color=ORANGE)
        final = self._fit(VGroup(comparison, final_message).arrange(DOWN, buff=0.62))
        self.play(FadeIn(comparison)); self.play(FadeIn(final_message)); self.wait(2.0)
