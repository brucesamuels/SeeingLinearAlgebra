"""Renderer-independent content for CP163: rotations and reflections."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class RotationsReflectionsSnapshot:
    theta: float
    R: np.ndarray
    e1: np.ndarray
    e2: np.ndarray
    Re1: np.ndarray
    Re2: np.ndarray
    v: np.ndarray
    Rv: np.ndarray
    triangle: np.ndarray
    rotated_triangle: np.ndarray
    H: np.ndarray
    reflected_v: np.ndarray
    reflected_triangle: np.ndarray


class RotationsReflectionsLesson:
    """Exact 60-degree rotation and x-axis reflection examples."""

    ROTATION_MATRIX = (
        r"R_\theta=\begin{bmatrix}"
        r"\cos\theta&-\sin\theta\\"
        r"\sin\theta&\cos\theta"
        r"\end{bmatrix}"
    )
    ROTATION_INVERSE = r"R_\theta^{-1}=R_{-\theta}=R_\theta^T"
    REFLECTION_MATRIX = r"H=\begin{bmatrix}1&0\\0&-1\end{bmatrix}"
    REFLECTION_INVERSE = r"H^{-1}=H=H^T"
    ORTHOGONAL_CRITERION = r"\text{orthogonal}\iff\text{columns are orthonormal}"
    CLOSING_IDEA = "Rotations preserve orientation; reflections reverse it."

    def snapshot(self) -> RotationsReflectionsSnapshot:
        theta = np.pi / 3.0
        c = np.cos(theta)
        s = np.sin(theta)
        R = np.array([[c, -s], [s, c]])

        e1 = np.array([1.0, 0.0])
        e2 = np.array([0.0, 1.0])
        Re1 = R @ e1
        Re2 = R @ e2

        v = np.array([2.0, 1.0])
        Rv = R @ v

        triangle = np.array(
            [
                [0.0, 0.0],
                [2.0, 0.0],
                [0.5, 1.0],
            ]
        )
        rotated_triangle = triangle @ R.T

        H = np.array([[1.0, 0.0], [0.0, -1.0]])
        reflected_v = H @ v
        reflected_triangle = triangle @ H.T

        return RotationsReflectionsSnapshot(
            theta=theta,
            R=R,
            e1=e1,
            e2=e2,
            Re1=Re1,
            Re2=Re2,
            v=v,
            Rv=Rv,
            triangle=triangle,
            rotated_triangle=rotated_triangle,
            H=H,
            reflected_v=reflected_v,
            reflected_triangle=reflected_triangle,
        )
