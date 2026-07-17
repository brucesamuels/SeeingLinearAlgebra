from __future__ import annotations

import inspect

from manim import Scene

from engine.vector_representation_lesson import (
    VECTOR_REPRESENTATION_LESSON_SEQUENCE,
)
from scenes.vector_representation_presentation import (
    VectorRepresentationPresentation,
)


def test_presentation_scene_is_scene_with_explicit_construct() -> None:
    assert issubclass(VectorRepresentationPresentation, Scene)
    assert "construct" in VectorRepresentationPresentation.__dict__
    assert callable(VectorRepresentationPresentation.__dict__["construct"])


def test_presentation_scene_declares_canonical_lesson_sequence() -> None:
    assert (
        VectorRepresentationPresentation.LESSON_SEQUENCE
        is VECTOR_REPRESENTATION_LESSON_SEQUENCE
    )


def test_scene_uses_existing_vector_pipeline() -> None:
    source = inspect.getsource(VectorRepresentationPresentation.construct)

    assert "VectorRepresentation(" in source
    assert "VectorRepresentationDisplayProjector(" in source
    assert "ManimVectorRepresentationDisplay(" in source


def test_scene_keeps_timing_at_scene_level() -> None:
    source = inspect.getsource(VectorRepresentationPresentation.construct)

    assert "self.play(" in source
    assert "self.wait(" in source


def test_scene_contains_all_five_pedagogical_phases() -> None:
    source = inspect.getsource(VectorRepresentationPresentation.construct)

    for phase in ("ORIENT", "PREDICT", "OBSERVE", "STABILIZE", "REFLECT"):
        assert f"# {phase}" in source


def test_scene_does_not_duplicate_vector_arithmetic() -> None:
    source = inspect.getsource(VectorRepresentationPresentation.construct)

    assert "np.array" not in source
    assert "np.linalg" not in source
    assert "sqrt(" not in source
