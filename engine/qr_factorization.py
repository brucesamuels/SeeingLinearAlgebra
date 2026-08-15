"""Renderer-independent content for CP160: QR Factorization."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class QRFactorizationSnapshot:
    a1: FloatArray
    a2: FloatArray
    A: FloatArray
    q1: FloatArray
    q2: FloatArray
    Q: FloatArray
    R: FloatArray
    a1_q1_component: FloatArray
    a2_q1_component: FloatArray
    a2_q2_component: FloatArray


class QRFactorizationLesson:
    Q_ORTHONORMAL = r"Q^TQ=I"
    R_FROM_QA = r"R=Q^TA"
    R_FROM_QINV_A = r"R=Q^{-1}A"
    Q_INVERSE_TRANSPOSE = r"Q^{-1}=Q^T"
    QR_FACTORIZATION = r"A=QR"
    TRIANGULAR_REASON = "Each new Gram-Schmidt direction is perpendicular to the earlier ones."

    def snapshot(self) -> QRFactorizationSnapshot:
        sqrt5 = np.sqrt(5.0)
        a1 = np.array([1.0, 2.0])
        a2 = np.array([4.0, 3.0])
        A = np.column_stack((a1, a2))
        q1 = np.array([1.0, 2.0]) / sqrt5
        q2 = np.array([2.0, -1.0]) / sqrt5
        Q = np.column_stack((q1, q2))
        R = np.array([[sqrt5, 2.0 * sqrt5], [0.0, sqrt5]])
        return QRFactorizationSnapshot(
            a1=a1,
            a2=a2,
            A=A,
            q1=q1,
            q2=q2,
            Q=Q,
            R=R,
            a1_q1_component=sqrt5 * q1,
            a2_q1_component=2.0 * sqrt5 * q1,
            a2_q2_component=sqrt5 * q2,
        )

    @property
    def bridge_prompt(self) -> str:
        return "What if b is not exactly in the column space of A?"
