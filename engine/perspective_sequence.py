"""Renderer-independent instructional perspectives and synthesis."""

from __future__ import annotations

from dataclasses import dataclass


def _normalized_text(value: str, label: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{label} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{label} must be nonempty")
    return normalized


@dataclass(frozen=True, slots=True)
class Perspective:
    """One disciplinary viewpoint on a shared concept."""

    title: str
    question: str
    examples: tuple[str, ...]
    takeaway: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "title",
            _normalized_text(self.title, "perspective title"),
        )
        object.__setattr__(
            self,
            "question",
            _normalized_text(self.question, "perspective question"),
        )
        object.__setattr__(
            self,
            "takeaway",
            _normalized_text(self.takeaway, "perspective takeaway"),
        )

        try:
            examples = tuple(self.examples)
        except TypeError as exc:
            raise TypeError("perspective examples must be iterable") from exc

        if not examples:
            raise ValueError("perspective must contain at least one example")

        normalized_examples = tuple(
            _normalized_text(example, "perspective example")
            for example in examples
        )
        object.__setattr__(self, "examples", normalized_examples)


@dataclass(frozen=True, slots=True)
class PerspectiveSequence:
    """Ordered perspectives culminating in a unifying synthesis."""

    title: str
    guiding_question: str
    perspectives: tuple[Perspective, ...]
    synthesis: str
    bridge_question: str
    bridge_statement: str

    def __post_init__(self) -> None:
        for attribute_name in (
            "title",
            "guiding_question",
            "synthesis",
            "bridge_question",
            "bridge_statement",
        ):
            object.__setattr__(
                self,
                attribute_name,
                _normalized_text(
                    getattr(self, attribute_name),
                    attribute_name,
                ),
            )

        try:
            perspectives = tuple(self.perspectives)
        except TypeError as exc:
            raise TypeError("perspectives must be iterable") from exc

        if not perspectives:
            raise ValueError(
                "perspective sequence must contain at least one perspective"
            )
        if not all(isinstance(item, Perspective) for item in perspectives):
            raise TypeError(
                "perspective sequence entries must be Perspective instances"
            )

        titles = tuple(item.title for item in perspectives)
        if len(set(titles)) != len(titles):
            raise ValueError("perspective titles must be unique")

        object.__setattr__(self, "perspectives", perspectives)
