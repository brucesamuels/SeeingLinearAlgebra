from __future__ import annotations

from engine.chapter_learning_experience import (
    CHAPTER_ONE_INTERLUDES_BY_AFTER_LESSON,
    CHAPTER_ONE_TITLE,
    ChapterInterlude,
)


def test_chapter_one_title_metadata() -> None:
    assert CHAPTER_ONE_TITLE.series_title == "SEEING LINEAR ALGEBRA"
    assert CHAPTER_ONE_TITLE.chapter_label == "Chapter 1"
    assert CHAPTER_ONE_TITLE.chapter_title == "VECTORS"
    assert CHAPTER_ONE_TITLE.subtitle == "Direction • Magnitude • Combination"


def test_chapter_one_interludes_follow_approved_lessons() -> None:
    assert tuple(CHAPTER_ONE_INTERLUDES_BY_AFTER_LESSON) == (
        "vector_representation",
        "special_vectors",
        "vector_subtraction",
    )

    assert CHAPTER_ONE_INTERLUDES_BY_AFTER_LESSON[
        "vector_representation"
    ].heading == "Pause and Reflect"
    assert CHAPTER_ONE_INTERLUDES_BY_AFTER_LESSON[
        "special_vectors"
    ].kind == "reflection"
    assert CHAPTER_ONE_INTERLUDES_BY_AFTER_LESSON[
        "vector_subtraction"
    ].kind == "prediction"


def test_interlude_rejects_invalid_metadata() -> None:
    try:
        ChapterInterlude(
            key="bad",
            heading="Bad",
            prompt_lines=(),
            think_time=0.0,
            kind="other",
        )
    except ValueError:
        pass
    else:
        raise AssertionError("invalid interlude metadata should fail")
