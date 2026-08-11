"""Renderer-independent mathematics for CP146: determinants and Jacobian area scaling."""
from __future__ import annotations


def linear_area_tex() -> str:
    return r"\text{area after }A=|\det(A)|\,\text{area before}"


def jacobian_matrix_tex() -> str:
    return (
        r"J_F(u,v)=\begin{bmatrix}"
        r"\frac{\partial x}{\partial u}&\frac{\partial x}{\partial v}\\"
        r"\frac{\partial y}{\partial u}&\frac{\partial y}{\partial v}"
        r"\end{bmatrix}"
    )


def local_area_tex() -> str:
    return r"dA_{xy}\approx |\det J_F(u,v)|\,dA_{uv}"


def linear_example_tex() -> tuple[str, str, str]:
    return (
        r"F(u,v)=(2u,\,u+3v)",
        r"J_F=\begin{bmatrix}2&0\\1&3\end{bmatrix}",
        r"\det(J_F)=6",
    )


def polar_jacobian_tex() -> tuple[str, str, str]:
    return (
        r"x=r\cos\theta,\qquad y=r\sin\theta",
        r"J=\begin{bmatrix}\cos\theta&-r\sin\theta\\\sin\theta&r\cos\theta\end{bmatrix}",
        r"\det(J)=r",
    )


def polar_area_tex() -> str:
    return r"dA=r\,dr\,d\theta"


def closing_lines() -> tuple[str, str, str]:
    return (
        "For a linear map, one determinant gives the same area scale everywhere.",
        "For a nonlinear map, the Jacobian determinant gives the local area scale.",
        "The determinant is the bridge between algebraic transformations and geometric measure.",
    )
