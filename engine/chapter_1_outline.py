"""Initial Chapter 1 outline derived from the vectors lesson progression."""

from __future__ import annotations

from engine.chapter_outline import ChapterOutline, ChapterSection


CHAPTER_1_OUTLINE = ChapterOutline(
    key="vectors_span_coordinates",
    title="Vectors, Span, and Coordinates",
    sections=(
        ChapterSection(
            key="vector_perspectives",
            title="What Is a Vector?",
            purpose=(
                "Connect geometric arrows, coordinate lists, and the broader "
                "mathematical idea of a vector."
            ),
        ),
        ChapterSection(
            key="scalar_multiplication",
            title="Scalar Multiplication",
            purpose=(
                "Show stretching, shrinking, reversal, and collapse to the "
                "zero vector."
            ),
        ),
        ChapterSection(
            key="vector_addition",
            title="Vector Addition",
            purpose=(
                "Develop componentwise addition and the tip-to-tail geometric "
                "construction."
            ),
        ),
        ChapterSection(
            key="magnitude",
            title="Magnitude",
            purpose=(
                "Interpret Euclidean norm as vector length and connect scaling "
                "to changes in magnitude."
            ),
        ),
        ChapterSection(
            key="unit_vectors_and_basis",
            title="Unit Vectors and the Standard Basis",
            purpose=(
                "Introduce unitizing and interpret coordinates as scaled "
                "standard-basis steps."
            ),
        ),
        ChapterSection(
            key="linear_combinations_and_span",
            title="Linear Combinations and Span",
            purpose=(
                "Show how coefficients generate reachable vectors and how "
                "dependence changes the dimension of the span."
            ),
            lesson_keys=(
                "full_rank_3d_linear_combination",
                "rank_collapse",
            ),
        ),
    ),
)
