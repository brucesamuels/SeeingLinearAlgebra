"""Renderer-independent content for the Eigenvalues and Eigenvectors chapter review."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReviewTopic:
    title: str
    takeaway: str


class EigenvaluesChapterReview:
    """Curated conceptual checkpoints for the chapter review."""

    def topics(self) -> tuple[ReviewTopic, ...]:
        return (
            ReviewTopic("Eigenpairs", "Av = lambda v identifies invariant directions."),
            ReviewTopic("Eigenspaces", "E_lambda = Null(A-lambda I)."),
            ReviewTopic("Diagonalization", "A = P D P^{-1} when eigenvectors form a basis."),
            ReviewTopic("Repeated eigenvalues", "Diagonalizability depends on enough independent eigenvectors."),
            ReviewTopic("Symmetric matrices", "A = Q D Q^T with an orthonormal eigenbasis."),
            ReviewTopic("Applications", "Eigenvector coordinates decouple powers, ODEs, and recurrences."),
        )
