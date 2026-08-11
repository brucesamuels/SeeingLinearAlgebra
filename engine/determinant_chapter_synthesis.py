"""Renderer-independent content for CP147: determinant chapter synthesis."""
from __future__ import annotations


def computation_methods() -> tuple[str, str, str]:
    return (
        r"\text{Elimination: track row-operation effects}",
        r"\text{Cofactors: reduce dimension recursively}",
        r"\text{Big Formula: sum over permutations}",
    )


def invertibility_chain() -> str:
    return (
        r"\det(A)\ne0"
        r"\Longleftrightarrow \operatorname{rank}(A)=n"
        r"\Longleftrightarrow \mathcal N(A)=\{\mathbf 0\}"
        r"\Longleftrightarrow A^{-1}\text{ exists}"
    )


def singular_chain() -> str:
    return (
        r"\det(A)=0"
        r"\Longleftrightarrow \operatorname{rank}(A)<n"
        r"\Longleftrightarrow \mathcal N(A)\ne\{\mathbf 0\}"
        r"\Longleftrightarrow A\text{ is singular}"
    )


def geometric_lines() -> tuple[str, str, str]:
    return (
        r"|\det(A)|=\text{area/volume scale factor}",
        r"\operatorname{sgn}(\det A)=\text{orientation}",
        r"\det(A)=0\Longrightarrow\text{collapse to lower dimension}",
    )


def algebraic_rules() -> tuple[str, str, str]:
    return (
        r"\det(AB)=\det(A)\det(B)",
        r"\det(A^T)=\det(A)",
        r"\det(A^{-1})=\frac{1}{\det(A)}",
    )


def system_formulas() -> tuple[str, str]:
    return (
        r"x_k=\frac{\det(A_k)}{\det(A)}",
        r"A^{-1}=\frac{1}{\det(A)}\operatorname{adj}(A)",
    )


def jacobian_bridge() -> tuple[str, str]:
    return (
        r"\text{linear map: }|\det(A)|=\text{global area scale}",
        r"\text{nonlinear map: }|\det J|=\text{local area scale}",
    )


def closing_words() -> tuple[str, str, str]:
    return (
        "Computation",
        "Structure",
        "Geometry",
    )
