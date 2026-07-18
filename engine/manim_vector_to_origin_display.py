"""Thin Manim display adapter for a vector translated to the origin."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import numpy as np
from manim import (
    Arrow,
    DecimalNumber,
    Dot,
    DOWN,
    LEFT,
    MathTex,
    NumberPlane,
    RIGHT,
    UP,
    VGroup,
)

from engine.vector_to_origin_translation import (
    VectorToOriginTranslationSnapshot,
)


def _format_number(value: float) -> str:
    numeric = float(value)
    if np.isclose(numeric, round(numeric), atol=1e-8):
        return str(int(round(numeric)))
    text = f"{numeric:.2f}".rstrip("0").rstrip(".")
    return "0" if text == "-0" else text


def _pair_source(values: np.ndarray) -> str:
    return rf"\left({_format_number(values[0])},{_format_number(values[1])}\right)"


def _copied_options(
    options: Mapping[str, Any] | None,
    *,
    name: str,
) -> dict[str, Any]:
    if options is None:
        return {}
    if not isinstance(options, Mapping):
        raise TypeError(f"{name} must be a mapping")
    return dict(options)


class _CoordinatePair(VGroup):
    """Persistent ordered-pair readout built from two DecimalNumber objects."""

    def __init__(self, values: np.ndarray, options: Mapping[str, Any]) -> None:
        self.x_value = DecimalNumber(
            float(values[0]),
            num_decimal_places=1,
            **options,
        )
        self.y_value = DecimalNumber(
            float(values[1]),
            num_decimal_places=1,
            **options,
        )
        punctuation_options = {
            key: value
            for key, value in options.items()
            if key in {"color", "font_size"}
        }
        super().__init__(
            MathTex("(", **punctuation_options),
            self.x_value,
            MathTex(",", **punctuation_options),
            self.y_value,
            MathTex(")", **punctuation_options),
        )
        self.arrange(RIGHT, buff=0.035)

    def set_values(self, values: np.ndarray) -> None:
        self.x_value.set_value(float(values[0]))
        self.y_value.set_value(float(values[1]))
        self.arrange(RIGHT, buff=0.035)


class ManimVectorToOriginDisplay:
    """Own synchronized Manim objects for one translation snapshot."""

    __slots__ = (
        "_arrow_kwargs",
        "_delta_pair",
        "_formula_anchor",
        "_formula_kwargs",
        "_formula_tail_pair",
        "_formula_tail_minus_pair",
        "_formula_tip_minus_pair",
        "_formula_tip_pair",
        "_label_kwargs",
        "_plane",
        "_point_kwargs",
        "_progress_number",
        "_snapshot",
        "_tail_pair",
        "_tip_pair",
        "_vector_coordinates",
        "arrow",
        "formula",
        "mobject",
        "tail_dot",
        "tail_label",
        "tip_dot",
        "tip_label",
    )

    def __init__(
        self,
        snapshot: VectorToOriginTranslationSnapshot,
        plane: NumberPlane,
        *,
        formula_anchor: tuple[float, float, float] = (3.6, -0.25, 0.0),
        arrow_kwargs: Mapping[str, Any] | None = None,
        point_kwargs: Mapping[str, Any] | None = None,
        label_kwargs: Mapping[str, Any] | None = None,
        formula_kwargs: Mapping[str, Any] | None = None,
    ) -> None:
        self._validate_snapshot(snapshot)
        if not isinstance(plane, NumberPlane):
            raise TypeError("plane must be a NumberPlane")

        anchor = np.asarray(formula_anchor, dtype=float)
        if anchor.shape != (3,) or not np.all(np.isfinite(anchor)):
            raise ValueError("formula_anchor must contain three finite values")

        self._plane = plane
        self._formula_anchor = np.array(anchor, dtype=float, copy=True)
        self._arrow_kwargs = _copied_options(arrow_kwargs, name="arrow_kwargs")
        self._point_kwargs = _copied_options(point_kwargs, name="point_kwargs")
        self._label_kwargs = _copied_options(label_kwargs, name="label_kwargs")
        self._formula_kwargs = _copied_options(formula_kwargs, name="formula_kwargs")
        self._vector_coordinates = np.array(
            snapshot.vector_coordinates,
            dtype=float,
            copy=True,
        )

        start = self._display_point(snapshot.current_initial_point)
        end = self._display_point(snapshot.current_terminal_point)

        self.arrow = Arrow(start=start, end=end, buff=0.0, **self._arrow_kwargs)
        self.tail_dot = Dot(start, **self._point_kwargs)
        self.tip_dot = Dot(end, **self._point_kwargs)

        self._tail_pair = _CoordinatePair(
            snapshot.current_initial_point,
            self._label_kwargs,
        )
        self._tip_pair = _CoordinatePair(
            snapshot.current_terminal_point,
            self._label_kwargs,
        )
        self.tail_label = VGroup(
            MathTex(r"\text{initial }", **self._label_kwargs),
            self._tail_pair,
        ).arrange(RIGHT, buff=0.08)
        self.tip_label = VGroup(
            MathTex(r"\text{terminal }", **self._label_kwargs),
            self._tip_pair,
        ).arrange(RIGHT, buff=0.08)

        self._progress_number = DecimalNumber(
            snapshot.progress,
            num_decimal_places=2,
            **self._formula_kwargs,
        )
        self._delta_pair = _CoordinatePair(
            snapshot.translation,
            self._formula_kwargs,
        )
        self._formula_tail_pair = _CoordinatePair(
            snapshot.current_initial_point,
            self._formula_kwargs,
        )
        self._formula_tip_pair = _CoordinatePair(
            snapshot.current_terminal_point,
            self._formula_kwargs,
        )
        self._formula_tip_minus_pair = _CoordinatePair(
            snapshot.current_terminal_point,
            self._formula_kwargs,
        )
        vector_pair = _CoordinatePair(
            snapshot.vector_coordinates,
            self._formula_kwargs,
        )

        original_tail_source = _pair_source(snapshot.original.origin)
        original_tip_source = _pair_source(snapshot.original.endpoint)
        row_one = VGroup(
            MathTex(r"t=", **self._formula_kwargs),
            self._progress_number,
            MathTex(
                rf",\quad \Delta_t=-t{original_tail_source}=",
                **self._formula_kwargs,
            ),
            self._delta_pair,
        ).arrange(RIGHT, buff=0.06)
        row_two = VGroup(
            MathTex(
                rf"P_t={original_tail_source}+\Delta_t=",
                **self._formula_kwargs,
            ),
            self._formula_tail_pair,
        ).arrange(RIGHT, buff=0.06)
        row_three = VGroup(
            MathTex(
                rf"Q_t={original_tip_source}+\Delta_t=",
                **self._formula_kwargs,
            ),
            self._formula_tip_pair,
        ).arrange(RIGHT, buff=0.06)
        row_four = VGroup(
            MathTex(r"\mathbf{v}=Q_t-P_t=", **self._formula_kwargs),
            self._formula_tip_minus_pair,
            MathTex("-", **self._formula_kwargs),
            _CoordinatePair(
                snapshot.current_initial_point,
                self._formula_kwargs,
            ),
            MathTex("=", **self._formula_kwargs),
            vector_pair,
        ).arrange(RIGHT, buff=0.06)

        # The copied tail pair in row four needs its own persistent handle.
        self._formula_tail_minus_pair = row_four[3]

        self.formula = VGroup(row_one, row_two, row_three, row_four).arrange(
            DOWN,
            buff=0.16,
            aligned_edge=LEFT,
        )

        self._position_coordinate_labels()
        self.formula.move_to(self._formula_anchor)

        self.mobject = VGroup(
            self.arrow,
            self.tail_dot,
            self.tip_dot,
            self.tail_label,
            self.tip_label,
            self.formula,
        )
        self._snapshot = snapshot

    @property
    def snapshot(self) -> VectorToOriginTranslationSnapshot:
        return self._snapshot

    @property
    def tail_label_source(self) -> str:
        return rf"\text{{initial }}{_pair_source(self._snapshot.current_initial_point)}"

    @property
    def tip_label_source(self) -> str:
        return rf"\text{{terminal }}{_pair_source(self._snapshot.current_terminal_point)}"

    @property
    def formula_source(self) -> str:
        snapshot = self._snapshot
        progress = _format_number(snapshot.progress)
        return (
            rf"\Delta_{{{progress}}}={_pair_source(snapshot.translation)}; "
            rf"P_{{{progress}}}={_pair_source(snapshot.current_initial_point)}; "
            rf"Q_{{{progress}}}={_pair_source(snapshot.current_terminal_point)}; "
            rf"\mathbf{{v}}={_pair_source(snapshot.current_terminal_point)}"
            rf"-{_pair_source(snapshot.current_initial_point)}"
            rf"={_pair_source(snapshot.vector_coordinates)}"
        )

    def update_from_snapshot(
        self,
        snapshot: VectorToOriginTranslationSnapshot,
    ) -> None:
        self._validate_snapshot(snapshot)
        if not np.allclose(snapshot.vector_coordinates, self._vector_coordinates):
            raise ValueError("display updates must preserve vector coordinates")

        start = self._display_point(snapshot.current_initial_point)
        end = self._display_point(snapshot.current_terminal_point)
        self.arrow.put_start_and_end_on(start, end)
        self.tail_dot.move_to(start)
        self.tip_dot.move_to(end)

        self._tail_pair.set_values(snapshot.current_initial_point)
        self._tip_pair.set_values(snapshot.current_terminal_point)
        self.tail_label.arrange(RIGHT, buff=0.08)
        self.tip_label.arrange(RIGHT, buff=0.08)

        self._progress_number.set_value(snapshot.progress)
        self._delta_pair.set_values(snapshot.translation)
        self._formula_tail_pair.set_values(snapshot.current_initial_point)
        self._formula_tip_pair.set_values(snapshot.current_terminal_point)
        self._formula_tip_minus_pair.set_values(snapshot.current_terminal_point)
        self._formula_tail_minus_pair.set_values(snapshot.current_initial_point)
        for row in self.formula:
            row.arrange(RIGHT, buff=0.06)
        self.formula.arrange(DOWN, buff=0.16, aligned_edge=LEFT)

        self._position_coordinate_labels()
        self.formula.move_to(self._formula_anchor)
        self._snapshot = snapshot

    def _display_point(self, point: np.ndarray) -> np.ndarray:
        return self._plane.c2p(float(point[0]), float(point[1]))

    def _position_coordinate_labels(self) -> None:
        axis_x = float(self._plane.c2p(0.0, 0.0)[0])
        progress = float(self._progress_number.get_value())
        progress = max(0.0, min(1.0, progress))

        self.tail_label.next_to(self.tail_dot, DOWN, buff=0.12)

        base_right_shift = 0.22
        additional_left_travel = 0.95 * progress
        horizontal_shift = base_right_shift - additional_left_travel
        self.tail_label.shift(RIGHT * horizontal_shift)

        label_left = float(self.tail_label.get_left()[0])
        label_right = float(self.tail_label.get_right()[0])
        axis_margin = 0.12
        if label_left - axis_margin <= axis_x <= label_right + axis_margin:
            extra_left_shift = label_right - axis_x + axis_margin
            self.tail_label.shift(LEFT * extra_left_shift)

        self.tail_label.set_z_index(10)
        self.tip_label.next_to(self.tip_dot, UP + RIGHT, buff=0.12)

    @staticmethod
    def _validate_snapshot(snapshot: VectorToOriginTranslationSnapshot) -> None:
        if not isinstance(snapshot, VectorToOriginTranslationSnapshot):
            raise TypeError("snapshot must be a VectorToOriginTranslationSnapshot")
        if snapshot.current.dimension != 2:
            raise ValueError("ManimVectorToOriginDisplay requires two dimensions")
