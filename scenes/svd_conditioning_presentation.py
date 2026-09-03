"""Manim presentation: Small Singular Values and Conditioning."""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    Circle,
    DOWN,
    Ellipse,
    FadeIn,
    FadeOut,
    GREEN_C,
    GREY_B,
    LEFT,
    MathTex,
    Matrix,
    ORANGE,
    RED_C,
    RIGHT,
    Scene,
    SurroundingRectangle,
    TEAL_C,
    Tex,
    Text,
    UP,
    VGroup,
    WHITE,
    YELLOW,
)

from engine.svd_conditioning import SVDConditioning


class SVDConditioningPresentation(Scene):
    CHAPTER_BANNER = "SINGULAR VALUES, RANK, AND APPROXIMATION"
    LESSON_TITLE = "Small Singular Values and Conditioning"

    def _heading(self, text):
        item = Text(text, font_size=27, color=WHITE)
        if item.width > 11.4:
            item.scale_to_fit_width(11.4)
        return item

    def _chrome(self, heading_text):
        banner = Tex(
            r"\textbf{SINGULAR VALUES, RANK, AND APPROXIMATION}",
            font_size=23,
            color=GREY_B,
        ).to_edge(UP, buff=0.16)
        title = Tex(
            r"\textbf{Small Singular Values and Conditioning}",
            font_size=33,
            color=YELLOW,
        ).next_to(banner, DOWN, buff=0.11)
        heading = self._heading(heading_text).next_to(title, DOWN, buff=0.16)
        return banner, title, heading

    def _replace_heading(self, old, text):
        new = self._heading(text).move_to(old)
        self.play(FadeOut(old), run_time=0.18)
        self.play(FadeIn(new), run_time=0.22)
        return new

    @staticmethod
    def _matrix(entries, scale=0.72, h_buff=0.96, v_buff=1.15):
        return Matrix(entries, h_buff=h_buff, v_buff=v_buff).scale(scale)

    @staticmethod
    def _align_entries_with_fraction_bars(matrix, indices, offset=0.15):
        entries = list(matrix.get_entries())
        for index in indices:
            entries[index].shift(UP * offset)

    @staticmethod
    def _card(label, formula, note, color):
        body = VGroup(
            Text(label, font_size=24, color=color, weight="BOLD"),
            MathTex(formula, font_size=38, color=WHITE),
            Text(note, font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.18)
        border = SurroundingRectangle(body, color=color, buff=0.18, stroke_width=2.1)
        return VGroup(border, body)

    def construct(self):
        model = SVDConditioning()
        if not np.allclose(model.singular_values(), [4, 0.25]):
            raise RuntimeError("unexpected singular values")
        if not np.allclose(model.inverse_singular_values(), [0.25, 4]):
            raise RuntimeError("unexpected inverse singular values")
        if not np.isclose(model.condition_number(), 16):
            raise RuntimeError("unexpected condition number")

        banner, title, heading = self._chrome(
            "This map is one-to-one and onto, but its inverse is unevenly sensitive."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        a_matrix = self._matrix([["4", "0"], ["0", r"\frac14"]], scale=0.78, v_buff=1.35)
        self._align_entries_with_fraction_bars(a_matrix, (2,), offset=0.15)
        opening = VGroup(
            VGroup(MathTex(r"A=", font_size=44), a_matrix).arrange(RIGHT, buff=0.16),
            VGroup(
                MathTex(r"A:\mathbb R^2\to\mathbb R^2", font_size=42, color=TEAL_C),
                MathTex(r"\det(A)=1\ne0", font_size=41, color=GREEN_C),
                Text("a bijection", font_size=28, color=YELLOW, weight="BOLD"),
            ).arrange(DOWN, buff=0.30),
        ).arrange(RIGHT, buff=1.18).move_to(DOWN * 0.02)
        warning = Text(
            "Invertible does not automatically mean stable.",
            font_size=29,
            color=ORANGE,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.62)
        self.play(FadeIn(opening[0]))
        self.play(FadeIn(opening[1]), FadeIn(warning))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "The singular values reveal a strong direction and a weak direction."
        )
        self.play(FadeOut(opening), FadeOut(warning))
        lanes = VGroup(
            VGroup(
                MathTex(r"v_1", font_size=43, color=TEAL_C),
                MathTex(r"\xrightarrow{\ \sigma_1=4\ }", font_size=43, color=YELLOW),
                MathTex(r"u_1", font_size=43, color=GREEN_C),
                Text("strong", font_size=25, color=GREEN_C, weight="BOLD"),
            ).arrange(RIGHT, buff=0.42),
            VGroup(
                MathTex(r"v_2", font_size=43, color=TEAL_C),
                MathTex(r"\xrightarrow{\ \sigma_2=\frac14\ }", font_size=43, color=YELLOW),
                MathTex(r"u_2", font_size=43, color=ORANGE),
                Text("weak", font_size=25, color=ORANGE, weight="BOLD"),
            ).arrange(RIGHT, buff=0.42),
        ).arrange(DOWN, buff=0.70).move_to(DOWN * 0.02)
        comparison = MathTex(r"\sigma_1=16\sigma_2", font_size=42, color=WHITE).to_edge(
            DOWN, buff=0.62
        )
        self.play(FadeIn(lanes[0]))
        self.play(FadeIn(lanes[1]), FadeIn(comparison))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "Geometrically, the unit circle becomes a long, thin ellipse."
        )
        self.play(FadeOut(lanes), FadeOut(comparison))
        circle = Circle(radius=1.02, color=TEAL_C, stroke_width=4).shift(LEFT * 3.35 + DOWN * 0.05)
        ellipse = Ellipse(width=4.9, height=0.62, color=GREEN_C, stroke_width=4).shift(
            RIGHT * 2.55 + DOWN * 0.05
        )
        map_arrow = Arrow(LEFT * 1.85, RIGHT * 0.05, buff=0.05, color=YELLOW)
        geometry = VGroup(
            circle,
            ellipse,
            map_arrow,
            MathTex(r"\|x\|=1", font_size=32, color=TEAL_C).next_to(circle, DOWN, buff=0.23),
            MathTex(r"Ax", font_size=34, color=YELLOW).next_to(map_arrow, UP, buff=0.12),
            Text("semiaxes 4 and 1/4", font_size=26, color=GREEN_C).next_to(
                ellipse, DOWN, buff=0.28
            ),
        )
        geometry.shift(DOWN * 0.02)
        self.play(FadeIn(circle), FadeIn(geometry[3]))
        self.play(FadeIn(map_arrow), FadeIn(geometry[4]), FadeIn(ellipse), FadeIn(geometry[5]))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "The inverse reciprocates both singular values."
        )
        self.play(FadeOut(geometry))
        inverse_matrix = self._matrix(
            [[r"\frac14", "0"], ["0", "4"]], scale=0.80, v_buff=1.35
        )
        self._align_entries_with_fraction_bars(inverse_matrix, (1,), offset=0.15)
        inverse_display = VGroup(
            VGroup(MathTex(r"A^{-1}=", font_size=46, color=YELLOW), inverse_matrix).arrange(
                RIGHT, buff=0.18
            ),
            VGroup(
                MathTex(r"4\mapsto\frac14", font_size=42, color=TEAL_C),
                MathTex(r"\frac14\mapsto4", font_size=42, color=ORANGE),
            ).arrange(RIGHT, buff=1.15),
            Text(
                "Undoing the weak direction requires a large expansion.",
                font_size=28,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.42).move_to(DOWN * 0.02)
        self.play(FadeIn(inverse_display[0]))
        self.play(FadeIn(inverse_display[1]))
        self.play(FadeIn(inverse_display[2]))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "Equal output perturbations produce very different input changes."
        )
        self.play(FadeOut(inverse_display))
        perturbations = VGroup(
            self._card(
                "STRONG OUTPUT DIRECTION",
                r"\varepsilon u_1\ \xrightarrow{\ A^{-1}\ }\ \frac{\varepsilon}{4}v_1",
                "the inverse contracts",
                TEAL_C,
            ),
            self._card(
                "WEAK OUTPUT DIRECTION",
                r"\varepsilon u_2\ \xrightarrow{\ A^{-1}\ }\ 4\varepsilon v_2",
                "the inverse amplifies",
                ORANGE,
            ),
        ).arrange(RIGHT, buff=0.58).move_to(DOWN * 0.02)
        self.play(FadeIn(perturbations[0]))
        self.play(FadeIn(perturbations[1]))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "The weak-direction response is sixteen times larger."
        )
        self.play(FadeOut(perturbations))
        amplification = VGroup(
            MathTex(
                r"\frac{\|A^{-1}(\varepsilon u_2)\|}{\|A^{-1}(\varepsilon u_1)\|}",
                font_size=47,
                color=WHITE,
            ),
            MathTex(r"=\frac{4\varepsilon}{\varepsilon/4}=16", font_size=51, color=YELLOW),
            Text(
                "The same-sized data error can have sixteen times the effect.",
                font_size=29,
                color=ORANGE,
                weight="BOLD",
            ),
        ).arrange(DOWN, buff=0.44).move_to(DOWN * 0.02)
        self.play(FadeIn(amplification[0]))
        self.play(FadeIn(amplification[1]))
        self.play(FadeIn(amplification[2]))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "The two-norm condition number measures this worst directional imbalance."
        )
        self.play(FadeOut(amplification))
        condition = VGroup(
            MathTex(
                r"\kappa_2(A)=\frac{\sigma_{\max}}{\sigma_{\min}}",
                font_size=51,
                color=WHITE,
            ),
            MathTex(r"=\frac{4}{1/4}=16", font_size=53, color=YELLOW),
            VGroup(
                Text("small kappa", font_size=27, color=GREEN_C, weight="BOLD"),
                Text("stable", font_size=27, color=GREEN_C),
                Text("large kappa", font_size=27, color=ORANGE, weight="BOLD"),
                Text("sensitive", font_size=27, color=ORANGE),
            ).arrange(RIGHT, buff=0.48),
        ).arrange(DOWN, buff=0.42).move_to(DOWN * 0.02)
        self.play(FadeIn(condition[0]))
        self.play(FadeIn(condition[1]))
        self.play(FadeIn(condition[2]))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "Conditioning bounds how much relative data error can be amplified."
        )
        self.play(FadeOut(condition))
        error_bound = VGroup(
            MathTex(r"A\mathbf x=\mathbf b", font_size=42, color=TEAL_C),
            MathTex(
                r"\frac{\|\Delta\mathbf x\|}{\|\mathbf x\|}"
                r"\ \le\ \kappa_2(A)\,"
                r"\frac{\|\Delta\mathbf b\|}{\|\mathbf b\|}",
                font_size=50,
                color=YELLOW,
            ),
            Text(
                "A condition number of sixteen permits up to sixteenfold relative amplification.",
                font_size=27,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.47).move_to(DOWN * 0.02)
        self.play(FadeIn(error_bound[0]))
        self.play(FadeIn(error_bound[1]))
        self.play(FadeIn(error_bound[2]))
        self.wait(2.4)

        heading = self._replace_heading(
            heading, "As the smallest singular value approaches zero, inversion becomes unstable."
        )
        self.play(FadeOut(error_bound))
        spectrum = VGroup(
            self._card("BALANCED", r"\sigma_{\min}=4", "condition number 1", GREEN_C),
            self._card("THIN", r"\sigma_{\min}=\frac14", "condition number 16", ORANGE),
            self._card("COLLAPSED", r"\sigma_{\min}=0", "condition number infinite", RED_C),
        ).arrange(RIGHT, buff=0.42).move_to(DOWN * 0.02)
        limit_note = MathTex(
            r"\sigma_{\min}\downarrow0\quad\Longrightarrow\quad\kappa_2(A)\uparrow\infty",
            font_size=42,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.60)
        self.play(FadeIn(spectrum[0]))
        self.play(FadeIn(spectrum[1]))
        self.play(FadeIn(spectrum[2]), FadeIn(limit_note))
        self.wait(2.4)

        heading = self._replace_heading(
            heading, "Small singular values are warnings: their reciprocals magnify uncertainty."
        )
        self.play(FadeOut(spectrum), FadeOut(limit_note))
        conclusion = VGroup(
            MathTex(
                r"\boxed{\kappa_2(A)=\frac{\sigma_{\max}}{\sigma_{\min}}}",
                font_size=54,
                color=YELLOW,
            ),
            VGroup(
                self._card("FORWARD MAP", r"\sigma_{\min}\ \text{is small}", "nearly loses a direction", TEAL_C),
                self._card("INVERSE MAP", r"1/\sigma_{\min}\ \text{is large}", "amplifies uncertainty", ORANGE),
            ).arrange(RIGHT, buff=0.62),
            Text(
                "Invertibility says an inverse exists. Conditioning says whether it is reliable.",
                font_size=28,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.04)
        self.play(FadeIn(conclusion[0]))
        self.play(FadeIn(conclusion[1]))
        self.play(FadeIn(conclusion[2]))
        self.wait(3.0)
