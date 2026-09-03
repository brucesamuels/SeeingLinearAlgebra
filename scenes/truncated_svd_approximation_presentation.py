"""Manim presentation: Truncated SVD and the Best Low-Rank Approximation."""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    FadeIn,
    FadeOut,
    GREEN_C,
    GREY_B,
    LEFT,
    MathTex,
    Matrix,
    ORANGE,
    Rectangle,
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

from engine.truncated_svd_approximation import TruncatedSVDApproximation


class TruncatedSVDApproximationPresentation(Scene):
    CHAPTER_BANNER = "SINGULAR VALUES, RANK, AND APPROXIMATION"
    LESSON_TITLE = "Truncated SVD and the Best Low-Rank Approximation"

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
            r"\textbf{Truncated SVD and the Best Low-Rank Approximation}",
            font_size=32,
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
    def _matrix(entries, scale=0.66, h_buff=0.95, v_buff=1.18):
        return Matrix(entries, h_buff=h_buff, v_buff=v_buff).scale(scale)

    @staticmethod
    def _align_entries_with_fraction_bars(matrix, indices, offset=0.14):
        entries = list(matrix.get_entries())
        for index in indices:
            entries[index].shift(UP * offset)

    @staticmethod
    def _card(label, formula, note, color):
        body = VGroup(
            Text(label, font_size=24, color=color, weight="BOLD"),
            MathTex(formula, font_size=37, color=WHITE),
            Text(note, font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.18)
        border = SurroundingRectangle(body, color=color, buff=0.18, stroke_width=2.1)
        return VGroup(border, body)

    @staticmethod
    def _mode_bar(label, value, width, color):
        bar = Rectangle(width=width, height=0.38, color=color, fill_color=color, fill_opacity=0.45)
        return VGroup(
            MathTex(label, font_size=35, color=color),
            bar,
            MathTex(value, font_size=35, color=WHITE),
        ).arrange(RIGHT, buff=0.28)

    def construct(self):
        model = TruncatedSVDApproximation()
        if not np.allclose(model.singular_values(), [5, 2, 0.5]):
            raise RuntimeError("unexpected singular values")
        if not np.allclose(model.truncated(2), np.diag([5, 2, 0])):
            raise RuntimeError("unexpected rank-two truncation")
        if not np.isclose(model.spectral_error(2), 0.5):
            raise RuntimeError("unexpected rank-two error")

        banner, title, heading = self._chrome(
            "Can a simpler, lower-rank matrix preserve the most important action of A?"
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        a_matrix = self._matrix(
            [["5", "0", "0"], ["0", "2", "0"], ["0", "0", r"\frac12"]],
            scale=0.69,
            h_buff=1.06,
            v_buff=1.24,
        )
        self._align_entries_with_fraction_bars(a_matrix, (6, 7))
        opening = VGroup(
            VGroup(MathTex(r"A=", font_size=43), a_matrix).arrange(RIGHT, buff=0.15),
            VGroup(
                MathTex(r"\sigma_1=5", font_size=39, color=TEAL_C),
                MathTex(r"\sigma_2=2", font_size=39, color=GREEN_C),
                MathTex(r"\sigma_3=\frac12", font_size=39, color=ORANGE),
            ).arrange(DOWN, buff=0.28),
        ).arrange(RIGHT, buff=1.20).move_to(DOWN * 0.02)
        ordering = MathTex(
            r"\sigma_1\ge\sigma_2\ge\sigma_3\ge0",
            font_size=40,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.61)
        self.play(FadeIn(opening[0]))
        self.play(FadeIn(opening[1]), FadeIn(ordering))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "The SVD writes A as an ordered sum of rank-one layers."
        )
        self.play(FadeOut(opening), FadeOut(ordering))
        decomposition = VGroup(
            MathTex(
                r"A=\sigma_1u_1v_1^T+\sigma_2u_2v_2^T+\sigma_3u_3v_3^T",
                font_size=43,
                color=WHITE,
            ),
            MathTex(
                r"A=5u_1v_1^T+2u_2v_2^T+\frac12u_3v_3^T",
                font_size=47,
                color=YELLOW,
            ),
            Text(
                "Each outer product contributes one independent direction.",
                font_size=28,
                color=GREEN_C,
            ),
        ).arrange(DOWN, buff=0.50).move_to(DOWN * 0.02)
        self.play(FadeIn(decomposition[0]))
        self.play(FadeIn(decomposition[1]))
        self.play(FadeIn(decomposition[2]))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "The singular values rank those layers by strength."
        )
        self.play(FadeOut(decomposition))
        mode_bars = VGroup(
            self._mode_bar(r"u_1v_1^T", "5", 4.8, TEAL_C),
            self._mode_bar(r"u_2v_2^T", "2", 1.92, GREEN_C),
            self._mode_bar(r"u_3v_3^T", r"\frac12", 0.48, ORANGE),
        ).arrange(DOWN, buff=0.48, aligned_edge=LEFT).move_to(DOWN * 0.01)
        mode_note = Text(
            "Large singular value: strong contribution     Small singular value: weak contribution",
            font_size=25,
            color=WHITE,
        ).to_edge(DOWN, buff=0.60)
        self.play(FadeIn(mode_bars[0]))
        self.play(FadeIn(mode_bars[1]))
        self.play(FadeIn(mode_bars[2]), FadeIn(mode_note))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "Truncate after two layers to obtain a rank-two approximation."
        )
        self.play(FadeOut(mode_bars), FadeOut(mode_note))
        a_two = self._matrix(
            [["5", "0", "0"], ["0", "2", "0"], ["0", "0", "0"]],
            scale=0.70,
            h_buff=1.06,
            v_buff=1.05,
        )
        truncation = VGroup(
            MathTex(r"A_2=5u_1v_1^T+2u_2v_2^T", font_size=45, color=YELLOW),
            VGroup(MathTex(r"A_2=", font_size=42, color=TEAL_C), a_two).arrange(RIGHT, buff=0.15),
            VGroup(
                Text("kept", font_size=26, color=GREEN_C, weight="BOLD"),
                MathTex(r"\sigma_1=5,\ \sigma_2=2", font_size=34, color=GREEN_C),
                Text("discarded", font_size=26, color=ORANGE, weight="BOLD"),
                MathTex(r"\sigma_3=\frac12", font_size=34, color=ORANGE),
            ).arrange(RIGHT, buff=0.34),
        ).arrange(DOWN, buff=0.32).move_to(DOWN * 0.02)
        self.play(FadeIn(truncation[0]))
        self.play(FadeIn(truncation[1]))
        self.play(FadeIn(truncation[2]))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "The approximation error is exactly the discarded layer."
        )
        self.play(FadeOut(truncation))
        residual_matrix = self._matrix(
            [["0", "0", "0"], ["0", "0", "0"], ["0", "0", r"\frac12"]],
            scale=0.71,
            h_buff=1.06,
            v_buff=1.06,
        )
        self._align_entries_with_fraction_bars(residual_matrix, (6, 7))
        residual = VGroup(
            MathTex(r"A-A_2=\frac12u_3v_3^T", font_size=47, color=ORANGE),
            VGroup(MathTex(r"A-A_2=", font_size=41), residual_matrix).arrange(RIGHT, buff=0.16),
            Text(
                "Only the weakest singular direction is missing.",
                font_size=29,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.40).move_to(DOWN * 0.02)
        self.play(FadeIn(residual[0]))
        self.play(FadeIn(residual[1]))
        self.play(FadeIn(residual[2]))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "Both standard error measures read the discarded singular values."
        )
        self.play(FadeOut(residual))
        errors = VGroup(
            self._card(
                "SPECTRAL NORM",
                r"\|A-A_2\|_2=\sigma_3=\frac12",
                "largest omitted stretch",
                TEAL_C,
            ),
            self._card(
                "FROBENIUS NORM",
                r"\|A-A_2\|_F=\sqrt{\sigma_3^2}=\frac12",
                "energy of omitted stretches",
                GREEN_C,
            ),
        ).arrange(RIGHT, buff=0.62).move_to(DOWN * 0.02)
        error_note = Text(
            "With one discarded layer, the two errors agree.",
            font_size=28,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.60)
        self.play(FadeIn(errors[0]))
        self.play(FadeIn(errors[1]), FadeIn(error_note))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "Eckart–Young says no other rank-two matrix can be closer."
        )
        self.play(FadeOut(errors), FadeOut(error_note))
        theorem = VGroup(
            Text("ECKART–YOUNG THEOREM", font_size=27, color=YELLOW, weight="BOLD"),
            MathTex(
                r"\min_{\operatorname{rank}(B)\le k}\|A-B\|_2=\sigma_{k+1}",
                font_size=47,
                color=TEAL_C,
            ),
            MathTex(
                r"\min_{\operatorname{rank}(B)\le k}\|A-B\|_F"
                r"=\sqrt{\sum_{i>k}\sigma_i^2}",
                font_size=45,
                color=GREEN_C,
            ),
            MathTex(r"k=2\quad\Longrightarrow\quad A_2\ \text{is optimal}", font_size=41, color=WHITE),
        ).arrange(DOWN, buff=0.36).move_to(DOWN * 0.02)
        self.play(FadeIn(theorem[0]))
        self.play(FadeIn(theorem[1]))
        self.play(FadeIn(theorem[2]))
        self.play(FadeIn(theorem[3]))
        self.wait(2.5)

        heading = self._replace_heading(
            heading, "Keeping the largest singular values is the decisive choice."
        )
        self.play(FadeOut(theorem))
        choices = VGroup(
            self._card(
                "KEEP 5 AND 2",
                r"\text{discard }\frac12\quad\Rightarrow\quad\|A-B\|_2=\frac12",
                "truncated SVD",
                GREEN_C,
            ),
            self._card(
                "KEEP 5 AND 1/2",
                r"\text{discard }2\quad\Rightarrow\quad\|A-B\|_2=2",
                "a worse rank-two choice",
                RED_C,
            ),
        ).arrange(DOWN, buff=0.45).move_to(DOWN * 0.02)
        verdict = Text(
            "Discard the weakest layer, not a stronger one.",
            font_size=29,
            color=YELLOW,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.58)
        self.play(FadeIn(choices[0]))
        self.play(FadeIn(choices[1]), FadeIn(verdict))
        self.wait(2.4)

        heading = self._replace_heading(
            heading, "Increasing rank creates a controlled ladder of approximations."
        )
        self.play(FadeOut(choices), FadeOut(verdict))
        ladder = VGroup(
            self._card("RANK 1", r"A_1=5u_1v_1^T", "spectral error 2", TEAL_C),
            self._card("RANK 2", r"A_2=A_1+2u_2v_2^T", "spectral error 1/2", GREEN_C),
            self._card("RANK 3", r"A_3=A", "spectral error 0", YELLOW),
        ).arrange(RIGHT, buff=0.38).move_to(DOWN * 0.02)
        ladder_note = MathTex(
            r"\text{more layers}\quad\Longrightarrow\quad\text{smaller error}",
            font_size=39,
            color=WHITE,
        ).to_edge(DOWN, buff=0.60)
        self.play(FadeIn(ladder[0]))
        self.play(FadeIn(ladder[1]))
        self.play(FadeIn(ladder[2]), FadeIn(ladder_note))
        self.wait(2.4)

        heading = self._replace_heading(
            heading, "Truncated SVD keeps the strongest structure with the smallest possible error."
        )
        self.play(FadeOut(ladder), FadeOut(ladder_note))
        conclusion = VGroup(
            MathTex(
                r"\boxed{A_k=\sum_{i=1}^{k}\sigma_i u_i v_i^T}",
                font_size=53,
                color=YELLOW,
            ),
            VGroup(
                self._card("KEEP", r"\sigma_1,\ldots,\sigma_k", "strongest rank-one layers", TEAL_C),
                self._card("ERROR", r"\sigma_{k+1},\sigma_{k+2},\ldots", "discarded layers", ORANGE),
            ).arrange(RIGHT, buff=0.62),
            Text(
                "Lower rank means a simpler model; the SVD makes it the best one.",
                font_size=29,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.04)
        self.play(FadeIn(conclusion[0]))
        self.play(FadeIn(conclusion[1]))
        self.play(FadeIn(conclusion[2]))
        self.wait(3.0)
