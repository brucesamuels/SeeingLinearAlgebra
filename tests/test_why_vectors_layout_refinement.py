from __future__ import annotations

import inspect

from engine.manim_lesson_layout import LessonLayout
from scenes.why_vectors_presentation import WhyVectorsPresentation


def test_scene_uses_shared_lesson_layout() -> None:
    assert isinstance(WhyVectorsPresentation.LAYOUT, LessonLayout)


def test_scene_uses_layout_for_title_question_content_and_footer() -> None:
    construct_source = inspect.getsource(
        WhyVectorsPresentation.construct
    )
    parts_source = inspect.getsource(
        WhyVectorsPresentation._perspective_parts
    )

    assert "self.LAYOUT.place_title(title)" in construct_source
    assert "self.LAYOUT.place_question(guiding_question)" in construct_source
    assert "self.LAYOUT.place_footer(bridge_statement)" in construct_source
    assert "self.LAYOUT.place_content(content)" in parts_source


def test_content_is_left_aligned() -> None:
    source = inspect.getsource(
        WhyVectorsPresentation._perspective_parts
    )

    assert "aligned_edge=[-1.0, 0.0, 0.0]" in source
