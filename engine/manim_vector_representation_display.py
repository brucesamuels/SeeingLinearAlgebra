"""Thin Manim adapter for vector-representation display snapshots."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from manim import Arrow, DOWN, LEFT, MathTex, RIGHT, Text, VGroup

from engine.vector_representation_display import VectorRepresentationDisplaySnapshot


@dataclass(frozen=True, slots=True)
class VectorRepresentationDisplayStyle:
    arrow_buff: float = 0.0
    coordinate_scale: float = 0.8
    label_scale: float = 0.65
    horizontal_gap: float = 0.7
    vertical_gap: float = 0.35

    def __post_init__(self) -> None:
        for name in ("coordinate_scale", "label_scale", "horizontal_gap", "vertical_gap"):
            if float(getattr(self, name)) <= 0.0:
                raise ValueError(f"{name} must be positive")


class ManimVectorRepresentationDisplay(VGroup):
    """Construct mobjects only; scene timing remains external."""

    def __init__(
        self,
        snapshot: VectorRepresentationDisplaySnapshot,
        *,
        style: VectorRepresentationDisplayStyle | None = None,
    ) -> None:
        if not isinstance(snapshot, VectorRepresentationDisplaySnapshot):
            raise TypeError("snapshot must be a VectorRepresentationDisplaySnapshot")

        self.snapshot = snapshot
        self.style = style or VectorRepresentationDisplayStyle()

        self.arrow = Arrow(
            start=self._point3(snapshot.projected_origin),
            end=self._point3(snapshot.projected_endpoint),
            buff=self.style.arrow_buff,
        )
        self.row_coordinates = MathTex(snapshot.row_text).scale(
            self.style.coordinate_scale
        )
        column_body = r"\begin{bmatrix}" + r"\\".join(
            snapshot.column_entries
        ) + r"\end{bmatrix}"
        self.column_coordinates = MathTex(column_body).scale(
            self.style.coordinate_scale
        )
        self.magnitude_label = Text(snapshot.magnitude_text).scale(
            self.style.label_scale
        )
        self.dimension_label = Text(snapshot.dimension_text).scale(
            self.style.label_scale
        )
        self.zero_annotation = (
            Text(snapshot.zero_annotation).scale(self.style.label_scale)
            if snapshot.zero_annotation is not None
            else None
        )

        coordinate_group = VGroup(
            self.row_coordinates,
            self.column_coordinates,
        ).arrange(RIGHT, buff=self.style.horizontal_gap)

        items = [coordinate_group, self.magnitude_label, self.dimension_label]
        if self.zero_annotation is not None:
            items.append(self.zero_annotation)

        self.information_group = VGroup(*items).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=self.style.vertical_gap,
        )
        self.information_group.next_to(
            self.arrow,
            RIGHT,
            buff=self.style.horizontal_gap,
        )

        super().__init__(self.arrow, self.information_group)

    @staticmethod
    def _point3(point: np.ndarray) -> np.ndarray:
        values = np.asarray(point, dtype=float)
        if values.shape == (2,):
            return np.array([values[0], values[1], 0.0])
        if values.shape == (3,):
            return np.array(values, dtype=float, copy=True)
        raise ValueError("display point must have dimension 2 or 3")
