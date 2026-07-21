"""Renderer-independent chapter title and reflection metadata."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True, slots=True)
class ChapterTitleMetadata:
    series_title: str
    chapter_label: str
    chapter_title: str
    subtitle: str


@dataclass(frozen=True, slots=True)
class ChapterInterlude:
    key: str
    heading: str
    prompt_lines: tuple[str, ...]
    think_time: float
    kind: str

    def __post_init__(self) -> None:
        if self.kind not in {"reflection", "prediction"}:
            raise ValueError("kind must be reflection or prediction")
        if self.think_time <= 0:
            raise ValueError("think_time must be positive")
        if not self.prompt_lines:
            raise ValueError("at least one prompt line is required")


CHAPTER_ONE_TITLE = ChapterTitleMetadata(
    series_title="SEEING LINEAR ALGEBRA",
    chapter_label="Chapter 1",
    chapter_title="VECTORS",
    subtitle="Direction • Magnitude • Combination",
)


CHAPTER_ONE_INTERLUDES_BY_AFTER_LESSON: Mapping[str, ChapterInterlude] = (
    MappingProxyType(
        {
            "vector_representation": ChapterInterlude(
                key="reflect_equal_vectors",
                heading="Pause and Reflect",
                prompt_lines=(
                    "If two arrows have the same length and direction,",
                    "must they begin at the same point",
                    "to represent the same vector?",
                ),
                think_time=6.0,
                kind="reflection",
            ),
            "special_vectors": ChapterInterlude(
                key="reflect_normalization",
                heading="Pause and Reflect",
                prompt_lines=(
                    "What changed when we replaced v",
                    "by its unit vector?",
                    "What stayed the same?",
                ),
                think_time=6.0,
                kind="reflection",
            ),
            "vector_subtraction": ChapterInterlude(
                key="predict_combined_operations",
                heading="Pause and Predict",
                prompt_lines=(
                    "If subtraction is addition of the opposite,",
                    "what other vector operations might combine",
                    "ideas we already know?",
                ),
                think_time=7.0,
                kind="prediction",
            ),
        }
    )
)
