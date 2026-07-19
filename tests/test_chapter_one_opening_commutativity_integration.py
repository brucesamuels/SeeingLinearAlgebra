from __future__ import annotations

import ast
from pathlib import Path


SCENE_PATH = Path("scenes/chapter_one_opening_presentation.py")
STANDALONE_SCENE_PATH = Path(
    "scenes/vector_addition_commutativity_presentation.py"
)


def test_commutativity_follows_vector_addition_and_precedes_subtraction() -> None:
    from engine.chapter_one_opening_sequence import (
        CHAPTER_ONE_OPENING_SEQUENCE,
    )

    lesson_keys = CHAPTER_ONE_OPENING_SEQUENCE.lesson_keys
    vector_addition_index = lesson_keys.index("vector_addition")
    commutativity_index = lesson_keys.index(
        "vector_addition_commutativity"
    )

    assert lesson_keys[vector_addition_index + 1] == (
        "vector_addition_commutativity"
    )
    assert lesson_keys[commutativity_index + 1] == "vector_subtraction"


def test_combined_scene_reuses_the_approved_commutativity_scene() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    assert (
        "from scenes.vector_addition_commutativity_presentation import (\n"
        "    VectorAdditionCommutativityPresentation,\n"
        ")"
    ) in source
    assert '"vector_addition_commutativity": (' in source
    assert "VectorAdditionCommutativityPresentation" in source
    assert (
        "VectorAdditionCommutativityPresentation.construct(self)"
        not in source
    )
    assert "presentation_class.construct(self)" in source


def test_combined_scene_does_not_copy_commutativity_implementation() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")
    forbidden_fragments = (
        "uv_snapshot = VectorAddition(",
        "vu_snapshot = VectorAddition(",
        "v_after_u_target = Arrow(",
        "u_after_v_target = Arrow(",
        r"\mathbf{u}+\mathbf{v}=\mathbf{v}+\mathbf{u}",
        "Changing the order changes the path, but not the sum",
    )

    for fragment in forbidden_fragments:
        assert fragment not in source


def test_commutativity_scene_remains_independently_renderable() -> None:
    source = STANDALONE_SCENE_PATH.read_text(encoding="utf-8")
    module = ast.parse(source)
    class_names = {
        node.name for node in module.body if isinstance(node, ast.ClassDef)
    }

    assert "VectorAdditionCommutativityPresentation" in class_names
    assert (
        "class VectorAdditionCommutativityPresentation(Scene):" in source
    )
