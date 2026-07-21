from __future__ import annotations

import ast
from pathlib import Path


SCENE_PATH = Path("scenes/chapter_one_opening_presentation.py")
STANDALONE_SCENE_PATH = Path(
    "scenes/scalar_multiplication_presentation.py"
)


def test_scalar_multiplication_follows_standard_position_and_precedes_addition() -> None:
    from engine.chapter_one_opening_sequence import (
        CHAPTER_ONE_OPENING_SEQUENCE,
    )

    lesson_keys = CHAPTER_ONE_OPENING_SEQUENCE.lesson_keys
    standard_position_index = lesson_keys.index("placing_vector_at_origin")
    scalar_multiplication_index = lesson_keys.index("scalar_multiplication")

    special_vectors_index = lesson_keys.index("special_vectors")

    assert lesson_keys[standard_position_index + 1] == "special_vectors"
    assert lesson_keys[special_vectors_index + 1] == "scalar_multiplication"
    assert lesson_keys[scalar_multiplication_index + 1] == "vector_addition"


def test_combined_scene_reuses_the_approved_scalar_multiplication_scene() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    assert "ScalarMultiplicationPresentation" in source
    assert '"scalar_multiplication": ScalarMultiplicationPresentation' in source
    assert '"scalar_multiplication": ScalarMultiplicationPresentation' in source
    assert "ScalarMultiplicationPresentation.construct(self)" not in source
    assert "presentation_class.construct(self)" in source


def test_combined_scene_does_not_copy_scalar_multiplication_implementation() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")
    forbidden_fragments = (
        "SCALAR_MULTIPLICATION_STAGES",
        "scaled_vector(",
        "BASE_VECTOR",
        "target_arrow = Arrow(",
        "target_readout = MathTex(",
        r"(-1)\mathbf{v}=-\mathbf{v}",
    )

    for fragment in forbidden_fragments:
        assert fragment not in source


def test_scalar_multiplication_scene_remains_independently_renderable() -> None:
    source = STANDALONE_SCENE_PATH.read_text(encoding="utf-8")
    module = ast.parse(source)
    class_names = {
        node.name
        for node in module.body
        if isinstance(node, ast.ClassDef)
    }

    assert "ScalarMultiplicationPresentation" in class_names
    assert "class ScalarMultiplicationPresentation(Scene):" in source


def test_combined_scene_preserves_3d_capability() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")
    module = ast.parse(source)
    combined_class = next(
        node
        for node in module.body
        if isinstance(node, ast.ClassDef)
        and node.name == "ChapterOneOpeningPresentation"
    )
    base_names = tuple(
        base.id
        for base in combined_class.bases
        if isinstance(base, ast.Name)
    )

    assert base_names == (
        "ThreeVectorAdditionPresentation",
        "WhyVectorsPresentation",
    )


def test_combined_scene_exposes_scalar_multiplication_stage_configuration() -> None:
    from scenes.chapter_one_opening_presentation import (
        ChapterOneOpeningPresentation,
    )
    from scenes.scalar_multiplication_presentation import (
        ScalarMultiplicationPresentation,
    )

    assert ChapterOneOpeningPresentation.LESSON_STAGES is (
        ScalarMultiplicationPresentation.LESSON_STAGES
    )
