from __future__ import annotations

import ast
from pathlib import Path


SCENE_PATH = Path("scenes/chapter_one_opening_presentation.py")
STANDALONE_SCENE_PATH = Path(
    "scenes/three_vector_addition_presentation.py"
)


def test_three_vector_addition_remains_the_closing_capstone() -> None:
    from engine.chapter_one_opening_sequence import (
        CHAPTER_ONE_OPENING_SEQUENCE,
    )

    lesson_keys = CHAPTER_ONE_OPENING_SEQUENCE.lesson_keys
    subtraction_index = lesson_keys.index("vector_subtraction")

    assert lesson_keys[subtraction_index + 1] == "three_vector_addition"
    assert lesson_keys[-1] == "three_vector_addition"
    assert CHAPTER_ONE_OPENING_SEQUENCE.lesson_titles[-1] == (
        "Three Vectors in 3-Space"
    )


def test_combined_scene_reuses_approved_three_vector_scene() -> None:
    source = SCENE_PATH.read_text(encoding="utf-8")

    assert (
        "from scenes.three_vector_addition_presentation import (\n"
        "    ThreeVectorAdditionPresentation,\n"
        ")"
    ) in source
    assert (
        '"three_vector_addition": ThreeVectorAdditionPresentation'
    ) in source
    assert "ThreeVectorAdditionPresentation.construct(self)" not in source
    assert "presentation_class.construct(self)" in source


def test_combined_scene_is_3d_capable_without_copying_3d_implementation() -> None:
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

    forbidden_fragments = (
        "ThreeVectorAddition(",
        "Arrow3D(",
        "Line3D(",
        "ThreeDAxes(",
        "parallelepiped_edges =",
        r"\mathbf{u}+\mathbf{v}+\mathbf{w}=(4,4,5)",
    )

    for fragment in forbidden_fragments:
        assert fragment not in source


def test_three_vector_scene_remains_independently_renderable() -> None:
    source = STANDALONE_SCENE_PATH.read_text(encoding="utf-8")
    module = ast.parse(source)
    class_names = {
        node.name
        for node in module.body
        if isinstance(node, ast.ClassDef)
    }

    assert "ThreeVectorAdditionPresentation" in class_names
    assert "class ThreeVectorAdditionPresentation(ThreeDScene):" in source


def test_registry_keys_match_complete_renderer_independent_sequence() -> None:
    from engine.chapter_one_opening_sequence import (
        CHAPTER_ONE_OPENING_SEQUENCE,
    )

    source = SCENE_PATH.read_text(encoding="utf-8")
    expected_bindings = {
        "why_vectors": "WhyVectorsPresentation",
        "vector_representation": "VectorRepresentationPresentation",
        "free_vector_equality": "FreeVectorEqualityPresentation",
        "placing_vector_at_origin": "PlacingVectorAtOriginPresentation",
        "scalar_multiplication": "ScalarMultiplicationPresentation",
        "vector_addition": "VectorAdditionPresentation",
        "vector_addition_commutativity": (
            "VectorAdditionCommutativityPresentation"
        ),
        "vector_subtraction": "VectorSubtractionPresentation",
        "three_vector_addition": "ThreeVectorAdditionPresentation",
    }

    assert tuple(expected_bindings) == (
        CHAPTER_ONE_OPENING_SEQUENCE.lesson_keys
    )

    for key, presentation_name in expected_bindings.items():
        binding = f'"{key}": {presentation_name}'
        if key == "vector_addition_commutativity":
            assert source.count('"vector_addition_commutativity": (') == 1
            assert source.count(presentation_name) == 2
        else:
            assert source.count(binding) == 1
