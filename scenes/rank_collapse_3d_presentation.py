"""CP72: three vectors can have rank 3, rank 2, or rank 1."""
from __future__ import annotations

import numpy as np
from manim import (
    DEGREES,
    DOWN,
    FadeIn,
    FadeOut,
    Line3D,
    MathTex,
    Polygon,
    Text,
    ThreeDAxes,
    ThreeDScene,
    UP,
    UpdateFromAlphaFunc,
)

from engine.manim_rank_collapse_3d import ManimRankCollapse3D
from engine.rank_collapse_3d import RankCollapse3D, RankCollapse3DSnapshot

TITLE = "Three vectors — but how many directions?"
PREDICTION = "Watch the yellow vector move.\nAs its direction changes, the whole span changes with it."
RANK_3_TEXT = "RANK 3   •   three independent directions   •   space"
RANK_2_TEXT = "RANK 2   •   two independent directions   •   plane"
RANK_1_TEXT = "RANK 1   •   one independent direction   •   line"
FINAL_IDEA = "Rank counts the independent directions that remain."

BACKGROUND = "#0A0D13"
TEXT = "#E8EAED"
MUTED = "#A9B2C3"
U_COLOR = "#5DADE2"
V_COLOR = "#AF7AC5"
W_COLOR = "#F6C85F"
FIELD_COLOR = "#55D6BE"
EDGE_COLOR = "#B8E8DF"

U = np.array([2.1, 0.15, 0.15])
V = np.array([0.25, 1.75, 0.35])
W = np.array([0.20, -0.30, 1.75])


class RankCollapse3DPresentation(ThreeDScene):
    """Continuously collapse a 3D span from space to plane to line."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND
        self.set_camera_orientation(phi=67 * DEGREES, theta=-48 * DEGREES, zoom=0.90)

        coefficients = np.array(
            [(a, b, c) for a in np.linspace(-1.8, 1.8, 5)
             for b in np.linspace(-1.8, 1.8, 5)
             for c in np.linspace(-1.8, 1.8, 5)],
            dtype=float,
        )
        model = RankCollapse3D(U, V, W, coefficients)
        initial = model.space_to_plane(0.0)

        axes = ThreeDAxes(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            z_range=(-4, 4, 1),
            x_length=8.5,
            y_length=8.5,
            z_length=6.0,
        )

        adapter = ManimRankCollapse3D(
            initial,
            axes.c2p,
            arrow_kwargs=(
                {"color": U_COLOR, "thickness": 0.035, "height": 0.20, "base_radius": 0.075},
                {"color": V_COLOR, "thickness": 0.035, "height": 0.20, "base_radius": 0.075},
                {"color": W_COLOR, "thickness": 0.040, "height": 0.22, "base_radius": 0.085},
            ),
            dot_kwargs={"color": FIELD_COLOR, "radius": 0.032, "fill_opacity": 0.40},
            edge_kwargs={"color": EDGE_COLOR, "thickness": 0.008},
        )
        adapter.edges.set_opacity(0.22)

        title = Text(TITLE, font_size=38, color=TEXT).to_edge(UP, buff=0.30)
        prediction = Text(PREDICTION, font_size=27, color=TEXT, line_spacing=0.9).to_edge(DOWN, buff=0.42)
        rank3 = Text(RANK_3_TEXT, font_size=27, color=TEXT).to_edge(DOWN, buff=0.38)
        rank2 = Text(RANK_2_TEXT, font_size=27, color=TEXT).to_edge(DOWN, buff=0.38)
        rank1 = Text(RANK_1_TEXT, font_size=27, color=TEXT).to_edge(DOWN, buff=0.38)
        final_idea = Text(FINAL_IDEA, font_size=29, color=MUTED).to_edge(DOWN, buff=0.38)
        formula = MathTex(
            r"3\text{ vectors}\;\not\Rightarrow\;3\text{ independent directions}",
            font_size=38,
            color=TEXT,
        ).next_to(final_idea, UP, buff=0.25)

        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title), FadeIn(axes), FadeIn(adapter.dots), FadeIn(adapter.edges), FadeIn(adapter.arrows))
        self.wait(0.5)

        self.add_fixed_in_frame_mobjects(rank3)
        self.play(FadeIn(rank3))
        self.wait(1.0)
        self.play(FadeOut(rank3))

        self.add_fixed_in_frame_mobjects(prediction)
        self.play(FadeIn(prediction))
        self.wait(1.3)
        self.play(FadeOut(prediction))

        extent = 2.9
        rank2_snapshot = model.space_to_plane(1.0)
        span_plane = Polygon(
            *(axes.c2p(*(np.zeros(3))) for _ in range(4)),
            color=FIELD_COLOR,
            fill_color=FIELD_COLOR,
            fill_opacity=0.0,
            stroke_opacity=0.0,
        )
        span_plane.set_z_index(-1)
        self.add(span_plane)

        def plane_points(snapshot: RankCollapse3DSnapshot) -> list[np.ndarray]:
            corners = np.array([
                -extent * snapshot.generator_u - extent * snapshot.generator_v,
                extent * snapshot.generator_u - extent * snapshot.generator_v,
                extent * snapshot.generator_u + extent * snapshot.generator_v,
                -extent * snapshot.generator_u + extent * snapshot.generator_v,
            ])
            return [axes.c2p(*corner) for corner in corners]

        def animate_space_to_plane(_mob, alpha: float) -> None:
            snapshot = model.space_to_plane(alpha)
            adapter.update_from_snapshot(snapshot)
            points = plane_points(snapshot)
            span_plane.set_points_as_corners([*points, points[0]])
            span_plane.set_fill(opacity=0.12 * alpha)

        self.play(
            UpdateFromAlphaFunc(adapter.mobject, animate_space_to_plane),
            run_time=9.0,
        )
        adapter.update_from_snapshot(rank2_snapshot)
        final_points = plane_points(rank2_snapshot)
        span_plane.set_points_as_corners([*final_points, final_points[0]])
        span_plane.set_fill(opacity=0.12)
        self.play(FadeOut(adapter.edges), run_time=0.8)
        self.wait(0.8)

        self.add_fixed_in_frame_mobjects(rank2)
        self.play(FadeIn(rank2))
        self.wait(2.0)
        self.play(FadeOut(rank2))

        initial_direction = rank2_snapshot.generator_u / np.linalg.norm(rank2_snapshot.generator_u)
        span_line = Line3D(
            axes.c2p(*(-5.8 * initial_direction)),
            axes.c2p(*(5.8 * initial_direction)),
            color=FIELD_COLOR,
            thickness=0.018,
        )
        span_line.set_opacity(0.0)
        self.add(span_line)

        def animate_plane_to_line(_mob, alpha: float) -> None:
            snapshot = model.plane_to_line(alpha)
            adapter.update_from_snapshot(snapshot)
            points = plane_points(snapshot)
            span_plane.set_points_as_corners([*points, points[0]])
            span_plane.set_fill(opacity=0.12 * (1.0 - alpha))
            direction = snapshot.generator_u / np.linalg.norm(snapshot.generator_u)
            span_line.put_start_and_end_on(
                axes.c2p(*(-5.8 * direction)),
                axes.c2p(*(5.8 * direction)),
            )
            span_line.set_opacity(0.65 * alpha)

        rank1_snapshot = model.plane_to_line(1.0)
        self.play(
            UpdateFromAlphaFunc(adapter.mobject, animate_plane_to_line),
            run_time=9.5,
        )
        adapter.update_from_snapshot(rank1_snapshot)
        final_direction = rank1_snapshot.generator_u / np.linalg.norm(rank1_snapshot.generator_u)
        span_line.put_start_and_end_on(
            axes.c2p(*(-5.8 * final_direction)),
            axes.c2p(*(5.8 * final_direction)),
        )
        span_line.set_opacity(0.65)
        self.play(FadeOut(span_plane), run_time=0.6)
        self.wait(0.8)

        self.add_fixed_in_frame_mobjects(rank1)
        self.play(FadeIn(rank1))
        self.wait(2.0)
        self.play(FadeOut(rank1))

        self.add_fixed_in_frame_mobjects(formula, final_idea)
        self.play(FadeIn(formula), FadeIn(final_idea))
        self.wait(3.0)
