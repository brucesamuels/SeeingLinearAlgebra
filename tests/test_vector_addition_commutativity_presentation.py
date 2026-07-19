from __future__ import annotations

import inspect

from manim import Scene

from engine.manim_lesson_layout import LessonLayout
from engine.manim_lesson_theme import LessonTheme
from engine.vector_addition_commutativity_lesson import (
    VECTOR_ADDITION_COMMUTATIVITY_LESSON_SEQUENCE,
)
from scenes.vector_addition_commutativity_presentation import (
    FIRST_VECTOR,
    SECOND_VECTOR,
    VectorAdditionCommutativityPresentation,
)


def test_scene_declares_sequence_theme_and_layout() -> None:
    assert issubclass(VectorAdditionCommutativityPresentation, Scene)
    assert (
        VectorAdditionCommutativityPresentation.LESSON_SEQUENCE
        is VECTOR_ADDITION_COMMUTATIVITY_LESSON_SEQUENCE
    )
    assert isinstance(
        VectorAdditionCommutativityPresentation.THEME,
        LessonTheme,
    )
    assert isinstance(
        VectorAdditionCommutativityPresentation.LAYOUT,
        LessonLayout,
    )


def test_scene_reuses_the_approved_vectors() -> None:
    assert FIRST_VECTOR == (3.0, 1.0)
    assert SECOND_VECTOR == (1.0, 2.0)


def test_scene_evaluates_vector_addition_in_both_orders() -> None:
    source = inspect.getsource(
        VectorAdditionCommutativityPresentation.construct
    )

    assert "uv_snapshot = VectorAddition(" in source
    assert "FIRST_VECTOR,\n            SECOND_VECTOR," in source
    assert "vu_snapshot = VectorAddition(" in source
    assert "SECOND_VECTOR,\n            FIRST_VECTOR," in source
    assert "assert uv_snapshot.result == vu_snapshot.result" in source


def test_scene_constructs_both_head_to_tail_routes() -> None:
    source = inspect.getsource(
        VectorAdditionCommutativityPresentation.construct
    )

    assert "v_after_u_target = Arrow(" in source
    assert "u_after_v_target = Arrow(" in source
    assert "Transform(moving_v, v_after_u_target)" in source
    assert "Transform(moving_u, u_after_v_target)" in source


def test_scene_constructs_u_plus_v_before_v_plus_u() -> None:
    source = inspect.getsource(
        VectorAdditionCommutativityPresentation.construct
    )

    uv_index = source.index("Transform(moving_v, v_after_u_target)")
    vu_index = source.index("Transform(moving_u, u_after_v_target)")
    assert uv_index < vu_index


def test_scene_shows_same_endpoint_and_coordinate_sum() -> None:
    source = inspect.getsource(
        VectorAdditionCommutativityPresentation.construct
    )

    assert r"\mathbf{u}+\mathbf{v}=(4,3)" in source
    assert r"\mathbf{v}+\mathbf{u}=(4,3)" in source
    assert "Create(resultant_arrow)" in source
    assert "FadeIn(endpoint)" in source


def test_scene_states_commutative_property() -> None:
    source = inspect.getsource(
        VectorAdditionCommutativityPresentation.construct
    )

    assert r"\mathbf{u}+\mathbf{v}=\mathbf{v}+\mathbf{u}" in source
    assert (
        "Changing the order changes the path, but not the sum"
        in source
    )
    assert "Both routes reach the same opposite corner." in source


def test_scene_uses_shared_visual_identity_and_pacing() -> None:
    source = inspect.getsource(
        VectorAdditionCommutativityPresentation.construct
    )

    assert "ThemedText.lesson_title" in source
    assert "ThemedText.guiding_question" in source
    assert "ThemedText.body" in source
    assert "ThemedText.takeaway" in source
    assert "self.THEME.timing.normal" in source
    assert "self.THEME.timing.read" in source
    assert "self.THEME.timing.reflection" in source
