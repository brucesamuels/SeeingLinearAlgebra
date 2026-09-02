"""Manim presentation: Full SVD and the Four Fundamental Subspaces."""

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

from engine.svd_fundamental_subspaces import SVDFundamentalSubspaces


class SVDFundamentalSubspacesPresentation(Scene):
    CHAPTER_BANNER = "SINGULAR VALUES, RANK, AND APPROXIMATION"
    LESSON_TITLE = "Full SVD and the Four Fundamental Subspaces"

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
            r"\textbf{Full SVD and the Four Fundamental Subspaces}",
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
    def _compact_entries(matrix, factor=0.78):
        entries = list(matrix.get_entries())
        centers = [entry.get_center().copy() for entry in entries]
        for entry, center in zip(entries, centers, strict=True):
            entry.scale(factor).move_to(center)

    @staticmethod
    def _space_card(title, basis, description, color):
        body = VGroup(
            Text(title, font_size=25, color=color, weight="BOLD"),
            MathTex(basis, font_size=34, color=WHITE),
            Text(description, font_size=23, color=GREY_B),
        ).arrange(DOWN, buff=0.17)
        border = SurroundingRectangle(body, color=color, buff=0.17, stroke_width=2.1)
        return VGroup(border, body)

    def construct(self):
        model = SVDFundamentalSubspaces()
        if not np.allclose(model.singular_values(), [2, 0]):
            raise RuntimeError("unexpected singular values")
        if not np.allclose(model.full_u().T @ model.full_u(), np.eye(3)):
            raise RuntimeError("U is not orthogonal")
        if not np.allclose(model.full_v().T @ model.full_v(), np.eye(2)):
            raise RuntimeError("V is not orthogonal")
        if not np.allclose(model.reconstruction(), model.matrix):
            raise RuntimeError("full SVD reconstruction failed")

        banner, title, heading = self._chrome(
            "The previous lesson found a lost direction. Where do all the remaining directions live?"
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        a_matrix = self._matrix([["1", "1"], ["1", "1"], ["0", "0"]], scale=0.72)
        opening = VGroup(
            VGroup(MathTex("A=", font_size=42), a_matrix).arrange(RIGHT, buff=0.14),
            VGroup(
                MathTex(r"A:\mathbb R^2\to\mathbb R^3", font_size=43, color=TEAL_C),
                MathTex(r"\operatorname{rank}(A)=1", font_size=39, color=GREEN_C),
            ).arrange(DOWN, buff=0.36),
        ).arrange(RIGHT, buff=1.35).move_to(DOWN * 0.02)
        opening_question = Text(
            "How does the full SVD organize both spaces?",
            font_size=29,
            color=YELLOW,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.70)
        self.play(FadeIn(opening[0]))
        self.play(FadeIn(opening[1]), FadeIn(opening_question))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "The full SVD supplies an orthonormal basis in the input and output spaces."
        )
        self.play(FadeOut(opening), FadeOut(opening_question))
        pipeline = VGroup(
            VGroup(
                Text("INPUT", font_size=24, color=TEAL_C, weight="BOLD"),
                MathTex(r"\mathbb R^2", font_size=43),
            ).arrange(DOWN, buff=0.14),
            MathTex(r"\xrightarrow{\ V^T\ }", font_size=40, color=TEAL_C),
            VGroup(
                Text("SINGULAR COORDINATES", font_size=21, color=GREY_B),
                MathTex(r"\mathbb R^2", font_size=43),
            ).arrange(DOWN, buff=0.14),
            MathTex(r"\xrightarrow{\ \Sigma\ }", font_size=40, color=YELLOW),
            VGroup(
                Text("OUTPUT COORDINATES", font_size=21, color=GREY_B),
                MathTex(r"\mathbb R^3", font_size=43),
            ).arrange(DOWN, buff=0.14),
            MathTex(r"\xrightarrow{\ U\ }", font_size=40, color=GREEN_C),
            VGroup(
                Text("OUTPUT", font_size=24, color=GREEN_C, weight="BOLD"),
                MathTex(r"\mathbb R^3", font_size=43),
            ).arrange(DOWN, buff=0.14),
        ).arrange(RIGHT, buff=0.24).move_to(DOWN * 0.02)
        if pipeline.width > 11.3:
            pipeline.scale_to_fit_width(11.3)
        factorization = MathTex(r"A=U\Sigma V^T", font_size=45, color=YELLOW).to_edge(
            DOWN, buff=0.72
        )
        self.play(FadeIn(pipeline[0]), FadeIn(pipeline[1]), FadeIn(pipeline[2]))
        self.play(FadeIn(pipeline[3]), FadeIn(pipeline[4]))
        self.play(FadeIn(pipeline[5]), FadeIn(pipeline[6]), FadeIn(factorization))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "The columns of V split the input into a surviving and a lost direction."
        )
        self.play(FadeOut(pipeline), FadeOut(factorization))
        v_one = self._matrix([["1"], ["1"]], scale=0.66)
        v_two = self._matrix([["1"], ["-1"]], scale=0.66)
        input_directions = VGroup(
            VGroup(
                Text("SURVIVES", font_size=25, color=TEAL_C, weight="BOLD"),
                VGroup(MathTex(r"v_1=\frac1{\sqrt2}", font_size=38), v_one).arrange(RIGHT, buff=0.12),
                MathTex(r"Av_1=2u_1", font_size=36, color=TEAL_C),
            ).arrange(DOWN, buff=0.24),
            MathTex(r"\perp", font_size=48, color=WHITE),
            VGroup(
                Text("LOST", font_size=25, color=ORANGE, weight="BOLD"),
                VGroup(MathTex(r"v_2=\frac1{\sqrt2}", font_size=38), v_two).arrange(RIGHT, buff=0.12),
                MathTex(r"Av_2=0", font_size=36, color=ORANGE),
            ).arrange(DOWN, buff=0.24),
        ).arrange(RIGHT, buff=0.88).move_to(DOWN * 0.02)
        self.play(FadeIn(input_directions[0]))
        self.play(FadeIn(input_directions[1]), FadeIn(input_directions[2]))
        self.wait(2.2)

        prediction = Text(
            "Pause: which fundamental subspace contains each singular direction?",
            font_size=28,
            color=YELLOW,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.70)
        self.play(FadeIn(prediction))
        self.wait(2.8)

        heading = self._replace_heading(
            heading, "V separates the row space from the null space."
        )
        self.play(FadeOut(input_directions), FadeOut(prediction))
        domain_cards = VGroup(
            self._space_card(
                "ROW SPACE",
                r"\mathcal R(A^T)=\operatorname{span}\{v_1\}",
                "input detected by A",
                TEAL_C,
            ),
            self._space_card(
                "NULL SPACE",
                r"\mathcal N(A)=\operatorname{span}\{v_2\}",
                "input lost by A",
                ORANGE,
            ),
        ).arrange(RIGHT, buff=0.75).move_to(DOWN * 0.02)
        domain_split = MathTex(
            r"\mathbb R^2=\mathcal R(A^T)\oplus\mathcal N(A)",
            font_size=43,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.70)
        self.play(FadeIn(domain_cards[0]))
        self.play(FadeIn(domain_cards[1]), FadeIn(domain_split))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "U separates the column space from the left null space."
        )
        self.play(FadeOut(domain_cards), FadeOut(domain_split))
        codomain_cards = VGroup(
            self._space_card(
                "COLUMN SPACE",
                r"\mathcal R(A)=\operatorname{span}\{u_1\}",
                "outputs produced by A",
                GREEN_C,
            ),
            self._space_card(
                "LEFT NULL SPACE",
                r"\mathcal N(A^T)=\operatorname{span}\{u_2,u_3\}",
                "output directions never reached",
                RED_C,
            ),
        ).arrange(RIGHT, buff=0.65).move_to(DOWN * 0.02)
        codomain_split = MathTex(
            r"\mathbb R^3=\mathcal R(A)\oplus\mathcal N(A^T)",
            font_size=43,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.70)
        self.play(FadeIn(codomain_cards[0]))
        self.play(FadeIn(codomain_cards[1]), FadeIn(codomain_split))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "Only the row-space coordinate passes through Sigma into the column space."
        )
        self.play(FadeOut(codomain_cards), FadeOut(codomain_split))
        active_lane = VGroup(
            MathTex(r"v_1", font_size=41, color=TEAL_C),
            MathTex(r"\xrightarrow{\ \sigma_1=2\ }", font_size=41, color=YELLOW),
            MathTex(r"u_1", font_size=41, color=GREEN_C),
        ).arrange(RIGHT, buff=0.48)
        lost_lane = VGroup(
            MathTex(r"v_2", font_size=41, color=ORANGE),
            MathTex(r"\xrightarrow{\ \sigma_2=0\ }", font_size=41, color=YELLOW),
            MathTex(r"0", font_size=41, color=RED_C),
        ).arrange(RIGHT, buff=0.48)
        unreachable = VGroup(
            MathTex(r"u_2,u_3", font_size=40, color=RED_C),
            Text("complete the output basis but are never produced", font_size=27, color=WHITE),
        ).arrange(RIGHT, buff=0.45)
        lanes = VGroup(active_lane, lost_lane, unreachable).arrange(DOWN, buff=0.48).move_to(DOWN * 0.05)
        self.play(FadeIn(active_lane))
        self.play(FadeIn(lost_lane))
        self.play(FadeIn(unreachable))
        self.wait(2.4)

        heading = self._replace_heading(
            heading, "The full matrices display every active and null direction explicitly."
        )
        self.play(FadeOut(lanes))
        u_matrix = self._matrix(
            [
                [r"\frac1{\sqrt2}", r"\frac1{\sqrt2}", "0"],
                [r"\frac1{\sqrt2}", r"-\frac1{\sqrt2}", "0"],
                ["0", "0", "1"],
            ],
            scale=0.46,
            h_buff=1.12,
            v_buff=0.92,
        )
        sigma_matrix = self._matrix(
            [["2", "0"], ["0", "0"], ["0", "0"]],
            scale=0.53,
            h_buff=0.90,
            v_buff=0.90,
        )
        vt_matrix = self._matrix(
            [
                [r"\frac1{\sqrt2}", r"\frac1{\sqrt2}"],
                [r"\frac1{\sqrt2}", r"-\frac1{\sqrt2}"],
            ],
            scale=0.48,
            h_buff=1.22,
            v_buff=0.96,
        )
        self._compact_entries(u_matrix, 0.76)
        self._compact_entries(vt_matrix, 0.76)
        full_factors = VGroup(
            MathTex(r"A=", font_size=39), u_matrix, sigma_matrix, vt_matrix
        ).arrange(RIGHT, buff=0.23).move_to(DOWN * 0.02)
        factor_labels = VGroup(
            MathTex(r"U\ (3\times3)", font_size=27, color=GREEN_C).next_to(u_matrix, DOWN, buff=0.16),
            MathTex(r"\Sigma\ (3\times2)", font_size=27, color=YELLOW).next_to(sigma_matrix, DOWN, buff=0.16),
            MathTex(r"V^T\ (2\times2)", font_size=27, color=TEAL_C).next_to(vt_matrix, DOWN, buff=0.16),
        )
        self.play(FadeIn(full_factors[0]), FadeIn(u_matrix))
        self.play(FadeIn(sigma_matrix))
        self.play(FadeIn(vt_matrix), FadeIn(factor_labels))
        self.wait(2.5)

        heading = self._replace_heading(
            heading, "Rank fixes the dimensions of all four subspaces."
        )
        self.play(FadeOut(full_factors), FadeOut(factor_labels))
        dimension_cards = VGroup(
            self._space_card("ROW", r"\dim\mathcal R(A^T)=r=1", "inside R2", TEAL_C),
            self._space_card("NULL", r"\dim\mathcal N(A)=n-r=1", "inside R2", ORANGE),
            self._space_card("COLUMN", r"\dim\mathcal R(A)=r=1", "inside R3", GREEN_C),
            self._space_card("LEFT NULL", r"\dim\mathcal N(A^T)=m-r=2", "inside R3", RED_C),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.55, 0.32)).move_to(DOWN * 0.02)
        dimensions = MathTex(r"m=3,\quad n=2,\quad r=1", font_size=40, color=YELLOW).to_edge(
            DOWN, buff=0.60
        )
        self.play(FadeIn(dimension_cards[0]), FadeIn(dimension_cards[1]))
        self.play(FadeIn(dimension_cards[2]), FadeIn(dimension_cards[3]), FadeIn(dimensions))
        self.wait(2.4)

        heading = self._replace_heading(
            heading, "The SVD gives orthonormal bases for every fundamental subspace."
        )
        self.play(FadeOut(dimension_cards), FadeOut(dimensions))
        conclusion = VGroup(
            MathTex(r"V=[\ \mathcal R(A^T)\mid\mathcal N(A)\ ]", font_size=45, color=TEAL_C),
            MathTex(r"U=[\ \mathcal R(A)\mid\mathcal N(A^T)\ ]", font_size=45, color=GREEN_C),
            MathTex(r"\boxed{A=U\Sigma V^T}", font_size=54, color=YELLOW),
            Text(
                "V organizes inputs. U organizes outputs. Sigma connects the active directions.",
                font_size=28,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.40).move_to(DOWN * 0.05)
        self.play(FadeIn(conclusion[0]))
        self.play(FadeIn(conclusion[1]))
        self.play(FadeIn(conclusion[2]))
        self.play(FadeIn(conclusion[3]))
        self.wait(3.0)
