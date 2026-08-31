"""Manim presentation: Positive Definite Matrices — Why Covariance Is Positive Semidefinite."""
from __future__ import annotations

import numpy as np
from manim import (
    Axes, Create, DashedLine, Dot, FadeIn, FadeOut, GREEN_C, GREY_B,
    MathTex, Matrix, ORANGE, RED_C, RIGHT, LEFT, DOWN, UP, Scene,
    SurroundingRectangle, TEAL_C, Tex, Text, VGroup, WHITE, YELLOW,
)

from engine.covariance_definiteness import CovarianceDefiniteness


class CovarianceDefinitenessPresentation(Scene):
    CHAPTER_BANNER = "POSITIVE DEFINITE MATRICES"
    LESSON_TITLE = "Why Covariance Is Positive Semidefinite"

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
            r"\textbf{Why Covariance Is Positive Semidefinite}",
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
    def _raw_axes():
        return Axes(
            x_range=[0, 6, 1], y_range=[0, 4, 1],
            x_length=5.4, y_length=3.4,
            axis_config={"color": GREY_B, "stroke_width": 2.2},
            tips=False,
        )

    @staticmethod
    def _centered_axes():
        return Axes(
            x_range=[-3, 3, 1], y_range=[-2, 2, 1],
            x_length=5.4, y_length=3.4,
            axis_config={"color": GREY_B, "stroke_width": 2.2},
            tips=False,
        )

    @staticmethod
    def _dots(axes, points, color=TEAL_C):
        return VGroup(*[
            Dot(axes.c2p(float(x), float(y)), radius=0.085, color=color)
            for x, y in points
        ])

    def construct(self):
        model = CovarianceDefiniteness()
        line_model = CovarianceDefiniteness([[2, 3], [3, 5], [4, 7]])
        if not np.allclose(model.mean(), [3, 2]):
            raise RuntimeError("unexpected observation mean")
        if not np.allclose(model.population_covariance(), [[2, 1], [1, 1]]):
            raise RuntimeError("unexpected covariance matrix")
        if not np.allclose(line_model.centered_projections([-2, 1]), [0, 0, 0]):
            raise RuntimeError("line-data zero-variance direction failed")

        banner, title, heading = self._chrome(
            "Covariance begins with a collection of observations."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        raw_axes = self._raw_axes().move_to(LEFT * 2.55 + DOWN * 0.18)
        raw_points = model.observations
        raw_dots = self._dots(raw_axes, raw_points)
        point_labels = VGroup(*[
            MathTex(f"({int(x)},{int(y)})", font_size=25, color=WHITE).next_to(
                raw_axes.c2p(x, y), UP, buff=0.08
            )
            for x, y in raw_points
        ])
        observations = VGroup(
            Text("four observations", font_size=29, color=YELLOW, weight="BOLD"),
            MathTex(
                r"p_1=(1,1),\ p_2=(3,1)",
                font_size=34,
            ),
            MathTex(
                r"p_3=(3,3),\ p_4=(5,3)",
                font_size=34,
            ),
        ).arrange(DOWN, buff=0.30).move_to(RIGHT * 3.25 + DOWN * 0.12)
        self.play(Create(raw_axes), FadeIn(raw_dots))
        self.play(FadeIn(point_labels), FadeIn(observations))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "The mean marks the center of the data cloud."
        )
        mean_dot = Dot(raw_axes.c2p(3, 2), radius=0.11, color=RED_C)
        mean_label = MathTex(
            r"\mu=\frac14\sum_{i=1}^4p_i=(3,2)",
            font_size=42,
            color=YELLOW,
        ).move_to(RIGHT * 3.05 + DOWN * 0.02)
        mean_note = Text(
            "mean",
            font_size=25,
            color=RED_C,
            weight="BOLD",
        ).next_to(mean_dot, RIGHT, buff=0.10)
        self.play(FadeOut(observations), FadeIn(mean_dot), FadeIn(mean_note))
        self.play(FadeIn(mean_label))
        self.wait(1.8)

        heading = self._replace_heading(
            heading, "Centering subtracts the mean from every observation."
        )
        self.play(
            FadeOut(raw_axes), FadeOut(raw_dots), FadeOut(point_labels),
            FadeOut(mean_dot), FadeOut(mean_note), FadeOut(mean_label),
        )
        centered_axes = self._centered_axes().move_to(LEFT * 2.75 + DOWN * 0.16)
        centered_points = model.centered_matrix()
        centered_dots = self._dots(centered_axes, centered_points)
        origin = Dot(centered_axes.c2p(0, 0), radius=0.075, color=RED_C)
        center_rule = VGroup(
            MathTex(r"c_i=p_i-\mu", font_size=45, color=YELLOW),
            Text("the centered observations", font_size=29, color=WHITE),
            MathTex(
                r"(-2,-1),\ (0,-1),\ (0,1),\ (2,1)",
                font_size=34,
                color=TEAL_C,
            ),
        ).arrange(DOWN, buff=0.34).move_to(RIGHT * 3.10 + DOWN * 0.10)
        self.play(Create(centered_axes), FadeIn(centered_dots), FadeIn(origin))
        self.play(FadeIn(center_rule))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Stack the centered observations as rows of a data matrix."
        )
        self.play(FadeOut(centered_axes), FadeOut(centered_dots), FadeOut(origin), FadeOut(center_rule))
        c_matrix = self._matrix(
            [["-2", "-1"], ["0", "-1"], ["0", "1"], ["2", "1"]],
            scale=0.70,
        )
        centered_matrix_display = VGroup(
            MathTex("C=", font_size=42), c_matrix
        ).arrange(RIGHT, buff=0.14).move_to(LEFT * 2.40 + DOWN * 0.02)
        row_note = VGroup(
            Text("one centered observation per row", font_size=28, color=TEAL_C),
            MathTex(r"\sum_{i=1}^4 c_i=0", font_size=40, color=GREEN_C),
        ).arrange(DOWN, buff=0.38).move_to(RIGHT * 2.75 + DOWN * 0.02)
        self.play(FadeIn(centered_matrix_display))
        self.play(FadeIn(row_note))
        self.wait(1.8)

        heading = self._replace_heading(
            heading, "The covariance matrix averages centered outer products."
        )
        self.play(FadeOut(centered_matrix_display), FadeOut(row_note))
        definition = VGroup(
            Text("population covariance matrix", font_size=34, color=YELLOW, weight="BOLD"),
            MathTex(
                r"\boxed{\Sigma=\frac1m\sum_{i=1}^m c_ic_i^T=\frac1m C^TC}",
                font_size=49,
                color=WHITE,
            ),
            Text(
                "It summarizes how the centered coordinates vary.",
                font_size=29,
                color=GREEN_C,
            ),
        ).arrange(DOWN, buff=0.50).move_to(DOWN * 0.08)
        self.play(FadeIn(definition[0]))
        self.play(FadeIn(definition[1]))
        self.play(FadeIn(definition[2]))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Diagonal entries measure spread; off-diagonal entries measure joint variation."
        )
        self.play(FadeOut(definition))
        symbolic_covariance = self._matrix(
            [[r"\sigma_{11}", r"\sigma_{12}"], [r"\sigma_{21}", r"\sigma_{22}"]],
            scale=0.90,
            h_buff=1.25,
            v_buff=0.95,
        ).move_to(LEFT * 2.65 + DOWN * 0.02)
        entries = symbolic_covariance.get_entries()
        diagonal_boxes = VGroup(
            SurroundingRectangle(entries[0], color=GREEN_C, buff=0.11),
            SurroundingRectangle(entries[3], color=GREEN_C, buff=0.11),
        )
        off_diagonal_boxes = VGroup(
            SurroundingRectangle(entries[1], color=ORANGE, buff=0.11),
            SurroundingRectangle(entries[2], color=ORANGE, buff=0.11),
        )
        entry_meanings = VGroup(
            VGroup(
                Text("diagonal", font_size=28, color=GREEN_C, weight="BOLD"),
                Text("variance of each coordinate", font_size=27, color=WHITE),
            ).arrange(DOWN, buff=0.18),
            VGroup(
                Text("off diagonal", font_size=28, color=ORANGE, weight="BOLD"),
                Text("how coordinates vary together", font_size=27, color=WHITE),
            ).arrange(DOWN, buff=0.18),
        ).arrange(DOWN, buff=0.55).move_to(RIGHT * 2.85 + DOWN * 0.02)
        self.play(FadeIn(symbolic_covariance), Create(diagonal_boxes))
        self.play(FadeIn(entry_meanings[0]))
        self.play(Create(off_diagonal_boxes), FadeIn(entry_meanings[1]))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "For these four observations, the covariance has simple entries."
        )
        self.play(
            FadeOut(symbolic_covariance), FadeOut(diagonal_boxes),
            FadeOut(off_diagonal_boxes), FadeOut(entry_meanings),
        )
        gram_matrix = self._matrix([["8", "4"], ["4", "4"]], scale=0.80)
        covariance_matrix = self._matrix([["2", "1"], ["1", "1"]], scale=0.84)
        computation = VGroup(
            MathTex(r"\Sigma=\frac14", font_size=43),
            gram_matrix,
            MathTex("=", font_size=42),
            covariance_matrix,
        ).arrange(RIGHT, buff=0.30).move_to(DOWN * 0.02)
        matrix_labels = VGroup(
            MathTex(r"C^TC", font_size=32, color=TEAL_C).next_to(gram_matrix, DOWN, buff=0.22),
            MathTex(r"\Sigma", font_size=34, color=YELLOW).next_to(covariance_matrix, DOWN, buff=0.22),
        )
        self.play(FadeIn(computation), FadeIn(matrix_labels))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "A direction v turns every centered observation into one scalar projection."
        )
        self.play(FadeOut(computation), FadeOut(matrix_labels))
        projection_axes = self._centered_axes().move_to(LEFT * 2.75 + DOWN * 0.15)
        projection_dots = self._dots(projection_axes, centered_points)
        direction_line = projection_axes.plot(
            lambda x: 0, x_range=[-2.7, 2.7], color=YELLOW, stroke_width=4
        )
        projection_guides = VGroup(*[
            DashedLine(
                projection_axes.c2p(float(x), float(y)),
                projection_axes.c2p(float(x), 0),
                color=GREY_B,
                stroke_opacity=0.75,
            )
            for x, y in centered_points
        ])
        direction_label = MathTex(r"v=(1,0)^T", font_size=34, color=YELLOW).next_to(
            direction_line, DOWN, buff=0.16
        )
        projection_formula = VGroup(
            Text("centered projections", font_size=29, color=TEAL_C, weight="BOLD"),
            MathTex(r"Cv=(-2,0,0,2)^T", font_size=40, color=WHITE),
            MathTex(r"v^T\Sigma v=2", font_size=45, color=GREEN_C),
        ).arrange(DOWN, buff=0.38).move_to(RIGHT * 3.05 + DOWN * 0.02)
        self.play(Create(projection_axes), FadeIn(projection_dots))
        self.play(Create(direction_line), FadeIn(direction_label), Create(projection_guides))
        self.play(FadeIn(projection_formula))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Directional variance is a squared norm, so it can never be negative."
        )
        self.play(
            FadeOut(projection_axes), FadeOut(projection_dots), FadeOut(direction_line),
            FadeOut(direction_label), FadeOut(projection_guides), FadeOut(projection_formula),
        )
        identity = VGroup(
            MathTex(
                r"v^T\Sigma v=v^T\left(\frac1mC^TC\right)v",
                font_size=46,
                color=WHITE,
            ),
            MathTex(
                r"\boxed{v^T\Sigma v=\frac1m\lVert Cv\rVert^2\ge0}",
                font_size=52,
                color=YELLOW,
            ),
            Text(
                "Every covariance matrix is positive semidefinite.",
                font_size=32,
                color=GREEN_C,
                weight="BOLD",
            ),
        ).arrange(DOWN, buff=0.50).move_to(DOWN * 0.10)
        self.play(FadeIn(identity[0]))
        self.play(FadeIn(identity[1]))
        self.play(FadeIn(identity[2]))
        self.wait(2.0)

        prediction = Text(
            "Pause: when can a nonzero direction have zero variance?",
            font_size=29,
            color=YELLOW,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.48)
        self.play(FadeIn(prediction))
        self.wait(2.8)
        self.play(FadeOut(prediction))

        heading = self._replace_heading(
            heading, "Zero variance means every centered observation has the same projection."
        )
        self.play(FadeOut(identity))
        line_axes = Axes(
            x_range=[-2, 2, 1], y_range=[-3, 3, 1],
            x_length=4.4, y_length=4.2,
            axis_config={"color": GREY_B, "stroke_width": 2.2},
            tips=False,
        ).move_to(LEFT * 2.75 + DOWN * 0.16)
        line_points = line_model.centered_matrix()
        line_dots = self._dots(line_axes, line_points, color=TEAL_C)
        data_line = line_axes.plot(
            lambda x: 2 * x, x_range=[-1.35, 1.35], color=TEAL_C, stroke_width=4
        )
        zero_direction = DashedLine(
            line_axes.c2p(0, 0), line_axes.c2p(-1.35, 0.675),
            color=YELLOW, stroke_width=4,
        )
        d_matrix = self._matrix(
            [["-1", "-2"], ["0", "0"], ["1", "2"]], scale=0.62
        )
        singular_logic = VGroup(
            VGroup(MathTex("D=", font_size=37), d_matrix).arrange(RIGHT, buff=0.12),
            MathTex(r"v=(-2,1)^T\ne0", font_size=40, color=YELLOW),
            MathTex(r"Dv=0", font_size=46, color=TEAL_C),
            MathTex(r"v^T\Sigma v=0", font_size=46, color=GREEN_C),
        ).arrange(DOWN, buff=0.30).move_to(RIGHT * 3.00 + DOWN * 0.08)
        self.play(Create(line_axes), Create(data_line), FadeIn(line_dots))
        self.play(Create(zero_direction), FadeIn(singular_logic[0]), FadeIn(singular_logic[1]))
        self.play(FadeIn(singular_logic[2]), FadeIn(singular_logic[3]))
        self.wait(2.2)

        heading = self._replace_heading(
            heading, "The data vary along a line, but not in the perpendicular feature direction."
        )
        collapse_note = Text(
            "All projections onto v collapse to zero.",
            font_size=30,
            color=YELLOW,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.48)
        self.play(FadeIn(collapse_note))
        self.wait(2.0)

        heading = self._replace_heading(
            heading, "Covariance is definite exactly when the centered data vary in every direction."
        )
        self.play(
            FadeOut(line_axes), FadeOut(data_line), FadeOut(line_dots),
            FadeOut(zero_direction), FadeOut(singular_logic), FadeOut(collapse_note),
        )
        final = VGroup(
            MathTex(
                r"\boxed{\Sigma\ \text{is always positive semidefinite}}",
                font_size=47,
                color=GREEN_C,
            ),
            MathTex(
                r"\boxed{\Sigma\ \text{is positive definite}"
                r"\quad\Longleftrightarrow\quad C\ \text{has full column rank}}",
                font_size=43,
                color=YELLOW,
            ),
            Text(
                "Sample covariance uses 1/(m−1); the positive scaling does not change this result.",
                font_size=25,
                color=GREY_B,
            ),
        ).arrange(DOWN, buff=0.58).move_to(DOWN * 0.10)
        if final.width > 11.4:
            final.scale_to_fit_width(11.4)
        self.play(FadeIn(final[0]))
        self.play(FadeIn(final[1]))
        self.play(FadeIn(final[2]))
        self.wait(2.8)
