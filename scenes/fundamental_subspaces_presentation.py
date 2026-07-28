"""CP80: a Strang-inspired living diagram of the four fundamental subspaces."""
from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    Create,
    DOWN,
    FadeIn,
    FadeOut,
    LEFT,
    Line,
    MathTex,
    ORIGIN,
    Rectangle,
    RIGHT,
    RoundedRectangle,
    Scene,
    SurroundingRectangle,
    Text,
    UP,
    VGroup,
)

from engine.fundamental_subspaces import FundamentalSubspaces

TITLE = "The Four Fundamental Subspaces"
SUBTITLE = "What a Matrix Sees, Loses, Produces, and Cannot Reach"

BACKGROUND = "#0A0D13"
TEXT = "#E8EAED"
MUTED = "#A9B2C3"
INPUT_COLOR = "#7FB3FF"
OUTPUT_COLOR = "#A5D6A7"
ROW_COLOR = "#5DADE2"
NULL_COLOR = "#F6C85F"
COL_COLOR = "#AF7AC5"
LEFT_NULL_COLOR = "#F28B82"
ARROW_COLOR = "#DADCE0"
ZERO_COLOR = "#D0D7DE"

MATRIX = np.array([
    [1.0, 2.0, 1.0],
    [0.0, 1.0, 1.0],
    [1.0, 3.0, 2.0],
])


class FundamentalSubspacesPresentation(Scene):
    """Use one master diagram to organize the four subspaces."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND
        model = FundamentalSubspaces(MATRIX)
        snapshot = model.snapshot()

        title = Text(TITLE, font_size=40, color=TEXT).to_edge(UP, buff=0.22)
        subtitle = Text(SUBTITLE, font_size=24, color=MUTED).next_to(title, DOWN, buff=0.16)
        matrix_tex = MathTex(
            r"A=\begin{bmatrix}1&2&1\\0&1&1\\1&3&2\end{bmatrix}",
            font_size=34,
            color=TEXT,
        ).to_corner(UP + LEFT, buff=0.42).shift(DOWN * 0.50)
        self.play(FadeIn(title), FadeIn(subtitle), FadeIn(matrix_tex))

        opener = Text(
            "A matrix connects an input space to an output space.",
            font_size=28,
            color=TEXT,
        ).to_edge(DOWN, buff=0.44)
        self.play(FadeIn(opener))

        input_frame = RoundedRectangle(corner_radius=0.20, width=4.2, height=4.8, color=INPUT_COLOR)
        output_frame = RoundedRectangle(corner_radius=0.20, width=4.2, height=4.8, color=OUTPUT_COLOR)
        input_frame.shift(LEFT * 3.5 + DOWN * 0.70)
        output_frame.shift(RIGHT * 3.5 + DOWN * 0.70)

        input_title = MathTex(r"\mathbb R^n", font_size=38, color=INPUT_COLOR)
        input_subtitle = Text("input space", font_size=24, color=MUTED)
        input_label_block = VGroup(input_title, input_subtitle).arrange(DOWN, buff=0.04, aligned_edge=ORIGIN).next_to(input_frame, UP, buff=0.22)
        output_title = MathTex(r"\mathbb R^m", font_size=38, color=OUTPUT_COLOR)
        output_subtitle = Text("output space", font_size=24, color=MUTED)
        output_label_block = VGroup(output_title, output_subtitle).arrange(DOWN, buff=0.04, aligned_edge=ORIGIN).next_to(output_frame, UP, buff=0.22)

        matrix_arrow = Arrow(
            input_frame.get_right() + RIGHT * 0.18,
            output_frame.get_left() + LEFT * 0.18,
            color=ARROW_COLOR,
            buff=0.08,
            stroke_width=5,
        )
        matrix_label = MathTex(r"A", font_size=40, color=TEXT).move_to(matrix_arrow.get_center() + UP * 0.38)

        self.play(
            FadeOut(opener),
            Create(input_frame), Create(output_frame),
            FadeIn(input_title), FadeIn(input_subtitle),
            FadeIn(output_title), FadeIn(output_subtitle),
            Create(matrix_arrow), FadeIn(matrix_label),
            run_time=2.0,
        )

        # Input-side split.
        input_divider = Line(input_frame.get_top() + DOWN * 2.4, input_frame.get_bottom() + UP * 2.4, color=INPUT_COLOR, stroke_width=0)
        row_panel = Rectangle(width=3.5, height=1.5, color=ROW_COLOR).set_fill(ROW_COLOR, opacity=0.12)
        null_panel = Rectangle(width=3.5, height=1.5, color=NULL_COLOR).set_fill(NULL_COLOR, opacity=0.12)
        row_panel.move_to(input_frame.get_center() + UP * 1.0)
        null_panel.move_to(input_frame.get_center() + DOWN * 1.0)
        row_label = MathTex(r"\operatorname{row}(A)", font_size=34, color=ROW_COLOR).move_to(row_panel)
        null_label = MathTex(r"\operatorname{null}(A)", font_size=34, color=NULL_COLOR).move_to(null_panel)
        input_eq = MathTex(
            r"\mathbb R^n=\operatorname{row}(A)\oplus\operatorname{null}(A)",
            font_size=34,
            color=TEXT,
        ).to_edge(DOWN, buff=0.44)
        input_text = Text(
            "Inside the input space, the row space and the null space are perpendicular.",
            font_size=27,
            color=TEXT,
        ).to_edge(DOWN, buff=0.44)
        input_perp = MathTex(r"\perp", font_size=42, color=TEXT).move_to(input_frame.get_center())
        input_perp_box = SurroundingRectangle(input_perp, color=MUTED, buff=0.10, corner_radius=0.08)

        self.play(FadeIn(row_panel), FadeIn(null_panel), FadeIn(row_label), FadeIn(null_label), run_time=1.6)
        self.play(FadeIn(input_perp), Create(input_perp_box), FadeIn(input_text), run_time=1.2)
        self.wait(1.4)
        self.play(FadeOut(input_text), FadeIn(input_eq), run_time=1.0)
        self.wait(1.2)
        self.play(FadeOut(input_eq), run_time=0.8)

        # Output-side split.
        col_panel = Rectangle(width=3.5, height=1.5, color=COL_COLOR).set_fill(COL_COLOR, opacity=0.12)
        left_null_panel = Rectangle(width=3.5, height=1.5, color=LEFT_NULL_COLOR).set_fill(LEFT_NULL_COLOR, opacity=0.12)
        col_panel.move_to(output_frame.get_center() + UP * 1.0)
        left_null_panel.move_to(output_frame.get_center() + DOWN * 1.0)
        col_label = MathTex(r"\operatorname{col}(A)", font_size=34, color=COL_COLOR).move_to(col_panel)
        left_null_label = MathTex(r"\operatorname{null}(A^T)", font_size=34, color=LEFT_NULL_COLOR).move_to(left_null_panel)
        output_eq = MathTex(
            r"\mathbb R^m=\operatorname{col}(A)\oplus\operatorname{null}(A^T)",
            font_size=34,
            color=TEXT,
        ).to_edge(DOWN, buff=0.44)
        output_text = Text(
            "Inside the output space, the column space and the left null space are perpendicular.",
            font_size=27,
            color=TEXT,
        ).to_edge(DOWN, buff=0.44)
        output_perp = MathTex(r"\perp", font_size=42, color=TEXT).move_to(output_frame.get_center())
        output_perp_box = SurroundingRectangle(output_perp, color=MUTED, buff=0.10, corner_radius=0.08)

        self.play(FadeIn(col_panel), FadeIn(left_null_panel), FadeIn(col_label), FadeIn(left_null_label), run_time=1.6)
        self.play(FadeIn(output_perp), Create(output_perp_box), FadeIn(output_text), run_time=1.2)
        self.wait(1.4)
        self.play(FadeOut(output_text), FadeIn(output_eq), run_time=1.0)
        self.wait(1.2)
        self.play(FadeOut(output_eq), run_time=0.8)

        # Action of A.
        row_to_col = Arrow(row_panel.get_right(), col_panel.get_left(), color=ROW_COLOR, buff=0.16, stroke_width=5)
        null_to_zero = Arrow(null_panel.get_right(), matrix_arrow.get_center() + DOWN * 1.15, color=NULL_COLOR, buff=0.16, stroke_width=5)
        zero_dot = MathTex(r"\mathbf 0", font_size=34, color=ZERO_COLOR).move_to(matrix_arrow.get_center() + DOWN * 1.15 + RIGHT * 0.42)
        action_text = Text(
            "The matrix sees the row space, loses the null space, and produces the column space.",
            font_size=26,
            color=TEXT,
        ).to_edge(DOWN, buff=0.44)
        left_null_text = Text(
            "The left null space contains output directions perpendicular to every possible output.",
            font_size=26,
            color=TEXT,
        ).to_edge(DOWN, buff=0.44)

        self.play(Create(row_to_col), Create(null_to_zero), FadeIn(zero_dot), run_time=1.6)
        self.play(FadeIn(action_text), run_time=1.0)
        self.wait(1.8)
        self.play(FadeOut(action_text), FadeIn(left_null_text), run_time=1.0)
        self.wait(1.8)

        # Dimension summary.
        rank_line = MathTex(r"\dim(\operatorname{row}(A))=\dim(\operatorname{col}(A))=r", font_size=36, color=TEXT)
        null_line = MathTex(r"\dim(\operatorname{null}(A))=n-r", font_size=36, color=TEXT)
        left_null_line = MathTex(r"\dim(\operatorname{null}(A^T))=m-r", font_size=36, color=TEXT)
        example_line = MathTex(
            rf"r={snapshot.rank},\quad n-r={snapshot.nullity},\quad m-r={snapshot.left_nullity}",
            font_size=36,
            color=TEXT,
        )
        summary = VGroup(rank_line, null_line, left_null_line, example_line).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(UP * 0.15)
        summary_box = SurroundingRectangle(summary, color=MUTED, buff=0.24, corner_radius=0.10)

        self.play(
            FadeOut(left_null_text),
            FadeOut(row_to_col), FadeOut(null_to_zero), FadeOut(zero_dot),
            FadeOut(input_perp), FadeOut(output_perp), FadeOut(input_perp_box), FadeOut(output_perp_box),
            FadeOut(matrix_label), FadeOut(matrix_arrow),
            FadeOut(matrix_tex), FadeOut(input_subtitle), FadeOut(output_subtitle),
            FadeOut(input_title), FadeOut(output_title),
            FadeOut(input_frame), FadeOut(output_frame),
            FadeOut(row_panel), FadeOut(null_panel), FadeOut(col_panel), FadeOut(left_null_panel),
            FadeOut(row_label), FadeOut(null_label), FadeOut(col_label), FadeOut(left_null_label),
            run_time=1.2,
        )
        self.play(FadeIn(summary_box), FadeIn(summary), run_time=1.4)
        self.wait(2.4)

        # Final conceptual summary.
        final_summary = VGroup(
            Text("Row space: what the matrix detects", font_size=30, color=ROW_COLOR),
            Text("Null space: what the matrix loses", font_size=30, color=NULL_COLOR),
            Text("Column space: what the matrix can produce", font_size=30, color=COL_COLOR),
            Text("Left null space: what the matrix cannot reach", font_size=30, color=LEFT_NULL_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to(DOWN * 0.26)
        final_title = Text(
            "The four fundamental subspaces organize everything a matrix can do.",
            font_size=31,
            color=TEXT,
        ).shift(UP * 2.1)
        self.play(FadeOut(summary), FadeOut(summary_box), run_time=0.8)
        self.play(FadeIn(final_title), FadeIn(final_summary), run_time=1.4)
        self.wait(3.0)
