"""Annotated full-rank 3D presentation with independent synchronized scalars.

The original matrix A is written first. Independent scalars a, b, and c are
then applied to its three columns. Each matrix column and its common-origin
vector are driven by the same ValueTracker. The resultant is revealed only
after all three scalar sweeps are complete.
"""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow3D,
    BLUE,
    Create,
    DEGREES,
    Dot3D,
    FadeIn,
    GREEN,
    LaggedStart,
    Line3D,
    MathTex,
    PURPLE,
    ReplacementTransform,
    Text,
    ThreeDAxes,
    ThreeDScene,
    ValueTracker,
    VGroup,
    WHITE,
    Write,
    YELLOW,
    always_redraw,
    linear,
)

from scenes.linear_combination_native_3d_smoke import (
    SMOKE_VECTORS,
    _parallelepiped_edges,
)


VECTOR_COLORS = (BLUE, GREEN, PURPLE)
VECTOR_NAMES = (r"\mathbf{u}", r"\mathbf{v}", r"\mathbf{w}")
TARGET_COEFFICIENTS = np.array([1.80, 0.45, 1.60], dtype=float)
ORIGINAL_VECTOR_RUN_TIME = 2.0
COEFFICIENT_RUN_TIME = 2.8
ARROW_EPSILON = 1.0e-4
HEAD_REVEAL_START = 0.18
HEAD_REVEAL_END = 0.45
CAMERA_ZOOM = 1.35


def _matrix_tex(matrix: np.ndarray) -> str:
    rows = [
        "&".join(f"{value:.2f}" for value in row)
        for row in matrix
    ]
    return (
        r"\begin{bmatrix}"
        + r"\\".join(rows)
        + r"\end{bmatrix}"
    )


def _coordinate_column(vector: np.ndarray) -> str:
    entries = r"\\".join(f"{value:.2f}" for value in vector)
    return rf"\begin{{bmatrix}}{entries}\end{{bmatrix}}"


def _original_column_matrix() -> np.ndarray:
    """Return A with u, v, w as columns."""

    return SMOKE_VECTORS.T.copy()


def _scaled_column_matrix(coefficients: np.ndarray) -> np.ndarray:
    """Return [a u, b v, c w]."""

    values = np.asarray(coefficients, dtype=float)
    if values.shape != (3,):
        raise ValueError("coefficients must have shape (3,)")
    return _original_column_matrix() * values[np.newaxis, :]


def _scaled_vectors(coefficients: np.ndarray) -> np.ndarray:
    """Return the three independently scaled common-origin vectors."""

    values = np.asarray(coefficients, dtype=float)
    if values.shape != (3,):
        raise ValueError("coefficients must have shape (3,)")
    return values[:, np.newaxis] * SMOKE_VECTORS


def _result_for_coefficients(coefficients: np.ndarray) -> np.ndarray:
    """Return a u + b v + c w."""

    return _scaled_vectors(coefficients).sum(axis=0)


def _head_reveal_factor(progress: float) -> float:
    normalized = (
        float(progress) - HEAD_REVEAL_START
    ) / (HEAD_REVEAL_END - HEAD_REVEAL_START)
    return float(np.clip(normalized, 0.0, 1.0))


def _dynamic_arrow(
    *,
    axes: ThreeDAxes,
    origin: np.ndarray,
    vector: np.ndarray,
    draw_tracker: ValueTracker,
    coefficient_tracker: ValueTracker,
    color,
    thickness: float = 0.04,
) -> Arrow3D:
    draw_progress = max(draw_tracker.get_value(), ARROW_EPSILON)
    coefficient = coefficient_tracker.get_value()
    endpoint = axes.c2p(*(draw_progress * coefficient * vector))
    head_factor = _head_reveal_factor(draw_progress)

    return Arrow3D(
        start=origin,
        end=endpoint,
        thickness=thickness,
        height=max(ARROW_EPSILON, 0.25 * head_factor),
        base_radius=max(ARROW_EPSILON, 0.08 * head_factor),
        resolution=12,
        color=color,
    )


class FullRankLinearCombination3DPresentation(ThreeDScene):
    """Present three independently scaled columns of a full-rank matrix."""

    def construct(self) -> None:
        axes = ThreeDAxes(
            x_range=(-5.0, 6.0, 1.0),
            y_range=(-5.0, 6.0, 1.0),
            z_range=(-4.0, 6.0, 1.0),
            x_length=7.0,
            y_length=7.0,
            z_length=6.0,
        )
        axes_origin = axes.c2p(0.0, 0.0, 0.0)

        title = Text("Independent Scalars in a 3D Linear Combination", font_size=29)
        title.to_edge(np.array([0.0, 1.0, 0.0]))

        origin_dot = Dot3D(point=axes_origin, radius=0.055, color=WHITE)
        origin_label = MathTex("O", font_size=28, color=WHITE)
        origin_label.move_to(axes_origin + np.array([-0.22, -0.18, 0.0]))

        axis_labels = VGroup(
            MathTex("x", font_size=26).move_to(axes.c2p(5.4, 0.0, 0.0)),
            MathTex("y", font_size=26).move_to(axes.c2p(0.0, 5.4, 0.0)),
            MathTex("z", font_size=26).move_to(axes.c2p(0.0, 0.0, 5.4)),
        )

        original_matrix_overlay = VGroup(
            MathTex(
                r"A=[\,\mathbf{u}\ \mathbf{v}\ \mathbf{w}\,]",
                font_size=28,
            ),
            MathTex(
                _matrix_tex(_original_column_matrix()),
                font_size=28,
            ),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.10)
        original_matrix_overlay.to_corner(np.array([-1.0, 1.0, 0.0]))

        coefficient_trackers = tuple(
            ValueTracker(1.0) for _ in range(3)
        )

        def current_coefficients() -> np.ndarray:
            return np.array(
                [tracker.get_value() for tracker in coefficient_trackers],
                dtype=float,
            )

        live_overlay = always_redraw(
            lambda: VGroup(
                MathTex(
                    rf"\begin{{bmatrix}}a\\b\\c\end{{bmatrix}}"
                    rf"={_coordinate_column(current_coefficients())}",
                    font_size=25,
                    color=YELLOW,
                ),
                MathTex(
                    rf"[\,a\mathbf{{u}}\ b\mathbf{{v}}\ c\mathbf{{w}}\,]"
                    rf"={_matrix_tex(_scaled_column_matrix(current_coefficients()))}",
                    font_size=24,
                ),
            )
            .arrange(np.array([0.0, -1.0, 0.0]), buff=0.08)
            .to_corner(np.array([-1.0, -1.0, 0.0]))
        )
        live_overlay.set_opacity(0.0)

        original_labels = VGroup(
            *(
                MathTex(name, font_size=31, color=color)
                for name, color in zip(
                    VECTOR_NAMES, VECTOR_COLORS, strict=True
                )
            )
        )
        scaled_labels = VGroup(
            *(
                MathTex(rf"{symbol}{name}", font_size=31, color=color)
                for symbol, name, color in zip(
                    ("a", "b", "c"),
                    VECTOR_NAMES,
                    VECTOR_COLORS,
                    strict=True,
                )
            )
        )
        original_labels.set_opacity(0.0)
        scaled_labels.set_opacity(0.0)

        self.set_camera_orientation(
            phi=68 * DEGREES,
            theta=-42 * DEGREES,
            zoom=CAMERA_ZOOM,
        )
        self.add_fixed_in_frame_mobjects(
            title,
            original_matrix_overlay,
            live_overlay,
        )
        self.add_fixed_orientation_mobjects(
            origin_label,
            axis_labels,
            original_labels,
            scaled_labels,
        )

        self.play(
            FadeIn(axes),
            FadeIn(origin_dot),
            FadeIn(origin_label),
            FadeIn(axis_labels),
            FadeIn(title),
        )
        self.play(Write(original_matrix_overlay), run_time=1.8)
        self.wait(0.6)

        draw_trackers = tuple(
            ValueTracker(0.0) for _ in range(3)
        )

        dynamic_arrows = VGroup(
            *(
                always_redraw(
                    lambda vector=vector,
                    color=color,
                    draw_tracker=draw_tracker,
                    coefficient_tracker=coefficient_tracker: _dynamic_arrow(
                        axes=axes,
                        origin=axes_origin,
                        vector=vector,
                        draw_tracker=draw_tracker,
                        coefficient_tracker=coefficient_tracker,
                        color=color,
                    )
                )
                for (
                    vector,
                    color,
                    draw_tracker,
                    coefficient_tracker,
                ) in zip(
                    SMOKE_VECTORS,
                    VECTOR_COLORS,
                    draw_trackers,
                    coefficient_trackers,
                    strict=True,
                )
            )
        )
        self.add(dynamic_arrows)

        for vector, label, draw_tracker in zip(
            SMOKE_VECTORS,
            original_labels,
            draw_trackers,
            strict=True,
        ):
            self.play(
                draw_tracker.animate.set_value(1.0),
                run_time=ORIGINAL_VECTOR_RUN_TIME,
                rate_func=linear,
            )
            endpoint = axes.c2p(*vector)
            label.move_to(endpoint + np.array([0.15, 0.15, 0.12]))
            self.play(label.animate.set_opacity(1.0), run_time=0.3)

        self.wait(0.6)
        self.play(live_overlay.animate.set_opacity(1.0), run_time=0.6)

        self.play(
            *(
                tracker.animate.set_value(float(target))
                for tracker, target in zip(
                    coefficient_trackers,
                    TARGET_COEFFICIENTS,
                    strict=True,
                )
            ),
            run_time=COEFFICIENT_RUN_TIME,
            rate_func=linear,
        )

        final_scaled_vectors = _scaled_vectors(TARGET_COEFFICIENTS)
        for vector, old_label, new_label in zip(
            final_scaled_vectors,
            original_labels,
            scaled_labels,
            strict=True,
        ):
            endpoint = axes.c2p(*vector)
            new_label.move_to(endpoint + np.array([0.15, 0.15, 0.12]))
            self.play(
                ReplacementTransform(old_label, new_label),
                run_time=0.35,
            )

        box_edges = tuple(
            Line3D(
                start=axes.c2p(*start),
                end=axes.c2p(*end),
                thickness=0.007,
                color=WHITE,
            ).set_opacity(0.30)
            for start, end in _parallelepiped_edges(
                *final_scaled_vectors
            )
        )
        self.play(
            LaggedStart(
                *(Create(edge) for edge in box_edges),
                lag_ratio=0.06,
            ),
            run_time=2.0,
        )
        self.wait(0.6)

        final_result = _result_for_coefficients(TARGET_COEFFICIENTS)
        result_point = axes.c2p(*final_result)
        result_endpoint = Dot3D(
            point=result_point,
            radius=0.075,
            color=YELLOW,
        )
        resultant = Arrow3D(
            start=axes_origin,
            end=result_point,
            thickness=0.06,
            height=0.25,
            base_radius=0.08,
            resolution=12,
            color=YELLOW,
        )

        result_overlay = VGroup(
            MathTex(
                r"\mathbf{r}"
                r"=a\mathbf{u}"
                r"+b\mathbf{v}"
                r"+c\mathbf{w}",
                font_size=31,
                color=YELLOW,
            ),
            MathTex(
                rf"\mathbf{{r}}={_coordinate_column(final_result)}",
                font_size=29,
                color=YELLOW,
            ),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.10)
        result_overlay.to_corner(np.array([1.0, 1.0, 0.0]))
        result_overlay.set_opacity(0.0)
        self.add_fixed_in_frame_mobjects(result_overlay)

        self.play(
            dynamic_arrows.animate.set_opacity(0.70),
            FadeIn(result_endpoint),
            run_time=0.6,
        )
        self.play(
            FadeIn(resultant),
            result_overlay.animate.set_opacity(1.0),
            run_time=1.3,
        )
        self.wait(1.2)

        self.move_camera(
            theta=138 * DEGREES,
            run_time=6.0,
            rate_func=linear,
        )
        self.wait(0.5)
