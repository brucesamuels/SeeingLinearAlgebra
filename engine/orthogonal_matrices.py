"""Renderer-independent content for CP162: orthogonal matrices preserve geometry."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class OrthogonalMatricesSnapshot:
    q1: np.ndarray
    q2: np.ndarray
    Q: np.ndarray
    u: np.ndarray
    v: np.ndarray
    Qu: np.ndarray
    Qv: np.ndarray
    rotation: np.ndarray
    reflection: np.ndarray
    unit_square: np.ndarray
    rotated_square: np.ndarray
    reflected_square: np.ndarray


class OrthogonalMatricesLesson:
    """A small 2D rotation example and a reflection comparison."""

    ORTHOGONAL_TEST = r"Q^TQ=I"
    INVERSE_RULE = r"Q^{-1}=Q^T"
    LENGTH_RULE = r"\|Q\mathbf v\|=\|\mathbf v\|"
    DOT_RULE = r"(Q\mathbf u)^T(Q\mathbf v)=\mathbf u^T\mathbf v"
    CLOSING_IDEA = "Orthogonal matrices preserve lengths and angles."

    def snapshot(self) -> OrthogonalMatricesSnapshot:
        root2 = np.sqrt(2.0)
        q1 = np.array([1.0 / root2, 1.0 / root2])
        q2 = np.array([-1.0 / root2, 1.0 / root2])
        Q = np.column_stack((q1, q2))

        u = np.array([2.0, 1.0])
        v = np.array([1.0, 2.0])
        Qu = Q @ u
        Qv = Q @ v

        rotation = Q
        reflection = np.array([[1.0, 0.0], [0.0, -1.0]])
        unit_square = np.array(
            [
                [0.0, 0.0],
                [1.0, 0.0],
                [1.0, 1.0],
                [0.0, 1.0],
            ]
        )
        rotated_square = unit_square @ rotation.T
        reflected_square = unit_square @ reflection.T

        return OrthogonalMatricesSnapshot(
            q1=q1,
            q2=q2,
            Q=Q,
            u=u,
            v=v,
            Qu=Qu,
            Qv=Qv,
            rotation=rotation,
            reflection=reflection,
            unit_square=unit_square,
            rotated_square=rotated_square,
            reflected_square=reflected_square,
        )
