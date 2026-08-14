"""Renderer-independent content for CP158: From Orthogonal to Orthonormal."""

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
class OrthonormalizationSnapshot:
    u1: FloatArray
    u2: FloatArray
    e1: FloatArray
    e2: FloatArray
    norm_u1: float
    norm_u2: float


class OrthonormalizationLesson:
    NORMALIZE_1 = r"\mathbf e_1=\frac{\mathbf u_1}{\|\mathbf u_1\|}"
    NORMALIZE_2 = r"\mathbf e_2=\frac{\mathbf u_2}{\|\mathbf u_2\|}"
    UNIT_FACTS = r"\|\mathbf e_1\|=\|\mathbf e_2\|=1"
    ORTHOGONALITY = r"\mathbf e_1\cdot\mathbf e_2=0"
    SPAN_FACT = (
        r"\operatorname{span}\{\mathbf e_1,\mathbf e_2\}="
        r"\operatorname{span}\{\mathbf u_1,\mathbf u_2\}"
    )

    def snapshot(self) -> OrthonormalizationSnapshot:
        u1 = _vec((1.0, 2.0), name="u1")
        u2 = _vec((2.0, -1.0), name="u2")
        norm_u1 = float(np.linalg.norm(u1))
        norm_u2 = float(np.linalg.norm(u2))
        return OrthonormalizationSnapshot(
            u1=u1,
            u2=u2,
            e1=u1 / norm_u1,
            e2=u2 / norm_u2,
            norm_u1=norm_u1,
            norm_u2=norm_u2,
        )

    @property
    def bridge_prompt(self) -> str:
        return "What happens when these orthonormal vectors become the columns of a matrix?"
