"""Manim presentation: powers of a diagonalizable matrix."""
from __future__ import annotations

from manim import (
    GREEN_C, GREY_B, ORANGE, PURPLE_C, WHITE, YELLOW,
    DOWN, RIGHT, UP,
    FadeIn, FadeOut, MathTex, ReplacementTransform, Scene, Text, VGroup,
)


class PowersOfDiagonalizableMatrixPresentation(Scene):
    CHAPTER_BANNER = "EIGENVALUES AND EIGENVECTORS"
    LESSON_TITLE = "Powers of a Diagonalizable Matrix"

    def _heading(self, text: str) -> Text:
        item = Text(text, font_size=27, color=WHITE)
        if item.width > 11.6:
            item.scale_to_fit_width(11.6)
        return item

    def _math_heading(self, tex: str) -> MathTex:
        item = MathTex(tex, font_size=35, color=WHITE)
        if item.width > 11.6:
            item.scale_to_fit_width(11.6)
        return item

    def _chrome(self, heading_text: str):
        banner = Text(self.CHAPTER_BANNER, font_size=22, color=GREY_B, weight="BOLD")
        banner.to_edge(UP, buff=0.16)
        title = Text(self.LESSON_TITLE, font_size=32, color=YELLOW, weight="BOLD")
        title.next_to(banner, DOWN, buff=0.12)
        heading = self._heading(heading_text)
        heading.next_to(title, DOWN, buff=0.17)
        return banner, title, heading

    def _replace_heading(self, old, text: str):
        new = self._heading(text).move_to(old)
        self.play(ReplacementTransform(old, new), run_time=0.55)
        return new

    def _replace_math_heading(self, old, tex: str):
        new = self._math_heading(tex).move_to(old)
        self.play(ReplacementTransform(old, new), run_time=0.55)
        return new

    def _fit(self, group: VGroup, heading, gap: float = 0.58) -> VGroup:
        group.next_to(heading, DOWN, buff=gap)
        if group.width > 11.8:
            group.scale_to_fit_width(11.8)
            group.next_to(heading, DOWN, buff=gap)
        bottom_limit = -3.25
        if group.get_bottom()[1] < bottom_limit:
            available = heading.get_bottom()[1] - gap - bottom_limit
            if available > 1.0:
                group.scale_to_fit_height(available)
                group.next_to(heading, DOWN, buff=gap)
        return group

    def construct(self) -> None:
        banner, title, heading = self._chrome("Diagonalization pays off when we need repeated powers of A.")
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading), run_time=0.75)

        # Card 1 — recall the diagonalization and pose the computational problem.
        a_line = MathTex(
            r"A=\begin{bmatrix}4&1&0\\2&3&0\\0&0&1\end{bmatrix}",
            font_size=46,
            color=WHITE,
        )
        diag_line = MathTex(r"A=PDP^{-1}", font_size=54, color=YELLOW)
        question = MathTex(r"\text{How can we compute }A^4\text{ efficiently?}", font_size=39, color=GREEN_C)
        card = self._fit(VGroup(a_line, diag_line, question).arrange(DOWN, buff=0.52), heading)
        self.play(FadeIn(a_line))
        self.play(FadeIn(diag_line))
        self.play(FadeIn(question))
        self.wait(1.4)

        # Card 2 — derive the cancellation for A^2.
        heading = self._replace_math_heading(heading, r"\text{Start with }A^2=(PDP^{-1})(PDP^{-1})\text{.}")
        self.play(FadeOut(card))
        line1 = MathTex(r"A^2=(PDP^{-1})(PDP^{-1})", font_size=47, color=WHITE)
        line2 = MathTex(r"=PD(P^{-1}P)DP^{-1}", font_size=48, color=WHITE)
        line3 = MathTex(r"=PDIDP^{-1}", font_size=48, color=PURPLE_C)
        line4 = MathTex(r"\boxed{A^2=PD^2P^{-1}}", font_size=57, color=YELLOW)
        card = self._fit(VGroup(line1, line2, line3, line4).arrange(DOWN, buff=0.38), heading, gap=0.48)
        self.play(FadeIn(line1))
        self.play(FadeIn(line2))
        self.play(FadeIn(line3))
        self.play(FadeIn(line4))
        self.wait(1.5)

        # Card 3 — extend the pattern to arbitrary powers.
        heading = self._replace_heading(heading, "The same cancellation repeats every time another factor of A is added.")
        self.play(FadeOut(card))
        a3 = MathTex(r"A^3=(PDP^{-1})(PDP^{-1})(PDP^{-1})", font_size=40, color=WHITE)
        a3b = MathTex(r"=PD^3P^{-1}", font_size=50, color=GREEN_C)
        dots = MathTex(r"\vdots", font_size=44, color=GREY_B)
        general = MathTex(r"\boxed{A^k=PD^kP^{-1}}", font_size=60, color=YELLOW)
        condition = Text("for every nonnegative integer k", font_size=27, color=WHITE)
        card = self._fit(VGroup(a3, a3b, dots, general, condition).arrange(DOWN, buff=0.32), heading, gap=0.46)
        self.play(FadeIn(a3))
        self.play(FadeIn(a3b))
        self.play(FadeIn(dots))
        self.play(FadeIn(general))
        self.play(FadeIn(condition))
        self.wait(1.5)

        # Card 4 — compute D^4.
        heading = self._replace_math_heading(heading, r"\text{For our example, computing }D^4\text{ is immediate.}")
        self.play(FadeOut(card))
        d = MathTex(
            r"D=\begin{bmatrix}1&0&0\\0&2&0\\0&0&5\end{bmatrix}",
            font_size=50,
            color=WHITE,
        )
        d4a = MathTex(
            r"D^4=\begin{bmatrix}1^4&0&0\\0&2^4&0\\0&0&5^4\end{bmatrix}",
            font_size=48,
            color=WHITE,
        )
        d4b = MathTex(
            r"\boxed{D^4=\begin{bmatrix}1&0&0\\0&16&0\\0&0&625\end{bmatrix}}",
            font_size=50,
            color=YELLOW,
        )
        note = Text("A diagonal matrix is powered entry by entry along its diagonal.", font_size=27, color=GREEN_C)
        card = self._fit(VGroup(d, d4a, d4b, note).arrange(DOWN, buff=0.38), heading, gap=0.46)
        self.play(FadeIn(d))
        self.play(FadeIn(d4a))
        self.play(FadeIn(d4b))
        self.play(FadeIn(note))
        self.wait(1.6)

        # Card 5 — reconstruct A^4.
        heading = self._replace_math_heading(heading, r"\text{Now reconstruct }A^4=PD^4P^{-1}\text{.}")
        self.play(FadeOut(card))
        p = MathTex(
            r"P=\begin{bmatrix}0&1&1\\0&-2&1\\1&0&0\end{bmatrix}",
            font_size=39,
            color=WHITE,
        )
        d4 = MathTex(
            r"D^4=\begin{bmatrix}1&0&0\\0&16&0\\0&0&625\end{bmatrix}",
            font_size=39,
            color=YELLOW,
        )
        pinv = MathTex(
            r"P^{-1}=\begin{bmatrix}0&0&1\\\frac13&-\frac13&0\\\frac23&\frac13&0\end{bmatrix}",
            font_size=39,
            color=WHITE,
        )
        factors = VGroup(p, d4, pinv).arrange(RIGHT, buff=0.42)
        result = MathTex(
            r"\boxed{A^4=\begin{bmatrix}422&203&0\\406&219&0\\0&0&1\end{bmatrix}}",
            font_size=50,
            color=GREEN_C,
        )
        card = self._fit(VGroup(factors, result).arrange(DOWN, buff=0.58), heading, gap=0.48)
        self.play(FadeIn(factors))
        self.play(FadeIn(result))
        self.wait(1.6)

        # Card 6 — contrast with direct multiplication.
        heading = self._replace_heading(heading, "Diagonalization moves the repeated work into the simplest possible matrix.")
        self.play(FadeOut(card))
        direct = MathTex(r"A^4=A\,A\,A\,A", font_size=51, color=WHITE)
        direct_note = Text("three full matrix multiplications", font_size=27, color=ORANGE)
        versus = Text("versus", font_size=26, color=GREY_B)
        diagonal = MathTex(r"A^4=PD^4P^{-1}", font_size=55, color=YELLOW)
        diagonal_note = Text("raise three diagonal entries, then change basis back", font_size=27, color=GREEN_C)
        card = self._fit(VGroup(direct, direct_note, versus, diagonal, diagonal_note).arrange(DOWN, buff=0.34), heading, gap=0.46)
        self.play(FadeIn(direct), FadeIn(direct_note))
        self.play(FadeIn(versus))
        self.play(FadeIn(diagonal), FadeIn(diagonal_note))
        self.wait(1.6)

        # Card 7 — conceptual takeaway and bridge to dynamics.
        heading = self._replace_heading(heading, "In an eigenvector basis, repeated transformations become repeated scalar multiplication.")
        self.play(FadeOut(card))
        eig1 = MathTex(r"\mathbf v_1:\;1^k", font_size=46, color=PURPLE_C)
        eig2 = MathTex(r"\mathbf v_2:\;2^k", font_size=46, color=GREEN_C)
        eig3 = MathTex(r"\mathbf v_3:\;5^k", font_size=46, color=YELLOW)
        eigs = VGroup(eig1, eig2, eig3).arrange(RIGHT, buff=0.85)
        final = MathTex(r"A^k=P\,\mathrm{diag}(1^k,2^k,5^k)\,P^{-1}", font_size=48, color=WHITE)
        takeaway = Text("The eigenvalues tell us how each eigenvector component grows under repeated application of A.", font_size=26, color=YELLOW)
        card = self._fit(VGroup(eigs, final, takeaway).arrange(DOWN, buff=0.62), heading, gap=0.62)
        self.play(FadeIn(eigs))
        self.play(FadeIn(final))
        self.play(FadeIn(takeaway))
        self.wait(2.0)
