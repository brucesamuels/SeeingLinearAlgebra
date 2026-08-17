"""Renderer-independent content for the Chapter 6 orthogonality finale."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ChapterSixFinaleSnapshot:
    u: np.ndarray
    v: np.ndarray
    q: np.ndarray
    sample: np.ndarray
    projection: np.ndarray
    residual: np.ndarray
    projection_matrix: np.ndarray
    ls_A: np.ndarray
    ls_b: np.ndarray
    ls_xhat: np.ndarray
    ls_projection: np.ndarray
    ls_residual: np.ndarray


class ChapterSixFinaleLesson:
    """Numerical anchors and summary identities for the Chapter 6 finale."""

    DOT_RULE = r"\mathbf u^T\mathbf v=0\iff \mathbf u\perp\mathbf v"
    DECOMPOSITION_RULE = r"\mathbf v=P\mathbf v+\mathbf r,\qquad \mathbf r\perp W"
    ORTHONORMAL_COORDINATES = r"\mathbf c=Q^T\mathbf v,\qquad P\mathbf v=Q\mathbf c=QQ^T\mathbf v"
    QR_RULE = r"A=QR,\qquad Q^TQ=I"
    LEAST_SQUARES_RULE = r"A^T(\mathbf b-A\hat{\mathbf x})=0"
    NORMAL_EQUATION = r"A^TA\hat{\mathbf x}=A^T\mathbf b"
    QR_LEAST_SQUARES = r"R\hat{\mathbf x}=Q^T\mathbf b"
    PROJECTION_SIGNATURE = r"P^T=P,\qquad P^2=P"
    ORTHOGONAL_SIGNATURE = r"U^TU=I,\qquad U^{-1}=U^T"
    CLOSING_IDEA = "Orthogonality turns geometry into computation."

    def snapshot(self) -> ChapterSixFinaleSnapshot:
        u = np.array([1.0, 2.0])
        v = np.array([2.0, -1.0])

        q = np.array([1.0, 2.0]) / np.sqrt(5.0)
        sample = np.array([4.0, 1.0])
        projection_matrix = np.outer(q, q)
        projection = projection_matrix @ sample
        residual = sample - projection

        ls_A = np.array(
            [
                [1.0, 0.0],
                [0.0, 1.0],
                [1.0, 1.0],
            ]
        )
        ls_b = np.array([2.0, 2.0, 1.0])
        ls_xhat = np.array([1.0, 1.0])
        ls_projection = ls_A @ ls_xhat
        ls_residual = ls_b - ls_projection

        return ChapterSixFinaleSnapshot(
            u=u,
            v=v,
            q=q,
            sample=sample,
            projection=projection,
            residual=residual,
            projection_matrix=projection_matrix,
            ls_A=ls_A,
            ls_b=ls_b,
            ls_xhat=ls_xhat,
            ls_projection=ls_projection,
            ls_residual=ls_residual,
        )
