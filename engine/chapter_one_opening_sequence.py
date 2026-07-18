"""Renderer-independent opening lesson order for Chapter 1."""

from __future__ import annotations

from engine.chapter_sequence import ChapterLessonReference, ChapterSequence


CHAPTER_ONE_OPENING_SEQUENCE = ChapterSequence(
    key="chapter_1_opening",
    title="Chapter 1: Vectors",
    lessons=(
        ChapterLessonReference(
            key="why_vectors",
            title="Why Vectors?",
        ),
        ChapterLessonReference(
            key="vector_representation",
            title="What Is a Vector?",
        ),
        ChapterLessonReference(
            key="free_vector_equality",
            title="Free Vectors and Equality",
        ),
        ChapterLessonReference(
            key="placing_vector_at_origin",
            title="Placing a Vector at the Origin",
        ),
    ),
)
