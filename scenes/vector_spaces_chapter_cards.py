"""Opening, section, and closing cards for the vector-spaces chapter."""
from __future__ import annotations

from manim import DOWN, FadeIn, FadeOut, MathTex, Scene, Text, UP, VGroup

from engine.vector_spaces_chapter import CHAPTER_QUESTION, CHAPTER_REFLECTION, CHAPTER_TITLE

BACKGROUND = "#0A0D13"
TEXT = "#E8EAED"
MUTED = "#A9B2C3"
ACCENT = "#7FB3FF"
CARD_TEXT_MAX_WIDTH = 11.0


class _ChapterCard(Scene):
    heading: str = ""
    subheading: str = ""
    hold: float = 2.2

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND
        heading = Text(self.heading, font_size=44, color=TEXT)
        subheading = Text(self.subheading, font_size=27, color=MUTED, line_spacing=1.12)
        group = VGroup(heading, subheading).arrange(DOWN, buff=0.42).move_to(UP * 0.05)
        self.play(FadeIn(heading), run_time=0.8)
        self.play(FadeIn(subheading), run_time=0.8)
        self.wait(self.hold)
        self.play(FadeOut(group), run_time=0.7)


class VectorSpacesChapterOpening(Scene):
    def construct(self) -> None:
        self.camera.background_color = BACKGROUND
        chapter = Text("CHAPTER 2", font_size=28, color=ACCENT).shift(UP * 2.35)
        title = Text(
            "Vector Spaces: Structure, Dimension,\nand the Spaces Inside a Matrix",
            font_size=42,
            color=TEXT,
            line_spacing=1.08,
        ).shift(UP * 0.65)
        question = Text(
            "What makes a collection of vectors\n"
            "into a space,\n"
            "and how can a matrix reveal\n"
            "its hidden structure?",
            font_size=22,
            color=MUTED,
            line_spacing=1.04,
        )
        if question.width > CARD_TEXT_MAX_WIDTH:
            question.scale_to_fit_width(CARD_TEXT_MAX_WIDTH)
        question.shift(DOWN * 1.68)
        self.play(FadeIn(chapter), FadeIn(title), run_time=1.5)
        self.wait(0.8)
        self.play(FadeIn(question), run_time=1.2)
        self.wait(3.0)
        self.play(FadeOut(chapter), FadeOut(title), FadeOut(question), run_time=0.9)


class VectorSpacesSectionOne(_ChapterCard):
    heading = "From Dependence to Subspaces"
    subheading = "When does a collection of vectors create a genuine space?"


class VectorSpacesSectionTwo(_ChapterCard):
    heading = "Basis and Dimension"
    subheading = "How few vectors are enough to describe the whole space?"


class VectorSpacesSectionThree(_ChapterCard):
    heading = "The Spaces Inside a Matrix"
    subheading = "Column space, null space, row space, and pivot structure"


class VectorSpacesSectionFour(_ChapterCard):
    heading = "How the Dimensions Fit Together"
    subheading = "Rank, nullity, and the four fundamental subspaces"


class VectorSpacesChapterClosing(Scene):
    def construct(self) -> None:
        self.camera.background_color = BACKGROUND
        heading = Text("Chapter Reflection", font_size=42, color=TEXT).shift(UP * 2.1)
        reflection = Text(
            "A matrix organizes directions into what survives, what disappears,\n"
            "what can be produced, and what remains unreachable.",
            font_size=27,
            color=MUTED,
            line_spacing=1.15,
        ).shift(UP * 0.55)
        equations = VGroup(
            MathTex(r"\operatorname{rank}(A)+\operatorname{nullity}(A)=n", font_size=40, color=TEXT),
            MathTex(r"\mathbb R^n=\operatorname{row}(A)\oplus\operatorname{null}(A)", font_size=36, color=TEXT),
            MathTex(r"\mathbb R^m=\operatorname{col}(A)\oplus\operatorname{null}(A^T)", font_size=36, color=TEXT),
        ).arrange(DOWN, buff=0.30).shift(DOWN * 1.15)
        self.play(FadeIn(heading), FadeIn(reflection), run_time=1.2)
        self.wait(1.0)
        self.play(FadeIn(equations), run_time=1.4)
        self.wait(3.4)
