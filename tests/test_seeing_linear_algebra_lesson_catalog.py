from __future__ import annotations

from engine.full_rank_3d_lesson_sequence import FULL_RANK_3D_LESSON_SEQUENCE
from engine.rank_collapse_lesson_sequence import RANK_COLLAPSE_LESSON_SEQUENCE
from engine.seeing_linear_algebra_lesson_catalog import (
    SEEING_LINEAR_ALGEBRA_LESSON_CATALOG,
)


def test_canonical_catalog_contains_two_proven_lessons() -> None:
    assert SEEING_LINEAR_ALGEBRA_LESSON_CATALOG.keys == (
        "full_rank_3d_linear_combination",
        "rank_collapse",
    )
    assert SEEING_LINEAR_ALGEBRA_LESSON_CATALOG.titles == (
        "Full-Rank 3D Linear Combination",
        "Rank Collapse",
    )


def test_canonical_catalog_reuses_existing_sequence_objects() -> None:
    assert (
        SEEING_LINEAR_ALGEBRA_LESSON_CATALOG
        .lesson("full_rank_3d_linear_combination")
        .sequence
        is FULL_RANK_3D_LESSON_SEQUENCE
    )
    assert (
        SEEING_LINEAR_ALGEBRA_LESSON_CATALOG
        .lesson("rank_collapse")
        .sequence
        is RANK_COLLAPSE_LESSON_SEQUENCE
    )


def test_catalog_does_not_define_chapter_order_or_execution() -> None:
    catalog = SEEING_LINEAR_ALGEBRA_LESSON_CATALOG

    assert not hasattr(catalog, "run")
    assert not hasattr(catalog, "render")
    assert not hasattr(catalog, "chapter")
