"""Manim presentation: Positive Definite Matrices — Computing the SVD from A-transpose A."""
from __future__ import annotations

import numpy as np
from manim import (
    FadeIn, FadeOut, GREEN_C, GREY_B, LEFT, MathTex, Matrix, ORANGE,
    RIGHT, Scene, SurroundingRectangle, TEAL_C, Tex, Text, UP, DOWN,
    VGroup, WHITE, YELLOW,
)

from engine.svd_computation import SingularValueDecompositionComputation


class SingularValueDecompositionComputationPresentation(Scene):
    CHAPTER_BANNER = "POSITIVE DEFINITE MATRICES"
    LESSON_TITLE = "Computing the SVD from AᵀA"

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
            r"\textbf{Computing the SVD from }$A^TA$",
            font_size=34,
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

    @staticmethod
    def _step(number, title_text, formula, color):
        content = VGroup(
            Text(f"STEP {number}", font_size=22, color=color, weight="BOLD"),
            Text(title_text, font_size=28, color=WHITE, weight="BOLD"),
            MathTex(formula, font_size=39, color=color),
        ).arrange(DOWN, buff=0.18)
        border = SurroundingRectangle(content, color=color, buff=0.20, stroke_width=2.2)
        return VGroup(border, content)

    def construct(self):
        model = SingularValueDecompositionComputation()
        eigenvalues, eigenvectors = model.gram_eigenpairs()
        if not np.allclose(eigenvalues, [4, 2]):
            raise RuntimeError("unexpected Gram eigenvalues")
        if not np.allclose(model.singular_values(), [2, np.sqrt(2)]):
            raise RuntimeError("unexpected singular values")
        if not np.allclose(model.reconstruction(), model.matrix):
            raise RuntimeError("thin SVD reconstruction failed")

        banner, title, heading = self._chrome(
            "The SVD separates a matrix into three meaningful factors."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        b_matrix = self._matrix(
            [["1", "1"], ["1", "-1"], ["1", "1"]], scale=0.80
        )
        opening = VGroup(
            VGroup(MathTex("B=", font_size=42), b_matrix).arrange(RIGHT, buff=0.14),
            VGroup(
                Text("Goal", font_size=29, color=YELLOW, weight="BOLD"),
                MathTex(r"B=U\Sigma V^T", font_size=48, color=WHITE),
                Text("compute every factor", font_size=28, color=GREEN_C),
            ).arrange(DOWN, buff=0.32),
        ).arrange(RIGHT, buff=1.35).move_to(DOWN * 0.08)
        dimensions = MathTex(
            r"B:\ 3\times2", font_size=35, color=TEAL_C
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(opening[0]))
        self.play(FadeIn(opening[1]))
        self.play(FadeIn(dimensions))
        self.wait(1.8)

        heading = self._replace_heading(
            heading, "Step 1: form the symmetric Gram matrix."
        )
        self.play(FadeOut(opening), FadeOut(dimensions))
        b_again = self._matrix(
            [["1", "1"], ["1", "-1"], ["1", "1"]], scale=0.68
        )
        gram = self._matrix([["3", "1"], ["1", "3"]], scale=0.82)
        gram_computation = VGroup(
            VGroup(MathTex("B=", font_size=38), b_again).arrange(RIGHT, buff=0.12),
            MathTex(r"\Longrightarrow", font_size=43, color=YELLOW),
            VGroup(MathTex(r"B^TB=", font_size=40), gram).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.55).move_to(DOWN * 0.02)
        gram_note = Text(
            "The right singular vectors come from this two-by-two matrix.",
            font_size=28,
            color=GREEN_C,
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(gram_computation))
        self.play(FadeIn(gram_note))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Step 2: solve the Gram-matrix eigenvalue equation."
        )
        self.play(FadeOut(gram_computation), FadeOut(gram_note))
        characteristic = VGroup(
            MathTex(
                r"\det(B^TB-\lambda I)=(3-\lambda)^2-1",
                font_size=47,
                color=WHITE,
            ),
            MathTex(
                r"=(\lambda-4)(\lambda-2)=0",
                font_size=47,
                color=YELLOW,
            ),
            VGroup(
                MathTex(r"\lambda_1=4", font_size=43, color=TEAL_C),
                MathTex(r"\lambda_2=2", font_size=43, color=ORANGE),
            ).arrange(RIGHT, buff=1.10),
        ).arrange(DOWN, buff=0.46).move_to(DOWN * 0.08)
        self.play(FadeIn(characteristic[0]))
        self.play(FadeIn(characteristic[1]))
        self.play(FadeIn(characteristic[2]))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Step 3: normalize the corresponding eigenvectors."
        )
        self.play(FadeOut(characteristic))
        v_one = self._matrix([["1"], ["1"]], scale=0.66)
        v_two = self._matrix([["1"], ["-1"]], scale=0.66)
        right_vectors = VGroup(
            VGroup(
                MathTex(r"v_1=\frac1{\sqrt2}", font_size=40, color=TEAL_C),
                v_one,
            ).arrange(RIGHT, buff=0.18),
            VGroup(
                MathTex(r"v_2=\frac1{\sqrt2}", font_size=40, color=ORANGE),
                v_two,
            ).arrange(RIGHT, buff=0.18),
        ).arrange(RIGHT, buff=1.20).move_to(DOWN * 0.05)
        v_note = MathTex(
            r"V=[\,v_1\ v_2\,],\qquad V^TV=I",
            font_size=40,
            color=GREEN_C,
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(right_vectors))
        self.play(FadeIn(v_note))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Step 4: take nonnegative square roots to obtain the singular values."
        )
        self.play(FadeOut(right_vectors), FadeOut(v_note))
        singular_values = VGroup(
            MathTex(r"\sigma_i=\sqrt{\lambda_i}", font_size=50, color=WHITE),
            VGroup(
                MathTex(r"\sigma_1=\sqrt4=2", font_size=45, color=TEAL_C),
                MathTex(r"\sigma_2=\sqrt2", font_size=45, color=ORANGE),
            ).arrange(RIGHT, buff=1.00),
            MathTex(
                r"\Sigma=\operatorname{diag}(2,\sqrt2)",
                font_size=44,
                color=YELLOW,
            ),
        ).arrange(DOWN, buff=0.48).move_to(DOWN * 0.08)
        self.play(FadeIn(singular_values[0]))
        self.play(FadeIn(singular_values[1]))
        self.play(FadeIn(singular_values[2]))
        self.wait(1.8)

        prediction = Text(
            "Pause: how can we recover U without solving another eigenvalue problem?",
            font_size=29,
            color=YELLOW,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(prediction))
        self.wait(2.8)
        self.play(FadeOut(prediction))

        heading = self._replace_heading(
            heading, "Step 5: map each right singular vector and divide by its singular value."
        )
        self.play(FadeOut(singular_values))
        recovery_rule = VGroup(
            MathTex(
                r"\boxed{u_i=\frac{Bv_i}{\sigma_i}}",
                font_size=53,
                color=YELLOW,
            ),
            MathTex(r"Bv_i=\sigma_i u_i", font_size=44, color=WHITE),
            Text(
                "No second eigenvalue computation is needed.",
                font_size=30,
                color=GREEN_C,
                weight="BOLD",
            ),
        ).arrange(DOWN, buff=0.50).move_to(DOWN * 0.08)
        self.play(FadeIn(recovery_rule[0]))
        self.play(FadeIn(recovery_rule[1]))
        self.play(FadeIn(recovery_rule[2]))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "The first mapped direction has length 2."
        )
        self.play(FadeOut(recovery_rule))
        mapped_one = self._matrix([[r"\sqrt2"], ["0"], [r"\sqrt2"]], scale=0.66)
        u_one = self._matrix([["1"], ["0"], ["1"]], scale=0.62)
        first_left = VGroup(
            VGroup(MathTex(r"Bv_1=", font_size=40), mapped_one).arrange(RIGHT, buff=0.14),
            MathTex(r"\Longrightarrow", font_size=41, color=YELLOW),
            VGroup(
                MathTex(r"u_1=\frac1{2}Bv_1=\frac1{\sqrt2}", font_size=38, color=TEAL_C),
                u_one,
            ).arrange(RIGHT, buff=0.14),
        ).arrange(RIGHT, buff=0.42).move_to(DOWN * 0.04)
        self.play(FadeIn(first_left[0]))
        self.play(FadeIn(first_left[1]), FadeIn(first_left[2]))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "The second mapped direction has length square root of 2."
        )
        self.play(FadeOut(first_left))
        mapped_two = self._matrix([["0"], [r"\sqrt2"], ["0"]], scale=0.66)
        u_two = self._matrix([["0"], ["1"], ["0"]], scale=0.62)
        second_left = VGroup(
            VGroup(MathTex(r"Bv_2=", font_size=40), mapped_two).arrange(RIGHT, buff=0.14),
            MathTex(r"\Longrightarrow", font_size=41, color=YELLOW),
            VGroup(
                MathTex(r"u_2=\frac1{\sqrt2}Bv_2=", font_size=38, color=ORANGE),
                u_two,
            ).arrange(RIGHT, buff=0.14),
        ).arrange(RIGHT, buff=0.42).move_to(DOWN * 0.04)
        orthonormal_u = MathTex(
            r"U=[\,u_1\ u_2\,],\qquad U^TU=I",
            font_size=40,
            color=GREEN_C,
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(second_left[0]))
        self.play(FadeIn(second_left[1]), FadeIn(second_left[2]))
        self.play(FadeIn(orthonormal_u))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Assemble the thin SVD with dimensions 3-by-2, 2-by-2, and 2-by-2."
        )
        self.play(FadeOut(second_left), FadeOut(orthonormal_u))
        u_matrix = self._matrix(
            [
                [r"\frac1{\sqrt2}", "0"],
                ["0", "1"],
                [r"\frac1{\sqrt2}", "0"],
            ],
            scale=0.58,
            h_buff=1.40,
            v_buff=1.02,
        )
        sigma_matrix = self._matrix(
            [["2", "0"], ["0", r"\sqrt2"]], scale=0.64, h_buff=1.08
        )
        vt_matrix = self._matrix(
            [
                [r"\frac1{\sqrt2}", r"\frac1{\sqrt2}"],
                [r"\frac1{\sqrt2}", r"-\frac1{\sqrt2}"],
            ],
            scale=0.56,
            h_buff=1.50,
            v_buff=1.02,
        )
        self._compact_entries(u_matrix, 0.78)
        self._compact_entries(vt_matrix, 0.78)
        factorization = VGroup(
            MathTex("B=", font_size=40), u_matrix, sigma_matrix, vt_matrix
        ).arrange(RIGHT, buff=0.26).move_to(DOWN * 0.02)
        if factorization.width > 11.2:
            factorization.scale_to_fit_width(11.2)
        labels = VGroup(
            MathTex(r"U\ (3\times2)", font_size=29, color=GREEN_C).next_to(u_matrix, DOWN, buff=0.18),
            MathTex(r"\Sigma\ (2\times2)", font_size=29, color=YELLOW).next_to(sigma_matrix, DOWN, buff=0.18),
            MathTex(r"V^T\ (2\times2)", font_size=29, color=TEAL_C).next_to(vt_matrix, DOWN, buff=0.18),
        )
        self.play(FadeIn(factorization[0]), FadeIn(u_matrix))
        self.play(FadeIn(sigma_matrix))
        self.play(FadeIn(vt_matrix), FadeIn(labels))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "Multiplying the three structural factors reconstructs the original matrix."
        )
        self.play(FadeOut(factorization), FadeOut(labels))
        reconstructed = self._matrix(
            [["1", "1"], ["1", "-1"], ["1", "1"]], scale=0.82
        )
        verification = VGroup(
            MathTex(r"U\Sigma V^T=", font_size=47, color=YELLOW),
            reconstructed,
            MathTex("=B", font_size=47, color=GREEN_C),
        ).arrange(RIGHT, buff=0.28).move_to(DOWN * 0.02)
        verify_note = Text(
            "The thin factors reproduce every entry of B.",
            font_size=29,
            color=WHITE,
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(verification))
        self.play(FadeIn(verify_note))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Singular-vector signs are not unique, but the matrix product is unchanged."
        )
        self.play(FadeOut(verification), FadeOut(verify_note))
        sign_choice = VGroup(
            MathTex(
                r"u_i\mapsto -u_i,\qquad v_i\mapsto -v_i",
                font_size=48,
                color=YELLOW,
            ),
            MathTex(
                r"\sigma_i(-u_i)(-v_i)^T=\sigma_i u_iv_i^T",
                font_size=46,
                color=WHITE,
            ),
            Text(
                "Different signs — the same SVD product",
                font_size=31,
                color=GREEN_C,
                weight="BOLD",
            ),
        ).arrange(DOWN, buff=0.48).move_to(DOWN * 0.08)
        self.play(FadeIn(sign_choice[0]))
        self.play(FadeIn(sign_choice[1]))
        self.play(FadeIn(sign_choice[2]))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "The same five-step recipe computes any full-column-rank thin SVD."
        )
        self.play(FadeOut(sign_choice))
        recipe = VGroup(
            self._step(1, "Form the Gram matrix", r"A^TA", TEAL_C),
            self._step(2, "Find ordered eigenpairs", r"(\lambda_i,v_i)", ORANGE),
            self._step(3, "Take square roots", r"\sigma_i=\sqrt{\lambda_i}", YELLOW),
            self._step(4, "Recover left directions", r"u_i=Av_i/\sigma_i", GREEN_C),
            self._step(5, "Assemble", r"A=U\Sigma V^T", WHITE),
        ).arrange(RIGHT, buff=0.22).move_to(DOWN * 0.08)
        if recipe.width > 11.5:
            recipe.scale_to_fit_width(11.5)
        self.play(FadeIn(recipe[0]), FadeIn(recipe[1]))
        self.play(FadeIn(recipe[2]))
        self.play(FadeIn(recipe[3]), FadeIn(recipe[4]))
        self.wait(2.8)
