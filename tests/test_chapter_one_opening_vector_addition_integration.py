from __future__ import annotations

import ast
from pathlib import Path


SCENE_PATH = Path("scenes/chapter_one_opening_presentation.py")
STANDALONE_SCENE_PATH = Path("scenes/vector_addition_presentation.py")


def test_vector_addition_follows_standard_position() -> None:
    from engine.chapter_one_opening_sequence import (
        CHAPTER_ONE_OPENING_SEQUENCE,
    )

    lesson_keys = CHAPTER_ONE_OPENING_SEQUENCE.lesson_keys
    standard_position_index = lesson_keys.index("placing_vector_at_origin")

    assert lesson_keys[standard_position_index + 1] == "vector_addition"


def test_combined_scene_reuses_the_approved_vector_addition_scene() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    assert (
        "from scenes.vector_addition_presentation import "
        "VectorAdditionPresentation"
    ) in source
    assert '"vector_addition": VectorAdditionPresentation' in source
    assert "VectorAdditionPresentation.construct(self)" not in source
    assert "presentation_class.construct(self)" in source


def test_combined_scene_does_not_copy_vector_addition_implementation() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    forbidden_fragments = (
        "VectorAddition(",
        "NumberPlane(",
        "translated_second_arrow",
        "resultant_arrow",
        r"\mathbf{u}+\mathbf{v}=(4,3)",
        "parallelogram",
    )

    for fragment in forbidden_fragments:
        assert fragment not in source


def test_vector_addition_scene_remains_independently_renderable() -> None:
    source = STANDALONE_SCENE_PATH.read_text(encoding="utf-8")
    module = ast.parse(source)

    class_names = {
        node.name
        for node in module.body
        if isinstance(node, ast.ClassDef)
    }

    assert "VectorAdditionPresentation" in class_names
    assert "class VectorAdditionPresentation(Scene):" in source


def test_registry_keys_match_the_first_five_sequence_entries() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")
    expected_bindings = (
        '"why_vectors": WhyVectorsPresentation',
        '"vector_representation": VectorRepresentationPresentation',
        '"free_vector_equality": FreeVectorEqualityPresentation',
        '"placing_vector_at_origin": PlacingVectorAtOriginPresentation',
        '"vector_addition": VectorAdditionPresentation',
    )

    for binding in expected_bindings:
        assert source.count(binding) == 1
