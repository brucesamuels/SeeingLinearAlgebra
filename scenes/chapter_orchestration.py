"""Reusable Manim helpers for chapter titles and reflection pauses."""

from __future__ import annotations

from manim import DOWN, FadeIn, FadeOut, Text, UP, VGroup, Write

from engine.chapter_learning_experience import (
    ChapterInterlude,
    ChapterTitleMetadata,
)
from engine.manim_instructional_widgets import ThemedText


def render_chapter_title(scene, metadata: ChapterTitleMetadata) -> None:
    """Render a restrained reusable chapter opening."""

    series = Text(metadata.series_title, font_size=30)
    chapter = Text(metadata.chapter_label, font_size=34)
    title = Text(metadata.chapter_title, font_size=64)
    subtitle = Text(metadata.subtitle, font_size=28)

    group = VGroup(series, chapter, title, subtitle).arrange(
        DOWN,
        buff=0.28,
    )
    group.move_to([0.0, 0.15, 0.0])

    scene.play(Write(series))
    scene.play(FadeIn(chapter), run_time=0.7)
    scene.play(Write(title), run_time=1.2)
    scene.play(FadeIn(subtitle), run_time=0.8)
    scene.wait(2.0)
    scene.play(FadeOut(group), run_time=1.0)
    scene.clear()


def render_chapter_interlude(scene, interlude: ChapterInterlude) -> None:
    """Render one consistent reflection or prediction pause."""

    heading = ThemedText.lesson_title(
        interlude.heading,
        theme=scene.THEME,
    )
    heading.to_edge(UP, buff=0.55)

    prompt = VGroup(
        *[
            ThemedText.body(line, theme=scene.THEME)
            for line in interlude.prompt_lines
        ]
    ).arrange(DOWN, buff=0.22)
    prompt.move_to([0.0, -0.05, 0.0])

    scene.play(Write(heading))
    scene.play(FadeIn(prompt))
    scene.wait(interlude.think_time)
    scene.play(FadeOut(heading), FadeOut(prompt))
    scene.clear()
