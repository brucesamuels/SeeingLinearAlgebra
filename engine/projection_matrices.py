"""Renderer-independent content for CP164: projection matrices."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ProjectionMatricesSnapshot:
    q: np.ndarray
    P: np.ndarray
    v: np.ndarray
    Pv: np.ndarray
    residual: np.ndarray
    repeated_projection: np.ndarray
    orthogonal_direction: np.ndarray
    projected_q: np.ndarray
    projected_orthogonal_direction: np.ndarray
    R: np.ndarray
    Rv: np.ndarray


class ProjectionMatricesLesson:
    """Projection onto the line spanned by q=(1,2)/sqrt(5)."""

    FULL_COLUMN_PROJECTION = r"P=A(A^TA)^{-1}A^T"
    ORTHONORMAL_PROJECTION = r"P=Q(Q^TQ)^{-1}Q^T=QQ^T"
    GENERAL_PROJECTION = r"P=QQ^T"
    GENERAL_ACTION = r"P\mathbf v=QQ^T\mathbf v"
    IDEMPOTENT_RULE = r"P^2=P"
    SYMMETRY_RULE = r"P^T=P"
    ORTHOGONAL_MATRIX_RULE = r"Q^TQ=I"
    CLOSING_IDEA = "Projection collapses toward a subspace; an orthogonal matrix preserves geometry."

    def snapshot(self) -> ProjectionMatricesSnapshot:
        q = np.array([1.0, 2.0]) / np.sqrt(5.0)
        P = np.outer(q, q)

        v = np.array([4.0, 1.0])
        Pv = P @ v
        residual = v - Pv
        repeated_projection = P @ Pv

        orthogonal_direction = np.array([2.0, -1.0]) / np.sqrt(5.0)
        projected_q = P @ q
        projected_orthogonal_direction = P @ orthogonal_direction

        # A 90-degree rotation for the final comparison.
        R = np.array([[0.0, -1.0], [1.0, 0.0]])
        Rv = R @ v

        return ProjectionMatricesSnapshot(
            q=q,
            P=P,
            v=v,
            Pv=Pv,
            residual=residual,
            repeated_projection=repeated_projection,
            orthogonal_direction=orthogonal_direction,
            projected_q=projected_q,
            projected_orthogonal_direction=projected_orthogonal_direction,
            R=R,
            Rv=Rv,
        )
