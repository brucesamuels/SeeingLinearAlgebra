from __future__ import annotations

import inspect

from manim import Scene

from engine.free_vector_equality_lesson import (
    FREE_VECTOR_EQUALITY_LESSON_SEQUENCE,
)
from scenes.free_vector_equality_presentation import (
    FreeVectorEqualityPresentation,
)


def test_presentation_scene_declares_canonical_sequence() -> None:
    assert issubclass(FreeVectorEqualityPresentation, Scene)
    assert (
        FreeVectorEqualityPresentation.LESSON_SEQUENCE
        is FREE_VECTOR_EQUALITY_LESSON_SEQUENCE
    )


def test_scene_animates_translated_copies() -> None:
    source = inspect.getsource(FreeVectorEqualityPresentation.construct)

    assert "ReplacementTransform" in source
    assert "for target in arrows[1:]" in source


def test_scene_states_equality_invariants() -> None:
    source = inspect.getsource(FreeVectorEqualityPresentation.construct)

    for phrase in (
        "same coordinates",
        "same direction",
        "same magnitude",
        "different location",
    ):
        assert phrase in source


def test_scene_uses_renderer_independent_equality_model() -> None:
    source = inspect.getsource(FreeVectorEqualityPresentation.construct)

    assert "FreeVectorEquality(" in source
    assert "translated_to(" not in source
