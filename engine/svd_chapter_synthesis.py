"""Renderer-independent content for the SVD chapter synthesis."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from engine.truncated_svd_approximation import TruncatedSVDApproximation


@dataclass(frozen=True)
class SynthesisTopic:
    title: str
    question: str
    takeaway: str


@dataclass(frozen=True)
class RecognitionRule:
    operation: str
    singular_value_action: str


class SVDChapterSynthesis:
    """Collect the chapter's concepts around one singular-value spectrum."""

    def __init__(self) -> None:
        self._matrix = np.array([[3.0, 0.0], [0.0, 0.5], [0.0, 0.0]])
        self._approximation = TruncatedSVDApproximation(self._matrix)

    @property
    def matrix(self) -> np.ndarray:
        return self._matrix.copy()

    def singular_values(self) -> np.ndarray:
        return self._approximation.singular_values()

    def rank(self) -> int:
        return int(np.linalg.matrix_rank(self._matrix))

    def condition_number(self) -> float:
        values = self.singular_values()
        positive = values[values > 0]
        return float(positive[0] / positive[-1])

    def pseudoinverse(self) -> np.ndarray:
        return np.linalg.pinv(self._matrix)

    def rank_one_approximation(self) -> np.ndarray:
        return self._approximation.truncated(1)

    def rank_one_error(self) -> float:
        return self._approximation.frobenius_error(1)

    def rank_one_retained_energy(self) -> float:
        values = self.singular_values()
        return float(values[0] ** 2 / np.sum(values**2))

    def topics(self) -> tuple[SynthesisTopic, ...]:
        return (
            SynthesisTopic(
                "Geometric structure",
                "How does the matrix act on orthogonal directions?",
                "V chooses input directions, Sigma scales them, and U places the outputs.",
            ),
            SynthesisTopic(
                "Rank and subspaces",
                "Which directions survive and which disappear?",
                "Positive singular values span the row and column spaces; zeros mark null spaces.",
            ),
            SynthesisTopic(
                "Pseudoinverse",
                "What can be reversed when information is lost?",
                "Reverse positive stretches, project to the image, and choose the shortest pre-image.",
            ),
            SynthesisTopic(
                "Conditioning",
                "How strongly can inversion amplify error?",
                "The smallest positive singular value controls the worst amplification.",
            ),
            SynthesisTopic(
                "Approximation",
                "Which structure should a simpler model retain?",
                "Keep the largest singular layers for the best low-rank approximation.",
            ),
            SynthesisTopic(
                "Image compression",
                "How can fewer values preserve visual structure?",
                "Store the strongest singular image layers and discard finer detail.",
            ),
            SynthesisTopic(
                "PCA",
                "How can data be viewed in fewer dimensions?",
                "Center the observations and retain the directions of greatest variation.",
            ),
            SynthesisTopic(
                "Recognition",
                "What should happen to each singular value?",
                "Reverse, leave at zero, or discard according to the problem being solved.",
            ),
        )

    def recognition_rules(self) -> tuple[RecognitionRule, ...]:
        return (
            RecognitionRule("Inverse", "reverse every singular value"),
            RecognitionRule("Pseudoinverse", "reverse positives; leave zeros at zero"),
            RecognitionRule("Truncated SVD", "keep the largest k singular layers"),
            RecognitionRule("PCA", "center data; keep the strongest directions"),
        )
