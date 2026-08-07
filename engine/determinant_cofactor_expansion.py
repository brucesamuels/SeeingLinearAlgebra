"""Renderer-independent mathematics for CP137: cofactor expansion from CP136."""
from __future__ import annotations


def six_term_formula_lines() -> tuple[str, str]:
    """Return the CP136 six-term 3x3 determinant formula as two display lines."""
    return (
        r"\det(A)=a_{11}a_{22}a_{33}+a_{12}a_{23}a_{31}+a_{13}a_{21}a_{32}",
        r"-a_{11}a_{23}a_{32}-a_{12}a_{21}a_{33}-a_{13}a_{22}a_{31}",
    )


def grouped_by_first_row_tex() -> str:
    """Group the six CP136 terms according to a11, a12, and a13."""
    return (
        r"\det(A)="
        r"a_{11}(a_{22}a_{33}-a_{23}a_{32})"
        r"-a_{12}(a_{21}a_{33}-a_{23}a_{31})"
        r"+a_{13}(a_{21}a_{32}-a_{22}a_{31})"
    )


def row_one_minor_determinants_tex() -> tuple[str, str, str]:
    """Return the three 2x2 determinant factors for expansion along row 1."""
    return (
        r"\begin{vmatrix}a_{22}&a_{23}\\a_{32}&a_{33}\end{vmatrix}",
        r"\begin{vmatrix}a_{21}&a_{23}\\a_{31}&a_{33}\end{vmatrix}",
        r"\begin{vmatrix}a_{21}&a_{22}\\a_{31}&a_{32}\end{vmatrix}",
    )


def row_one_expansion_tex() -> str:
    """Return the first-row Laplace/cofactor expansion in minor-determinant form."""
    m11, m12, m13 = row_one_minor_determinants_tex()
    return rf"\det(A)=a_{{11}}{m11}-a_{{12}}{m12}+a_{{13}}{m13}"


def checkerboard_signs() -> tuple[tuple[str, str, str], ...]:
    return (
        ("+", "-", "+"),
        ("-", "+", "-"),
        ("+", "-", "+"),
    )


def minor_definition_tex() -> str:
    return r"\text{Minor }M_{ij}:\ \text{delete row }i\text{ and column }j\text{, then take the determinant}"


def sign_origin_tex() -> str:
    return r"\text{Negative signs come from }(-1)^{i+j}\text{, inherited from permutation signs}"


def cofactor_definition_tex() -> str:
    return r"C_{ij}=(-1)^{i+j}M_{ij}"


def first_row_cofactor_tex() -> str:
    return r"\det(A)=a_{11}C_{11}+a_{12}C_{12}+a_{13}C_{13}"


def general_row_expansion_tex() -> str:
    return r"\det(A)=\sum_{j=1}^{n}a_{ij}C_{ij}"


def general_column_expansion_tex() -> str:
    return r"\det(A)=\sum_{i=1}^{n}a_{ij}C_{ij}"


def bridge_lines() -> tuple[str, str, str]:
    return (
        "Begin with the six-term determinant formula.",
        "Now collect the terms that contain the same first-row entry.",
        "Each pair becomes a 2x2 determinant.",
    )
