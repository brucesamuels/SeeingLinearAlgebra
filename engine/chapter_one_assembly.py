"""Assembly metadata for the complete revised Chapter 1 presentation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ChapterAssembly:
    key: str
    chapter_title: str
    sequence_module: str
    presentation_module: str
    presentation_file: str
    presentation_class: str
    lesson_keys: Tuple[str, ...]


CHAPTER_ONE_ASSEMBLY = ChapterAssembly(
    key="chapter_1_vectors",
    chapter_title="Chapter 1: Vectors",
    sequence_module="engine.chapter_one_opening_sequence",
    presentation_module="scenes.chapter_one_opening_presentation",
    presentation_file="scenes/chapter_one_opening_presentation.py",
    presentation_class="ChapterOneOpeningPresentation",
    lesson_keys=(
        "why_vectors",
        "vector_representation",
        "free_vector_equality",
        "placing_vector_at_origin",
        "special_vectors",
        "scalar_multiplication",
        "vector_addition",
        "vector_addition_commutativity",
        "vector_subtraction",
        "three_vector_addition",
        "infinite_possibilities",
    ),
)
