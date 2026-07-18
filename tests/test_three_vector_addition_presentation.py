from __future__ import annotations

import inspect

from manim import ThreeDScene

from engine.manim_lesson_layout import LessonLayout
from engine.manim_lesson_theme import LessonTheme
from engine.three_vector_addition_lesson import (
    THREE_VECTOR_ADDITION_LESSON_SEQUENCE,
)
from scenes.three_vector_addition_presentation import (
    FIRST_VECTOR_3D,
    SECOND_VECTOR_3D,
    THIRD_VECTOR_3D,
    ThreeVectorAdditionPresentation,
)


def test_scene_declares_sequence_theme_and_layout() -> None:
    assert issubclass(ThreeVectorAdditionPresentation, ThreeDScene)
    assert (
        ThreeVectorAdditionPresentation.LESSON_SEQUENCE
        is THREE_VECTOR_ADDITION_LESSON_SEQUENCE
    )
    assert isinstance(ThreeVectorAdditionPresentation.THEME, LessonTheme)
    assert isinstance(ThreeVectorAdditionPresentation.LAYOUT, LessonLayout)


def test_scene_uses_the_requested_three_vectors() -> None:
    assert FIRST_VECTOR_3D == (3.0, 0.0, 1.0)
    assert SECOND_VECTOR_3D == (0.0, 3.0, 1.0)
    assert THIRD_VECTOR_3D == (1.0, 1.0, 3.0)


def test_scene_reuses_renderer_independent_three_vector_model() -> None:
    source = inspect.getsource(ThreeVectorAdditionPresentation.construct)

    assert 'ThreeVectorAddition(' in source
    assert ').snapshot()' in source
    assert 'assert snapshot.coefficients == (1.0, 1.0, 1.0)' in source
    assert 'assert snapshot.result == (4.0, 4.0, 5.0)' in source
    assert 'assert snapshot.is_successive_path' in source


def test_scene_shows_three_vectors_then_translates_two_of_them() -> None:
    source = inspect.getsource(ThreeVectorAdditionPresentation.construct)

    assert 'Create(first_arrow)' in source
    assert 'Create(second_arrow)' in source
    assert 'Create(third_arrow)' in source
    assert 'ReplacementTransform(second_arrow, translated_second_arrow)' in source
    assert 'ReplacementTransform(third_arrow, translated_third_arrow)' in source


def test_scene_computes_three_vector_coordinate_sum() -> None:
    source = inspect.getsource(ThreeVectorAdditionPresentation.construct)

    assert r'\mathbf{u}+\mathbf{v}+\mathbf{w}=(3,0,1)+(0,3,1)+(1,1,3)' in source
    assert r'\mathbf{u}+\mathbf{v}+\mathbf{w}=(4,4,5)' in source


def test_scene_reveals_parallelepiped_edges_after_the_path() -> None:
    source = inspect.getsource(ThreeVectorAdditionPresentation.construct)

    assert 'parallelepiped_edges = VGroup(' in source
    assert 'Line3D(' in source
    resultant_index = source.index('Create(resultant_arrow)')
    parallelepiped_index = source.index('Create(parallelepiped_edges)')
    assert resultant_index < parallelepiped_index


def test_scene_hides_fixed_orientation_labels_until_reveal() -> None:
    helper_source = inspect.getsource(
        ThreeVectorAdditionPresentation._register_fixed_orientation_hidden
    )
    source = inspect.getsource(ThreeVectorAdditionPresentation.construct)

    assert 'mobject.set_opacity(0.0)' in helper_source
    assert 'first_label.animate.set_opacity(1.0)' in source
    assert 'second_label.animate.set_opacity(1.0)' in source
    assert 'third_label.animate.set_opacity(1.0)' in source
    assert 'resultant_label.animate.set_opacity(1.0)' in source


def test_scene_uses_wider_camera_angle_and_rotation() -> None:
    source = inspect.getsource(ThreeVectorAdditionPresentation.construct)

    assert 'self.set_camera_orientation(phi=74 * DEGREES, theta=-58 * DEGREES)' in source
    assert 'self.begin_ambient_camera_rotation(rate=0.18)' in source
    assert 'self.wait(1.8)' in source


def test_scene_closing_frame_keeps_parallelepiped_and_diagonal_visible() -> None:
    source = inspect.getsource(ThreeVectorAdditionPresentation.construct)

    assert 'The sum is the body diagonal of the parallelepiped' in source
    assert 'FadeOut(parallelepiped_edges)' not in source
    assert 'FadeOut(exact_sum)' not in source
    assert 'FadeOut(parallelepiped_caption)' in source
