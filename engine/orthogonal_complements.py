"""Renderer-independent content for CP156: Orthogonal Complements."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


def _vec(values: Iterable[float], *, name: str) -> FloatArray:
    vector = np.asarray(tuple(values), dtype=float)
    if vector.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    if vector.size == 0:
        raise ValueError(f"{name} must not be empty")
    if not np.all(np.isfinite(vector)):
        raise ValueError(f"{name} must contain finite values")
    return vector


@dataclass(frozen=True)
class OrthogonalComplement2DSnapshot:
    x: FloatArray
    projection: FloatArray
    residual: FloatArray
    w_direction: FloatArray
    wp_direction: FloatArray


@dataclass(frozen=True)
class OrthogonalComplement3DSnapshot:
    plane_basis_1: FloatArray
    plane_basis_2: FloatArray
    complement_direction: FloatArray


class OrthogonalComplementsLesson:
    DEFINITION = (
        r"W^\perp=\{\mathbf v\in\mathbb R^n:"
        r"\mathbf v\cdot\mathbf w=0\text{ for every }\mathbf w\in W\}"
    )
    DECOMPOSITION = r"\mathbb R^n=W\oplus W^\perp"
    SPLIT = r"\mathbf x=\mathbf p+\mathbf r,\qquad \mathbf p\in W,\quad \mathbf r\in W^\perp"
    DIMENSION_FACT = r"\dim W+\dim W^\perp=n"

    def residual_snapshot(self) -> OrthogonalComplement2DSnapshot:
        return OrthogonalComplement2DSnapshot(
            x=_vec((4.0, 2.0), name="x"),
            projection=_vec((3.0, 3.0), name="projection"),
            residual=_vec((1.0, -1.0), name="residual"),
            w_direction=_vec((1.0, 1.0), name="w_direction"),
            wp_direction=_vec((1.0, -1.0), name="wp_direction"),
        )

    def plane_snapshot(self) -> OrthogonalComplement3DSnapshot:
        return OrthogonalComplement3DSnapshot(
            plane_basis_1=_vec((2.0, 0.0, 0.0), name="plane_basis_1"),
            plane_basis_2=_vec((0.0, 2.0, 0.0), name="plane_basis_2"),
            complement_direction=_vec((0.0, 0.0, 2.4), name="complement_direction"),
        )

    @property
    def bridge_prompt(self) -> str:
        return "How can we build orthogonal directions that span a subspace?"
