"""Canonical content for the Chapter 1 prologue: Why Vectors?"""

from __future__ import annotations

from engine.perspective_sequence import Perspective, PerspectiveSequence


WHY_VECTORS_SEQUENCE = PerspectiveSequence(
    title="Why Vectors?",
    guiding_question="What is a vector?",
    perspectives=(
        Perspective(
            title="Physicist",
            question="How do we describe motion and force?",
            examples=(
                "velocity",
                "force",
                "acceleration",
                "gravity",
            ),
            takeaway="Vectors describe motion and force.",
        ),
        Perspective(
            title="Computer Scientist",
            question="How do we represent information?",
            examples=(
                "Netflix recommendations",
                "Spotify suggestions",
                "Google Maps coordinates",
                "RGB color values",
            ),
            takeaway="Vectors represent information.",
        ),
        Perspective(
            title="Engineer",
            question="How do we design and control systems?",
            examples=(
                "bridge loads",
                "robot arms",
                "aircraft motion",
                "satellite trajectories",
            ),
            takeaway="Vectors help us design and control systems.",
        ),
        Perspective(
            title="Mathematician",
            question="What common structure connects these ideas?",
            examples=(
                "vector addition",
                "scalar multiplication",
                "closure under both operations",
                "vector spaces",
            ),
            takeaway=(
                "Addition and scalar multiplication reveal the shared structure."
            ),
        ),
    ),
    synthesis="Different disciplines. One mathematical language.",
    bridge_question="How can one idea describe all of these?",
    bridge_statement=(
        "We begin with the simplest visual model: an arrow drawn from the origin."
    ),
)
