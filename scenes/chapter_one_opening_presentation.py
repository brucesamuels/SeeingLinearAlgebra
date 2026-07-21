"""Combined Manim presentation for the complete Chapter 1 experience."""

from __future__ import annotations

from types import MappingProxyType

from manim import FadeOut, PI

from engine.chapter_learning_experience import (
    CHAPTER_ONE_INTERLUDES_BY_AFTER_LESSON,
    CHAPTER_ONE_TITLE,
)
from engine.chapter_one_opening_sequence import CHAPTER_ONE_OPENING_SEQUENCE
from scenes.chapter_orchestration import (
    render_chapter_interlude,
    render_chapter_title,
)
from scenes.free_vector_equality_presentation import FreeVectorEqualityPresentation
from scenes.infinite_possibilities_presentation import InfinitePossibilitiesPresentation
from scenes.placing_vector_at_origin_presentation import PlacingVectorAtOriginPresentation
from scenes.scalar_multiplication_presentation import ScalarMultiplicationPresentation
from scenes.special_vectors_presentation import SpecialVectorsPresentation
from scenes.three_vector_addition_presentation import ThreeVectorAdditionPresentation
from scenes.vector_addition_commutativity_presentation import VectorAdditionCommutativityPresentation
from scenes.vector_addition_presentation import VectorAdditionPresentation
from scenes.vector_representation_presentation import VectorRepresentationPresentation
from scenes.vector_subtraction_presentation import VectorSubtractionPresentation
from scenes.why_vectors_presentation import WhyVectorsPresentation


class ChapterOneOpeningPresentation(
    ThreeVectorAdditionPresentation,
    WhyVectorsPresentation,
):
    """Render Chapter 1 by delegating to approved standalone lessons."""

    CHAPTER_SEQUENCE = CHAPTER_ONE_OPENING_SEQUENCE
    CHAPTER_TITLE = CHAPTER_ONE_TITLE
    INTERLUDES_BY_AFTER_LESSON = CHAPTER_ONE_INTERLUDES_BY_AFTER_LESSON

    # Configuration required by delegated approved lessons.
    LESSON_STAGES = ScalarMultiplicationPresentation.LESSON_STAGES
    SNAPSHOT = SpecialVectorsPresentation.SNAPSHOT
    U = InfinitePossibilitiesPresentation.U
    V = InfinitePossibilitiesPresentation.V
    LINEAR_COMBINATION = InfinitePossibilitiesPresentation.LINEAR_COMBINATION
    STORY = InfinitePossibilitiesPresentation.STORY
    coefficient_pair = staticmethod(
        InfinitePossibilitiesPresentation.coefficient_pair
    )

    PRESENTATIONS_BY_KEY = MappingProxyType(
        {
            "why_vectors": WhyVectorsPresentation,
            "vector_representation": VectorRepresentationPresentation,
            "free_vector_equality": FreeVectorEqualityPresentation,
            "placing_vector_at_origin": PlacingVectorAtOriginPresentation,
            "special_vectors": SpecialVectorsPresentation,
            "scalar_multiplication": ScalarMultiplicationPresentation,
            "vector_addition": VectorAdditionPresentation,
            "vector_addition_commutativity": VectorAdditionCommutativityPresentation,
            "vector_subtraction": VectorSubtractionPresentation,
            "three_vector_addition": ThreeVectorAdditionPresentation,
            "infinite_possibilities": InfinitePossibilitiesPresentation,
        }
    )

    def construct(self) -> None:
        self.next_section("chapter_title")
        render_chapter_title(self, self.CHAPTER_TITLE)

        for lesson_index, lesson in enumerate(self.CHAPTER_SEQUENCE):
            if lesson_index:
                self._transition_between_lessons()

            if lesson.key == "infinite_possibilities":
                self._restore_2d_camera()

            self.next_section(lesson.key)
            presentation_class = self.PRESENTATIONS_BY_KEY[lesson.key]
            presentation_class.construct(self)

            interlude = self.INTERLUDES_BY_AFTER_LESSON.get(lesson.key)
            if interlude is not None:
                self._transition_between_lessons()
                self.next_section(interlude.key)
                render_chapter_interlude(self, interlude)

    def _restore_2d_camera(self) -> None:
        """Return the shared 3D camera to a head-on 2D view."""

        self.stop_ambient_camera_rotation()
        self.set_camera_orientation(
            phi=0.0,
            theta=-PI / 2,
            gamma=0.0,
            zoom=1.0,
        )

    def _transition_between_lessons(self) -> None:
        current_mobjects = tuple(self.mobjects)
        if current_mobjects:
            self.play(
                *[FadeOut(mobject) for mobject in current_mobjects],
                run_time=self.THEME.timing.transition,
            )
        self.clear()
