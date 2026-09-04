"""Manim presentation: Principal Component Analysis through the SVD."""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    BLUE_C,
    DashedLine,
    Dot,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN_C,
    GREY_B,
    LEFT,
    Line,
    MathTex,
    Matrix,
    NumberPlane,
    ORANGE,
    ReplacementTransform,
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

from engine.pca_svd import PCASVD


class PCASVDPresentation(Scene):
    CHAPTER_BANNER = "SINGULAR VALUES, RANK, AND APPROXIMATION"
    LESSON_TITLE = "Principal Component Analysis through the SVD"

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
            r"\textbf{Principal Component Analysis through the SVD}",
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
    def _matrix(entries, scale=0.52, h_buff=1.05, v_buff=0.88):
        return Matrix(entries, h_buff=h_buff, v_buff=v_buff).scale(scale)

    @staticmethod
    def _card(label, formula, note, color, formula_size=36):
        body = VGroup(
            Text(label, font_size=23, color=color, weight="BOLD"),
            MathTex(formula, font_size=formula_size, color=WHITE),
            Text(note, font_size=21, color=GREY_B),
        ).arrange(DOWN, buff=0.17)
        border = SurroundingRectangle(body, color=color, buff=0.17, stroke_width=2.0)
        return VGroup(border, body)

    @staticmethod
    def _plane():
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=5.0,
            y_length=5.0,
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_width": 1.0,
                "stroke_opacity": 0.28,
            },
            axis_config={"stroke_color": GREY_B, "stroke_width": 1.6},
        )
        return plane

    @staticmethod
    def _dots(plane, points, color=ORANGE, radius=0.075):
        return VGroup(
            *[
                Dot(plane.c2p(float(x), float(y)), radius=radius, color=color)
                for x, y in points
            ]
        )

    @staticmethod
    def _principal_axes(plane):
        main = Line(plane.c2p(-3.7, -3.7), plane.c2p(3.7, 3.7), color=GREEN_C, stroke_width=4)
        minor = Line(plane.c2p(-3.2, 3.2), plane.c2p(3.2, -3.2), color=BLUE_C, stroke_width=3)
        v1 = MathTex(r"v_1", font_size=31, color=GREEN_C).next_to(main.get_end(), LEFT, buff=0.08)
        v2 = MathTex(r"v_2", font_size=31, color=BLUE_C).next_to(minor.get_start(), RIGHT, buff=0.08)
        return VGroup(main, minor, v1, v2)

    def construct(self):
        model = PCASVD()
        if model.shape != (6, 2):
            raise RuntimeError("unexpected PCA data dimensions")
        if not np.allclose(model.gram_matrix(), [[28, 26], [26, 28]]):
            raise RuntimeError("unexpected PCA Gram matrix")
        if not np.isclose(model.explained_variance_ratio(1), 54 / 56):
            raise RuntimeError("unexpected first-component variation")

        data = model.data()
        rank_one = model.reconstruction(1)
        first_direction = model.principal_directions()[:, 0]

        banner, title, heading = self._chrome(
            "Can a two-coordinate dataset be represented faithfully by one coordinate?"
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        plane = self._plane().move_to(DOWN * 0.08)
        dots = self._dots(plane, data)
        question = VGroup(
            Text("six observations", font_size=25, color=TEAL_C, weight="BOLD"),
            MathTex(r"(x_i,y_i)\in\mathbb R^2", font_size=37, color=WHITE),
            Text("look for one informative direction", font_size=24, color=YELLOW),
        ).arrange(DOWN, buff=0.24).to_edge(RIGHT, buff=0.62).shift(DOWN * 0.08)
        plane_group = VGroup(plane, dots).shift(LEFT * 2.35)
        self.play(FadeIn(plane_group))
        self.play(FadeIn(question))
        self.wait(2.4)

        heading = self._replace_heading(
            heading, "The mean is the coordinate-wise average, or balance point, of the data."
        )
        self.play(FadeOut(plane_group), FadeOut(question))
        raw_matrix = self._matrix(
            [["3", "2"], ["2", "3"], ["-3", "-2"], ["-2", "-3"], ["1", "1"], ["-1", "-1"]],
            scale=0.46,
            h_buff=0.86,
            v_buff=0.61,
        )
        centering = VGroup(
            Text("THE MEAN", font_size=25, color=YELLOW, weight="BOLD"),
            MathTex(
                r"\bar{\mathbf x}=\frac1{6}\sum_{i=1}^{6}\mathbf x_i=(0,0)",
                font_size=38,
                color=WHITE,
            ),
            Text(
                "coordinate-wise average and balance point",
                font_size=23,
                color=GREY_B,
            ),
            MathTex(
                r"\mathbf x_i^{\,(c)}=\mathbf x_i-\bar{\mathbf x}",
                font_size=40,
                color=YELLOW,
            ),
            Text(
                "each row becomes a displacement from the average",
                font_size=23,
                color=GREY_B,
            ),
            MathTex(r"X_c=X-\mathbf1\bar{\mathbf x}^{T}=X", font_size=38, color=GREEN_C),
            Text(
                "PCA now measures spread around what is typical.",
                font_size=25,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.17)
        centered_card = VGroup(
            VGroup(MathTex(r"X=", font_size=42), raw_matrix).arrange(RIGHT, buff=0.14),
            centering,
        ).arrange(RIGHT, buff=0.85).move_to(DOWN * 0.04)
        self.play(FadeIn(centered_card[0]))
        self.play(FadeIn(centering))
        self.wait(3.2)

        heading = self._replace_heading(
            heading, "Rows are observations; columns are measured features."
        )
        self.play(FadeOut(centered_card))
        symbolic = self._matrix(
            [[r"x_1", r"y_1"], [r"x_2", r"y_2"], [r"\vdots", r"\vdots"], [r"x_6", r"y_6"]],
            scale=0.55,
            h_buff=1.02,
            v_buff=0.74,
        )
        data_roles = VGroup(
            VGroup(MathTex(r"X=", font_size=44), symbolic).arrange(RIGHT, buff=0.15),
            VGroup(
                self._card("6 ROWS", r"\text{observations}", "one point per row", TEAL_C, 31),
                self._card("2 COLUMNS", r"\text{features}", "horizontal and vertical", ORANGE, 31),
            ).arrange(DOWN, buff=0.34),
        ).arrange(RIGHT, buff=1.05).move_to(DOWN * 0.02)
        self.play(FadeIn(data_roles[0]))
        self.play(FadeIn(data_roles[1]))
        self.wait(2.4)

        heading = self._replace_heading(
            heading, "In the SVD, the right singular vectors are directions in feature space."
        )
        self.play(FadeOut(data_roles))
        svd_roles = VGroup(
            MathTex(r"X=U\Sigma V^T", font_size=57, color=YELLOW),
            VGroup(
                self._card("SCORES", r"\sigma_i u_i=Xv_i", "coordinates of the observations", TEAL_C, 34),
                self._card("DIRECTIONS", r"v_i", "axes in feature space", GREEN_C, 38),
            ).arrange(RIGHT, buff=0.64),
            Text("PCA orders these directions by captured variation.", font_size=28, color=WHITE),
        ).arrange(DOWN, buff=0.42).move_to(DOWN * 0.03)
        self.play(FadeIn(svd_roles[0]))
        self.play(FadeIn(svd_roles[1]))
        self.play(FadeIn(svd_roles[2]))
        self.wait(2.5)

        heading = self._replace_heading(
            heading, "The eigenvectors of X-transpose-X reveal the principal directions."
        )
        self.play(FadeOut(svd_roles))
        gram = VGroup(
            MathTex(
                r"X^TX=\begin{bmatrix}28&26\\26&28\end{bmatrix}",
                font_size=48,
                color=YELLOW,
            ),
            VGroup(
                self._card(
                    "FIRST",
                    r"\begin{gathered}\lambda_1=54\\v_1=\frac1{\sqrt2}(1,1)\end{gathered}",
                    "principal direction",
                    GREEN_C,
                    32,
                ),
                self._card(
                    "SECOND",
                    r"\begin{gathered}\lambda_2=2\\v_2=\frac1{\sqrt2}(1,-1)\end{gathered}",
                    "remaining direction",
                    BLUE_C,
                    32,
                ),
            ).arrange(RIGHT, buff=0.58),
            MathTex(r"\sigma_i^2=\lambda_i", font_size=40, color=WHITE),
        ).arrange(DOWN, buff=0.36).move_to(DOWN * 0.02)
        self.play(FadeIn(gram[0]))
        self.play(FadeIn(gram[1]))
        self.play(FadeIn(gram[2]))
        self.wait(2.5)

        heading = self._replace_heading(
            heading, "The first direction follows the cloud; the second measures its narrow spread."
        )
        self.play(FadeOut(gram))
        axis_plane = self._plane().move_to(DOWN * 0.08).shift(LEFT * 2.25)
        axis_dots = self._dots(axis_plane, data)
        axes = self._principal_axes(axis_plane)
        direction_notes = VGroup(
            self._card("MAJOR AXIS", r"v_1=\frac1{\sqrt2}(1,1)", "largest variation", GREEN_C, 34),
            self._card("MINOR AXIS", r"v_2=\frac1{\sqrt2}(1,-1)", "remaining variation", BLUE_C, 34),
        ).arrange(DOWN, buff=0.42).to_edge(RIGHT, buff=0.48).shift(DOWN * 0.02)
        self.play(FadeIn(axis_plane), FadeIn(axis_dots))
        self.play(FadeIn(axes[0]), FadeIn(axes[2]))
        self.play(FadeIn(axes[1]), FadeIn(axes[3]), FadeIn(direction_notes))
        self.wait(2.5)

        heading = self._replace_heading(
            heading, "Projecting onto v-one gives one principal-component score per observation."
        )
        self.play(FadeOut(axis_plane), FadeOut(axis_dots), FadeOut(axes), FadeOut(direction_notes))
        score_values = model.scores(1).reshape(-1)
        score_matrix = self._matrix(
            [[rf"{value:.1f}"] for value in score_values],
            scale=0.43,
            h_buff=0.62,
            v_buff=0.58,
        )
        scores = VGroup(
            MathTex(r"z=Xv_1=\sigma_1u_1", font_size=49, color=YELLOW),
            VGroup(
                MathTex(r"z=", font_size=41),
                score_matrix,
                MathTex(r"\in\mathbb R^{6\times1}", font_size=38, color=GREEN_C),
            ).arrange(RIGHT, buff=0.16),
            Text("Each two-coordinate point now has one coordinate along the principal line.", font_size=27, color=WHITE),
        ).arrange(DOWN, buff=0.37).move_to(DOWN * 0.02)
        self.play(FadeIn(scores[0]))
        self.play(FadeIn(scores[1]))
        self.play(FadeIn(scores[2]))
        self.wait(2.6)

        heading = self._replace_heading(
            heading, "The rank-one reconstruction places every point on the principal line."
        )
        self.play(FadeOut(scores))
        projection_plane = self._plane().move_to(DOWN * 0.08).shift(LEFT * 2.25)
        original_dots = self._dots(projection_plane, data, ORANGE)
        projected_dots = self._dots(projection_plane, rank_one, GREEN_C)
        main_axis = Line(
            projection_plane.c2p(-3.7, -3.7),
            projection_plane.c2p(3.7, 3.7),
            color=GREEN_C,
            stroke_width=4,
        )
        residuals = VGroup(
            *[
                DashedLine(
                    projection_plane.c2p(*point),
                    projection_plane.c2p(*projected),
                    color=GREY_B,
                    stroke_width=2,
                )
                for point, projected in zip(data, rank_one)
            ]
        )
        reconstruction_formula = VGroup(
            MathTex(r"X_1=(Xv_1)v_1^T", font_size=43, color=YELLOW),
            MathTex(r"X_1=\sigma_1u_1v_1^T", font_size=43, color=GREEN_C),
            Text("discard the perpendicular coordinate", font_size=25, color=WHITE),
        ).arrange(DOWN, buff=0.31).to_edge(RIGHT, buff=0.58).shift(DOWN * 0.03)
        self.play(FadeIn(projection_plane), FadeIn(original_dots), FadeIn(main_axis))
        self.play(FadeIn(residuals))
        moving_dots = original_dots.copy()
        self.add(moving_dots)
        self.play(ReplacementTransform(moving_dots, projected_dots), run_time=1.35)
        self.play(FadeIn(reconstruction_formula))
        self.wait(2.6)

        heading = self._replace_heading(
            heading, "One component preserves 96.4 percent of the dataset's total variation."
        )
        self.play(
            FadeOut(projection_plane),
            FadeOut(original_dots),
            FadeOut(projected_dots),
            FadeOut(main_axis),
            FadeOut(residuals),
            FadeOut(reconstruction_formula),
        )
        variation = VGroup(
            MathTex(
                r"\text{retained variation}=\frac{\sigma_1^2}{\sigma_1^2+\sigma_2^2}",
                font_size=43,
                color=WHITE,
            ),
            MathTex(r"=\frac{54}{54+2}=96.4\%", font_size=51, color=GREEN_C),
            VGroup(
                self._card("BEFORE", r"(x_i,y_i)", "two coordinates", ORANGE, 36),
                Arrow(LEFT, RIGHT, color=YELLOW, buff=0.0, max_tip_length_to_length_ratio=0.18),
                self._card("AFTER", r"z_i=x_i^Tv_1", "one score", TEAL_C, 34),
            ).arrange(RIGHT, buff=0.46),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.03)
        self.play(FadeIn(variation[0]))
        self.play(FadeIn(variation[1]))
        self.play(FadeIn(variation[2]))
        self.wait(2.7)

        heading = self._replace_heading(
            heading, "PCA is truncated SVD applied to centered data."
        )
        self.play(FadeOut(variation))
        conclusion = VGroup(
            MathTex(
                r"\boxed{X_k=U_k\Sigma_kV_k^T}",
                font_size=54,
                color=YELLOW,
            ),
            VGroup(
                self._card("KEEP", r"v_1,\ldots,v_k", "strongest variation", GREEN_C, 37),
                self._card("DISCARD", r"v_{k+1},\ldots", "smaller variation", ORANGE, 37),
            ).arrange(RIGHT, buff=0.62),
            Text(
                "Choose a lower-dimensional view that preserves the most information.",
                font_size=28,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.40).move_to(DOWN * 0.03)
        self.play(FadeIn(conclusion[0]))
        self.play(FadeIn(conclusion[1]))
        self.play(FadeIn(conclusion[2]))
        self.wait(3.0)
