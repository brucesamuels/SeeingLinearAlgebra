"""CP88: inner products and the dot product through continuous geometry."""
from __future__ import annotations
import numpy as np
from manim import (
    Angle, Arrow, BLUE, Create, DecimalNumber, DOWN, FadeIn, FadeOut, GREEN,
    LEFT, MathTex, NumberPlane, ORANGE, RED, ReplacementTransform, RIGHT,
    Scene, Text, UP, ValueTracker, VGroup, WHITE, YELLOW, always_redraw, linear,
)
from engine.inner_product import InnerProduct

class InnerProductDotProductPresentation(Scene):
    TITLE = 'Can Two Vectors Produce a Number?'

    def construct(self) -> None:
        title = Text(self.TITLE, font_size=40).to_edge(UP)
        subtitle = Text('Watch what changes as one vector rotates.', font_size=25).next_to(title, DOWN, buff=0.16)
        self.play(FadeIn(title), FadeIn(subtitle))

        prompt = VGroup(
            MathTex(r'\mathbf{u}+\mathbf{v}\longrightarrow\text{vector}', font_size=32),
            MathTex(r'c\mathbf{v}\longrightarrow\text{vector}', font_size=32),
            MathTex(r'\mathbf{u},\mathbf{v}\longrightarrow\;?', font_size=37, color=YELLOW),
        ).arrange(DOWN, buff=0.30)
        self.play(FadeIn(prompt)); self.wait(1.2); self.play(FadeOut(prompt))

        plane = NumberPlane(
            x_range=(-4.5, 4.5, 1), y_range=(-3.2, 3.2, 1),
            x_length=8.0, y_length=5.2,
            background_line_style={'stroke_opacity': 0.28},
        ).shift(LEFT * 1.15 + DOWN * 0.52)
        fixed_u = np.array([3.0, 0.0])
        rotating_length = np.sqrt(8.0)
        angle = ValueTracker(np.pi / 4)
        u_arrow = Arrow(plane.c2p(0, 0), plane.c2p(*fixed_u), buff=0, color=BLUE, stroke_width=7, max_tip_length_to_length_ratio=0.15)
        u_label = MathTex(r'\mathbf{u}', font_size=30, color=BLUE).next_to(plane.c2p(*fixed_u), RIGHT + UP, buff=0.10)

        def current_v():
            theta = angle.get_value()
            return rotating_length * np.array([np.cos(theta), np.sin(theta)])

        v_arrow = always_redraw(lambda: Arrow(plane.c2p(0, 0), plane.c2p(*current_v()), buff=0, color=YELLOW, stroke_width=7, max_tip_length_to_length_ratio=0.15))
        v_label = always_redraw(lambda: MathTex(r'\mathbf{v}', font_size=30, color=YELLOW).next_to(plane.c2p(*current_v()), RIGHT + UP, buff=0.10))
        arc = always_redraw(lambda: Angle(u_arrow, v_arrow, radius=0.63, color=WHITE, stroke_width=3))

        readout_label = MathTex(r'\langle\mathbf{u},\mathbf{v}\rangle=', font_size=31)
        readout_number = DecimalNumber(InnerProduct.dot(fixed_u, current_v()), num_decimal_places=2, include_sign=True, font_size=37, color=YELLOW)
        readout_number.add_updater(lambda number: number.set_value(InnerProduct.dot(fixed_u, current_v())))
        readout = VGroup(readout_label, readout_number).arrange(RIGHT, buff=0.10).to_corner(RIGHT + UP).shift(LEFT * 0.24 + DOWN * 1.35)
        mystery = Text('What is this number measuring?', font_size=24, color=YELLOW).next_to(readout, DOWN, buff=0.28).shift(LEFT * 0.38)

        self.play(Create(plane), Create(u_arrow), FadeIn(u_label))
        self.play(Create(v_arrow), FadeIn(v_label), FadeIn(arc))
        self.play(FadeIn(readout), FadeIn(mystery)); self.wait(0.7)
        self.play(angle.animate.set_value(3 * np.pi / 4), run_time=5.0, rate_func=linear)
        self.wait(0.6)
        self.play(angle.animate.set_value(np.pi / 2), run_time=1.6, rate_func=linear); self.wait(1.0)

        zero_callout = VGroup(
            Text('Perpendicular vectors', font_size=27, color=GREEN),
            MathTex(r'\langle\mathbf{u},\mathbf{v}\rangle=0', font_size=34, color=GREEN),
        ).arrange(DOWN, buff=0.12).next_to(mystery, DOWN, buff=0.30)
        self.play(FadeIn(zero_callout)); self.wait(1.0); self.play(FadeOut(zero_callout))
        self.play(angle.animate.set_value(np.pi / 4), run_time=2.2, rate_func=linear)

        sign_card = VGroup(
            VGroup(MathTex(r'\langle\mathbf{u},\mathbf{v}\rangle>0', font_size=29, color=GREEN), Text('acute', font_size=23)).arrange(DOWN, buff=0.07),
            VGroup(MathTex(r'\langle\mathbf{u},\mathbf{v}\rangle=0', font_size=29, color=YELLOW), Text('right', font_size=23)).arrange(DOWN, buff=0.07),
            VGroup(MathTex(r'\langle\mathbf{u},\mathbf{v}\rangle<0', font_size=29, color=RED), Text('obtuse', font_size=23)).arrange(DOWN, buff=0.07),
        ).arrange(DOWN, buff=0.24).to_edge(RIGHT).shift(LEFT * 0.30 + DOWN * 0.30)
        self.play(ReplacementTransform(mystery, sign_card))
        self.play(angle.animate.set_value(3 * np.pi / 4), run_time=3.3, rate_func=linear)
        self.play(angle.animate.set_value(np.pi / 4), run_time=3.3, rate_func=linear); self.wait(0.8)

        self.play(FadeOut(sign_card), FadeOut(readout), FadeOut(arc), FadeOut(v_label), FadeOut(v_arrow), FadeOut(u_label), FadeOut(u_arrow), FadeOut(plane), FadeOut(subtitle))
        self._show_coordinate_rule(); self._show_geometric_rule(); self._show_inner_product_conclusion(); self.wait(1.5)

    def _show_coordinate_rule(self) -> None:
        heading = Text('The Rule', font_size=34, color=YELLOW).shift(UP * 1.85)
        formula = MathTex(r'\mathbf{u}\cdot\mathbf{v}=u_1v_1+u_2v_2', font_size=44).shift(UP * 0.55)
        example = VGroup(
            MathTex(r'\mathbf{u}=\begin{bmatrix}3\\0\end{bmatrix},\qquad\mathbf{v}=\begin{bmatrix}2\\2\end{bmatrix}', font_size=34),
            MathTex(r'\mathbf{u}\cdot\mathbf{v}=3(2)+0(2)=6', font_size=37, color=GREEN),
        ).arrange(DOWN, buff=0.30).shift(DOWN * 0.80)
        self.play(FadeIn(heading)); self.play(FadeIn(formula)); self.play(FadeIn(example)); self.wait(1.3)
        self.play(FadeOut(heading), FadeOut(example)); self.coordinate_formula = formula

    def _show_geometric_rule(self) -> None:
        geometric = MathTex(r'\mathbf{u}\cdot\mathbf{v}=\|\mathbf{u}\|\,\|\mathbf{v}\|\cos\theta', font_size=43)
        interpretation = VGroup(
            Text('The coordinate calculation measures geometric alignment.', font_size=28),
            Text('Same direction: positive   •   perpendicular: zero   •   opposite: negative', font_size=23, color=YELLOW),
        ).arrange(DOWN, buff=0.22).shift(DOWN * 1.10)
        self.play(ReplacementTransform(self.coordinate_formula, geometric)); self.play(FadeIn(interpretation)); self.wait(1.5)
        consequences = VGroup(
            MathTex(r'\mathbf{v}\cdot\mathbf{v}=\|\mathbf{v}\|^2', font_size=34, color=GREEN),
            MathTex(r'\mathbf{u}\cdot\mathbf{v}=0\quad\Longleftrightarrow\quad\mathbf{u}\perp\mathbf{v}', font_size=34, color=ORANGE),
        ).arrange(DOWN, buff=0.30).shift(DOWN * 0.95)
        self.play(FadeOut(interpretation)); self.play(FadeIn(consequences)); self.wait(1.4)
        self.play(FadeOut(geometric), FadeOut(consequences))

    def _show_inner_product_conclusion(self) -> None:
        group = VGroup(
            Text('A broader idea', font_size=36, color=YELLOW),
            Text('The dot product is one example of an inner product.', font_size=29),
            MathTex(r'\langle\mathbf{u},\mathbf{v}\rangle', font_size=48, color=BLUE),
            Text('An inner product turns geometric relationships into numbers.', font_size=29, color=GREEN),
        ).arrange(DOWN, buff=0.35)
        self.play(FadeIn(group))
