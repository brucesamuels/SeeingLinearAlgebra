"""Canonical catalog of currently proven Seeing Linear Algebra lessons."""

from __future__ import annotations

from engine.full_rank_3d_lesson_sequence import FULL_RANK_3D_LESSON_SEQUENCE
from engine.lesson_catalog import LessonCatalog, LessonDescriptor
from engine.rank_collapse_lesson_sequence import RANK_COLLAPSE_LESSON_SEQUENCE


SEEING_LINEAR_ALGEBRA_LESSON_CATALOG = LessonCatalog(
    (
        LessonDescriptor(
            key="full_rank_3d_linear_combination",
            title="Full-Rank 3D Linear Combination",
            sequence=FULL_RANK_3D_LESSON_SEQUENCE,
        ),
        LessonDescriptor(
            key="rank_collapse",
            title="Rank Collapse",
            sequence=RANK_COLLAPSE_LESSON_SEQUENCE,
        ),
    )
)
