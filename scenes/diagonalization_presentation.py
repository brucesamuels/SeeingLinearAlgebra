"""Manim presentation: derive the diagonal matrix from A and an eigenvector basis P."""
from __future__ import annotations

from manim import (
    GREEN_C, GREY_B, PURPLE_C, WHITE, YELLOW,
    DOWN, LEFT, RIGHT, UP,
    Arrow, FadeIn, FadeOut, MathTex, ReplacementTransform, Scene, Text, VGroup,
)


class DiagonalizationPresentation(Scene):
    CHAPTER_BANNER = "EIGENVALUES AND EIGENVECTORS"
    LESSON_TITLE = "Diagonalization"

    def _heading(self, text: str) -> Text:
        item = Text(text, font_size=27, color=WHITE)
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
        new = MathTex(tex, font_size=36, color=WHITE)
        if new.width > 11.6:
            new.scale_to_fit_width(11.6)
        new.move_to(old)
        self.play(ReplacementTransform(old, new), run_time=0.55)
        return new

    def _fit(self, group: VGroup, heading: Text, gap: float = 0.62) -> VGroup:
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
        banner, title, heading = self._chrome("Given A and an eigenvector basis P, what matrix represents A in that basis?")
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading), run_time=0.75)

        # Card 1 — start with A and the already-known eigenvector basis P.
        a_matrix = MathTex(
            r"A=\begin{bmatrix}4&1&0\\2&3&0\\0&0&1\end{bmatrix}",
            font_size=47,
            color=WHITE,
        )
        p_matrix = MathTex(
            r"P=[\mathbf v_1\ \mathbf v_2\ \mathbf v_3]="
            r"\begin{bmatrix}0&1&1\\0&-2&1\\1&0&0\end{bmatrix}",
            font_size=43,
            color=WHITE,
        )
        note = Text("P changes eigenbasis coordinates into standard coordinates.", font_size=27, color=YELLOW)
        card = self._fit(VGroup(a_matrix, p_matrix, note).arrange(DOWN, buff=0.50), heading)
        self.play(FadeIn(a_matrix))
        self.play(FadeIn(p_matrix))
        self.play(FadeIn(note))
        self.wait(1.4)

        # Card 2 — solve algebraically for the matrix D in the eigenvector basis.
        heading = self._replace_heading(heading, "Solve for the matrix D that represents A in the P-basis.")
        self.play(FadeOut(card))
        eq1 = MathTex(r"AP=PD", font_size=50, color=WHITE)
        eq2 = MathTex(r"P^{-1}AP=P^{-1}PD", font_size=46, color=WHITE)
        eq3 = MathTex(r"\boxed{D=P^{-1}AP}", font_size=58, color=YELLOW)
        expl = Text("So D is determined by A and P; we do not assume its entries in advance.", font_size=27, color=GREEN_C)
        card = self._fit(VGroup(eq1, eq2, eq3, expl).arrange(DOWN, buff=0.43), heading, gap=0.50)
        self.play(FadeIn(eq1))
        self.play(FadeIn(eq2))
        self.play(FadeIn(eq3))
        self.play(FadeIn(expl))
        self.wait(1.5)

        # Card 3 — compute P^{-1}.
        heading = self._replace_math_heading(heading, r"\text{First compute }P^{-1}\text{.}")
        self.play(FadeOut(card))
        p_line = MathTex(
            r"P=\begin{bmatrix}0&1&1\\0&-2&1\\1&0&0\end{bmatrix}",
            font_size=46,
            color=WHITE,
        )
        pinv_line = MathTex(
            r"P^{-1}=\begin{bmatrix}0&0&1\\\frac13&-\frac13&0\\\frac23&\frac13&0\end{bmatrix}",
            font_size=46,
            color=YELLOW,
        )
        card = self._fit(VGroup(p_line, pinv_line).arrange(DOWN, buff=0.62), heading)
        self.play(FadeIn(p_line))
        self.play(FadeIn(pinv_line))
        self.wait(1.4)

        # Card 4 — multiply P^{-1} A first, then multiply by P.
        heading = self._replace_math_heading(heading, r"\text{Now evaluate }D=P^{-1}AP\text{ step by step.}")
        self.play(FadeOut(card))
        line1 = MathTex(
            r"P^{-1}A="
            r"\begin{bmatrix}0&0&1\\\frac13&-\frac13&0\\\frac23&\frac13&0\end{bmatrix}"
            r"\begin{bmatrix}4&1&0\\2&3&0\\0&0&1\end{bmatrix}",
            font_size=34,
            color=WHITE,
        )
        line2 = MathTex(
            r"=\begin{bmatrix}0&0&1\\\frac23&-\frac23&0\\\frac{10}{3}&\frac53&0\end{bmatrix}",
            font_size=42,
            color=GREEN_C,
        )
        line3 = MathTex(
            r"D=(P^{-1}A)P="
            r"\begin{bmatrix}0&0&1\\\frac23&-\frac23&0\\\frac{10}{3}&\frac53&0\end{bmatrix}"
            r"\begin{bmatrix}0&1&1\\0&-2&1\\1&0&0\end{bmatrix}",
            font_size=31,
            color=WHITE,
        )
        line4 = MathTex(
            r"\boxed{D=\begin{bmatrix}1&0&0\\0&2&0\\0&0&5\end{bmatrix}}",
            font_size=51,
            color=YELLOW,
        )
        card = self._fit(VGroup(line1, line2, line3, line4).arrange(DOWN, buff=0.30), heading, gap=0.42)
        self.play(FadeIn(line1))
        self.play(FadeIn(line2))
        self.play(FadeIn(line3))
        self.play(FadeIn(line4))
        self.wait(1.6)

        # Card 5 — interpret what was discovered.
        heading = self._replace_heading(heading, "The calculation discovers a diagonal matrix.")
        self.play(FadeOut(card))
        discovered = MathTex(
            r"D=\begin{bmatrix}1&0&0\\0&2&0\\0&0&5\end{bmatrix}",
            font_size=55,
            color=YELLOW,
        )
        meaning1 = Text("Because the columns of P are eigenvectors, A does not mix these coordinates.", font_size=27, color=WHITE)
        meaning2 = Text("The diagonal entries 1, 2, and 5 are the corresponding eigenvalues.", font_size=28, color=GREEN_C)
        card = self._fit(VGroup(discovered, meaning1, meaning2).arrange(DOWN, buff=0.55), heading)
        self.play(FadeIn(discovered))
        self.play(FadeIn(meaning1))
        self.play(FadeIn(meaning2))
        self.wait(1.6)

        # Card 6 — recover the usual diagonalization identity.
        heading = self._replace_math_heading(heading, r"\text{Now rewrite }D=P^{-1}AP\text{ as a factorization of }A\text{.}")
        self.play(FadeOut(card))
        f1 = MathTex(r"D=P^{-1}AP", font_size=50, color=WHITE)
        f2 = MathTex(r"PD=AP", font_size=48, color=WHITE)
        f3 = MathTex(r"PDP^{-1}=A", font_size=50, color=WHITE)
        f4 = MathTex(r"\boxed{A=PDP^{-1}}", font_size=60, color=YELLOW)
        card = self._fit(VGroup(f1, f2, f3, f4).arrange(DOWN, buff=0.40), heading, gap=0.48)
        self.play(FadeIn(f1))
        self.play(FadeIn(f2))
        self.play(FadeIn(f3))
        self.play(FadeIn(f4))
        self.wait(1.5)

        # Card 7 — interpret right to left.
        heading = self._replace_math_heading(heading, r"\text{Read }A=PDP^{-1}\text{ from right to left.}")
        self.play(FadeOut(card))
        x0 = MathTex(r"\mathbf x", font_size=43, color=WHITE)
        c1 = MathTex(r"[\mathbf x]_{\mathcal B}", font_size=40, color=PURPLE_C)
        c2 = MathTex(r"[A\mathbf x]_{\mathcal B}", font_size=40, color=GREEN_C)
        x1 = MathTex(r"A\mathbf x", font_size=43, color=WHITE)
        a1 = Arrow(LEFT, RIGHT, buff=0, stroke_width=3).scale(0.62)
        a2 = Arrow(LEFT, RIGHT, buff=0, stroke_width=3).scale(0.62)
        a3 = Arrow(LEFT, RIGHT, buff=0, stroke_width=3).scale(0.62)
        l1 = MathTex(r"P^{-1}", font_size=31, color=YELLOW)
        l2 = MathTex(r"D", font_size=31, color=YELLOW)
        l3 = MathTex(r"P", font_size=31, color=YELLOW)
        flow = VGroup(x0, a1, c1, a2, c2, a3, x1).arrange(RIGHT, buff=0.28)
        l1.next_to(a1, UP, buff=0.12)
        l2.next_to(a2, UP, buff=0.12)
        l3.next_to(a3, UP, buff=0.12)
        captions = VGroup(
            Text("standard → eigenbasis", font_size=22, color=GREY_B),
            Text("apply the diagonal action", font_size=22, color=GREY_B),
            Text("eigenbasis → standard", font_size=22, color=GREY_B),
        ).arrange(RIGHT, buff=0.65)
        captions.next_to(flow, DOWN, buff=0.65)
        card = VGroup(flow, l1, l2, l3, captions)
        self._fit(card, heading, gap=0.85)
        self.play(FadeIn(x0), FadeIn(a1), FadeIn(l1), FadeIn(c1))
        self.play(FadeIn(a2), FadeIn(l2), FadeIn(c2))
        self.play(FadeIn(a3), FadeIn(l3), FadeIn(x1))
        self.play(FadeIn(captions))
        self.wait(1.8)

        # Card 8 — takeaway.
        heading = self._replace_heading(heading, "Diagonalization is a change-of-basis calculation, not a guess.")
        self.play(FadeOut(card))
        takeaway1 = MathTex(r"D=P^{-1}AP", font_size=56, color=YELLOW)
        takeaway2 = MathTex(r"A=PDP^{-1}", font_size=56, color=GREEN_C)
        takeaway3 = Text("Once D is known, powers of A become much easier to compute.", font_size=28, color=WHITE)
        card = self._fit(VGroup(takeaway1, takeaway2, takeaway3).arrange(DOWN, buff=0.58), heading)
        self.play(FadeIn(takeaway1))
        self.play(FadeIn(takeaway2))
        self.play(FadeIn(takeaway3))
        self.wait(2.0)
