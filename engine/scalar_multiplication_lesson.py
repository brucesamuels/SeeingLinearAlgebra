"""Renderer-independent instructional sequence for scalar multiplication."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ScalarMultiplicationStage:
    """One pedagogical state in the scalar-multiplication lesson."""

    key: str
    scalar: float
    interpretation: str


BASE_VECTOR = (2.0, 1.0)

SCALAR_MULTIPLICATION_STAGES = (
    ScalarMultiplicationStage(
        key="stretch",
        scalar=2.0,
        interpretation="A positive scalar greater than one stretches the vector.",
    ),
    ScalarMultiplicationStage(
        key="contract",
        scalar=0.5,
        interpretation="A positive scalar between zero and one contracts the vector.",
    ),
    ScalarMultiplicationStage(
        key="zero",
        scalar=0.0,
        interpretation="Multiplication by zero collapses the vector to the origin.",
    ),
    ScalarMultiplicationStage(
        key="reverse",
        scalar=-1.0,
        interpretation="A negative scalar reverses direction.",
    ),
)


def scaled_vector(scalar: float) -> tuple[float, float]:
    """Return ``scalar`` times the approved base vector."""

    return tuple(float(scalar * component) for component in BASE_VECTOR)
