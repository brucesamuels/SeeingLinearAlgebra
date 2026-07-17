from __future__ import annotations

import dataclasses

import pytest

from engine.perspective_sequence import Perspective, PerspectiveSequence


def sample_perspective() -> Perspective:
    return Perspective(
        title="Physicist",
        question="How do we describe motion?",
        examples=("velocity", "force"),
        takeaway="Vectors describe motion and force.",
    )


def test_perspective_normalizes_and_freezes_content() -> None:
    perspective = Perspective(
        title="  Physicist  ",
        question="  How?  ",
        examples=("  velocity  ", " force "),
        takeaway="  Motion and force.  ",
    )

    assert perspective.title == "Physicist"
    assert perspective.question == "How?"
    assert perspective.examples == ("velocity", "force")
    assert perspective.takeaway == "Motion and force."

    with pytest.raises(dataclasses.FrozenInstanceError):
        perspective.title = "Changed"  # type: ignore[misc]


def test_perspective_requires_examples() -> None:
    with pytest.raises(ValueError, match="at least one"):
        Perspective(
            title="Title",
            question="Question",
            examples=(),
            takeaway="Takeaway",
        )


def test_sequence_requires_unique_perspective_titles() -> None:
    perspective = sample_perspective()

    with pytest.raises(ValueError, match="unique"):
        PerspectiveSequence(
            title="Why?",
            guiding_question="What?",
            perspectives=(perspective, perspective),
            synthesis="One idea.",
            bridge_question="How?",
            bridge_statement="Begin visually.",
        )
