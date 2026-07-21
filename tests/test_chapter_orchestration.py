from __future__ import annotations

import inspect

from scenes import chapter_orchestration


def test_title_sequence_uses_reusable_metadata() -> None:
    source = inspect.getsource(chapter_orchestration.render_chapter_title)

    assert "metadata.series_title" in source
    assert "metadata.chapter_title" in source
    assert "metadata.subtitle" in source
    assert "scene.wait(2.0)" in source


def test_interlude_uses_configured_think_time() -> None:
    source = inspect.getsource(chapter_orchestration.render_chapter_interlude)

    assert "interlude.heading" in source
    assert "interlude.prompt_lines" in source
    assert "scene.wait(interlude.think_time)" in source
