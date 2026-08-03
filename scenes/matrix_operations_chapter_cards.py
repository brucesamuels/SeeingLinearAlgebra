"""Opening and closing cards for the Matrix Operations chapter."""

from __future__ import annotations

from manim import (
    DOWN,
    FadeIn,
    FadeOut,
    LEFT,
    MathTex,
    Scene,
    Text,
    UP,
    VGroup,
    Write,
    YELLOW,
)


class MatrixOperationsChapterTitleCard(Scene):
    """Opening card for the assembled Matrix Operations chapter."""

    def construct(self) -> None:
        chapter = Text(
            "Matrix Operations",
            weight="BOLD",
        ).scale(0.82).move_to(UP * 1.15)

        question = Text(
            "How do matrices combine, act, and preserve structure?",
        ).scale(0.43)
        question.scale_to_fit_width(11.0)
        question.move_to(UP * 0.2)

        roadmap = VGroup(
            Text("Add and scale matrices"),
            Text("Multiply matrices and compose transformations"),
            Text("Read trace and transpose"),
            Text("Understand order, identity, and undoing"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        roadmap.scale(0.36).move_to(DOWN * 1.18)

        self.play(Write(chapter))
        self.play(FadeIn(question, shift=UP * 0.08))
        self.play(FadeIn(roadmap, shift=UP * 0.08))
        self.wait(2.2)
        self.play(
            FadeOut(chapter),
            FadeOut(question),
            FadeOut(roadmap),
        )


class MatrixOperationsChapterReflectionCard(Scene):
    """Closing reflection for the assembled chapter."""

    def construct(self) -> None:
        heading = Text(
            "Chapter Reflection",
            weight="BOLD",
        ).scale(0.68).move_to(UP * 1.65)

        prompt = Text(
            "What does each operation produce—and what does it mean?",
        ).scale(0.43)
        prompt.scale_to_fit_width(11.0)
        prompt.move_to(UP * 0.75)

        ideas = VGroup(
            MathTex(r"A+B,\ cA:\ \text{combine entries}"),
            MathTex(r"A\mathbf{x},\ AB:\ \text{apply and compose}"),
            MathTex(r"\operatorname{tr}(A):\ \text{produce a number}"),
            MathTex(r"A^T:\ \text{exchange rows and columns}"),
            MathTex(r"AB\ne BA\ \text{in general}", color=YELLOW),
        ).arrange(DOWN, buff=0.28)
        ideas.scale(0.68).move_to(DOWN * 1.00)

        final = Text(
            "Matrices are both arrays of numbers and descriptions of linear action.",
        ).scale(0.38)
        final.scale_to_fit_width(11.2)
        final.move_to(DOWN * 2.45)

        self.play(Write(heading))
        self.play(FadeIn(prompt, shift=UP * 0.08))
        for line in ideas:
            self.play(FadeIn(line, shift=UP * 0.05), run_time=0.42)
        self.play(FadeIn(final, shift=UP * 0.08))
        self.wait(2.6)
