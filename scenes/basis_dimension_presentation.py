"""CP76: a basis has enough vectors, but not too many."""
from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    Create,
    DEGREES,
    DOWN,
    Dot3D,
    FadeIn,
    FadeOut,
    LEFT,
    MathTex,
    Polygon,
    RIGHT,
    Text,
    ThreeDAxes,
    ThreeDScene,
    UP,
    VGroup,
)

from engine.basis_dimension import BasisDimension

TITLE = "Basis: Enough, but Not Too Many"
QUESTION = "If three vectors generate this plane, do we really need all three?"
KEY_IDEA = "A basis spans the space, with no redundant vectors."
FINAL_IDEA = "The dimension is the number of vectors in a basis."

BACKGROUND = "#0A0D13"
TEXT = "#E8EAED"
MUTED = "#A9B2C3"
V1_COLOR = "#5DADE2"
V2_COLOR = "#AF7AC5"
V3_COLOR = "#F6C85F"
PLANE_COLOR = "#55D6BE"

V1 = np.array([2.0, 0.2, 0.4])
V2 = np.array([-0.4, 1.7, 0.9])
V3 = V1 + V2


class BasisDimensionPresentation(ThreeDScene):
    """Show that removing a redundant vector does not change the span."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND
        self.set_camera_orientation(phi=67 * DEGREES, theta=-50 * DEGREES, zoom=0.90)

        pair_grid = np.linspace(-2.0, 2.0, 5)
        triple_grid = np.linspace(-1.0, 1.0, 3)
        pair_coefficients = np.array([(a, b) for a in pair_grid for b in pair_grid], dtype=float)
        triple_coefficients = np.array(
            [(a, b, c) for a in triple_grid for b in triple_grid for c in triple_grid],
            dtype=float,
        )
        model = BasisDimension(V1, V2, V3, pair_coefficients, triple_coefficients)
        snapshot = model.snapshot()
        relation = model.express_vector_3_in_basis()

        axes = ThreeDAxes(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            z_range=(-4, 4, 1),
            x_length=8.4,
            y_length=8.4,
            z_length=6.2,
        )

        title = Text(TITLE, font_size=38, color=TEXT).to_edge(UP, buff=0.30)
        relation_tex = MathTex(
            rf"\mathbf v_3={relation[0]:.0f}\mathbf v_1+{relation[1]:.0f}\mathbf v_2",
            font_size=38,
            color=TEXT,
        ).to_edge(UP, buff=0.92)
        question = Text(QUESTION, font_size=27, color=TEXT).to_edge(UP, buff=1.52)
        equality = MathTex(
            r"\operatorname{span}\{\mathbf v_1,\mathbf v_2,\mathbf v_3\}="
            r"\operatorname{span}\{\mathbf v_1,\mathbf v_2\}",
            font_size=38,
            color=TEXT,
        ).to_edge(DOWN, buff=0.46)
        basis_text = MathTex(
            r"\{\mathbf v_1,\mathbf v_2\}\text{ is a basis}",
            font_size=40,
            color=TEXT,
        ).to_edge(DOWN, buff=1.02)
        dimension_text = MathTex(
            r"\dim(W)=2",
            font_size=42,
            color=TEXT,
        ).next_to(basis_text, UP, buff=0.26)
        key_idea = Text(KEY_IDEA, font_size=25, color=MUTED).to_edge(DOWN, buff=0.24)
        final_idea = Text(FINAL_IDEA, font_size=27, color=MUTED).to_edge(DOWN, buff=0.44)

        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title), FadeIn(axes))

        arrows = VGroup(
            self._arrow(V1, axes, V1_COLOR),
            self._arrow(V2, axes, V2_COLOR),
            self._arrow(V3, axes, V3_COLOR),
        )
        labels = VGroup(
            MathTex(r"\mathbf v_1", font_size=34, color=V1_COLOR).move_to(axes.c2p(*(V1 * 1.08))),
            MathTex(r"\mathbf v_2", font_size=34, color=V2_COLOR).move_to(axes.c2p(*(V2 * 1.10))),
            MathTex(r"\mathbf v_3", font_size=34, color=V3_COLOR).move_to(axes.c2p(*(V3 * 1.05 + np.array([0.1, 0.0, 0.1])))),
        )
        self.play(*(Create(arrow) for arrow in arrows), *(FadeIn(label) for label in labels), run_time=2.0)

        self.add_fixed_in_frame_mobjects(relation_tex)
        self.play(FadeIn(relation_tex))
        self.wait(1.2)

        u = V1 / np.linalg.norm(V1)
        v = V2 - np.dot(V2, u) * u
        v = v / np.linalg.norm(v)
        extent = 3.3
        corners = [
            -extent * u - extent * v,
            extent * u - extent * v,
            extent * u + extent * v,
            -extent * u + extent * v,
        ]
        plane = Polygon(
            *(axes.c2p(*point) for point in corners),
            color=PLANE_COLOR,
            fill_color=PLANE_COLOR,
            fill_opacity=0.12,
            stroke_opacity=0.24,
        )
        plane.set_z_index(-1)
        dots = VGroup(*(
            Dot3D(axes.c2p(*point), radius=0.032, color=PLANE_COLOR, fill_opacity=0.50)
            for point in snapshot.endpoints_basis
        ))
        self.play(FadeIn(plane), FadeIn(dots), run_time=1.8)

        self.add_fixed_in_frame_mobjects(question)
        self.play(FadeIn(question))
        self.wait(2.2)
        self.play(FadeOut(question))

        self.play(arrows[2].animate.set_opacity(0.18), labels[2].animate.set_opacity(0.18), run_time=1.2)
        self.wait(0.6)
        self.play(FadeOut(arrows[2]), FadeOut(labels[2]), run_time=1.0)

        self.add_fixed_in_frame_mobjects(equality)
        self.play(FadeIn(equality))
        self.wait(2.2)
        self.play(FadeOut(equality))

        self.add_fixed_in_frame_mobjects(dimension_text, basis_text, key_idea)
        self.play(FadeIn(dimension_text), FadeIn(basis_text), FadeIn(key_idea))
        self.wait(2.8)
        self.play(FadeOut(key_idea), FadeOut(basis_text), FadeOut(dimension_text))

        self.play(FadeOut(plane), FadeOut(dots), FadeOut(arrows[0]), FadeOut(arrows[1]), FadeOut(labels[0]), FadeOut(labels[1]), FadeOut(relation_tex), FadeOut(axes))

        summary = VGroup(
            MathTex(r"\text{spans }W", font_size=40, color=TEXT),
            MathTex(r"\text{independent}", font_size=40, color=TEXT),
            MathTex(r"\text{no redundancy}", font_size=40, color=TEXT),
            MathTex(r"\dim(W)=\text{number of basis vectors}", font_size=40, color=TEXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to(UP * 0.2)
        self.add_fixed_in_frame_mobjects(summary, final_idea)
        self.play(FadeIn(summary), FadeIn(final_idea))
        self.wait(3.0)

    @staticmethod
    def _arrow(vector: np.ndarray, axes: ThreeDAxes, color: str) -> Arrow:
        return Arrow(
            axes.c2p(0, 0, 0),
            axes.c2p(*vector),
            color=color,
            buff=0,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.16,
        )
