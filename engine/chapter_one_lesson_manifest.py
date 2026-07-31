"""Manifest and discovery rules for the complete Chapter 1 assembly."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class ChapterOneLessonSpec:
    key: str
    title: str
    filename_candidates: Tuple[str, ...]
    filename_tokens: Tuple[str, ...]


CHAPTER_ONE_LESSONS: Tuple[ChapterOneLessonSpec, ...] = (
    ChapterOneLessonSpec(
        "why_vectors",
        "Why Vectors?",
        ("why_vectors_presentation.py",),
        ("why", "vectors"),
    ),
    ChapterOneLessonSpec(
        "vector_representation",
        "What Is a Vector?",
        ("vector_representation_presentation.py", "what_is_a_vector_presentation.py"),
        ("vector", "representation"),
    ),
    ChapterOneLessonSpec(
        "free_vector_equality",
        "Free Vectors and Equality",
        ("free_vector_equality_presentation.py", "free_vectors_equality_presentation.py"),
        ("free", "vector", "equality"),
    ),
    ChapterOneLessonSpec(
        "placing_vector_at_origin",
        "Placing a Vector at the Origin",
        ("placing_vector_at_origin_presentation.py", "place_vector_at_origin_presentation.py"),
        ("vector", "origin"),
    ),
    ChapterOneLessonSpec(
        "special_vectors",
        "Special Vectors",
        ("special_vectors_presentation.py",),
        ("special", "vectors"),
    ),
    ChapterOneLessonSpec(
        "scalar_multiplication",
        "Scalar Multiplication",
        ("scalar_multiplication_presentation.py",),
        ("scalar", "multiplication"),
    ),
    ChapterOneLessonSpec(
        "unit_vector",
        "Unit Vectors",
        (
            "unit_vector_presentation.py",
            "unit_vectors_presentation.py",
            "unit_vector_lesson.py",
            "unit_vector_lesson_presentation.py",
            "unit_vector_magnitude_presentation.py",
        ),
        ("unit", "vector"),
    ),
    ChapterOneLessonSpec(
        "vector_addition",
        "Vector Addition",
        ("vector_addition_presentation.py",),
        ("vector", "addition"),
    ),
    ChapterOneLessonSpec(
        "vector_addition_commutativity",
        "Commutativity of Vector Addition",
        ("vector_addition_commutativity_presentation.py", "commutativity_of_vector_addition_presentation.py"),
        ("vector", "addition", "commut"),
    ),
    ChapterOneLessonSpec(
        "vector_subtraction",
        "Vector Subtraction",
        ("vector_subtraction_presentation.py",),
        ("vector", "subtraction"),
    ),
    ChapterOneLessonSpec(
        "three_vector_addition_3d",
        "Three-Vector Addition in 3D",
        (
            "three_vector_addition_3d_presentation.py",
            "three_vector_addition_presentation.py",
            "vector_addition_3d_presentation.py",
        ),
        ("vector", "addition", "3d"),
    ),
    ChapterOneLessonSpec(
        "infinite_possibilities",
        "Infinite Possibilities",
        ("infinite_possibilities_presentation.py",),
        ("infinite", "possibilities"),
    ),
    ChapterOneLessonSpec(
        "inner_product_dot_product",
        "Inner Products and the Dot Product",
        ("inner_product_dot_product_presentation.py",),
        ("inner", "product", "dot"),
    ),
    ChapterOneLessonSpec(
        "cross_product",
        "The Cross Product",
        ("cross_product_presentation.py",),
        ("cross", "product"),
    ),
    ChapterOneLessonSpec(
        "cross_product_computation",
        "Computing the Cross Product",
        ("cross_product_computation_presentation.py",),
        ("cross", "product", "computation"),
    ),
)


def _normalized_words(value: str) -> set[str]:
    """Return meaningful lowercase words for tolerant scene matching.

    Simple trailing-s plurals are normalized so lesson titles such as
    "Unit Vectors" match manifest tokens such as "unit vector".
    """
    raw_words = set(re.findall(r"[a-z0-9]+", value.lower()))
    stop_words = {
        "a", "an", "and", "at", "do", "does", "from", "in", "is",
        "of", "the", "to", "what", "why",
    }
    words = raw_words - stop_words
    normalized = set(words)
    for word in words:
        if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
            normalized.add(word[:-1])
    return normalized


def _scene_metadata(candidate: Path) -> tuple[set[str], set[str], str]:
    """Read class names, title strings, and normalized source for one scene."""
    source = candidate.read_text(encoding="utf-8")
    tree = ast.parse(source)
    class_names: set[str] = set()
    title_words: set[str] = set()

    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        class_names.add(node.name.lower())
        for statement in node.body:
            if not isinstance(statement, (ast.Assign, ast.AnnAssign)):
                continue
            targets = statement.targets if isinstance(statement, ast.Assign) else [statement.target]
            if not any(isinstance(target, ast.Name) and target.id == "TITLE" for target in targets):
                continue
            value = statement.value
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                title_words.update(_normalized_words(value.value))

    return class_names, title_words, source.lower()


def locate_scene_file(scenes_dir: Path, spec: ChapterOneLessonSpec) -> Path:
    """Locate a lesson by exact name, filename tokens, then semantic source metadata."""
    for filename in spec.filename_candidates:
        candidate = scenes_dir / filename
        if candidate.exists():
            return candidate

    scene_files = [
        candidate
        for candidate in scenes_dir.glob("*.py")
        if candidate.name != "__init__.py"
    ]

    filename_matches = []
    for candidate in scene_files:
        stem = candidate.stem.lower()
        if all(token.lower() in stem for token in spec.filename_tokens):
            filename_matches.append(candidate)
    if len(filename_matches) == 1:
        return filename_matches[0]

    desired_words = _normalized_words(f"{spec.key} {spec.title} {' '.join(spec.filename_tokens)}")
    scored_matches: list[tuple[int, Path]] = []
    for candidate in scene_files:
        class_names, title_words, source = _scene_metadata(candidate)
        stem_words = _normalized_words(candidate.stem.replace("_", " "))
        class_words = _normalized_words(" ".join(class_names))
        source_words = _normalized_words(source)

        score = 0
        score += 5 * len(desired_words & title_words)
        score += 4 * len(desired_words & class_words)
        score += 3 * len(desired_words & stem_words)
        score += len(desired_words & source_words)

        # A valid semantic candidate must contain every lesson filename token
        # somewhere in its filename, class names, TITLE, or source.
        searchable_words = stem_words | class_words | title_words | source_words
        required = {token.lower() for token in spec.filename_tokens}
        if required.issubset(searchable_words):
            scored_matches.append((score, candidate))

    scored_matches.sort(key=lambda item: (-item[0], item[1].name))
    if scored_matches:
        best_score = scored_matches[0][0]
        best = [path for score, path in scored_matches if score == best_score]
        if len(best) == 1:
            return best[0]
        names = ", ".join(path.name for path in best)
        raise RuntimeError(
            f"Ambiguous semantic scene match for {spec.title}: {names}"
        )

    tried = ", ".join(spec.filename_candidates)
    available = ", ".join(path.name for path in sorted(scene_files))
    raise FileNotFoundError(
        f"Could not locate scene for {spec.title}. Tried: {tried}. "
        f"Available scene files: {available}"
    )

