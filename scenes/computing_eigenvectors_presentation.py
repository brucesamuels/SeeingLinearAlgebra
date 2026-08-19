"""Manim presentation for Chapter 7 lesson 6: computing eigenvectors."""
from __future__ import annotations

import numpy as np
from manim import (
    BLUE_C,
    GREEN_C,
    GREY_B,
    WHITE,
    YELLOW,
    Circumscribe,
    FadeIn,
    FadeOut,
    MathTex,
    ReplacementTransform,
    Scene,
    Text,
    TransformMatchingTex,
    VGroup,
)

from engine.computing_eigenvectors import DEFAULT_MATRIX, EigenvectorComputationLesson


DOWN = np.array([0.0, -1.0, 0.0])
UP = np.array([0.0, 1.0, 0.0])
RIGHT = np.array([1.0, 0.0, 0.0])


class ComputingEigenvectorsPresentation(Scene):
    """Compute one eigenspace for each eigenvalue from the CP172 3x3 example."""

    CHAPTER_BANNER = "EIGENVALUES AND EIGENVECTORS"
    LESSON_TITLE = "Computing Eigenvectors"

    def _heading(self, text: str) -> Text:
        item = Text(text, font_size=26, color=WHITE)
        if item.width > 11.7:
            item.scale_to_fit_width(11.7)
        return item

    def _chrome(self, heading_text: str) -> tuple[Text, Text, Text]:
        banner = Text(self.CHAPTER_BANNER, font_size=22, color=GREY_B, weight="BOLD")
        banner.to_edge(UP, buff=0.16)
        title = Text(self.LESSON_TITLE, font_size=32, color=YELLOW, weight="BOLD")
        title.next_to(banner, DOWN, buff=0.12)
        heading = self._heading(heading_text)
        heading.next_to(title, DOWN, buff=0.16)
        return banner, title, heading

    def _replace_heading(self, old: Text, text: str) -> Text:
        new = self._heading(text)
        new.move_to(old)
        self.play(ReplacementTransform(old, new), run_time=0.55)
        return new

    def _fit_content(self, group: VGroup, heading: Text, gap: float = 0.68, bottom_margin: float = 0.42) -> VGroup:
        group.next_to(heading, DOWN, buff=gap)
        bottom_limit = -3.65 + bottom_margin
        if group.get_bottom()[1] < bottom_limit:
            available_height = heading.get_bottom()[1] - gap - bottom_limit
            if available_height > 1.2:
                group.scale_to_fit_height(available_height)
                group.next_to(heading, DOWN, buff=gap)
        return group

    def construct(self) -> None:
        EigenvectorComputationLesson(DEFAULT_MATRIX)
        banner, title, heading = self._chrome("For each eigenvalue, find the null space of A−λI.")
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading), run_time=0.9)

        # Card 1 — recall matrix and the null-space method.
        matrix = MathTex(r"A=\begin{bmatrix}4&1&0\\2&3&0\\0&0&1\end{bmatrix}", font_size=44, color=WHITE)
        roots = MathTex(r"\lambda=1,\ 2,\ 5", font_size=44, color=GREEN_C)
        method1 = MathTex(r"E_\lambda=\operatorname{Null}(A-\lambda I)", font_size=46, color=YELLOW)
        method2 = MathTex(r"(A-\lambda I)\mathbf v=\mathbf 0", font_size=46, color=BLUE_C)
        intro = VGroup(matrix, roots, method1, method2).arrange(DOWN, buff=0.38)
        self._fit_content(intro, heading, gap=0.74)
        self.play(FadeIn(matrix), FadeIn(roots))
        self.play(FadeIn(method1))
        self.play(FadeIn(method2))
        self.wait(1.2)

        # Card 2 — lambda = 1.
        heading = self._replace_heading(heading, "For λ=1, find Null(A−I) by solving line by line.")
        null1 = MathTex(r"E_1=\operatorname{Null}(A-I)", font_size=38, color=BLUE_C)
        subtract1a = MathTex(
            r"A-I=\begin{bmatrix}4&1&0\\2&3&0\\0&0&1\end{bmatrix}-\begin{bmatrix}1&0&0\\0&1&0\\0&0&1\end{bmatrix}",
            font_size=32,
            color=WHITE,
        )
        subtract1b = MathTex(r"=\begin{bmatrix}3&1&0\\2&2&0\\0&0&0\end{bmatrix}", font_size=38, color=WHITE)
        system1 = MathTex(
            r"\begin{bmatrix}3&1&0\\2&2&0\\0&0&0\end{bmatrix}\begin{bmatrix}x\\y\\z\end{bmatrix}=\begin{bmatrix}0\\0\\0\end{bmatrix}",
            font_size=34,
            color=WHITE,
        )
        line1a = MathTex(r"3x+y=0", font_size=38, color=WHITE)
        line1b = MathTex(r"2x+2y=0", font_size=38, color=WHITE)
        line1c = MathTex(r"x=0,\ y=0,\ z\text{ free}", font_size=38, color=YELLOW)
        span1 = MathTex(r"E_1=\operatorname{span}\left\{\begin{bmatrix}0\\0\\1\end{bmatrix}\right\}", font_size=42, color=GREEN_C)
        stack1 = VGroup(null1, subtract1a, subtract1b, system1, line1a, line1b, line1c, span1).arrange(DOWN, buff=0.20)
        self._fit_content(stack1, heading, gap=0.62)
        self.play(FadeOut(intro), FadeIn(null1))
        self.play(FadeIn(subtract1a))
        self.play(FadeIn(subtract1b))
        self.play(FadeIn(system1))
        self.play(FadeIn(line1a))
        self.play(FadeIn(line1b))
        self.play(FadeIn(line1c))
        self.play(FadeIn(span1))
        self.wait(1.4)

        # Card 3 — lambda = 2.
        heading = self._replace_heading(heading, "For λ=2, find Null(A−2I) by solving line by line.")
        null2 = MathTex(r"E_2=\operatorname{Null}(A-2I)", font_size=38, color=BLUE_C)
        subtract2a = MathTex(
            r"A-2I=\begin{bmatrix}4&1&0\\2&3&0\\0&0&1\end{bmatrix}-\begin{bmatrix}2&0&0\\0&2&0\\0&0&2\end{bmatrix}",
            font_size=32,
            color=WHITE,
        )
        subtract2b = MathTex(r"=\begin{bmatrix}2&1&0\\2&1&0\\0&0&-1\end{bmatrix}", font_size=38, color=WHITE)
        system2 = MathTex(
            r"\begin{bmatrix}2&1&0\\2&1&0\\0&0&-1\end{bmatrix}\begin{bmatrix}x\\y\\z\end{bmatrix}=\begin{bmatrix}0\\0\\0\end{bmatrix}",
            font_size=34,
            color=WHITE,
        )
        line2a = MathTex(r"2x+y=0", font_size=38, color=WHITE)
        line2b = MathTex(r"z=0", font_size=38, color=WHITE)
        line2c = MathTex(r"x=t,\ y=-2t,\ z=0", font_size=38, color=YELLOW)
        vector2 = MathTex(r"\mathbf v=t\begin{bmatrix}1\\-2\\0\end{bmatrix}", font_size=42, color=BLUE_C)
        span2 = MathTex(r"E_2=\operatorname{span}\left\{\begin{bmatrix}1\\-2\\0\end{bmatrix}\right\}", font_size=42, color=GREEN_C)
        stack2 = VGroup(null2, subtract2a, subtract2b, system2, line2a, line2b, line2c, vector2, span2).arrange(DOWN, buff=0.17)
        self._fit_content(stack2, heading, gap=0.60)
        self.play(FadeOut(stack1), FadeIn(null2))
        self.play(FadeIn(subtract2a))
        self.play(FadeIn(subtract2b))
        self.play(FadeIn(system2))
        self.play(FadeIn(line2a))
        self.play(FadeIn(line2b))
        self.play(FadeIn(line2c))
        self.play(TransformMatchingTex(line2c.copy(), vector2), run_time=0.8)
        self.play(FadeIn(span2))
        self.wait(1.4)

        # Card 4 — lambda = 5.
        heading = self._replace_heading(heading, "For λ=5, find Null(A−5I) by solving line by line.")
        null5 = MathTex(r"E_5=\operatorname{Null}(A-5I)", font_size=38, color=BLUE_C)
        subtract5a = MathTex(
            r"A-5I=\begin{bmatrix}4&1&0\\2&3&0\\0&0&1\end{bmatrix}-\begin{bmatrix}5&0&0\\0&5&0\\0&0&5\end{bmatrix}",
            font_size=32,
            color=WHITE,
        )
        subtract5b = MathTex(r"=\begin{bmatrix}-1&1&0\\2&-2&0\\0&0&-4\end{bmatrix}", font_size=38, color=WHITE)
        system5 = MathTex(
            r"\begin{bmatrix}-1&1&0\\2&-2&0\\0&0&-4\end{bmatrix}\begin{bmatrix}x\\y\\z\end{bmatrix}=\begin{bmatrix}0\\0\\0\end{bmatrix}",
            font_size=34,
            color=WHITE,
        )
        line5a = MathTex(r"-x+y=0", font_size=38, color=WHITE)
        line5b = MathTex(r"z=0", font_size=38, color=WHITE)
        line5c = MathTex(r"x=t,\ y=t,\ z=0", font_size=38, color=YELLOW)
        vector5 = MathTex(r"\mathbf v=t\begin{bmatrix}1\\1\\0\end{bmatrix}", font_size=42, color=BLUE_C)
        span5 = MathTex(r"E_5=\operatorname{span}\left\{\begin{bmatrix}1\\1\\0\end{bmatrix}\right\}", font_size=42, color=GREEN_C)
        stack5 = VGroup(null5, subtract5a, subtract5b, system5, line5a, line5b, line5c, vector5, span5).arrange(DOWN, buff=0.17)
        self._fit_content(stack5, heading, gap=0.60)
        self.play(FadeOut(stack2), FadeIn(null5))
        self.play(FadeIn(subtract5a))
        self.play(FadeIn(subtract5b))
        self.play(FadeIn(system5))
        self.play(FadeIn(line5a))
        self.play(FadeIn(line5b))
        self.play(FadeIn(line5c))
        self.play(TransformMatchingTex(line5c.copy(), vector5), run_time=0.8)
        self.play(FadeIn(span5))
        self.wait(1.4)

        # Card 5 — verify one result directly in Av=lambda v.
        heading = self._replace_heading(heading, "Check one computed eigenvector in the definition A v = λ v.")
        check_left = MathTex(r"A\begin{bmatrix}1\\-2\\0\end{bmatrix}=\begin{bmatrix}2\\-4\\0\end{bmatrix}", font_size=44, color=WHITE)
        check_right = MathTex(r"=2\begin{bmatrix}1\\-2\\0\end{bmatrix}", font_size=48, color=GREEN_C)
        check = VGroup(check_left, check_right).arrange(RIGHT, buff=0.50)
        self._fit_content(check, heading, gap=0.84)
        caption = Text("The null-space computation produced a vector that really satisfies A v = λ v.", font_size=27, color=WHITE)
        caption.next_to(check, DOWN, buff=0.60)
        self.play(FadeOut(stack5), FadeIn(check_left))
        self.play(FadeIn(check_right))
        self.play(Circumscribe(check_right, color=GREEN_C, fade_out=True), run_time=0.9)
        self.play(FadeIn(caption))
        self.wait(1.5)

        # Card 6 — collect the eigenspaces.
        heading = self._replace_heading(heading, "Each eigenspace is a null space, and its nonzero vectors are eigenvectors.")
        e1 = MathTex(r"E_1=\operatorname{Null}(A-I)=\operatorname{span}\left\{\begin{bmatrix}0\\0\\1\end{bmatrix}\right\}", font_size=36, color=WHITE)
        e2 = MathTex(r"E_2=\operatorname{Null}(A-2I)=\operatorname{span}\left\{\begin{bmatrix}1\\-2\\0\end{bmatrix}\right\}", font_size=36, color=WHITE)
        e5 = MathTex(r"E_5=\operatorname{Null}(A-5I)=\operatorname{span}\left\{\begin{bmatrix}1\\1\\0\end{bmatrix}\right\}", font_size=36, color=WHITE)
        all_spaces = VGroup(e1, e2, e5).arrange(DOWN, buff=0.34)
        self._fit_content(all_spaces, heading, gap=0.72)
        final_note = Text("For each eigenvalue, we find the null space of A−λI.", font_size=27, color=YELLOW)
        final_note.next_to(all_spaces, DOWN, buff=0.48)
        self.play(FadeOut(check), FadeOut(caption), FadeIn(e1))
        self.play(FadeIn(e2))
        self.play(FadeIn(e5))
        self.play(FadeIn(final_note))
        self.wait(1.8)

        # Card 7 — the three independent eigenvectors form an eigenvector basis for R^3.
        heading = self._replace_heading(heading, "The three eigenvectors are linearly independent.")
        basis_vectors = MathTex(
            r"\mathbf v_1=\begin{bmatrix}0\\0\\1\end{bmatrix},\quad"
            r"\mathbf v_2=\begin{bmatrix}1\\-2\\0\end{bmatrix},\quad"
            r"\mathbf v_3=\begin{bmatrix}1\\1\\0\end{bmatrix}",
            font_size=40,
            color=WHITE,
        )
        independent = MathTex(
            r"\mathbf v_1,\mathbf v_2,\mathbf v_3\text{ independent}",
            font_size=40,
            color=BLUE_C,
        )
        basis = MathTex(
            r"\mathcal B=\left\{\mathbf v_1,\mathbf v_2,\mathbf v_3\right\}\text{ is a basis for }\mathbb R^3",
            font_size=42,
            color=GREEN_C,
        )
        takeaway = Text(
            "Enough independent eigenvectors give us an eigenvector basis.",
            font_size=27,
            color=YELLOW,
        )
        finale = VGroup(basis_vectors, independent, basis, takeaway).arrange(DOWN, buff=0.46)
        self._fit_content(finale, heading, gap=0.74)
        self.play(FadeOut(all_spaces), FadeOut(final_note), FadeIn(basis_vectors))
        self.play(FadeIn(independent))
        self.play(FadeIn(basis))
        self.play(Circumscribe(basis, color=GREEN_C, fade_out=True), run_time=0.9)
        self.play(FadeIn(takeaway))
        self.wait(2.0)
