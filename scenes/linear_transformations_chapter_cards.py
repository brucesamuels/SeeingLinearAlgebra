"""Opening and closing cards for the Linear Transformations chapter."""

from manim import *


class LinearTransformationsChapterOpening(Scene):
    def construct(self):
        chapter = Text(
            "Linear Transformations",
            font_size=54,
            weight=BOLD,
        )

        question = Text(
            "How can one rule move every vector\n"
            "while preserving the structure of space?",
            font_size=32,
            line_spacing=1.15,
        )

        bridge = MathTex(
            r"T(a\mathbf u+b\mathbf v)"
            r"="
            r"aT(\mathbf u)+bT(\mathbf v)",
            font_size=42,
            color=YELLOW,
        )

        group = VGroup(chapter, question, bridge).arrange(DOWN, buff=0.52)
        frame = SurroundingRectangle(group, buff=0.48, color=WHITE)

        self.play(FadeIn(chapter))
        self.play(FadeIn(question))
        self.play(Write(bridge))
        self.play(Create(frame))
        self.wait(3.0)


class LinearTransformationsChapterReflection(Scene):
    def construct(self):
        heading = Text(
            "Reflection",
            font_size=44,
            color=YELLOW,
        ).to_edge(UP)

        question = Text(
            "If we know where a linear transformation sends a basis,\n"
            "what else remains to be determined?",
            font_size=31,
            line_spacing=1.15,
        ).shift(UP * 0.55)

        self.play(FadeIn(heading), FadeIn(question))
        self.wait(2.8)

        answer = Text(
            "Nothing.",
            font_size=44,
            color=GREEN,
        )

        reason = Text(
            "Every vector is a linear combination of the basis vectors.",
            font_size=29,
        )

        formula = Text(
            "x = x₁e₁ + x₂e₂    ⇒    T(x) = x₁T(e₁) + x₂T(e₂)",
            font_size=30,
        )

        matrix = MathTex(
            r"A="
            r"\begin{bmatrix}"
            r"\vert&\vert\\"
            r"T(\mathbf e_1)&T(\mathbf e_2)\\"
            r"\vert&\vert"
            r"\end{bmatrix}",
            font_size=42,
            color=YELLOW,
        )

        conclusion = VGroup(answer, reason, formula, matrix).arrange(
            DOWN,
            buff=0.38,
        ).shift(DOWN * 0.45)

        self.play(FadeOut(question))
        self.play(FadeIn(answer))
        self.play(FadeIn(reason))
        self.play(Write(formula))
        self.play(FadeIn(matrix))
        self.wait(3.2)
