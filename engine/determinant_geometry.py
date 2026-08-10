"""Renderer-independent mathematics for CP145: determinant as signed area/volume scaling."""
from __future__ import annotations


def theorem_tex() -> str:
    return r"|\det(A)|=\text{area/volume scale factor}"


def signed_scale_tex() -> str:
    return r"\det(A)=\text{signed volume scale factor}"


def area_example_matrix() -> tuple[tuple[int, int], tuple[int, int]]:
    return ((2, 1), (0, 1))


def area_example_det() -> int:
    return 2


def orientation_matrices() -> tuple[tuple[tuple[int, int], tuple[int, int]], ...]:
    return (
        ((1, 1), (0, 1)),
        ((-1, 0), (0, 1)),
    )


def orientation_determinants() -> tuple[int, int]:
    return (1, -1)


def singular_matrix() -> tuple[tuple[int, int], tuple[int, int]]:
    return ((1, 2), (1, 2))


def singular_det() -> int:
    return 0


def volume_scale() -> int:
    return 3


def product_scaling_tex() -> tuple[str, str, str]:
    return (
        r"B:\ 1\mapsto |\det(B)|",
        r"A:\ |\det(B)|\mapsto |\det(A)|\,|\det(B)|",
        r"AB:\ 1\mapsto |\det(AB)|=|\det(A)\det(B)|",
    )


def closing_lines() -> tuple[str, str, str]:
    return (
        "Magnitude tells how much area or volume is scaled.",
        "Sign tells whether orientation is preserved or reversed.",
        "A zero determinant means dimension collapses and volume vanishes.",
    )
