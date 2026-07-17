"""Renderer-independent display projection for vector representations."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray

from engine.vector_representation import VectorRepresentationSnapshot


FloatArray = NDArray[np.float64]


def _readonly_vector(values: ArrayLike, *, label: str) -> FloatArray:
    array = np.asarray(values, dtype=float)

    if array.ndim != 1:
        raise ValueError(f"{label} must be one-dimensional")
    if array.size not in (2, 3):
        raise ValueError(f"{label} must have display dimension 2 or 3")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{label} must contain finite values")

    result = np.array(array, dtype=float, copy=True)
    result.setflags(write=False)
    return result


@dataclass(frozen=True, slots=True)
class VectorRepresentationDisplaySnapshot:
    """Display-ready renderer-independent view of one vector."""

    projected_origin: FloatArray
    projected_endpoint: FloatArray
    projected_vector: FloatArray
    row_text: str
    column_entries: tuple[str, ...]
    magnitude_text: str
    dimension_text: str
    zero_annotation: str | None
    source_dimension: int
    display_dimension: int

    def __post_init__(self) -> None:
        origin = _readonly_vector(
            self.projected_origin,
            label="projected_origin",
        )
        endpoint = _readonly_vector(
            self.projected_endpoint,
            label="projected_endpoint",
        )
        vector = _readonly_vector(
            self.projected_vector,
            label="projected_vector",
        )

        if origin.shape != endpoint.shape or origin.shape != vector.shape:
            raise ValueError("projected arrays must have matching shapes")
        if not np.allclose(endpoint, origin + vector):
            raise ValueError(
                "projected_endpoint must equal projected_origin "
                "plus projected_vector"
            )
        if self.display_dimension != vector.size:
            raise ValueError(
                "display_dimension must equal projected vector size"
            )
        if self.source_dimension < self.display_dimension:
            raise ValueError(
                "source_dimension cannot be smaller than display_dimension"
            )

        for label, value in (
            ("row_text", self.row_text),
            ("magnitude_text", self.magnitude_text),
            ("dimension_text", self.dimension_text),
        ):
            if not isinstance(value, str):
                raise TypeError(f"{label} must be a string")
            if not value.strip():
                raise ValueError(f"{label} must be nonempty")

        if not isinstance(self.column_entries, tuple):
            raise TypeError("column_entries must be a tuple")
        if len(self.column_entries) != self.source_dimension:
            raise ValueError(
                "column entry count must equal source dimension"
            )
        if any(
            not isinstance(entry, str) or not entry.strip()
            for entry in self.column_entries
        ):
            raise ValueError("column entries must be nonempty strings")

        if self.zero_annotation is not None:
            if not isinstance(self.zero_annotation, str):
                raise TypeError("zero_annotation must be a string or None")
            if not self.zero_annotation.strip():
                raise ValueError(
                    "zero_annotation must be nonempty when present"
                )

        object.__setattr__(self, "projected_origin", origin)
        object.__setattr__(self, "projected_endpoint", endpoint)
        object.__setattr__(self, "projected_vector", vector)


class VectorRepresentationDisplayProjector:
    """Project mathematical vector state into display-ready values."""

    __slots__ = (
        "_display_dimension",
        "_number_format",
        "_magnitude_label",
        "_zero_annotation",
    )

    def __init__(
        self,
        *,
        display_dimension: int = 2,
        number_format: str = ".2f",
        magnitude_label: str = "magnitude",
        zero_annotation: str = "zero vector",
    ) -> None:
        if display_dimension not in (2, 3):
            raise ValueError("display_dimension must be 2 or 3")
        if not isinstance(number_format, str) or not number_format:
            raise ValueError("number_format must be a nonempty string")
        if not isinstance(magnitude_label, str) or not magnitude_label.strip():
            raise ValueError("magnitude_label must be nonempty")
        if not isinstance(zero_annotation, str) or not zero_annotation.strip():
            raise ValueError("zero_annotation must be nonempty")

        try:
            format(0.0, number_format)
        except (ValueError, TypeError) as exc:
            raise ValueError("number_format is invalid") from exc

        self._display_dimension = display_dimension
        self._number_format = number_format
        self._magnitude_label = magnitude_label.strip()
        self._zero_annotation = zero_annotation.strip()

    @property
    def display_dimension(self) -> int:
        return self._display_dimension

    def project(
        self,
        snapshot: VectorRepresentationSnapshot,
    ) -> VectorRepresentationDisplaySnapshot:
        if not isinstance(snapshot, VectorRepresentationSnapshot):
            raise TypeError(
                "snapshot must be a VectorRepresentationSnapshot"
            )
        if snapshot.dimension < self._display_dimension:
            raise ValueError(
                "source vector dimension is smaller than display dimension"
            )

        projected_origin = snapshot.origin[: self._display_dimension]
        projected_endpoint = snapshot.endpoint[: self._display_dimension]
        projected_vector = snapshot.coordinates[: self._display_dimension]

        formatted_entries = tuple(
            self._format_number(value)
            for value in snapshot.row_coordinates
        )
        row_text = "[" + ", ".join(formatted_entries) + "]"
        magnitude_text = (
            f"{self._magnitude_label} = "
            f"{self._format_number(snapshot.magnitude)}"
        )
        dimension_text = f"dimension = {snapshot.dimension}"

        return VectorRepresentationDisplaySnapshot(
            projected_origin=projected_origin,
            projected_endpoint=projected_endpoint,
            projected_vector=projected_vector,
            row_text=row_text,
            column_entries=formatted_entries,
            magnitude_text=magnitude_text,
            dimension_text=dimension_text,
            zero_annotation=(
                self._zero_annotation if snapshot.is_zero else None
            ),
            source_dimension=snapshot.dimension,
            display_dimension=self._display_dimension,
        )

    def _format_number(self, value: float) -> str:
        return format(float(value), self._number_format)
