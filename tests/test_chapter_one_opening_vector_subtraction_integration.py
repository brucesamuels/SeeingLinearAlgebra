from __future__ import annotations

import ast
from pathlib import Path


SCENE_PATH = Path("scenes/chapter_one_opening_presentation.py")
STANDALONE_SCENE_PATH = Path("scenes/vector_subtraction_presentation.py")


def test_subtraction_follows_commutativity_and_precedes_3d_capstone() -> None:
    from engine.chapter_one_opening_sequence import (
        CHAPTER_ONE_OPENING_SEQUENCE,
    )

    lesson_keys = CHAPTER_ONE_OPENING_SEQUENCE.lesson_keys
    commutativity_index = lesson_keys.index(
        "vector_addition_commutativity"
    )
    subtraction_index = lesson_keys.index("vector_subtraction")

    assert lesson_keys[commutativity_index + 1] == "vector_subtraction"
    assert lesson_keys[subtraction_index + 1] == "three_vector_addition"


def test_combined_scene_reuses_the_approved_subtraction_scene() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    assert (
        "from scenes.vector_subtraction_presentation import "
        "VectorSubtractionPresentation"
    ) in source
    assert '"vector_subtraction": VectorSubtractionPresentation' in source
    assert "VectorSubtractionPresentation.construct(self)" not in source
    assert "presentation_class.construct(self)" in source


def test_combined_scene_does_not_copy_subtraction_implementation() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")
    forbidden_fragments = (
        "snapshot = VectorSubtraction(",
        "negative_v_target = Arrow(",
        "translated_negative_target = Arrow(",
        "Rotate(v_arrow, angle=PI, about_point=origin)",
        r"\mathbf{u}+(-\mathbf{v})",
        "To subtract a vector, add its opposite",
    )

    for fragment in forbidden_fragments:
        assert fragment not in source


def test_subtraction_scene_remains_independently_renderable() -> None:
    source = STANDALONE_SCENE_PATH.read_text(encoding="utf-8")
    module = ast.parse(source)
    class_names = {
        node.name for node in module.body if isinstance(node, ast.ClassDef)
    }

    assert "VectorSubtractionPresentation" in class_names
    assert "class VectorSubtractionPresentation(Scene):" in source
