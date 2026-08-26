"""Manim presentation: Change of Basis — One Object, Many Descriptions."""
from __future__ import annotations

from manim import (
    BLUE_C, GREEN_C, GREY_B, ORANGE, PURPLE_C, TEAL_C, WHITE, YELLOW,
    DOWN, LEFT, RIGHT, UP,
    Arrow, Create, FadeIn, FadeOut, Line, MathTex, Matrix, NumberPlane,
    Rectangle, ReplacementTransform, Scene, Text, Transform, VGroup, smooth,
)


class ChangeOfBasisReviewPresentation(Scene):
    CHAPTER_BANNER = "CHANGE OF BASIS"
    LESSON_TITLE = "One Object, Many Descriptions"

    def _heading(self, text):
        item = Text(text, font_size=27, color=WHITE)
        if item.width > 11.6:
            item.scale_to_fit_width(11.6)
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
        if group.width > 11.2:
            group.scale_to_fit_width(11.2)
        if group.height > 4.7:
            group.scale_to_fit_height(4.7)
        group.move_to(DOWN * 0.42)
        return group

    @staticmethod
    def _matrix(entries, scale=0.82, v_buff=0.95):
        return Matrix(entries, v_buff=v_buff, h_buff=1.0).scale(scale)

    @staticmethod
    def _grid(plane, first, second, first_color, second_color):
        import numpy as np
        first, second = np.asarray(first), np.asarray(second)
        lines = VGroup()
        for first_count in range(-5, 8):
            start = first_count * first - 6 * second
            end = first_count * first + 6 * second
            lines.add(Line(
                plane.c2p(*start), plane.c2p(*end), color=second_color,
                stroke_width=3.4 if first_count == 0 else 2.0,
                stroke_opacity=1.0 if first_count == 0 else 0.82,
            ))
        for second_count in range(-6, 7):
            start = -5 * first + second_count * second
            end = 7 * first + second_count * second
            lines.add(Line(
                plane.c2p(*start), plane.c2p(*end), color=first_color,
                stroke_width=3.4 if second_count == 0 else 2.0,
                stroke_opacity=1.0 if second_count == 0 else 0.82,
            ))
        return lines

    @staticmethod
    def _box(label, formula, color):
        content = VGroup(
            Text(label, font_size=27, color=color, weight="BOLD"),
            MathTex(formula, font_size=39, color=WHITE),
        ).arrange(DOWN, buff=0.22)
        border = Rectangle(width=content.width + 0.48, height=content.height + 0.42, color=color, stroke_width=2.5)
        border.move_to(content)
        return VGroup(border, content)

    def construct(self):
        banner, title, heading = self._chrome("What changes—and what remains invariant—when we change basis?")
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))
        opening = self._fit(VGroup(
            Text("The geometric object does not change.", font_size=40, color=ORANGE),
            Text("Its coordinate description does.", font_size=40, color=YELLOW),
            MathTex(r"\text{object}\quad\ne\quad\text{description of the object}", font_size=50, color=WHITE),
        ).arrange(DOWN, buff=0.62))
        self.play(FadeIn(opening[0])); self.play(FadeIn(opening[1])); self.play(FadeIn(opening[2])); self.wait(1.8)

        heading = self._replace_heading(heading, "One fixed vector can be described in three coordinate languages.")
        self.play(FadeOut(opening))
        plane = NumberPlane(
            x_range=[-2, 8, 1], y_range=[-4, 5, 1], x_length=7.0, y_length=5.8,
            background_line_style={"stroke_opacity": 0.0},
            axis_config={"stroke_color": WHITE, "stroke_width": 2.6},
        ).shift(LEFT * 2.75 + DOWN * 0.42)
        grid_b = self._grid(plane, (1, 1), (1, -1), GREEN_C, BLUE_C)
        grid_c = self._grid(plane, (1, 1), (2, 0), TEAL_C, PURPLE_C)
        vector = Arrow(plane.c2p(0, 0), plane.c2p(3, 1), buff=0, color=ORANGE, stroke_width=9)
        vector_label = MathTex(r"\mathbf v=(3,1)", font_size=37, color=ORANGE).next_to(vector.get_end(), UP, buff=0.08)
        b_readout = VGroup(
            MathTex(r"\mathbf v=2\mathbf b_1+\mathbf b_2", font_size=42),
            VGroup(MathTex(r"[\mathbf v]_{\mathcal B}=", font_size=40, color=YELLOW), self._matrix([["2"], ["1"]], 0.72)).arrange(RIGHT, buff=0.10),
        ).arrange(DOWN, buff=0.42).move_to(RIGHT * 3.72 + DOWN * 0.30)
        c_readout = VGroup(
            MathTex(r"\mathbf v=\mathbf c_1+\mathbf c_2", font_size=42),
            VGroup(MathTex(r"[\mathbf v]_{\mathcal C}=", font_size=40, color=YELLOW), self._matrix([["1"], ["1"]], 0.72)).arrange(RIGHT, buff=0.10),
        ).arrange(DOWN, buff=0.42).move_to(b_readout)
        standard_readout = VGroup(
            MathTex(r"[\mathbf v]_{\mathcal E}=", font_size=38, color=WHITE),
            self._matrix([["3"], ["1"]], 0.68),
        ).arrange(RIGHT, buff=0.10).to_edge(DOWN, buff=0.10)
        self.play(Create(plane), Create(grid_b), FadeIn(vector), FadeIn(vector_label), FadeIn(b_readout), FadeIn(standard_readout))
        self.wait(1.2)
        self.play(
            Transform(grid_b, grid_c, rate_func=smooth),
            ReplacementTransform(b_readout, c_readout),
            run_time=4.0,
        )
        fixed_note = Text("The grid and coordinate column changed; the orange vector did not.", font_size=28, color=ORANGE).to_edge(DOWN, buff=0.10)
        self.play(ReplacementTransform(standard_readout, fixed_note)); self.wait(1.8)

        heading = self._replace_heading(heading, "Coordinate conversion is a map between descriptions of the same vector.")
        self.play(FadeOut(plane), FadeOut(grid_b), FadeOut(vector), FadeOut(vector_label), FadeOut(c_readout), FadeOut(fixed_note))
        box_b = self._box("B-coordinates", r"[\mathbf v]_{\mathcal B}", GREEN_C)
        box_e = self._box("standard coordinates", r"[\mathbf v]_{\mathcal E}", ORANGE)
        box_c = self._box("C-coordinates", r"[\mathbf v]_{\mathcal C}", TEAL_C)
        boxes = VGroup(box_b, box_e, box_c).arrange(RIGHT, buff=0.85)
        route_top = MathTex(r"P_{\mathcal B}\qquad\qquad P_{\mathcal C}^{-1}", font_size=39, color=YELLOW).next_to(boxes, UP, buff=0.34)
        direct = MathTex(r"Q_{\mathcal C\leftarrow\mathcal B}=P_{\mathcal C}^{-1}P_{\mathcal B}", font_size=47, color=YELLOW).next_to(boxes, DOWN, buff=0.47)
        route_card = self._fit(VGroup(route_top, boxes, direct))
        self.play(FadeIn(boxes)); self.play(FadeIn(route_top)); self.play(FadeIn(direct)); self.wait(2.0)

        heading = self._replace_heading(heading, "The transition matrix comes from linear-combination recipes.")
        self.play(FadeOut(route_card))
        combinations = VGroup(
            MathTex(r"\mathbf b_1=1\mathbf c_1+0\mathbf c_2", font_size=46),
            MathTex(r"\mathbf b_2=-\mathbf c_1+\mathbf c_2", font_size=46),
        ).arrange(DOWN, buff=0.20)
        columns = VGroup(
            MathTex(r"Q_{\mathcal C\leftarrow\mathcal B}=\big[\,[\mathbf b_1]_{\mathcal C}\ \ [\mathbf b_2]_{\mathcal C}\,\big]=", font_size=42, color=YELLOW),
            self._matrix([["1", "-1"], ["0", "1"]], 0.88),
        ).arrange(RIGHT, buff=0.13)
        meaning = Text("Each column answers: how do I build this old basis vector from the new basis?", font_size=28, color=ORANGE)
        transition_card = self._fit(VGroup(combinations, columns, meaning).arrange(DOWN, buff=0.49))
        self.play(FadeIn(combinations)); self.play(FadeIn(columns)); self.play(FadeIn(meaning)); self.wait(2.0)

        heading = self._replace_heading(heading, "The same matrix converts every B-coordinate recipe into a C-coordinate recipe.")
        self.play(FadeOut(transition_card))
        numerical = VGroup(
            self._matrix([["1", "-1"], ["0", "1"]], 0.96),
            self._matrix([["2"], ["1"]], 0.96),
            MathTex("=", font_size=58),
            self._matrix([["1"], ["1"]], 0.96),
        ).arrange(RIGHT, buff=0.28)
        numerical_labels = MathTex(
            r"Q_{\mathcal C\leftarrow\mathcal B}[\mathbf v]_{\mathcal B}=[\mathbf v]_{\mathcal C}",
            font_size=52, color=YELLOW,
        )
        check = MathTex(r"2\mathbf b_1+\mathbf b_2=\mathbf c_1+\mathbf c_2=(3,1)", font_size=45, color=ORANGE)
        numerical_card = self._fit(VGroup(numerical, numerical_labels, check).arrange(DOWN, buff=0.47))
        self.play(FadeIn(numerical)); self.play(FadeIn(numerical_labels)); self.play(FadeIn(check)); self.wait(2.0)

        heading = self._replace_heading(heading, "A transformation is fixed too; only its matrix description changes.")
        self.play(FadeOut(numerical_card))
        transformation_route = MathTex(
            r"[\mathbf v]_{\mathcal C}"
            r"\xrightarrow{\ Q_{\mathcal B\leftarrow\mathcal C}\ }"
            r"[\mathbf v]_{\mathcal B}"
            r"\xrightarrow{\ [T]_{\mathcal B}\ }"
            r"[T\mathbf v]_{\mathcal B}"
            r"\xrightarrow{\ Q_{\mathcal C\leftarrow\mathcal B}\ }"
            r"[T\mathbf v]_{\mathcal C}",
            font_size=39,
        )
        transformation_rule = MathTex(
            r"\boxed{[T]_{\mathcal C}=Q_{\mathcal C\leftarrow\mathcal B}[T]_{\mathcal B}Q_{\mathcal B\leftarrow\mathcal C}}",
            font_size=50, color=YELLOW,
        )
        action_note = Text("Convert the input, apply T, then convert the output.", font_size=31, color=ORANGE)
        transformation_card = self._fit(VGroup(transformation_route, transformation_rule, action_note).arrange(DOWN, buff=0.56))
        self.play(FadeIn(transformation_route)); self.play(FadeIn(transformation_rule)); self.play(FadeIn(action_note)); self.wait(2.1)

        heading = self._replace_heading(heading, "A good basis reveals structure that another basis can hide.")
        self.play(FadeOut(transformation_card))
        matrix_b = VGroup(
            MathTex(r"[T]_{\mathcal B}=", font_size=45),
            self._matrix([["2", "1"], ["0", "3"]], 0.90),
        ).arrange(RIGHT, buff=0.12)
        matrix_c = VGroup(
            MathTex(r"[T]_{\mathcal C}=", font_size=45, color=YELLOW),
            self._matrix([["2", "0"], ["0", "3"]], 0.90),
        ).arrange(RIGHT, buff=0.12)
        comparison = VGroup(matrix_b, MathTex(r"\longrightarrow", font_size=55, color=ORANGE), matrix_c).arrange(RIGHT, buff=0.48)
        eigen_note = Text("In the C-basis, the transformation simply scales the two coordinate axes.", font_size=30, color=WHITE)
        power_note = MathTex(r"[T^k]_{\mathcal C}=\operatorname{diag}(2^k,3^k)", font_size=50, color=YELLOW)
        good_basis_card = self._fit(VGroup(comparison, eigen_note, power_note).arrange(DOWN, buff=0.52))
        self.play(FadeIn(comparison)); self.play(FadeIn(eigen_note)); self.play(FadeIn(power_note)); self.wait(2.0)

        heading = self._replace_heading(heading, "Before computing, identify exactly which description must change.")
        self.play(FadeOut(good_basis_card))
        coordinates_case = self._box(
            "Changing vector coordinates",
            r"[\mathbf v]_{\mathcal C}=Q_{\mathcal C\leftarrow\mathcal B}[\mathbf v]_{\mathcal B}",
            TEAL_C,
        )
        transformation_case = self._box(
            "Changing a transformation matrix",
            r"[T]_{\mathcal C}=Q_{\mathcal C\leftarrow\mathcal B}[T]_{\mathcal B}Q_{\mathcal B\leftarrow\mathcal C}",
            PURPLE_C,
        )
        direction_rule = Text("Read the arrow right-to-left: target basis ← source basis.", font_size=31, color=YELLOW)
        checklist = self._fit(VGroup(coordinates_case, transformation_case, direction_rule).arrange(DOWN, buff=0.44))
        self.play(FadeIn(coordinates_case)); self.play(FadeIn(transformation_case)); self.play(FadeIn(direction_rule)); self.wait(2.1)

        heading = self._replace_heading(heading, "The entire chapter is one coherent idea.")
        self.play(FadeOut(checklist))
        final_card = self._fit(VGroup(
            Text("Basis vectors are the building blocks.", font_size=34, color=GREEN_C),
            Text("Coordinates are linear-combination recipes.", font_size=34, color=YELLOW),
            Text("Transition matrices translate those recipes.", font_size=34, color=TEAL_C),
            Text("Similarity translates a transformation without changing it.", font_size=34, color=PURPLE_C),
            Text("Choose a basis that makes the structure visible.", font_size=36, color=ORANGE, weight="BOLD"),
        ).arrange(DOWN, buff=0.36))
        for line in final_card:
            self.play(FadeIn(line))
        self.wait(2.3)

