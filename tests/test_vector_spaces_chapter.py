from engine.vector_spaces_chapter import (
    CHAPTER_QUESTION,
    CHAPTER_REFLECTION,
    CHAPTER_TITLE,
    SEGMENTS,
    card_segments,
    lesson_segments,
    validate_unique_keys,
)


def test_chapter_has_unique_segment_keys() -> None:
    assert validate_unique_keys()


def test_chapter_has_opening_closing_and_four_section_cards() -> None:
    cards = card_segments()
    assert cards[0].key == "opening"
    assert cards[-1].key == "closing"
    assert [segment.key for segment in cards[1:-1]] == [
        "section_1",
        "section_2",
        "section_3",
        "section_4",
    ]


def test_lesson_order_builds_to_fundamental_subspaces() -> None:
    assert [segment.key for segment in lesson_segments()] == [
        "rank_collapse",
        "subspace_test",
        "basis_dimension",
        "column_space",
        "null_space",
        "row_space",
        "pivot_columns",
        "rank_nullity",
        "fundamental_subspaces",
    ]


def test_chapter_language_frames_the_conceptual_arc() -> None:
    assert "Structure, Dimension" in CHAPTER_TITLE
    assert "What makes a collection of vectors into a space" in CHAPTER_QUESTION
    assert "what survives" in CHAPTER_REFLECTION
    assert "what remains unreachable" in CHAPTER_REFLECTION


def test_all_segments_name_scene_files_and_classes() -> None:
    assert len(SEGMENTS) == 15
    assert all(segment.scene_file.startswith("scenes/") for segment in SEGMENTS)
    assert all(segment.scene_class for segment in SEGMENTS)
