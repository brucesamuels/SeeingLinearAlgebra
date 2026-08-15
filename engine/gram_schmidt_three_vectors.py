"""Renderer-independent content for CP159: Gram-Schmidt in R^3."""

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
class GramSchmidtThreeVectorsSnapshot:
    v1: FloatArray
    v2: FloatArray
    v3: FloatArray
    proj_v2_on_u1: FloatArray
    u1: FloatArray
    u2: FloatArray
    proj_v3_on_u1: FloatArray
    w3: FloatArray
    proj_v3_on_u2: FloatArray
    u3: FloatArray


class GramSchmidtThreeVectorsLesson:
    GENERAL_STEP = r"\mathbf u_k=\mathbf v_k-\sum_{j=1}^{k-1}\operatorname{proj}_{\mathbf u_j}\mathbf v_k"
    NORMALIZE_NOTE = r"\mathbf e_k=\frac{\mathbf u_k}{\|\mathbf u_k\|}\quad\text{if an orthonormal set is desired}"
    SPAN_FACT = r"\operatorname{span}\{\mathbf u_1,\mathbf u_2,\mathbf u_3\}=\operatorname{span}\{\mathbf v_1,\mathbf v_2,\mathbf v_3\}"

    def snapshot(self) -> GramSchmidtThreeVectorsSnapshot:
        v1 = _vec((2.0, 2.0, 0.0), name="v1")
        v2 = _vec((2.0, 0.0, 2.0), name="v2")
        v3 = _vec((3.0, -1.0, 1.0), name="v3")
        proj_v2_on_u1 = _vec((1.0, 1.0, 0.0), name="proj_v2_on_u1")
        u1 = _vec((2.0, 2.0, 0.0), name="u1")
        u2 = _vec((1.0, -1.0, 2.0), name="u2")
        proj_v3_on_u1 = _vec((1.0, 1.0, 0.0), name="proj_v3_on_u1")
        w3 = _vec((2.0, -2.0, 1.0), name="w3")
        proj_v3_on_u2 = _vec((1.0, -1.0, 2.0), name="proj_v3_on_u2")
        u3 = _vec((1.0, -1.0, -1.0), name="u3")
        return GramSchmidtThreeVectorsSnapshot(
            v1=v1,
            v2=v2,
            v3=v3,
            proj_v2_on_u1=proj_v2_on_u1,
            u1=u1,
            u2=u2,
            proj_v3_on_u1=proj_v3_on_u1,
            w3=w3,
            proj_v3_on_u2=proj_v3_on_u2,
            u3=u3,
        )

    @property
    def closing_prompt(self) -> str:
        return "Subtract every earlier projection, then normalize if you want an orthonormal basis."
