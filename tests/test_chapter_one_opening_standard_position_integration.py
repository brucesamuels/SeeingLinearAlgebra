from __future__ import annotations

import ast
from pathlib import Path


SEQUENCE_PATH = Path("engine/chapter_one_opening_sequence.py")
SCENE_PATH = Path("scenes/chapter_one_opening_presentation.py")
STANDALONE_SCENE_PATH = Path(
    "scenes/placing_vector_at_origin_presentation.py"
)


def test_standard_position_lesson_follows_free_vector_equality() -> None:
    # This is an adjacency invariant, not an end-of-sequence invariant.
    from engine.chapter_one_opening_sequence import (
        CHAPTER_ONE_OPENING_SEQUENCE,
    )

    lesson_keys = CHAPTER_ONE_OPENING_SEQUENCE.lesson_keys
    free_vector_index = lesson_keys.index("free_vector_equality")

    assert lesson_keys[free_vector_index + 1] == "placing_vector_at_origin"


def test_combined_scene_reuses_the_approved_standard_position_scene() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    assert "PlacingVectorAtOriginPresentation" in source
    assert (
        '"placing_vector_at_origin": PlacingVectorAtOriginPresentation'
    ) in source
    assert (
        '"placing_vector_at_origin": '
        "PlacingVectorAtOriginPresentation"
    ) in source
    assert "PlacingVectorAtOriginPresentation.construct(self)" not in source
    assert "presentation_class.construct(self)" in source


def test_combined_scene_does_not_copy_standard_position_implementation() -> None:
    combined_source = SCENE_PATH.read_text(encoding="utf-8")

    forbidden_fragments = (
        "VectorToOriginTranslation(",
        "ManimVectorToOriginDisplay(",
        "ValueTracker(",
        "NumberPlane(",
        "INITIAL_POINT =",
        "TERMINAL_POINT =",
    )

    for fragment in forbidden_fragments:
        assert fragment not in combined_source


def test_standard_position_scene_remains_independently_renderable() -> None:
    source = STANDALONE_SCENE_PATH.read_text(encoding="utf-8")
    module = ast.parse(source)

    class_names = {
        node.name
        for node in module.body
        if isinstance(node, ast.ClassDef)
    }

    assert "PlacingVectorAtOriginPresentation" in class_names
    assert "class PlacingVectorAtOriginPresentation(Scene):" in source
