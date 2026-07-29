"""Renderer-independent chapter plan for Vector Spaces and Subspaces."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChapterSegment:
    key: str
    title: str
    scene_file: str
    scene_class: str
    kind: str = "lesson"


CHAPTER_TITLE = "Vector Spaces: Structure, Dimension, and the Spaces Inside a Matrix"
CHAPTER_QUESTION = "What makes a collection of vectors into a space, and how can a matrix reveal its hidden structure?"
CHAPTER_REFLECTION = (
    "A matrix organizes directions into what survives, what disappears, "
    "what can be produced, and what remains unreachable."
)

SEGMENTS: tuple[ChapterSegment, ...] = (
    ChapterSegment("opening", CHAPTER_TITLE, "scenes/vector_spaces_chapter_cards.py", "VectorSpacesChapterOpening", "card"),
    ChapterSegment("section_1", "From Dependence to Subspaces", "scenes/vector_spaces_chapter_cards.py", "VectorSpacesSectionOne", "card"),
    ChapterSegment("rank_collapse", "When Space Collapses", "scenes/rank_collapse_3d_presentation.py", "RankCollapse3DPresentation"),
    ChapterSegment("subspace_test", "The Subspace Test", "scenes/subspace_test_presentation.py", "SubspaceTestPresentation"),
    ChapterSegment("section_2", "Basis and Dimension", "scenes/vector_spaces_chapter_cards.py", "VectorSpacesSectionTwo", "card"),
    ChapterSegment("basis_dimension", "Basis and Dimension", "scenes/basis_dimension_presentation.py", "BasisDimensionPresentation"),
    ChapterSegment("section_3", "The Spaces Inside a Matrix", "scenes/vector_spaces_chapter_cards.py", "VectorSpacesSectionThree", "card"),
    ChapterSegment("column_space", "Column Space", "scenes/column_space_presentation.py", "ColumnSpacePresentation"),
    ChapterSegment("null_space", "Null Space", "scenes/null_space_presentation.py", "NullSpacePresentation"),
    ChapterSegment("row_space", "Row Space", "scenes/row_space_presentation.py", "RowSpacePresentation"),
    ChapterSegment("pivot_columns", "Pivot Columns", "scenes/pivot_columns_presentation.py", "PivotColumnsPresentation"),
    ChapterSegment("section_4", "How the Dimensions Fit Together", "scenes/vector_spaces_chapter_cards.py", "VectorSpacesSectionFour", "card"),
    ChapterSegment("rank_nullity", "Rank and Nullity", "scenes/rank_nullity_presentation.py", "RankNullityPresentation"),
    ChapterSegment("fundamental_subspaces", "The Four Fundamental Subspaces", "scenes/fundamental_subspaces_presentation.py", "FundamentalSubspacesPresentation"),
    ChapterSegment("closing", "Chapter Reflection", "scenes/vector_spaces_chapter_cards.py", "VectorSpacesChapterClosing", "card"),
)


def lesson_segments() -> tuple[ChapterSegment, ...]:
    return tuple(segment for segment in SEGMENTS if segment.kind == "lesson")


def card_segments() -> tuple[ChapterSegment, ...]:
    return tuple(segment for segment in SEGMENTS if segment.kind == "card")


def validate_unique_keys() -> bool:
    keys = [segment.key for segment in SEGMENTS]
    return len(keys) == len(set(keys))
