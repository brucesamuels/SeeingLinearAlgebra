"""Manim presentation: Positive Definite Matrices — The Big Picture."""
from __future__ import annotations

import numpy as np
from manim import (
    DOWN, FadeIn, FadeOut, GREEN_C, GREY_B, MathTex, Matrix, ORANGE, RIGHT,
    Scene, SurroundingRectangle, TEAL_C, Tex, Text, UP, VGroup, WHITE, YELLOW,
)

from engine.positive_definiteness_summary import PositiveDefinitenessSummary


class PositiveDefinitenessSummaryPresentation(Scene):
    CHAPTER_BANNER = "POSITIVE DEFINITE MATRICES"
    LESSON_TITLE = "Positive Definiteness: The Big Picture"

    def _heading(self, text):
        item = Text(text, font_size=27, color=WHITE)
        if item.width > 11.4:
            item.scale_to_fit_width(11.4)
        return item

    def _chrome(self, heading_text):
        banner = Tex(
            r"\textbf{POSITIVE DEFINITE MATRICES}", font_size=24, color=GREY_B
        ).to_edge(UP, buff=0.16)
        title = Tex(
            r"\textbf{Positive Definiteness: The Big Picture}",
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
        for entry, center in zip(entries, centers):
            entry.scale(factor).move_to(center)
        return entries

    def _matrix_card(self, name, entries, color):
        matrix = self._matrix(entries, scale=0.66)
        content = VGroup(
            Text(name, font_size=27, color=color, weight="BOLD"),
            matrix,
        ).arrange(DOWN, buff=0.20)
        border = SurroundingRectangle(content, color=color, buff=0.24, stroke_width=2.2)
        return VGroup(border, content)

    @staticmethod
    def _test_card(title_text, formula, color, subtitle=None):
        items = [
            Text(title_text, font_size=26, color=color, weight="BOLD"),
            MathTex(formula, font_size=38, color=WHITE),
        ]
        if subtitle:
            items.append(Text(subtitle, font_size=23, color=color))
        content = VGroup(*items).arrange(DOWN, buff=0.17)
        border = SurroundingRectangle(content, color=color, buff=0.22, stroke_width=2.1)
        return VGroup(border, content)

    def construct(self):
        positive = PositiveDefinitenessSummary()
        semidefinite = PositiveDefinitenessSummary([[1, 1], [1, 1]])
        indefinite = PositiveDefinitenessSummary([[1, 0], [0, -1]])
        if positive.classification() != "positive definite":
            raise RuntimeError("positive-definite summary example failed")
        if semidefinite.classification() != "positive semidefinite":
            raise RuntimeError("positive-semidefinite summary example failed")
        if indefinite.classification() != "indefinite":
            raise RuntimeError("indefinite summary example failed")
        if not all(positive.positive_definite_checks().values()):
            raise RuntimeError("positive-definite equivalence checks disagree")

        banner, title, heading = self._chrome(
            "Three symmetric matrices can produce three different kinds of energy."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        mystery_cards = VGroup(
            self._matrix_card("Matrix A", [["2", "1"], ["1", "2"]], TEAL_C),
            self._matrix_card("Matrix B", [["1", "1"], ["1", "1"]], ORANGE),
            self._matrix_card("Matrix C", [["1", "0"], ["0", "-1"]], YELLOW),
        ).arrange(RIGHT, buff=0.58).move_to(DOWN * 0.03)
        prediction = Text(
            "Pause: which matrices have strictly positive energy in every nonzero direction?",
            font_size=28,
            color=YELLOW,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(mystery_cards[0]), FadeIn(mystery_cards[1]), FadeIn(mystery_cards[2]))
        self.play(FadeIn(prediction))
        self.wait(3.0)
        self.play(FadeOut(prediction))

        heading = self._replace_heading(
            heading, "The sign of x-transpose A x classifies the quadratic energy."
        )
        self.play(FadeOut(mystery_cards))
        classifications = VGroup(
            self._test_card(
                "POSITIVE DEFINITE",
                r"x^TAx>0\quad(x\ne0)",
                TEAL_C,
                "strictly positive",
            ),
            self._test_card(
                "POSITIVE SEMIDEFINITE",
                r"x^TBx\ge0",
                ORANGE,
                "zero is possible",
            ),
            self._test_card(
                "INDEFINITE",
                r"x^TCx\text{ has both signs}",
                YELLOW,
                "positive and negative",
            ),
        ).arrange(RIGHT, buff=0.34).move_to(DOWN * 0.04)
        if classifications.width > 11.4:
            classifications.scale_to_fit_width(11.4)
        evidence = VGroup(
            MathTex(r"A:\ \lambda=1,3", font_size=31, color=TEAL_C),
            MathTex(r"B:\ (1,-1)^TB(1,-1)=0", font_size=31, color=ORANGE),
            MathTex(r"C:\ q(1,0)=1,\ q(0,1)=-1", font_size=31, color=YELLOW),
        ).arrange(RIGHT, buff=0.42).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(classifications[0]))
        self.play(FadeIn(classifications[1]))
        self.play(FadeIn(classifications[2]))
        self.play(FadeIn(evidence))
        self.wait(2.4)

        heading = self._replace_heading(
            heading, "For a real symmetric matrix, several tests answer the same question."
        )
        self.play(FadeOut(classifications), FadeOut(evidence))
        a_matrix = self._matrix([["2", "1"], ["1", "2"]], scale=0.78)
        focus = VGroup(
            VGroup(MathTex(r"A=", font_size=42), a_matrix).arrange(RIGHT, buff=0.14),
            MathTex(r"A=A^T", font_size=40, color=TEAL_C),
            Text("Is every nonzero directional energy positive?", font_size=30, color=GREEN_C),
        ).arrange(DOWN, buff=0.42).move_to(DOWN * 0.04)
        self.play(FadeIn(focus[0]))
        self.play(FadeIn(focus[1]), FadeIn(focus[2]))
        self.wait(1.8)

        heading = self._replace_heading(
            heading, "The definition and the eigenvalue test describe directional energy."
        )
        self.play(FadeOut(focus))
        spectral_tests = VGroup(
            self._test_card(
                "ENERGY TEST",
                r"x^TAx>0\quad\forall x\ne0",
                TEAL_C,
                "the definition",
            ),
            MathTex(r"\Longleftrightarrow", font_size=48, color=YELLOW),
            self._test_card(
                "EIGENVALUE TEST",
                r"\lambda_1=1,\ \lambda_2=3",
                ORANGE,
                "every eigenvalue is positive",
            ),
        ).arrange(RIGHT, buff=0.48).move_to(DOWN * 0.04)
        spectral_note = MathTex(
            r"x^TAx=\lambda_1c_1^2+\lambda_2c_2^2",
            font_size=39,
            color=GREEN_C,
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(spectral_tests[0]))
        self.play(FadeIn(spectral_tests[1]), FadeIn(spectral_tests[2]))
        self.play(FadeIn(spectral_note))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "Elimination turns the same question into pivots and determinants."
        )
        self.play(FadeOut(spectral_tests), FadeOut(spectral_note))
        elimination_tests = VGroup(
            self._test_card(
                "PIVOT TEST",
                r"p_1=2,\quad p_2=\frac32",
                TEAL_C,
                "every pivot is positive",
            ),
            MathTex(r"\Longleftrightarrow", font_size=46, color=YELLOW),
            self._test_card(
                "MINOR TEST",
                r"\Delta_1=2,\quad\Delta_2=3",
                ORANGE,
                "every leading minor is positive",
            ),
        ).arrange(RIGHT, buff=0.42).move_to(DOWN * 0.04)
        pivot_minor_relation = MathTex(
            r"p_k=\frac{\Delta_k}{\Delta_{k-1}},\qquad \Delta_0=1",
            font_size=39,
            color=GREEN_C,
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(elimination_tests[0]))
        self.play(FadeIn(elimination_tests[1]), FadeIn(elimination_tests[2]))
        self.play(FadeIn(pivot_minor_relation))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "Factorizations expose positive energy as weighted squares or a norm."
        )
        self.play(FadeOut(elimination_tests), FadeOut(pivot_minor_relation))
        d_matrix = self._matrix([["2", "0"], ["0", r"\frac32"]], scale=0.70, v_buff=1.00)
        self._compact_entries(d_matrix, 0.82)
        factorization_tests = VGroup(
            VGroup(
                Text("LDLᵀ", font_size=28, color=TEAL_C, weight="BOLD"),
                VGroup(MathTex(r"D=", font_size=39), d_matrix).arrange(RIGHT, buff=0.12),
                MathTex(r"x^TAx=y^TDy", font_size=36, color=TEAL_C),
            ).arrange(DOWN, buff=0.20),
            MathTex(r"\Longleftrightarrow", font_size=46, color=YELLOW),
            VGroup(
                Text("CHOLESKY", font_size=28, color=ORANGE, weight="BOLD"),
                MathTex(r"A=R^TR", font_size=43, color=WHITE),
                MathTex(r"x^TAx=\lVert Rx\rVert^2", font_size=36, color=ORANGE),
            ).arrange(DOWN, buff=0.28),
        ).arrange(RIGHT, buff=0.64).move_to(DOWN * 0.04)
        factor_note = Text(
            "Positive diagonal D and invertible R certify positive definiteness.",
            font_size=28,
            color=GREEN_C,
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(factorization_tests[0]))
        self.play(FadeIn(factorization_tests[1]), FadeIn(factorization_tests[2]))
        self.play(FadeIn(factor_note))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "Six equivalent statements form one positive-definiteness toolkit."
        )
        self.play(FadeOut(factorization_tests), FadeOut(factor_note))
        toolkit = VGroup(
            self._test_card("ENERGY", r"x^TAx>0", TEAL_C),
            self._test_card("EIGENVALUES", r"\lambda_i>0", ORANGE),
            self._test_card("PIVOTS", r"p_i>0", YELLOW),
            self._test_card("LEADING MINORS", r"\Delta_i>0", GREEN_C),
            self._test_card("LDLᵀ", r"D>0", TEAL_C),
            self._test_card("CHOLESKY", r"A=R^TR", ORANGE),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.34, 0.30)).move_to(DOWN * 0.05)
        if toolkit.width > 11.3:
            toolkit.scale_to_fit_width(11.3)
        self.play(FadeIn(toolkit[0]), FadeIn(toolkit[1]), FadeIn(toolkit[2]))
        self.play(FadeIn(toolkit[3]), FadeIn(toolkit[4]), FadeIn(toolkit[5]))
        self.wait(2.5)

        heading = self._replace_heading(
            heading, "Choose the test that best matches the information you already have."
        )
        self.play(FadeOut(toolkit))
        decision = VGroup(
            self._test_card("GEOMETRY", r"x^TAx", TEAL_C, "inspect directional energy"),
            self._test_card("SPECTRAL DATA", r"\lambda_i", ORANGE, "inspect eigenvalue signs"),
            self._test_card("ELIMINATION", r"p_i,\ \Delta_i", YELLOW, "reuse pivots or minors"),
            self._test_card("SOLVING", r"R^TR", GREEN_C, "use Cholesky"),
        ).arrange(RIGHT, buff=0.24).move_to(DOWN * 0.04)
        if decision.width > 11.4:
            decision.scale_to_fit_width(11.4)
        decision_note = Text(
            "Different computations — the same conclusion.",
            font_size=30,
            color=WHITE,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(decision[0]), FadeIn(decision[1]))
        self.play(FadeIn(decision[2]), FadeIn(decision[3]))
        self.play(FadeIn(decision_note))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "The same energy idea explains several important applications."
        )
        self.play(FadeOut(decision), FadeOut(decision_note))
        applications = VGroup(
            self._test_card("GRAM MATRICES", r"x^TA^TAx=\lVert Ax\rVert^2", TEAL_C),
            self._test_card("COVARIANCE", r"v^T\Sigma v\ge0", ORANGE),
            self._test_card("SVD", r"\lambda_i(A^TA)=\sigma_i^2", YELLOW),
            self._test_card("MINIMIZATION", r"Kc=f", GREEN_C),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.50, 0.30)).move_to(DOWN * 0.05)
        application_note = Text(
            "Strictly positive energy gives a unique minimizer and a uniquely solvable system.",
            font_size=27,
            color=WHITE,
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(applications[0]), FadeIn(applications[1]))
        self.play(FadeIn(applications[2]), FadeIn(applications[3]))
        self.play(FadeIn(application_note))
        self.wait(2.4)

        heading = self._replace_heading(
            heading, "Positive definiteness is one idea seen through many mathematical lenses."
        )
        self.play(FadeOut(applications), FadeOut(application_note))
        conclusion = VGroup(
            MathTex(
                r"\boxed{x^TAx>0\ \text{ for every }x\ne0}",
                font_size=52,
                color=YELLOW,
            ),
            VGroup(
                Text("positive energy", font_size=29, color=TEAL_C, weight="BOLD"),
                MathTex(r"\Longrightarrow", font_size=40, color=WHITE),
                Text("unique minimum", font_size=29, color=ORANGE, weight="BOLD"),
                MathTex(r"\Longrightarrow", font_size=40, color=WHITE),
                Text("unique solution", font_size=29, color=GREEN_C, weight="BOLD"),
            ).arrange(RIGHT, buff=0.28),
            Text(
                "Energy, eigenvalues, elimination, and factorization all tell the same story.",
                font_size=28,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.52).move_to(DOWN * 0.04)
        self.play(FadeIn(conclusion[0]))
        self.play(FadeIn(conclusion[1]))
        self.play(FadeIn(conclusion[2]))
        self.wait(3.0)
