"""Manim presentation: Coordinates Relative to a Basis."""
from __future__ import annotations

from manim import (
    BLUE_C, GREEN_C, GREY_B, GREY_D, ORANGE, WHITE, YELLOW,
    DOWN, LEFT, RIGHT, UP,
    Arrow, Create, FadeIn, FadeOut, MathTex, NumberPlane,
    ReplacementTransform, Scene, Text, VGroup,
)


class CoordinatesRelativeToBasisPresentation(Scene):
    CHAPTER_BANNER = "CHANGE OF BASIS"
    LESSON_TITLE = "Coordinates Relative to a Basis"

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

    def construct(self) -> None:
        banner, title, heading = self._chrome(
            "Coordinates record how much of each ordered basis vector is needed."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading), run_time=0.8)

        plane = NumberPlane(
            x_range=[-1, 6, 1], y_range=[-2, 5, 1],
            x_length=6.2, y_length=6.0,
            background_line_style={"stroke_color": GREY_D, "stroke_width": 1.2, "stroke_opacity": 0.70},
            axis_config={"stroke_color": GREY_B, "stroke_width": 2.0},
        ).shift(LEFT * 3.05 + DOWN * 0.38)
        vector = Arrow(
            plane.c2p(0, 0), plane.c2p(4, 2),
            buff=0, color=ORANGE, stroke_width=8, max_tip_length_to_length_ratio=0.10,
        )
        vector_label = MathTex(r"\mathbf v", font_size=39, color=ORANGE)
        vector_label.next_to(vector.get_end(), UP + RIGHT, buff=0.10)
        b1 = Arrow(plane.c2p(0, 0), plane.c2p(1, 1), buff=0, color=GREEN_C, stroke_width=6)
        b2 = Arrow(plane.c2p(0, 0), plane.c2p(1, -1), buff=0, color=BLUE_C, stroke_width=6)
        b1_label = MathTex(r"\mathbf b_1", font_size=32, color=GREEN_C).next_to(b1.get_end(), UP, buff=0.08)
        b2_label = MathTex(r"\mathbf b_2", font_size=32, color=BLUE_C).next_to(b2.get_end(), DOWN, buff=0.08)

        basis_definition = MathTex(
            r"\mathcal B=(\mathbf b_1,\mathbf b_2)",
            font_size=48, color=WHITE,
        )
        basis_vectors = MathTex(
            r"\mathbf b_1=\begin{bmatrix}1\\1\end{bmatrix},\qquad"
            r"\mathbf b_2=\begin{bmatrix}1\\-1\end{bmatrix}",
            font_size=40, color=WHITE,
        )
        question = Text("Which coefficients build v?", font_size=28, color=YELLOW)
        opening_panel = self._fit_right(VGroup(basis_definition, basis_vectors, question).arrange(DOWN, buff=0.48))

        self.play(Create(plane), run_time=0.9)
        self.play(FadeIn(vector), FadeIn(vector_label), FadeIn(b1), FadeIn(b2), FadeIn(b1_label), FadeIn(b2_label))
        self.play(FadeIn(opening_panel))
        self.wait(1.5)

        # Build 3 b1 + b2 tip-to-tail while the resultant remains visible.
        heading = self._replace_heading(heading, "Build the vector from copies of the basis directions.")
        self.play(FadeOut(opening_panel), FadeOut(b1), FadeOut(b2), FadeOut(b1_label), FadeOut(b2_label))
        p0 = plane.c2p(0, 0)
        p1 = plane.c2p(1, 1)
        p2 = plane.c2p(2, 2)
        p3 = plane.c2p(3, 3)
        p4 = plane.c2p(4, 2)
        step1 = Arrow(p0, p1, buff=0, color=GREEN_C, stroke_width=6)
        step2 = Arrow(p1, p2, buff=0, color=GREEN_C, stroke_width=6)
        step3 = Arrow(p2, p3, buff=0, color=GREEN_C, stroke_width=6)
        step4 = Arrow(p3, p4, buff=0, color=BLUE_C, stroke_width=6)
        count1 = MathTex(r"1\mathbf b_1", font_size=31, color=GREEN_C).next_to(step1, LEFT, buff=0.10)
        count2 = MathTex(r"2\mathbf b_1", font_size=31, color=GREEN_C).next_to(step2, LEFT, buff=0.10)
        count3 = MathTex(r"3\mathbf b_1", font_size=31, color=GREEN_C).next_to(step3, LEFT, buff=0.10)
        plus_b2 = MathTex(r"+\mathbf b_2", font_size=31, color=BLUE_C).next_to(step4, UP, buff=0.10)
        construction_formula = MathTex(
            r"\mathbf v=3\mathbf b_1+1\mathbf b_2",
            font_size=48, color=WHITE,
        )
        coefficient_note = Text("The coefficients are 3 and 1.", font_size=29, color=YELLOW)
        construction_panel = self._fit_right(VGroup(construction_formula, coefficient_note).arrange(DOWN, buff=0.48))
        self.play(FadeIn(step1), FadeIn(count1))
        self.play(FadeIn(step2), ReplacementTransform(count1, count2))
        self.play(FadeIn(step3), ReplacementTransform(count2, count3))
        self.play(FadeIn(step4), FadeIn(plus_b2))
        self.play(FadeIn(construction_panel))
        self.wait(1.6)

        # Package the ordered coefficients into a coordinate column.
        heading = self._replace_heading(heading, "Place the ordered coefficients into a coordinate column.")
        self.play(FadeOut(construction_panel))
        coefficient_column = MathTex(
            r"[\mathbf v]_{\mathcal B}=\begin{bmatrix}3\\1\end{bmatrix}",
            font_size=58, color=YELLOW,
        )
        correspondence = MathTex(
            r"3\longleftrightarrow\mathbf b_1,\qquad 1\longleftrightarrow\mathbf b_2",
            font_size=39, color=WHITE,
        )
        coordinate_panel = self._fit_right(VGroup(coefficient_column, correspondence).arrange(DOWN, buff=0.55))
        self.play(FadeIn(coordinate_panel))
        self.wait(1.5)

        # Distinguish the coordinate column from the geometric vector.
        heading = self._replace_heading(heading, "The coordinate column is a description, not the geometric vector itself.")
        self.play(FadeOut(coordinate_panel), FadeOut(step1), FadeOut(step2), FadeOut(step3), FadeOut(step4), FadeOut(count3), FadeOut(plus_b2))
        geometric = VGroup(
            Text("Geometric vector", font_size=28, color=ORANGE),
            MathTex(r"\mathbf v=\begin{bmatrix}4\\2\end{bmatrix}", font_size=56, color=ORANGE),
        ).arrange(DOWN, buff=0.28)
        description = VGroup(
            Text("B-coordinate description", font_size=28, color=YELLOW),
            MathTex(r"[\mathbf v]_{\mathcal B}=\begin{bmatrix}3\\1\end{bmatrix}", font_size=56, color=YELLOW),
        ).arrange(DOWN, buff=0.28)
        distinction_panel = self._fit_right(VGroup(geometric, description).arrange(DOWN, buff=0.60))
        self.play(FadeIn(distinction_panel))
        self.wait(1.6)

        # The order of the basis controls the order of the coordinates.
        heading = self._replace_heading(heading, "A basis is ordered, so reversing its order reverses the coordinates.")
        self.play(FadeOut(distinction_panel), FadeOut(plane), FadeOut(vector), FadeOut(vector_label))
        original = VGroup(
            MathTex(r"\mathcal B=(\mathbf b_1,\mathbf b_2)", font_size=54, color=GREEN_C),
            MathTex(r"[\mathbf v]_{\mathcal B}=\begin{bmatrix}3\\1\end{bmatrix}", font_size=54, color=GREEN_C),
        ).arrange(DOWN, buff=0.12)
        reversed_basis = VGroup(
            MathTex(r"\mathcal B'=(\mathbf b_2,\mathbf b_1)", font_size=54, color=BLUE_C),
            MathTex(r"[\mathbf v]_{\mathcal B'}=\begin{bmatrix}1\\3\end{bmatrix}", font_size=54, color=BLUE_C),
        ).arrange(DOWN, buff=0.12)
        fixed = VGroup(
            Text("Same vector; different ordering.", font_size=30, color=YELLOW),
            Text("Different coordinate column.", font_size=30, color=YELLOW),
        ).arrange(DOWN, buff=0.08)
        basis_comparison = VGroup(original, reversed_basis).arrange(RIGHT, buff=1.25)
        order_panel = VGroup(basis_comparison, fixed).arrange(DOWN, buff=0.48)
        if order_panel.width > 11.2:
            order_panel.scale_to_fit_width(11.2)
        order_panel.move_to(DOWN * 0.48)
        self.play(FadeIn(original))
        self.play(FadeIn(reversed_basis))
        self.play(FadeIn(fixed))
        self.wait(1.8)

        # Synthesis.
        heading = self._replace_heading(heading, "Coordinates are the unique ordered coefficients relative to a basis.")
        self.play(FadeOut(order_panel))
        definition = MathTex(
            r"\mathbf v=c_1\mathbf b_1+c_2\mathbf b_2"
            r"\quad\Longrightarrow\quad"
            r"[\mathbf v]_{\mathcal B}=\begin{bmatrix}c_1\\c_2\end{bmatrix}",
            font_size=42, color=WHITE,
        )
        takeaway = Text("The basis supplies the directions; the coordinates supply the amounts.", font_size=27, color=YELLOW)
        final_panel = VGroup(definition, takeaway).arrange(DOWN, buff=0.55)
        if final_panel.width > 11.2:
            final_panel.scale_to_fit_width(11.2)
        final_panel.move_to(DOWN * 0.42)
        self.play(FadeIn(definition))
        self.play(FadeIn(takeaway))
        self.wait(2.0)
