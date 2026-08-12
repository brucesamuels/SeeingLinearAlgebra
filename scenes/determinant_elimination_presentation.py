"""CP134 presentation: determinants and elimination."""
from __future__ import annotations

import numpy as np
from manim import Arrow, FadeIn, FadeOut, MathTex, Matrix, Scene, Text, VGroup, WHITE, YELLOW, GREY_B, ORANGE, GREEN, BLUE, RED, Write

from engine.determinant_elimination import build_elimination_example, overview_rule_lines


class DeterminantEliminationPresentation(Scene):
    """Use determinant properties during elimination and recover det(A) from a triangular matrix."""

    def construct(self) -> None:
        banner = Text("Methods of Computation", font_size=38)
        banner.to_edge(np.array([0.0, 1.0, 0.0]), buff=0.24)
        subtitle = Text(
            "Using elimination to compute determinants",
            font_size=25,
            color=GREY_B,
        ).next_to(banner, np.array([0.0, -1.0, 0.0]), buff=0.12)
        self.play(Write(banner), FadeIn(subtitle))
        self.wait(0.8)
        self.play(FadeOut(subtitle))

        self.show_overview(banner)
        self.show_example_setup(banner)
        self.show_elimination_steps(banner)
        self.show_final_recovery(banner)

    def show_overview(self, banner: Text) -> None:
        label = Text("Determinants and elimination", font_size=30, color=YELLOW)
        label.move_to(np.array([0.0, 2.25, 0.0]))
        lines = overview_rule_lines()
        rules = VGroup(
            Text(lines[0], font_size=23, color=WHITE),
            Text(lines[1], font_size=23, color=WHITE),
            Text(lines[2], font_size=22, color=WHITE),
            Text(lines[3], font_size=22, color=WHITE),
        ).arrange(np.array([0.0, -1.0, 0.0]), aligned_edge=np.array([-1.0, 0.0, 0.0]), buff=0.24)
        rules.move_to(np.array([0.0, 0.15, 0.0]))
        note = Text(
            "Important: the pivot product gives det(U). Then undo every row swap and row scaling to recover det(A).",
            font_size=21,
            color=GREY_B,
        )
        note.scale_to_fit_width(11.6)
        note.move_to(np.array([0.0, -3.0, 0.0]))
        self.play(FadeIn(label))
        for line in rules:
            self.play(FadeIn(line))
        self.play(FadeIn(note))
        self.wait(1.5)
        self.clear_stage((banner,))

    def show_example_setup(self, banner: Text) -> None:
        label = Text("Example: track determinant changes during elimination", font_size=28, color=YELLOW)
        label.move_to(np.array([0.0, 2.2, 0.0]))
        example = build_elimination_example()
        matrix = self.matrix_mobject(example.initial_matrix, font_size=32)
        matrix.move_to(np.array([-4.1, 0.25, 0.0]))
        name = MathTex(r"A", font_size=36, color=WHITE).next_to(matrix, np.array([0.0, 1.0, 0.0]), buff=0.25)
        goal = VGroup(
            Text("Goal:", font_size=27, color=WHITE),
            Text("Use elimination to reach a triangular matrix U.", font_size=24, color=WHITE),
            Text("Track how each row operation changes the determinant.", font_size=24, color=WHITE),
            Text("Then recover det(A) from det(U).", font_size=24, color=WHITE),
        ).arrange(np.array([0.0, -1.0, 0.0]), aligned_edge=np.array([-1.0, 0.0, 0.0]), buff=0.22)
        goal.move_to(np.array([2.95, 0.0, 0.0]))
        self.play(FadeIn(label), FadeIn(matrix), FadeIn(name))
        for line in goal:
            self.play(FadeIn(line))
        self.wait(1.3)
        self.clear_stage((banner,))

    def show_elimination_steps(self, banner: Text) -> None:
        label = Text("Step-by-step elimination", font_size=34, color=YELLOW)
        label.move_to(np.array([0.0, 3.02, 0.0]))
        example = build_elimination_example()

        stage_data = [
            ("Start", example.initial_matrix, WHITE, np.array([-5.25, 1.56, 0.0])),
            ("Step 1", example.steps[0].matrix, ORANGE, np.array([-1.55, 1.56, 0.0])),
            ("Step 2", example.steps[1].matrix, BLUE, np.array([2.40, 1.56, 0.0])),
            ("Step 3", example.steps[2].matrix, GREEN, np.array([2.15, -1.46, 0.0])),
            ("Step 4", example.steps[3].matrix, RED, np.array([-1.55, -1.46, 0.0])),
        ]

        stage_groups = []
        for title, mat, color, pos in stage_data:
            title_mob = Text(title, font_size=22, color=color)
            title_mob.move_to(pos + np.array([0.0, 0.98, 0.0]))
            matrix_mob = self.matrix_mobject(mat, font_size=17, h_buff=0.56, v_buff=0.42)
            matrix_mob.move_to(pos)
            stage_groups.append(VGroup(title_mob, matrix_mob))

        top_left_arrow = Arrow(
            np.array([-4.20, 1.56, 0.0]),
            np.array([-3.55, 1.56, 0.0]),
            buff=0.0,
            stroke_width=5,
            color=ORANGE,
        )
        top_left_op = MathTex(r"r_1 \leftrightarrow r_2", font_size=25, color=ORANGE)
        top_left_op.move_to(np.array([-3.35, 1.98, 0.0]))
        top_left_det = MathTex(r"\det(S_1)=-\det(A)", font_size=19, color=ORANGE)
        top_left_det.move_to(np.array([-3.35, 1.00, 0.0]))

        top_right_arrow = Arrow(
            np.array([-0.45, 1.56, 0.0]),
            np.array([0.20, 1.56, 0.0]),
            buff=0.0,
            stroke_width=5,
            color=BLUE,
        )
        top_right_op = MathTex(r"r_2 \to \tfrac12 r_2", font_size=25, color=BLUE)
        top_right_op.move_to(np.array([0.45, 1.98, 0.0]))
        top_right_det = VGroup(
            MathTex(r"\det(S_2)=\tfrac12\det(S_1)", font_size=19, color=BLUE),
            MathTex(r"=-\tfrac12\det(A)", font_size=19, color=BLUE),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.06)
        top_right_det.move_to(np.array([0.45, 0.93, 0.0]))

        vertical_arrow = Arrow(
            np.array([2.88, 0.82, 0.0]),
            np.array([2.88, 0.18, 0.0]),
            buff=0.0,
            stroke_width=5,
            color=GREEN,
        )
        vertical_op = MathTex(r"r_3 \to r_3-2r_1", font_size=25, color=GREEN)
        vertical_op.move_to(np.array([2.05, 0.55, 0.0]))
        vertical_det = MathTex(r"\det(S_3)=\det(S_2)", font_size=19, color=GREEN)
        vertical_det.move_to(np.array([2.05, -0.20, 0.0]))

        bottom_arrow = Arrow(
            np.array([0.95, -1.46, 0.0]),
            np.array([0.30, -1.46, 0.0]),
            buff=0.0,
            stroke_width=5,
            color=RED,
        )
        bottom_op = MathTex(r"r_3 \to r_3-r_2", font_size=25, color=RED)
        bottom_op.move_to(np.array([0.30, -0.98, 0.0]))
        bottom_det = MathTex(r"\det(U)=\det(S_3)", font_size=19, color=RED)
        bottom_det.move_to(np.array([0.30, -1.88, 0.0]))

        transition_groups = [
            VGroup(top_left_arrow, top_left_op, top_left_det),
            VGroup(top_right_arrow, top_right_op, top_right_det),
            VGroup(vertical_arrow, vertical_op, vertical_det),
            VGroup(bottom_arrow, bottom_op, bottom_det),
        ]

        self.play(FadeIn(label))
        for stage_group in stage_groups:
            self.play(FadeIn(stage_group))
        for transition_group in transition_groups:
            self.play(FadeIn(transition_group))
        self.wait(1.8)
        self.clear_stage((banner,))

    def show_final_recovery(self, banner: Text) -> None:
        label = Text("Recover det(A) from the triangular matrix", font_size=29, color=YELLOW)
        label.move_to(np.array([0.0, 2.2, 0.0]))
        example = build_elimination_example()

        left = self.matrix_mobject(example.triangular_matrix, font_size=32)
        left.move_to(np.array([-4.0, 0.6, 0.0]))
        name = MathTex(r"U", font_size=36, color=WHITE).next_to(left, np.array([0.0, 1.0, 0.0]), buff=0.24)
        diag = MathTex(r"\det(U)=1\cdot 1 \cdot \tfrac72 = \tfrac72", font_size=34, color=GREEN)
        diag.move_to(np.array([1.7, 1.0, 0.0]))
        recovery = VGroup(
            MathTex(r"\det(U)=-\tfrac12\det(A)", font_size=34, color=WHITE),
            MathTex(r"\tfrac72 = -\tfrac12\det(A)", font_size=34, color=BLUE),
            MathTex(r"\det(A)=-7", font_size=40, color=YELLOW),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.22).move_to(np.array([1.7, -0.95, 0.0]))
        summary = Text(
            "The pivot product gives det(U). Accounting for the swap and the scaling recovers det(A).",
            font_size=22,
            color=GREY_B,
        )
        summary.scale_to_fit_width(11.4)
        summary.move_to(np.array([0.0, -3.15, 0.0]))

        self.play(FadeIn(label), FadeIn(left), FadeIn(name))
        self.play(Write(diag))
        for line in recovery:
            self.play(Write(line))
        self.play(FadeIn(summary))
        self.wait(2.0)

    @staticmethod
    def matrix_mobject(matrix: np.ndarray, font_size: int, h_buff: float = 0.9, v_buff: float = 0.68) -> Matrix:
        rows = []
        for row in matrix:
            current = []
            for value in row:
                if abs(value - round(value)) < 1e-9:
                    current.append(str(int(round(value))))
                elif abs(value - 0.5) < 1e-9:
                    current.append(r"\tfrac{1}{2}")
                elif abs(value - 3.5) < 1e-9:
                    current.append(r"\tfrac{7}{2}")
                else:
                    current.append(f"{value:g}")
            rows.append(current)
        return Matrix(
            rows,
            element_to_mobject_config={"font_size": font_size},
            h_buff=h_buff,
            v_buff=v_buff,
        )

    def clear_stage(self, preserve: tuple[object, ...]) -> None:
        self.play(*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve])
