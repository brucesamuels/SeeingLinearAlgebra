from __future__ import annotations

import inspect

from scenes.chapter_one_opening_presentation import ChapterOneOpeningPresentation


def test_combined_scene_renders_title_before_lessons() -> None:
    source = inspect.getsource(ChapterOneOpeningPresentation.construct)

    assert 'self.next_section("chapter_title")' in source
    assert "render_chapter_title(self, self.CHAPTER_TITLE)" in source


def test_combined_scene_renders_interludes_from_metadata() -> None:
    source = inspect.getsource(ChapterOneOpeningPresentation.construct)

    assert "self.INTERLUDES_BY_AFTER_LESSON.get(lesson.key)" in source
    assert "render_chapter_interlude(self, interlude)" in source
    assert "self.next_section(interlude.key)" in source


def test_combined_scene_reuses_special_vectors_and_living_vector() -> None:
    source = inspect.getsource(ChapterOneOpeningPresentation)

    assert '"special_vectors": SpecialVectorsPresentation' in source
    assert '"infinite_possibilities": InfinitePossibilitiesPresentation' in source
    assert "SpecialVectorsPresentation.construct(self)" not in source
    assert "InfinitePossibilitiesPresentation.construct(self)" not in source


def test_combined_scene_forwards_required_lesson_configuration() -> None:
    source = inspect.getsource(ChapterOneOpeningPresentation)

    assert "SNAPSHOT = SpecialVectorsPresentation.SNAPSHOT" in source
    assert "LESSON_STAGES = ScalarMultiplicationPresentation.LESSON_STAGES" in source
    assert "LINEAR_COMBINATION = InfinitePossibilitiesPresentation.LINEAR_COMBINATION" in source
    assert "STORY = InfinitePossibilitiesPresentation.STORY" in source
    assert "coefficient_pair = staticmethod(" in source


def test_combined_scene_remains_3d_capable() -> None:
    bases = ChapterOneOpeningPresentation.__bases__

    assert bases[0].__name__ == "ThreeVectorAdditionPresentation"
    assert bases[1].__name__ == "WhyVectorsPresentation"
