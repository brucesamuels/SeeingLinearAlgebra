from __future__ import annotations

from engine.why_vectors_content import WHY_VECTORS_SEQUENCE


def test_why_vectors_contains_four_perspectives() -> None:
    assert tuple(
        perspective.title
        for perspective in WHY_VECTORS_SEQUENCE.perspectives
    ) == (
        "Physicist",
        "Computer Scientist",
        "Engineer",
        "Mathematician",
    )


def test_computer_science_examples_include_familiar_applications() -> None:
    computer_scientist = WHY_VECTORS_SEQUENCE.perspectives[1]

    assert "Netflix recommendations" in computer_scientist.examples
    assert "Spotify suggestions" in computer_scientist.examples
    assert "Google Maps coordinates" in computer_scientist.examples
    assert "RGB color values" in computer_scientist.examples


def test_mathematical_perspective_names_core_operations() -> None:
    mathematician = WHY_VECTORS_SEQUENCE.perspectives[3]

    assert "vector addition" in mathematician.examples
    assert "scalar multiplication" in mathematician.examples


def test_prologue_bridges_to_origin_based_arrow_model() -> None:
    assert "arrow" in WHY_VECTORS_SEQUENCE.bridge_statement
    assert "origin" in WHY_VECTORS_SEQUENCE.bridge_statement
