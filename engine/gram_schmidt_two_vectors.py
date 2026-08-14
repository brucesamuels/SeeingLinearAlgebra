"""Renderer-independent content for CP157: Gram-Schmidt with two vectors."""

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
class GramSchmidtPairSnapshot:
    v1: FloatArray
    v2: FloatArray
    projection: FloatArray
    u1: FloatArray
    u2: FloatArray


class GramSchmidtTwoVectorsLesson:
    ORTHOGONALITY = r"\mathbf u_1\cdot\mathbf u_2=0"
    SPAN_FACT = r"\operatorname{span}\{\mathbf u_1,\mathbf u_2\}=\operatorname{span}\{\mathbf v_1,\mathbf v_2\}"
    STEP_FORMULA = (
        r"\mathbf u_2=\mathbf v_2-\operatorname{proj}_{\mathbf u_1}\mathbf v_2"
    )
    GENERAL_FORMULA = (
        r"\mathbf u_2=\mathbf v_2-"
        r"\frac{\mathbf v_2\cdot\mathbf u_1}{\mathbf u_1\cdot\mathbf u_1}\mathbf u_1"
    )

    def pair_snapshot(self) -> GramSchmidtPairSnapshot:
        return GramSchmidtPairSnapshot(
            v1=_vec((1.0, 2.0), name="v1"),
            v2=_vec((4.0, 3.0), name="v2"),
            projection=_vec((2.0, 4.0), name="projection"),
            u1=_vec((1.0, 2.0), name="u1"),
            u2=_vec((2.0, -1.0), name="u2"),
        )

    @property
    def bridge_prompt(self) -> str:
        return "Next, scale the orthogonal directions to make them orthonormal."
