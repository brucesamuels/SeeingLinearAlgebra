"""Manim presentation: Changing Between Two Nonstandard Bases."""
from manim import (
    BLUE_C, GREEN_C, GREY_B, ORANGE, PURPLE_C, TEAL_C, WHITE, YELLOW,
    DOWN, RIGHT, UP,
    Arrow, Create, FadeIn, FadeOut, Line, MathTex, Matrix, NumberPlane,
    ReplacementTransform, Scene, Text, Transform, VGroup, smooth,
)


class TwoBasisCoordinatesPresentation(Scene):
    CHAPTER_BANNER = "CHANGE OF BASIS"
    LESSON_TITLE = "Changing Between Two Nonstandard Bases"

    def _heading(self, text):
        item = Text(text, font_size=27, color=WHITE)
        if item.width > 11.6:
            item.scale_to_fit_width(11.6)
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
        if group.width > 11.2:
            group.scale_to_fit_width(11.2)
        if group.height > 4.65:
            group.scale_to_fit_height(4.65)
        group.move_to(DOWN * 0.42)
        return group

    @staticmethod
    def _grid(plane, first, second, color_first, color_second):
        lines = VGroup()
        for fixed_first in range(-4, 5):
            start = fixed_first * first - 4 * second
            end = fixed_first * first + 4 * second
            lines.add(Line(plane.c2p(*start), plane.c2p(*end), color=color_second,
                           stroke_width=3.2 if fixed_first == 0 else 1.8,
                           stroke_opacity=1.0 if fixed_first == 0 else 0.72))
        for fixed_second in range(-4, 5):
            start = -4 * first + fixed_second * second
            end = 4 * first + fixed_second * second
            lines.add(Line(plane.c2p(*start), plane.c2p(*end), color=color_first,
                           stroke_width=3.2 if fixed_second == 0 else 1.8,
                           stroke_opacity=1.0 if fixed_second == 0 else 0.72))
        return lines

    def construct(self):
        import numpy as np
        banner, title, heading = self._chrome("How do we translate directly between two nonstandard descriptions?")
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))
        question = VGroup(
            Text("The vector is described in basis B.", font_size=37, color=WHITE),
            Text("How do we describe it in basis C?", font_size=37, color=WHITE),
        ).arrange(DOWN, buff=0.18)
        unknown = MathTex(r"[\mathbf v]_{\mathcal B}\xrightarrow{\qquad ?\qquad}[\mathbf v]_{\mathcal C}", font_size=70, color=YELLOW)
        invariant = Text("One fixed geometric vector; two nonstandard coordinate languages.", font_size=30, color=ORANGE)
        opening = self._fit(VGroup(question, unknown, invariant).arrange(DOWN, buff=0.60))
        self.play(FadeIn(question)); self.play(FadeIn(unknown)); self.play(FadeIn(invariant)); self.wait(1.7)

        heading = self._replace_heading(heading, "Watch the coordinate frame move while the vector stays fixed.")
        self.play(FadeOut(opening))
        plane = NumberPlane(x_range=[-6, 7, 1], y_range=[-6, 7, 1], x_length=6.3, y_length=6.0).shift(DOWN * 0.38)
        b1v, b2v = np.array([1, 1]), np.array([1, -1])
        c1v, c2v = np.array([1, 1]), np.array([2, 0])
        grid_b = self._grid(plane, b1v, b2v, GREEN_C, BLUE_C)
        grid_c = self._grid(plane, c1v, c2v, TEAL_C, PURPLE_C)
        vector = Arrow(plane.c2p(0, 0), plane.c2p(4, 2), buff=0, color=ORANGE, stroke_width=9)
        b1 = Arrow(plane.c2p(0, 0), plane.c2p(*b1v), buff=0, color=GREEN_C, stroke_width=7)
        b2 = Arrow(plane.c2p(0, 0), plane.c2p(*b2v), buff=0, color=BLUE_C, stroke_width=7)
        c1 = Arrow(plane.c2p(0, 0), plane.c2p(*c1v), buff=0, color=TEAL_C, stroke_width=7)
        c2 = Arrow(plane.c2p(0, 0), plane.c2p(*c2v), buff=0, color=PURPLE_C, stroke_width=7)
        label_b = MathTex(r"[\mathbf v]_{\mathcal B}=(3,1)", font_size=42, color=YELLOW).next_to(vector.get_end(), UP, buff=0.12)
        label_c = MathTex(r"[\mathbf v]_{\mathcal C}=(2,1)", font_size=42, color=YELLOW).move_to(label_b)
        basis_b = MathTex(r"\mathcal B=\{(1,1),(1,-1)\}", font_size=34, color=WHITE).to_edge(DOWN, buff=0.16)
        basis_c = MathTex(r"\mathcal C=\{(1,1),(2,0)\}", font_size=34, color=WHITE).move_to(basis_b)
        self.play(Create(grid_b), FadeIn(vector), FadeIn(b1), FadeIn(b2), FadeIn(label_b), FadeIn(basis_b)); self.wait(1.2)
        self.play(
            Transform(grid_b, grid_c, rate_func=smooth), Transform(b1, c1), Transform(b2, c2),
            ReplacementTransform(label_b, label_c), ReplacementTransform(basis_b, basis_c),
            run_time=4.0,
        )
        self.wait(1.8)

        heading = self._replace_heading(heading, "Use standard coordinates as a bridge between the two bases.")
        self.play(FadeOut(grid_b), FadeOut(vector), FadeOut(b1), FadeOut(b2), FadeOut(label_c), FadeOut(basis_c))
        route = MathTex(
            r"[\mathbf v]_{\mathcal B}"
            r"\xrightarrow{\quad P_{\mathcal B}\quad}"
            r"[\mathbf v]_{\mathcal E}"
            r"\xrightarrow{\quad P_{\mathcal C}^{-1}\quad}"
            r"[\mathbf v]_{\mathcal C}",
            font_size=54, color=WHITE,
        )
        right_to_left = Text("Read the matrix product from right to left.", font_size=31, color=ORANGE)
        bridge = self._fit(VGroup(route, right_to_left).arrange(DOWN, buff=0.65))
        self.play(FadeIn(route)); self.play(FadeIn(right_to_left)); self.wait(1.7)

        heading = self._replace_heading(heading, "Combine the two coordinate changes into one transition matrix.")
        self.play(FadeOut(bridge))
        formula = MathTex(r"\boxed{[\mathbf v]_{\mathcal C}=P_{\mathcal C}^{-1}P_{\mathcal B}[\mathbf v]_{\mathcal B}}", font_size=63, color=YELLOW)
        direction = MathTex(r"T_{\mathcal C\leftarrow\mathcal B}=P_{\mathcal C}^{-1}P_{\mathcal B}", font_size=58, color=WHITE)
        direction_note = Text("The arrow in the subscript records: input B, output C.", font_size=30, color=ORANGE)
        combined = self._fit(VGroup(formula, direction, direction_note).arrange(DOWN, buff=0.48))
        self.play(FadeIn(formula)); self.play(FadeIn(direction)); self.play(FadeIn(direction_note)); self.wait(1.7)

        heading = self._replace_heading(heading, "Compute the transition matrix for this pair of bases.")
        self.play(FadeOut(combined))
        pb_card = VGroup(
            MathTex(r"P_{\mathcal B}=", font_size=46),
            Matrix([["1", "1"], ["1", "-1"]]).scale(0.72),
        ).arrange(RIGHT, buff=0.12)
        pc_card = VGroup(
            MathTex(r"P_{\mathcal C}=", font_size=46),
            Matrix([["1", "2"], ["1", "0"]]).scale(0.72),
        ).arrange(RIGHT, buff=0.12)
        pc_inverse_card = VGroup(
            MathTex(r"P_{\mathcal C}^{-1}=", font_size=46),
            Matrix(
                [["0", "1"], [r"\tfrac{1}{2}", r"-\tfrac{1}{2}"]],
                v_buff=1.15,
            ).scale(0.72),
        ).arrange(RIGHT, buff=0.12)
        matrices = VGroup(pb_card, pc_card, pc_inverse_card).arrange(RIGHT, buff=0.48)

        product = VGroup(
            MathTex(r"T_{\mathcal C\leftarrow\mathcal B}=", font_size=47, color=YELLOW),
            Matrix(
                [["0", "1"], [r"\tfrac{1}{2}", r"-\tfrac{1}{2}"]],
                v_buff=1.15,
            ).scale(0.76),
            Matrix([["1", "1"], ["1", "-1"]]).scale(0.76),
            MathTex("=", font_size=48, color=YELLOW),
            Matrix([["1", "-1"], ["0", "1"]]).scale(0.76),
        ).arrange(RIGHT, buff=0.18)
        product.set_color(YELLOW)
        calculation = self._fit(VGroup(matrices, product).arrange(DOWN, buff=0.62))
        self.play(FadeIn(matrices)); self.play(FadeIn(product)); self.wait(1.8)

        heading = self._replace_heading(heading, "Apply the transition matrix to the B-coordinate column.")
        self.play(FadeOut(calculation))
        numerical = VGroup(
            MathTex(r"[\mathbf v]_{\mathcal C}=", font_size=49),
            Matrix([["1", "-1"], ["0", "1"]]).scale(0.78),
            Matrix([["3"], ["1"]]).scale(0.78),
            MathTex("=", font_size=49),
            Matrix([["3-1"], ["1"]]).scale(0.78),
            MathTex("=", font_size=49),
            Matrix([["2"], ["1"]]).scale(0.78),
        ).arrange(RIGHT, buff=0.16)
        check = MathTex(r"2(1,1)+1(2,0)=(4,2)=\mathbf v", font_size=52, color=ORANGE)
        result = MathTex(r"\boxed{(3,1)_{\mathcal B}\longmapsto(2,1)_{\mathcal C}}", font_size=61, color=YELLOW)
        worked = self._fit(VGroup(numerical, check, result).arrange(DOWN, buff=0.48))
        self.play(FadeIn(numerical)); self.play(FadeIn(check)); self.play(FadeIn(result)); self.wait(1.9)

        heading = self._replace_heading(heading, "The transition matrix changes coordinates—not the vector.")
        self.play(FadeOut(worked))
        final = self._fit(VGroup(
            MathTex(r"[\mathbf v]_{\mathcal B}\xrightarrow{\ P_{\mathcal C}^{-1}P_{\mathcal B}\ }[\mathbf v]_{\mathcal C}", font_size=62, color=WHITE),
            MathTex(r"\boxed{T_{\mathcal C\leftarrow\mathcal B}=P_{\mathcal C}^{-1}P_{\mathcal B}}", font_size=62, color=YELLOW),
            Text("Same geometric vector. New coordinate language.", font_size=34, color=ORANGE),
        ).arrange(DOWN, buff=0.52))
        self.play(FadeIn(final)); self.wait(2.0)
