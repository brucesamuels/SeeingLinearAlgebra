from __future__ import annotations

import inspect

from manim import Scene

from engine.manim_lesson_layout import LessonLayout
from engine.manim_lesson_theme import LessonTheme
from engine.vector_to_origin_lesson import VECTOR_TO_ORIGIN_LESSON_SEQUENCE
from scenes.placing_vector_at_origin_presentation import (
    INITIAL_POINT,
    TERMINAL_POINT,
    PlacingVectorAtOriginPresentation,
    update_vector_to_origin_display,
)


def test_scene_declares_canonical_sequence_theme_and_layout() -> None:
    assert issubclass(PlacingVectorAtOriginPresentation, Scene)
    assert (
        PlacingVectorAtOriginPresentation.LESSON_SEQUENCE
        is VECTOR_TO_ORIGIN_LESSON_SEQUENCE
    )
    assert isinstance(PlacingVectorAtOriginPresentation.THEME, LessonTheme)
    assert isinstance(PlacingVectorAtOriginPresentation.LAYOUT, LessonLayout)


def test_scene_uses_requested_initial_and_terminal_points() -> None:
    assert INITIAL_POINT == (2.0, 1.0)
    assert TERMINAL_POINT == (5.0, 3.0)


def test_scene_projects_vector_before_revealing_coordinate_system() -> None:
    source = inspect.getsource(PlacingVectorAtOriginPresentation.construct)

    arrow_index = source.index("self.play(Create(display.arrow))")
    plane_index = source.index("self.play(FadeIn(plane))")
    assert arrow_index < plane_index


def test_scene_reveals_initial_and_terminal_coordinate_labels() -> None:
    source = inspect.getsource(PlacingVectorAtOriginPresentation.construct)

    assert "FadeIn(display.tail_label)" in source
    assert "FadeIn(display.tip_label)" in source
    assert "FadeIn(display.tail_dot)" in source
    assert "FadeIn(display.tip_dot)" in source


def test_scene_uses_one_renderer_independent_snapshot_per_update() -> None:
    helper_source = inspect.getsource(update_vector_to_origin_display)

    assert helper_source.count("translation_path.snapshot(progress)") == 1
    assert "display.update_from_snapshot(snapshot)" in helper_source
    assert "return snapshot" in helper_source


def test_scene_synchronizes_subtraction_readout_with_translation() -> None:
    source = inspect.getsource(PlacingVectorAtOriginPresentation.construct)

    assert "FadeIn(display.formula)" in source
    assert "ValueTracker(0.0)" in source
    assert "display.arrow.add_updater" in source
    assert "progress.animate.set_value(1.0)" in source
    assert "update_vector_to_origin_display(" in source


def test_scene_pins_exact_final_snapshot_and_names_standard_position() -> None:
    source = inspect.getsource(PlacingVectorAtOriginPresentation.construct)

    assert "translation_path,\n            1.0," in source
    assert "assert final_snapshot.is_at_origin" in source
    assert "Same vector, now in standard position" in source
    assert "terminal minus initial" in source


def test_scene_uses_shared_visual_identity_roles_and_timing() -> None:
    source = inspect.getsource(PlacingVectorAtOriginPresentation.construct)

    assert "ThemedText.lesson_title" in source
    assert "ThemedText.guiding_question" in source
    assert "ThemedText.body" in source
    assert "ThemedText.takeaway" in source
    assert "self.THEME.timing.normal" in source
    assert "self.THEME.timing.read" in source
    assert "self.THEME.timing.reflection" in source
