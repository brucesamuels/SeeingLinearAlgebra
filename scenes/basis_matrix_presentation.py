"""Manim presentation: The Basis Matrix."""
from __future__ import annotations

from manim import (
    BLUE_C, GREEN_C, GREY_B, GREY_D, ORANGE, WHITE, YELLOW,
    DOWN, LEFT, RIGHT, UP,
    Arrow, Create, FadeIn, FadeOut, MathTex, NumberPlane,
    ReplacementTransform, Scene, Text, VGroup,
)


class BasisMatrixPresentation(Scene):
    CHAPTER_BANNER = "CHANGE OF BASIS"
    LESSON_TITLE = "The Basis Matrix"

    def _heading(self, text: str) -> Text:
        item = Text(text, font_size=27, color=WHITE)
        if item.width > 11.6:
            item.scale_to_fit_width(11.6)
        return item

    def _chrome(self, heading_text: str):
        banner = Text(self.CHAPTER_BANNER, font_size=22, color=GREY_B, weight="BOLD")
        banner.to_edge(UP, buff=0.16)
        title = Text(self.LESSON_TITLE, font_size=32, color=YELLOW, weight="BOLD")
        title.next_to(banner, DOWN, buff=0.12)
        heading = self._heading(heading_text)
        heading.next_to(title, DOWN, buff=0.17)
        return banner, title, heading

    def _replace_heading(self, old, text: str):
        new = self._heading(text).move_to(old)
        self.play(ReplacementTransform(old, new), run_time=0.6)
        return new

    @staticmethod
    def _fit_right(group: VGroup) -> VGroup:
        if group.width > 5.35:
            group.scale_to_fit_width(5.35)
        if group.height > 4.65:
            group.scale_to_fit_height(4.65)
        group.move_to(RIGHT * 3.15 + DOWN * 0.38)
        return group

    @staticmethod
    def _fit_full(group: VGroup) -> VGroup:
        if group.width > 11.2:
            group.scale_to_fit_width(11.2)
        if group.height > 4.65:
            group.scale_to_fit_height(4.65)
        group.move_to(DOWN * 0.42)
        return group

    def construct(self) -> None:
        banner, title, heading = self._chrome("What problem does the basis matrix solve?")
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading), run_time=0.8)

        # Opening problem: translate between two coordinate descriptions.
        question = VGroup(
            Text("How do we translate a vector's coordinates", font_size=36, color=WHITE),
            Text("from a nonstandard basis into the standard basis?", font_size=36, color=WHITE),
        ).arrange(DOWN, buff=0.16)
        translation = MathTex(
            r"[\mathbf v]_{\mathcal B}"
            r"\xrightarrow{\qquad ?\qquad}"
            r"[\mathbf v]_{\mathcal E}",
            font_size=69, color=YELLOW,
        )
        same_vector = Text("Two coordinate columns describing the same vector", font_size=30, color=ORANGE)
        problem_card = self._fit_full(VGroup(question, translation, same_vector).arrange(DOWN, buff=0.62))
        self.play(FadeIn(question))
        self.play(FadeIn(translation))
        self.play(FadeIn(same_vector))
        self.wait(1.8)

        heading = self._replace_heading(
            heading, "Place the geometric basis vectors into the columns of one matrix."
        )
        self.play(FadeOut(problem_card))

        plane = NumberPlane(
            x_range=[-1, 6, 1], y_range=[-2, 5, 1],
            x_length=6.2, y_length=6.0,
            background_line_style={"stroke_color": GREY_B, "stroke_width": 1.8, "stroke_opacity": 0.88},
            axis_config={"stroke_color": WHITE, "stroke_width": 3.0},
        ).shift(LEFT * 3.05 + DOWN * 0.38)
        b1 = Arrow(plane.c2p(0, 0), plane.c2p(1, 1), buff=0, color=GREEN_C, stroke_width=7)
        b2 = Arrow(plane.c2p(0, 0), plane.c2p(1, -1), buff=0, color=BLUE_C, stroke_width=7)
        b1_label = MathTex(r"\mathbf b_1", font_size=34, color=GREEN_C).next_to(b1.get_end(), UP, buff=0.08)
        b2_label = MathTex(r"\mathbf b_2", font_size=34, color=BLUE_C).next_to(b2.get_end(), DOWN, buff=0.08)

        basis = MathTex(
            r"\mathbf b_1=\begin{bmatrix}1\\1\end{bmatrix},\qquad"
            r"\mathbf b_2=\begin{bmatrix}1\\-1\end{bmatrix}",
            font_size=42, color=WHITE,
        )
        columns = MathTex(
            r"P_{\mathcal B}=[\,\mathbf b_1\ \mathbf b_2\,]"
            r"=\begin{bmatrix}1&1\\1&-1\end{bmatrix}",
            font_size=48, color=YELLOW,
        )
        column_note = Text("Each column is one geometric basis vector.", font_size=28, color=GREY_B)
        opening_panel = self._fit_right(VGroup(basis, columns, column_note).arrange(DOWN, buff=0.45))

        self.play(Create(plane), run_time=0.9)
        self.play(FadeIn(b1), FadeIn(b2), FadeIn(b1_label), FadeIn(b2_label))
        self.play(FadeIn(basis))
        self.play(FadeIn(columns), FadeIn(column_note))
        self.wait(1.6)

        # Coordinates become weights on the columns.
        heading = self._replace_heading(heading, "Basis coordinates tell the matrix how much of each column to use.")
        self.play(FadeOut(opening_panel))
        weighted = MathTex(
            r"P_{\mathcal B}[\mathbf v]_{\mathcal B}"
            r"=\begin{bmatrix}1&1\\1&-1\end{bmatrix}"
            r"\begin{bmatrix}3\\1\end{bmatrix}",
            font_size=46, color=WHITE,
        )
        combination = MathTex(r"=3\mathbf b_1+1\mathbf b_2", font_size=53, color=YELLOW)
        weights = VGroup(
            Text("first coordinate weights the first column", font_size=25, color=GREEN_C),
            Text("second coordinate weights the second column", font_size=25, color=BLUE_C),
        ).arrange(DOWN, buff=0.16)
        weighted_panel = self._fit_right(VGroup(weighted, combination, weights).arrange(DOWN, buff=0.42))
        self.play(FadeIn(weighted))
        self.play(FadeIn(combination))
        self.play(FadeIn(weights))
        self.wait(1.5)

        # Full-width computation.
        heading = self._replace_heading(heading, "Matrix multiplication carries out the geometric linear combination.")
        self.play(FadeOut(weighted_panel), FadeOut(plane), FadeOut(b1), FadeOut(b2), FadeOut(b1_label), FadeOut(b2_label))
        expansion = MathTex(
            r"\begin{bmatrix}1&1\\1&-1\end{bmatrix}"
            r"\begin{bmatrix}3\\1\end{bmatrix}"
            r"=3\begin{bmatrix}1\\1\end{bmatrix}"
            r"+1\begin{bmatrix}1\\-1\end{bmatrix}"
            r"=\begin{bmatrix}4\\2\end{bmatrix}",
            font_size=49, color=WHITE,
        )
        identity = MathTex(
            r"\boxed{\mathbf v=P_{\mathcal B}[\mathbf v]_{\mathcal B}}",
            font_size=63, color=YELLOW,
        )
        full_computation = self._fit_full(VGroup(expansion, identity).arrange(DOWN, buff=0.65))
        self.play(FadeIn(expansion))
        self.play(FadeIn(identity))
        self.wait(1.7)

        # Return to geometry and show the basis matrix as a coordinate decoder.
        heading = self._replace_heading(heading, "The basis matrix translates coordinate instructions into geometry.")
        self.play(FadeOut(full_computation))
        self.play(FadeIn(plane), FadeIn(b1), FadeIn(b2))
        input1 = MathTex(r"\begin{bmatrix}1\\0\end{bmatrix}_{\mathcal B}", font_size=47, color=GREEN_C)
        output1 = MathTex(r"P_{\mathcal B}\begin{bmatrix}1\\0\end{bmatrix}=\mathbf b_1", font_size=44, color=GREEN_C)
        arrow1 = Arrow(plane.c2p(0, 0), plane.c2p(1, 1), buff=0, color=GREEN_C, stroke_width=8)
        coordinate1 = MathTex(r"[\mathbf b_1]_{\mathcal E}=(1,1)", font_size=30, color=GREEN_C)
        coordinate1.next_to(arrow1.get_end(), UP + LEFT, buff=0.10)
        decoder_panel = self._fit_right(VGroup(input1, output1).arrange(DOWN, buff=0.50))
        self.play(FadeIn(input1), FadeIn(output1), FadeIn(arrow1), FadeIn(coordinate1))
        self.wait(0.8)

        input2 = MathTex(r"\begin{bmatrix}0\\1\end{bmatrix}_{\mathcal B}", font_size=47, color=BLUE_C).move_to(input1)
        output2 = MathTex(r"P_{\mathcal B}\begin{bmatrix}0\\1\end{bmatrix}=\mathbf b_2", font_size=44, color=BLUE_C).move_to(output1)
        arrow2 = Arrow(plane.c2p(0, 0), plane.c2p(1, -1), buff=0, color=BLUE_C, stroke_width=8)
        coordinate2 = MathTex(r"[\mathbf b_2]_{\mathcal E}=(1,-1)", font_size=30, color=BLUE_C)
        coordinate2.next_to(arrow2.get_end(), DOWN + LEFT, buff=0.10)
        self.play(
            ReplacementTransform(input1, input2),
            ReplacementTransform(output1, output2),
            ReplacementTransform(arrow1, arrow2),
            ReplacementTransform(coordinate1, coordinate2),
        )
        self.wait(0.8)

        input3 = MathTex(r"\begin{bmatrix}3\\1\end{bmatrix}_{\mathcal B}", font_size=47, color=YELLOW).move_to(input2)
        output3 = MathTex(r"P_{\mathcal B}\begin{bmatrix}3\\1\end{bmatrix}=\mathbf v", font_size=44, color=ORANGE).move_to(output2)
        arrow3 = Arrow(plane.c2p(0, 0), plane.c2p(4, 2), buff=0, color=ORANGE, stroke_width=8)
        coordinate3 = MathTex(r"[\mathbf v]_{\mathcal E}=(4,2)", font_size=32, color=ORANGE)
        coordinate3.next_to(arrow3.get_end(), UP + RIGHT, buff=0.10)
        self.play(
            ReplacementTransform(input2, input3),
            ReplacementTransform(output2, output3),
            ReplacementTransform(arrow2, arrow3),
            ReplacementTransform(coordinate2, coordinate3),
        )
        self.wait(1.4)

        # Detailed numerical conversion from B-coordinates to standard coordinates.
        heading = self._replace_heading(heading, "Convert a new coordinate description into standard-basis coordinates.")
        self.play(FadeOut(plane), FadeOut(b1), FadeOut(b2), FadeOut(input3), FadeOut(output3), FadeOut(arrow3), FadeOut(coordinate3))
        given = MathTex(
            r"[\mathbf u]_{\mathcal B}=\begin{bmatrix}2\\-1\end{bmatrix}",
            font_size=54, color=YELLOW,
        )
        substitute = MathTex(
            r"[\mathbf u]_{\mathcal E}"
            r"=P_{\mathcal B}[\mathbf u]_{\mathcal B}"
            r"=\begin{bmatrix}1&1\\1&-1\end{bmatrix}"
            r"\begin{bmatrix}2\\-1\end{bmatrix}",
            font_size=46, color=WHITE,
        )
        row_arithmetic = MathTex(
            r"=\begin{bmatrix}1(2)+1(-1)\\1(2)+(-1)(-1)\end{bmatrix}"
            r"=\begin{bmatrix}1\\3\end{bmatrix}",
            font_size=48, color=WHITE,
        )
        result = MathTex(
            r"\boxed{[\mathbf u]_{\mathcal E}=\begin{bmatrix}1\\3\end{bmatrix}}",
            font_size=57, color=ORANGE,
        )
        standard_note = Text("These are the coordinates of u in the standard basis.", font_size=29, color=YELLOW)
        conversion_panel = self._fit_full(
            VGroup(given, substitute, row_arithmetic, result, standard_note).arrange(DOWN, buff=0.32)
        )
        self.play(FadeIn(given))
        self.play(FadeIn(substitute))
        self.play(FadeIn(row_arithmetic))
        self.play(FadeIn(result), FadeIn(standard_note))
        self.wait(1.8)

        # Synthesis.
        heading = self._replace_heading(heading, "The basis matrix converts basis coordinates into standard coordinates.")
        self.play(FadeOut(conversion_panel))
        map_line = MathTex(
            r"[\mathbf v]_{\mathcal B}"
            r"\xrightarrow{\quad P_{\mathcal B}\quad}"
            r"[\mathbf v]_{\mathcal E}",
            font_size=64, color=WHITE,
        )
        final_identity = MathTex(
            r"\boxed{[\mathbf v]_{\mathcal E}=P_{\mathcal B}[\mathbf v]_{\mathcal B}}",
            font_size=65, color=YELLOW,
        )
        standard_identity = MathTex(
            r"[\mathbf v]_{\mathcal E}=\mathbf v\quad\text{when vectors are written as standard columns}",
            font_size=40, color=ORANGE,
        )
        final_panel = self._fit_full(VGroup(map_line, final_identity, standard_identity).arrange(DOWN, buff=0.52))
        self.play(FadeIn(map_line))
        self.play(FadeIn(final_identity))
        self.play(FadeIn(standard_identity))
        self.wait(2.0)
