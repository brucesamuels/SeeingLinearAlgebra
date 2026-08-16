"""Numerical model for CP161: least squares as orthogonal projection."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class LeastSquaresProjectionSnapshot:
    A: np.ndarray
    b: np.ndarray
    a1: np.ndarray
    a2: np.ndarray
    x_hat: np.ndarray
    projection: np.ndarray
    residual: np.ndarray
    ata: np.ndarray
    atb: np.ndarray
    q1: np.ndarray
    q2: np.ndarray
    Q: np.ndarray
    R: np.ndarray
    qtb: np.ndarray


class LeastSquaresProjectionLesson:
    """A small full-column-rank example with exact, readable arithmetic."""

    NORMAL_EQUATION = r"A^TA\widehat{\mathbf x}=A^T\mathbf b"
    RESIDUAL_ORTHOGONALITY = r"A^T\mathbf r=\mathbf 0"
    QR_LEAST_SQUARES = r"R\widehat{\mathbf x}=Q^T\mathbf b"
    CLOSING_IDEA = "Least squares is orthogonal projection translated into equations."

    def snapshot(self) -> LeastSquaresProjectionSnapshot:
        a1 = np.array([1.0, 0.0, 1.0])
        a2 = np.array([0.0, 1.0, 1.0])
        A = np.column_stack((a1, a2))
        b = np.array([2.0, 2.0, 1.0])

        ata = A.T @ A
        atb = A.T @ b
        x_hat = np.linalg.solve(ata, atb)
        projection = A @ x_hat
        residual = b - projection

        q1 = a1 / np.linalg.norm(a1)
        u2 = a2 - np.dot(q1, a2) * q1
        q2 = u2 / np.linalg.norm(u2)
        Q = np.column_stack((q1, q2))
        R = Q.T @ A
        qtb = Q.T @ b

        return LeastSquaresProjectionSnapshot(
            A=A,
            b=b,
            a1=a1,
            a2=a2,
            x_hat=x_hat,
            projection=projection,
            residual=residual,
            ata=ata,
            atb=atb,
            q1=q1,
            q2=q2,
            Q=Q,
            R=R,
            qtb=qtb,
        )
