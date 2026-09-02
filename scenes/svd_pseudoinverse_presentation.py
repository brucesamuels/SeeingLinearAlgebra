"""Manim presentation: The Pseudoinverse — Undo What Can Be Undone."""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    FadeIn,
    FadeOut,
    GREEN_C,
    GREY_B,
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

from engine.svd_pseudoinverse import SVDPseudoinverse


class SVDPseudoinversePresentation(Scene):
    CHAPTER_BANNER = "SINGULAR VALUES, RANK, AND APPROXIMATION"
    LESSON_TITLE = "The Pseudoinverse: Undo What Can Be Undone"

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
            r"\textbf{The Pseudoinverse: Undo What Can Be Undone}",
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
    def _matrix(entries, scale=0.72, h_buff=0.90, v_buff=0.80):
        return Matrix(entries, h_buff=h_buff, v_buff=v_buff).scale(scale)

    @staticmethod
    def _align_entries_with_fraction_bars(matrix, indices, offset=0.15):
        entries = list(matrix.get_entries())
        for index in indices:
            entries[index].shift(UP * offset)

    @staticmethod
    def _card(label, formula, note, color):
        body = VGroup(
            Text(label, font_size=25, color=color, weight="BOLD"),
            MathTex(formula, font_size=36, color=WHITE),
            Text(note, font_size=23, color=GREY_B),
        ).arrange(DOWN, buff=0.18)
        border = SurroundingRectangle(body, color=color, buff=0.18, stroke_width=2.1)
        return VGroup(border, body)

    def construct(self):
        model = SVDPseudoinverse()
        if not np.allclose(model.pseudoinverse(), [[0.25, 0.25, 0], [0.25, 0.25, 0]]):
            raise RuntimeError("unexpected pseudoinverse")
        if not np.allclose(model.row_projection() @ model.row_projection(), model.row_projection()):
            raise RuntimeError("row-space projection is not idempotent")
        if not np.allclose(model.column_projection() @ model.column_projection(), model.column_projection()):
            raise RuntimeError("column-space projection is not idempotent")

        banner, title, heading = self._chrome(
            "A rectangular matrix that loses a direction cannot have an ordinary inverse."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        a_matrix = self._matrix([["1", "1"], ["1", "1"], ["0", "0"]], scale=0.72)
        opening = VGroup(
            VGroup(MathTex(r"A=", font_size=42), a_matrix).arrange(RIGHT, buff=0.14),
            VGroup(
                MathTex(r"A:\mathbb R^2\to\mathbb R^3", font_size=41, color=TEAL_C),
                Text("rectangular", font_size=28, color=ORANGE, weight="BOLD"),
                Text("rank one", font_size=28, color=ORANGE, weight="BOLD"),
            ).arrange(DOWN, buff=0.25),
        ).arrange(RIGHT, buff=1.25).move_to(DOWN * 0.02)
        no_inverse = MathTex(r"A^{-1}\ \text{does not exist}", font_size=43, color=RED_C).to_edge(
            DOWN, buff=0.68
        )
        self.play(FadeIn(opening[0]))
        self.play(FadeIn(opening[1]), FadeIn(no_inverse))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "The SVD isolates one reversible stretch and one irreversible loss."
        )
        self.play(FadeOut(opening), FadeOut(no_inverse))
        lanes = VGroup(
            VGroup(
                MathTex(r"v_1", font_size=42, color=TEAL_C),
                MathTex(r"\xrightarrow{\ \sigma_1=2\ }", font_size=42, color=YELLOW),
                MathTex(r"u_1", font_size=42, color=GREEN_C),
                Text("survives", font_size=25, color=GREEN_C, weight="BOLD"),
            ).arrange(RIGHT, buff=0.42),
            VGroup(
                MathTex(r"v_2", font_size=42, color=ORANGE),
                MathTex(r"\xrightarrow{\ \sigma_2=0\ }", font_size=42, color=YELLOW),
                MathTex(r"0", font_size=42, color=RED_C),
                Text("lost", font_size=25, color=RED_C, weight="BOLD"),
            ).arrange(RIGHT, buff=0.42),
        ).arrange(DOWN, buff=0.70).move_to(DOWN * 0.02)
        self.play(FadeIn(lanes[0]))
        self.play(FadeIn(lanes[1]))
        self.wait(2.2)

        prediction = Text(
            "Pause: when we reverse the SVD, what should happen to the zero singular value?",
            font_size=27,
            color=YELLOW,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.68)
        self.play(FadeIn(prediction))
        self.wait(2.8)

        heading = self._replace_heading(
            heading, "Reciprocate positive singular values; keep every zero at zero."
        )
        self.play(FadeOut(lanes), FadeOut(prediction))
        reciprocal_rule = VGroup(
            MathTex(
                r"\sigma_i^+=\begin{cases}1/\sigma_i,&\sigma_i>0,\\0,&\sigma_i=0,\end{cases}",
                font_size=47,
                color=WHITE,
            ),
            VGroup(
                MathTex(r"2\mapsto\frac12", font_size=43, color=TEAL_C),
                MathTex(r"0\mapsto0", font_size=43, color=ORANGE),
            ).arrange(RIGHT, buff=1.10),
            Text("Never divide by zero.", font_size=29, color=GREEN_C, weight="BOLD"),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.04)
        self.play(FadeIn(reciprocal_rule[0]))
        self.play(FadeIn(reciprocal_rule[1]))
        self.play(FadeIn(reciprocal_rule[2]))
        self.wait(2.2)

        heading = self._replace_heading(
            heading,
            "Form Sigma-plus: swap Sigma's dimensions, reciprocate nonzero diagonal entries, and keep zeros zero.",
        )
        self.play(FadeOut(reciprocal_rule))
        sigma = self._matrix([["2", "0"], ["0", "0"], ["0", "0"]], scale=0.67)
        sigma_plus = self._matrix(
            [[r"\frac12", "0", "0"], ["0", "0", "0"]],
            scale=0.66,
            h_buff=1.00,
            v_buff=1.15,
        )
        self._align_entries_with_fraction_bars(sigma_plus, (1, 2))
        sigma_comparison = VGroup(
            VGroup(
                MathTex(r"\Sigma=", font_size=40),
                sigma,
                MathTex(r"3\times2", font_size=29, color=GREY_B),
            ).arrange(RIGHT, buff=0.14),
            MathTex(r"\Longrightarrow", font_size=44, color=YELLOW),
            VGroup(
                MathTex(r"\Sigma^+=", font_size=40),
                sigma_plus,
                MathTex(r"2\times3", font_size=29, color=GREY_B),
            ).arrange(RIGHT, buff=0.14),
        ).arrange(RIGHT, buff=0.55).move_to(DOWN * 0.02)
        self.play(FadeIn(sigma_comparison[0]))
        self.play(FadeIn(sigma_comparison[1]), FadeIn(sigma_comparison[2]))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "Reverse the order of the orthogonal factors around Sigma-plus."
        )
        self.play(FadeOut(sigma_comparison))
        reverse_pipeline = VGroup(
            MathTex(r"A=U\Sigma V^T", font_size=48, color=WHITE),
            MathTex(r"\Downarrow", font_size=42, color=YELLOW),
            MathTex(r"\boxed{A^+=V\Sigma^+U^T}", font_size=54, color=YELLOW),
            VGroup(
                MathTex(r"A:\mathbb R^2\to\mathbb R^3", font_size=35, color=TEAL_C),
                MathTex(r"A^+:\mathbb R^3\to\mathbb R^2", font_size=35, color=GREEN_C),
            ).arrange(RIGHT, buff=0.85),
        ).arrange(DOWN, buff=0.36).move_to(DOWN * 0.03)
        self.play(FadeIn(reverse_pipeline[0]))
        self.play(FadeIn(reverse_pipeline[1]), FadeIn(reverse_pipeline[2]))
        self.play(FadeIn(reverse_pipeline[3]))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "For this matrix, the pseudoinverse is an explicit two-by-three map."
        )
        self.play(FadeOut(reverse_pipeline))
        a_plus = self._matrix(
            [[r"\frac14", r"\frac14", "0"], [r"\frac14", r"\frac14", "0"]],
            scale=0.74,
            h_buff=1.22,
            v_buff=1.42,
        )
        self._align_entries_with_fraction_bars(a_plus, (2, 5))
        explicit = VGroup(
            MathTex(r"A^+=", font_size=46, color=YELLOW),
            a_plus,
        ).arrange(RIGHT, buff=0.18).move_to(DOWN * 0.02)
        explicit_note = MathTex(
            r"A^+=\frac12v_1u_1^T",
            font_size=42,
            color=GREEN_C,
        ).to_edge(DOWN, buff=0.70)
        self.play(FadeIn(explicit))
        self.play(FadeIn(explicit_note))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "The surviving direction is recovered; the lost direction cannot be recovered."
        )
        self.play(FadeOut(explicit), FadeOut(explicit_note))
        domain_round_trips = VGroup(
            self._card("SURVIVING INPUT", r"A^+Av_1=v_1", "recovered exactly", TEAL_C),
            self._card("LOST INPUT", r"A^+Av_2=0", "information is gone", ORANGE),
        ).arrange(RIGHT, buff=0.80).move_to(DOWN * 0.02)
        not_identity = MathTex(r"A^+A\ne I_2", font_size=41, color=RED_C).to_edge(DOWN, buff=0.68)
        self.play(FadeIn(domain_round_trips[0]))
        self.play(FadeIn(domain_round_trips[1]), FadeIn(not_identity))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "The first round trip is projection onto the row space."
        )
        self.play(FadeOut(domain_round_trips), FadeOut(not_identity))
        row_projection = self._matrix(
            [[r"\frac12", r"\frac12"], [r"\frac12", r"\frac12"]],
            scale=0.74,
            h_buff=1.22,
            v_buff=1.42,
        )
        row_projector = VGroup(
            MathTex(r"A^+A=", font_size=44, color=TEAL_C),
            row_projection,
            MathTex(r"=P_{\mathcal R(A^T)}", font_size=42, color=YELLOW),
        ).arrange(RIGHT, buff=0.24).move_to(DOWN * 0.02)
        row_note = Text(
            "Keep the row-space component; remove the null-space component.",
            font_size=28,
            color=WHITE,
        ).to_edge(DOWN, buff=0.70)
        self.play(FadeIn(row_projector))
        self.play(FadeIn(row_note))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "The other round trip is projection onto the column space."
        )
        self.play(FadeOut(row_projector), FadeOut(row_note))
        column_projection = self._matrix(
            [
                [r"\frac12", r"\frac12", "0"],
                [r"\frac12", r"\frac12", "0"],
                ["0", "0", "0"],
            ],
            scale=0.68,
            h_buff=1.12,
            v_buff=1.24,
        )
        self._align_entries_with_fraction_bars(column_projection, (2, 5))
        column_projector = VGroup(
            MathTex(r"AA^+=", font_size=43, color=GREEN_C),
            column_projection,
            MathTex(r"=P_{\mathcal R(A)}", font_size=42, color=YELLOW),
        ).arrange(RIGHT, buff=0.22).move_to(DOWN * 0.02)
        column_note = Text(
            "Keep reachable output; remove the left-null-space component.",
            font_size=28,
            color=WHITE,
        ).to_edge(DOWN, buff=0.70)
        self.play(FadeIn(column_projector))
        self.play(FadeIn(column_note))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "The pseudoinverse undoes exactly the information that the matrix preserves."
        )
        self.play(FadeOut(column_projector), FadeOut(column_note))
        conclusion = VGroup(
            MathTex(r"\boxed{A^+=V\Sigma^+U^T}", font_size=54, color=YELLOW),
            VGroup(
                MathTex(r"A^+A=P_{\mathcal R(A^T)}", font_size=40, color=TEAL_C),
                MathTex(r"AA^+=P_{\mathcal R(A)}", font_size=40, color=GREEN_C),
            ).arrange(RIGHT, buff=0.70),
            Text(
                "Reverse positive stretches. Leave lost directions at zero.",
                font_size=29,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.48).move_to(DOWN * 0.05)
        self.play(FadeIn(conclusion[0]))
        self.play(FadeIn(conclusion[1]))
        self.play(FadeIn(conclusion[2]))
        self.wait(3.0)
