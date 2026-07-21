from __future__ import annotations

import inspect

from scenes.chapter_one_opening_presentation import ChapterOneOpeningPresentation


def test_living_vector_restores_head_on_2d_camera() -> None:
    construct_source = inspect.getsource(ChapterOneOpeningPresentation.construct)
    reset_source = inspect.getsource(
        ChapterOneOpeningPresentation._restore_2d_camera
    )

    assert 'if lesson.key == "infinite_possibilities":' in construct_source
    assert "self._restore_2d_camera()" in construct_source
    assert "self.stop_ambient_camera_rotation()" in reset_source
    assert "phi=0.0" in reset_source
    assert "theta=-PI / 2" in reset_source
    assert "gamma=0.0" in reset_source
    assert "zoom=1.0" in reset_source
