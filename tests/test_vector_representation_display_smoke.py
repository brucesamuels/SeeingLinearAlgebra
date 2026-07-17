from __future__ import annotations

from manim import Scene

from scenes.vector_representation_display_smoke import (
    VectorRepresentationDisplaySmoke,
)


def test_smoke_scene_is_a_scene_with_explicit_construct() -> None:
    assert issubclass(VectorRepresentationDisplaySmoke, Scene)
    assert "construct" in VectorRepresentationDisplaySmoke.__dict__
    assert callable(VectorRepresentationDisplaySmoke.__dict__["construct"])
