from __future__ import annotations

from engine.chapter_1_outline import CHAPTER_1_OUTLINE
from engine.seeing_linear_algebra_lesson_catalog import (
    SEEING_LINEAR_ALGEBRA_LESSON_CATALOG,
)


def test_chapter_1_follows_source_lesson_progression() -> None:
    assert CHAPTER_1_OUTLINE.section_keys == (
        "vector_perspectives",
        "scalar_multiplication",
        "vector_addition",
        "magnitude",
        "unit_vectors_and_basis",
        "linear_combinations_and_span",
    )


def test_chapter_1_references_only_cataloged_lessons() -> None:
    assert (
        CHAPTER_1_OUTLINE.validate_lesson_references(
            SEEING_LINEAR_ALGEBRA_LESSON_CATALOG
        )
        == ()
    )


def test_existing_lessons_support_final_span_section() -> None:
    section = CHAPTER_1_OUTLINE.section("linear_combinations_and_span")

    assert section.lesson_keys == (
        "full_rank_3d_linear_combination",
        "rank_collapse",
    )


def test_outline_exposes_content_gaps_without_fabricating_lessons() -> None:
    sections_without_lessons = tuple(
        section.key
        for section in CHAPTER_1_OUTLINE
        if not section.lesson_keys
    )

    assert sections_without_lessons == (
        "vector_perspectives",
        "scalar_multiplication",
        "vector_addition",
        "magnitude",
        "unit_vectors_and_basis",
    )
