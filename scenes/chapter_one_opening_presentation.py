"""Combined Manim presentation for the approved Chapter 1 opening lessons."""

from __future__ import annotations

from types import MappingProxyType

from manim import FadeOut

from engine.chapter_one_opening_sequence import CHAPTER_ONE_OPENING_SEQUENCE
from scenes.free_vector_equality_presentation import FreeVectorEqualityPresentation
from scenes.placing_vector_at_origin_presentation import (
    PlacingVectorAtOriginPresentation,
)
from scenes.vector_representation_presentation import VectorRepresentationPresentation
from scenes.why_vectors_presentation import WhyVectorsPresentation


class ChapterOneOpeningPresentation(WhyVectorsPresentation):
    """Render the Chapter 1 opening by delegating to proven lesson scenes.

    The scene intentionally inherits from ``WhyVectorsPresentation`` so its
    private renderer-side helpers remain available when that approved lesson's
    ``construct`` method is executed on this shared Manim scene. The remaining
    approved lessons currently require no additional helper methods.
    """

    CHAPTER_SEQUENCE = CHAPTER_ONE_OPENING_SEQUENCE
    PRESENTATIONS_BY_KEY = MappingProxyType(
        {
            "why_vectors": WhyVectorsPresentation,
            "vector_representation": VectorRepresentationPresentation,
            "free_vector_equality": FreeVectorEqualityPresentation,
            "placing_vector_at_origin": PlacingVectorAtOriginPresentation,
        }
    )

    def construct(self) -> None:
        for lesson_index, lesson in enumerate(self.CHAPTER_SEQUENCE):
            if lesson_index:
                self._transition_between_lessons()

            self.next_section(lesson.key)
            presentation_class = self.PRESENTATIONS_BY_KEY[lesson.key]
            presentation_class.construct(self)

    def _transition_between_lessons(self) -> None:
        """Fade the completed lesson away before reusing the shared canvas."""
        current_mobjects = tuple(self.mobjects)
        if current_mobjects:
            self.play(
                *[FadeOut(mobject) for mobject in current_mobjects],
                run_time=self.THEME.timing.transition,
            )

        self.clear()
