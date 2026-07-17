from __future__ import annotations

import inspect

from manim import Scene

from scenes.why_vectors_presentation import WhyVectorsPresentation


def test_presentation_is_scene_with_explicit_construct() -> None:
    assert issubclass(WhyVectorsPresentation, Scene)
    assert "construct" in WhyVectorsPresentation.__dict__


def test_title_and_guiding_question_are_fixed_before_perspectives() -> None:
    source = inspect.getsource(WhyVectorsPresentation.construct)

    assert "self.play(Write(title))" in source
    assert "self.play(FadeIn(guiding_question))" in source
    assert "for perspective in WHY_VECTORS_SEQUENCE.perspectives" in source


def test_presentation_contains_convergence_synthesis() -> None:
    source = (
        inspect.getsource(WhyVectorsPresentation.construct)
        + inspect.getsource(WhyVectorsPresentation._synthesis_group)
    )

    for label in (
        "Physics",
        "Computer Science",
        "Engineering",
        "Mathematics",
        "VECTOR",
    ):
        assert label in source


def test_presentation_ends_with_arrow_at_origin() -> None:
    source = inspect.getsource(WhyVectorsPresentation.construct)

    assert "geometric_arrow = Arrow(" in source
    assert "start=ORIGIN" in source
    assert 'MathTex("(0,0)")' in source
