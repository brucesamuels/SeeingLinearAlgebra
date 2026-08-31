"""Manim presentation: Positive Definite Matrices — Why the Singular Value Decomposition?"""
from __future__ import annotations

import numpy as np
from manim import (
    Arrow, Circle, Create, DOWN, Ellipse, FadeIn, FadeOut, GREEN_C, GREY_B,
    LEFT, MathTex, Matrix, ORANGE, RED_C, RIGHT, Scene, SurroundingRectangle,
    TEAL_C, Tex, Text, UP, VGroup, WHITE, YELLOW,
)

from engine.svd_introduction import SingularValueDecompositionIntroduction


class SingularValueDecompositionIntroductionPresentation(Scene):
    CHAPTER_BANNER = "POSITIVE DEFINITE MATRICES"
    LESSON_TITLE = "Why the Singular Value Decomposition?"

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
            r"\textbf{Why the Singular Value Decomposition?}",
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
    def _card(label, content, color):
        body = VGroup(
            Text(label, font_size=27, color=color, weight="BOLD"),
            content,
        ).arrange(DOWN, buff=0.24)
        border = SurroundingRectangle(body, color=color, buff=0.20, stroke_width=2.2)
        return VGroup(border, body)

    def construct(self):
        model = SingularValueDecompositionIntroduction()
        eigenvalues, right_vectors = model.gram_eigendecomposition()
        singular_values = model.singular_values()
        left_vectors = model.left_singular_vectors()
        if not np.allclose(eigenvalues, [3, 1]):
            raise RuntimeError("unexpected Gram eigenvalues")
        if not np.allclose(singular_values, [np.sqrt(3), 1]):
            raise RuntimeError("unexpected singular values")
        if not model.mapped_directions_are_orthogonal():
            raise RuntimeError("mapped right-singular directions are not orthogonal")
        if not np.allclose(model.reconstruction(), model.matrix):
            raise RuntimeError("SVD reconstruction failed")

        banner, title, heading = self._chrome(
            "A-transpose A stores directional information about a rectangular matrix."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        a_matrix = self._matrix(
            [["1", "0"], ["1", "1"], ["0", "1"]], scale=0.78
        )
        gram_matrix = self._matrix([["2", "1"], ["1", "2"]], scale=0.82)
        opening = VGroup(
            VGroup(MathTex("A=", font_size=41), a_matrix).arrange(RIGHT, buff=0.14),
            MathTex(r"\Longrightarrow", font_size=44, color=YELLOW),
            VGroup(MathTex(r"A^TA=", font_size=41), gram_matrix).arrange(RIGHT, buff=0.14),
        ).arrange(RIGHT, buff=0.58).move_to(DOWN * 0.05)
        callback = Text(
            "CP205 proved that this Gram matrix is positive definite.",
            font_size=29,
            color=GREEN_C,
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(opening[0]))
        self.play(FadeIn(opening[1]), FadeIn(opening[2]))
        self.play(FadeIn(callback))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "The eigenvectors of A-transpose A identify special orthonormal input directions."
        )
        self.play(FadeOut(opening), FadeOut(callback))
        v_one = self._matrix([["1"], ["1"]], scale=0.66)
        v_two = self._matrix([["1"], ["-1"]], scale=0.66)
        eig_one = VGroup(
            MathTex(r"v_1=\frac1{\sqrt2}", font_size=39, color=TEAL_C),
            v_one,
            MathTex(r"\lambda_1=3", font_size=39, color=GREEN_C),
        ).arrange(RIGHT, buff=0.24)
        eig_two = VGroup(
            MathTex(r"v_2=\frac1{\sqrt2}", font_size=39, color=ORANGE),
            v_two,
            MathTex(r"\lambda_2=1", font_size=39, color=GREEN_C),
        ).arrange(RIGHT, buff=0.24)
        eigenpairs = VGroup(eig_one, eig_two).arrange(DOWN, buff=0.55).move_to(DOWN * 0.08)
        orthonormal_note = MathTex(
            r"v_i^Tv_j=\delta_{ij}", font_size=39, color=YELLOW
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeIn(eig_one))
        self.play(FadeIn(eig_two))
        self.play(FadeIn(orthonormal_note))
        self.wait(2.0)

        prediction = Text(
            "Pause: what stretch factors should A assign to these directions?",
            font_size=29,
            color=YELLOW,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.72)
        self.play(FadeOut(orthonormal_note), FadeIn(prediction))
        self.wait(2.8)
        self.play(FadeOut(prediction))

        heading = self._replace_heading(
            heading, "Singular values are the nonnegative square roots of the Gram eigenvalues."
        )
        self.play(FadeOut(eigenpairs))
        singular_definition = VGroup(
            Text("singular values", font_size=36, color=YELLOW, weight="BOLD"),
            MathTex(
                r"\boxed{\sigma_i=\sqrt{\lambda_i(A^TA)}}",
                font_size=52,
                color=WHITE,
            ),
            VGroup(
                MathTex(r"\sigma_1=\sqrt3", font_size=46, color=TEAL_C),
                MathTex(r"\sigma_2=1", font_size=46, color=ORANGE),
            ).arrange(RIGHT, buff=1.05),
        ).arrange(DOWN, buff=0.50).move_to(DOWN * 0.10)
        self.play(FadeIn(singular_definition[0]))
        self.play(FadeIn(singular_definition[1]))
        self.play(FadeIn(singular_definition[2]))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Applying A sends each special input direction to a scaled output direction."
        )
        self.play(FadeOut(singular_definition))
        u_one = self._matrix([["1"], ["2"], ["1"]], scale=0.60)
        u_two = self._matrix([["1"], ["0"], ["-1"]], scale=0.60)
        mapping_one = VGroup(
            MathTex(r"Av_1=\sqrt3\,u_1", font_size=42, color=TEAL_C),
            MathTex(r"u_1=\frac1{\sqrt6}", font_size=37),
            u_one,
        ).arrange(RIGHT, buff=0.20)
        mapping_two = VGroup(
            MathTex(r"Av_2=1\,u_2", font_size=42, color=ORANGE),
            MathTex(r"u_2=\frac1{\sqrt2}", font_size=37),
            u_two,
        ).arrange(RIGHT, buff=0.20)
        mappings = VGroup(mapping_one, mapping_two).arrange(DOWN, buff=0.48).move_to(DOWN * 0.08)
        self.play(FadeIn(mapping_one))
        self.play(FadeIn(mapping_two))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "The Gram eigenvectors map to orthogonal output directions."
        )
        self.play(FadeOut(mappings))
        orthogonality = VGroup(
            MathTex(
                r"(Av_i)^T(Av_j)=v_i^TA^TAv_j",
                font_size=47,
                color=WHITE,
            ),
            MathTex(
                r"=v_i^T(\lambda_jv_j)=\lambda_jv_i^Tv_j=0"
                r"\qquad(i\ne j)",
                font_size=43,
                color=YELLOW,
            ),
            MathTex(r"u_1^Tu_2=0", font_size=47, color=GREEN_C),
        ).arrange(DOWN, buff=0.48).move_to(DOWN * 0.08)
        self.play(FadeIn(orthogonality[0]))
        self.play(FadeIn(orthogonality[1]))
        self.play(FadeIn(orthogonality[2]))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "In singular-vector coordinates, A turns a circle into an ellipse."
        )
        self.play(FadeOut(orthogonality))
        input_circle = Circle(radius=1.15, color=TEAL_C, stroke_width=4).move_to(LEFT * 3.25 + DOWN * 0.05)
        input_axes = VGroup(
            Arrow(input_circle.get_center(), input_circle.get_center() + RIGHT * 1.45, buff=0, color=TEAL_C),
            Arrow(input_circle.get_center(), input_circle.get_center() + UP * 1.45, buff=0, color=ORANGE),
        )
        input_labels = VGroup(
            MathTex(r"v_1", font_size=31, color=TEAL_C).next_to(input_axes[0], RIGHT, buff=0.05),
            MathTex(r"v_2", font_size=31, color=ORANGE).next_to(input_axes[1], UP, buff=0.05),
            MathTex(r"\mathbb R^2", font_size=32, color=WHITE).next_to(input_circle, DOWN, buff=0.20),
        )
        output_ellipse = Ellipse(width=4.00, height=2.30, color=GREEN_C, stroke_width=4).move_to(
            RIGHT * 3.10 + DOWN * 0.05
        )
        output_axes = VGroup(
            Arrow(output_ellipse.get_center(), output_ellipse.get_center() + RIGHT * 2.22, buff=0, color=TEAL_C),
            Arrow(output_ellipse.get_center(), output_ellipse.get_center() + UP * 1.42, buff=0, color=ORANGE),
        )
        output_labels = VGroup(
            MathTex(r"\sqrt3\,u_1", font_size=31, color=TEAL_C).next_to(output_axes[0], RIGHT, buff=0.05),
            MathTex(r"1\,u_2", font_size=31, color=ORANGE).next_to(output_axes[1], UP, buff=0.05),
            Text("column space of A", font_size=25, color=WHITE).next_to(output_ellipse, DOWN, buff=0.20),
        )
        map_arrow = Arrow(LEFT * 1.28, RIGHT * 1.05, color=YELLOW, buff=0.10)
        map_label = MathTex("A", font_size=38, color=YELLOW).next_to(map_arrow, UP, buff=0.10)
        self.play(Create(input_circle), FadeIn(input_axes), FadeIn(input_labels))
        self.play(Create(map_arrow), FadeIn(map_label))
        self.play(Create(output_ellipse), FadeIn(output_axes), FadeIn(output_labels))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "The SVD separates the transformation into orthogonal coordinates and diagonal stretching."
        )
        self.play(
            FadeOut(input_circle), FadeOut(input_axes), FadeOut(input_labels),
            FadeOut(output_ellipse), FadeOut(output_axes), FadeOut(output_labels),
            FadeOut(map_arrow), FadeOut(map_label),
        )
        pipeline = VGroup(
            self._card("input", MathTex("x", font_size=42), WHITE),
            MathTex(r"\xrightarrow{\ V^T\ }", font_size=41, color=TEAL_C),
            self._card("singular coordinates", MathTex(r"V^Tx", font_size=38), TEAL_C),
            MathTex(r"\xrightarrow{\ \Sigma\ }", font_size=41, color=YELLOW),
            self._card("stretched", MathTex(r"\Sigma V^Tx", font_size=36), YELLOW),
            MathTex(r"\xrightarrow{\ U\ }", font_size=41, color=GREEN_C),
            self._card("output", MathTex("Ax", font_size=40), GREEN_C),
        ).arrange(RIGHT, buff=0.22).move_to(DOWN * 0.06)
        if pipeline.width > 11.5:
            pipeline.scale_to_fit_width(11.5)
        self.play(FadeIn(pipeline[0]), FadeIn(pipeline[1]), FadeIn(pipeline[2]))
        self.play(FadeIn(pipeline[3]), FadeIn(pipeline[4]))
        self.play(FadeIn(pipeline[5]), FadeIn(pipeline[6]))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "For this rectangular matrix, the three factors can be written explicitly."
        )
        self.play(FadeOut(pipeline))
        u_matrix = self._matrix(
            [
                [r"\frac1{\sqrt6}", r"\frac1{\sqrt2}"],
                [r"\frac2{\sqrt6}", "0"],
                [r"\frac1{\sqrt6}", r"-\frac1{\sqrt2}"],
            ],
            scale=0.54,
            h_buff=1.55,
            v_buff=1.05,
        )
        sigma_matrix = self._matrix(
            [[r"\sqrt3", "0"], ["0", "1"]], scale=0.62, h_buff=1.10
        )
        vt_matrix = self._matrix(
            [
                [r"\frac1{\sqrt2}", r"\frac1{\sqrt2}"],
                [r"\frac1{\sqrt2}", r"-\frac1{\sqrt2}"],
            ],
            scale=0.54,
            h_buff=1.55,
            v_buff=1.05,
        )
        u_entries = list(u_matrix.get_entries())
        vt_entries = list(vt_matrix.get_entries())
        for entry in [*u_entries, *vt_entries]:
            entry.scale(0.78)
        u_entries[3].move_to([
            u_entries[1].get_center()[0],
            u_entries[2].get_center()[1],
            0,
        ])
        factorization = VGroup(
            MathTex("A=", font_size=40),
            u_matrix,
            sigma_matrix,
            vt_matrix,
        ).arrange(RIGHT, buff=0.25).move_to(DOWN * 0.02)
        if factorization.width > 11.2:
            factorization.scale_to_fit_width(11.2)
        factor_labels = VGroup(
            MathTex("U", font_size=32, color=GREEN_C).next_to(u_matrix, DOWN, buff=0.18),
            MathTex(r"\Sigma", font_size=32, color=YELLOW).next_to(sigma_matrix, DOWN, buff=0.18),
            MathTex(r"V^T", font_size=32, color=TEAL_C).next_to(vt_matrix, DOWN, buff=0.18),
        )
        self.play(FadeIn(factorization[0]), FadeIn(u_matrix))
        self.play(FadeIn(sigma_matrix))
        self.play(FadeIn(vt_matrix), FadeIn(factor_labels))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "The singular value decomposition extends spectral structure to every real matrix."
        )
        self.play(FadeOut(factorization), FadeOut(factor_labels))
        final = VGroup(
            Text("singular value decomposition", font_size=35, color=YELLOW, weight="BOLD"),
            MathTex(r"\boxed{A=U\Sigma V^T}", font_size=58, color=WHITE),
            VGroup(
                Text("V", font_size=30, color=TEAL_C, weight="BOLD"),
                Text("orthonormal input directions", font_size=27, color=WHITE),
                Text("Σ", font_size=30, color=YELLOW, weight="BOLD"),
                Text("nonnegative stretches", font_size=27, color=WHITE),
                Text("U", font_size=30, color=GREEN_C, weight="BOLD"),
                Text("orthonormal output directions", font_size=27, color=WHITE),
            ).arrange_in_grid(rows=3, cols=2, buff=(0.32, 0.25), col_alignments="ll"),
            Text(
                "Next: compute the factors systematically from A-transpose A.",
                font_size=27,
                color=GREY_B,
            ),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.10)
        self.play(FadeIn(final[0]))
        self.play(FadeIn(final[1]))
        self.play(FadeIn(final[2]))
        self.play(FadeIn(final[3]))
        self.wait(2.8)
