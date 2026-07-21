"""Renderer-independent opening lesson order for Chapter 1."""

from __future__ import annotations

from engine.chapter_sequence import ChapterLessonReference, ChapterSequence


CHAPTER_ONE_OPENING_SEQUENCE = ChapterSequence(
    key="chapter_1_opening",
    title="Chapter 1: Vectors",
    lessons=(
        ChapterLessonReference(key="why_vectors", title="Why Vectors?"),
        ChapterLessonReference(key="vector_representation", title="What Is a Vector?"),
        ChapterLessonReference(key="free_vector_equality", title="Free Vectors and Equality"),
        ChapterLessonReference(key="placing_vector_at_origin", title="Placing a Vector at the Origin"),
        ChapterLessonReference(key="special_vectors", title="Special Vectors"),
        ChapterLessonReference(key="scalar_multiplication", title="Scalar Multiplication"),
        ChapterLessonReference(key="vector_addition", title="Vector Addition"),
        ChapterLessonReference(key="vector_addition_commutativity", title="Commutativity of Vector Addition"),
        ChapterLessonReference(key="vector_subtraction", title="Vector Subtraction"),
        ChapterLessonReference(key="three_vector_addition", title="Three Vectors in 3-Space"),
        ChapterLessonReference(key="infinite_possibilities", title="Infinite Possibilities"),
    ),
)
