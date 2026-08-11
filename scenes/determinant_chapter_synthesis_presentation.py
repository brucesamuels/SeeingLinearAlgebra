"""CP147 presentation: determinant chapter synthesis."""
from __future__ import annotations

import numpy as np
from manim import (
    BLUE, FadeIn, FadeOut, GREEN, GREY_B, Line, MathTex, RED, Scene,
    SurroundingRectangle, Text, VGroup, WHITE, YELLOW, Write,
)

from engine.determinant_chapter_synthesis import (
    algebraic_rules,
    closing_words,
    computation_methods,
    geometric_lines,
    invertibility_chain,
    jacobian_bridge,
    singular_chain,
    system_formulas,
)


class DeterminantChapterSynthesisPresentation(Scene):
    """Close the determinant chapter by connecting its major themes."""

    def construct(self) -> None:
        banner = Text("Determinants: A Chapter Synthesis", font_size=38)
        banner.to_edge(np.array([0.0, 1.0, 0.0]), buff=0.22)
        subtitle = Text("One scalar, many meanings", font_size=25, color=GREY_B)
        subtitle.next_to(banner, np.array([0.0, -1.0, 0.0]), buff=0.10)
        self.play(Write(banner), FadeIn(subtitle))
        self.wait(0.8)
        self.play(FadeOut(subtitle))

        self.show_overview(banner)
        self.show_computation(banner)
        self.show_invertibility(banner)
        self.show_geometry(banner)
        self.show_algebraic_rules(banner)
        self.show_systems(banner)
        self.show_jacobian_bridge(banner)
        self.show_final_map(banner)

    def stage_title(self, text: str, size: int = 27) -> Text:
        title = Text(text, font_size=size, color=YELLOW)
        title.move_to(np.array([0.0, 2.35, 0.0]))
        return title

    def clear_stage(self, preserve: tuple[object, ...]) -> None:
        self.play(*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve])

    def show_overview(self, banner: Text) -> None:
        title = self.stage_title("What has the determinant been telling us?")
        center = MathTex(r"\det(A)", font_size=58, color=GREEN)
        center.move_to(np.array([0.0, 0.15, 0.0]))

        labels = (
            ("Computation", np.array([-4.1, 1.05, 0.0]), BLUE),
            ("Invertibility", np.array([4.1, 1.05, 0.0]), WHITE),
            ("Geometry", np.array([-4.1, -1.25, 0.0]), YELLOW),
            ("Structure", np.array([4.1, -1.25, 0.0]), RED),
        )
        cards = VGroup()
        connectors = VGroup()
        for label, pos, color in labels:
            txt = Text(label, font_size=24, color=color)
            txt.move_to(pos)
            box = SurroundingRectangle(txt, buff=0.20, color=color)
            cards.add(VGroup(box, txt))
            connectors.add(Line(center.get_center(), pos * 0.78, color=GREY_B))

        note = Text(
            "Different questions kept leading back to the same scalar.",
            font_size=20,
            color=GREY_B,
        )
        note.move_to(np.array([0.0, -2.55, 0.0]))

        self.play(FadeIn(title), Write(center))
        self.play(FadeIn(connectors), FadeIn(cards))
        self.play(FadeIn(note))
        self.wait(1.8)
        self.clear_stage((banner,))

    def show_computation(self, banner: Text) -> None:
        title = self.stage_title("Three ways to compute")
        methods = computation_methods()
        stack = VGroup(
            MathTex(methods[0], font_size=27, color=BLUE),
            MathTex(methods[1], font_size=27, color=GREEN),
            MathTex(methods[2], font_size=27, color=WHITE),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.58)
        stack.scale_to_fit_width(10.7)
        stack.move_to(np.array([0.0, -0.20, 0.0]))

        note = Text(
            "Choose the method that matches the structure you see.",
            font_size=21,
            color=GREY_B,
        )
        note.move_to(np.array([0.0, -2.45, 0.0]))

        self.play(FadeIn(title))
        for line in stack:
            self.play(Write(line))
        self.play(FadeIn(note))
        self.wait(1.8)
        self.clear_stage((banner,))

    def show_invertibility(self, banner: Text) -> None:
        title = self.stage_title("One nonzero determinant gives a whole chain of conclusions", size=24)
        nonzero = MathTex(invertibility_chain(), font_size=30, color=GREEN)
        nonzero.scale_to_fit_width(11.2)
        nonzero.move_to(np.array([0.0, 0.55, 0.0]))

        zero = MathTex(singular_chain(), font_size=27, color=RED)
        zero.scale_to_fit_width(11.2)
        zero.move_to(np.array([0.0, -1.20, 0.0]))

        self.play(FadeIn(title))
        self.play(Write(nonzero))
        self.play(Write(zero))
        self.wait(2.0)
        self.clear_stage((banner,))

    def show_geometry(self, banner: Text) -> None:
        title = self.stage_title("The determinant is geometric")
        lines = geometric_lines()
        stack = VGroup(
            MathTex(lines[0], font_size=34, color=GREEN),
            MathTex(lines[1], font_size=31, color=BLUE),
            MathTex(lines[2], font_size=30, color=RED),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.55)
        stack.scale_to_fit_width(10.9)
        stack.move_to(np.array([0.0, -0.25, 0.0]))

        self.play(FadeIn(title))
        for line in stack:
            self.play(Write(line))
        self.wait(2.0)
        self.clear_stage((banner,))

    def show_algebraic_rules(self, banner: Text) -> None:
        title = self.stage_title("The determinant respects matrix structure")
        lines = algebraic_rules()
        stack = VGroup(
            MathTex(lines[0], font_size=36, color=GREEN),
            MathTex(lines[1], font_size=36, color=BLUE),
            MathTex(lines[2], font_size=36, color=WHITE),
        ).arrange(np.array([0.0, -1.0, 0.0]), buff=0.52)
        stack.move_to(np.array([0.0, -0.20, 0.0]))

        note = Text(
            "Products multiply scale factors; transposition preserves them.",
            font_size=20,
            color=GREY_B,
        )
        note.move_to(np.array([0.0, -2.45, 0.0]))

        self.play(FadeIn(title))
        for line in stack:
            self.play(Write(line))
        self.play(FadeIn(note))
        self.wait(1.8)
        self.clear_stage((banner,))

    def show_systems(self, banner: Text) -> None:
        title = self.stage_title("Determinants can solve systems — when the matrix is invertible", size=23)
        cramer, inverse = system_formulas()

        left_title = Text("Cramer's Rule", font_size=22, color=BLUE)
        left_title.move_to(np.array([-3.5, 0.95, 0.0]))
        left_math = MathTex(cramer, font_size=37, color=BLUE)
        left_math.move_to(np.array([-3.5, -0.10, 0.0]))

        right_title = Text("Adjugate inverse", font_size=22, color=GREEN)
        right_title.move_to(np.array([3.5, 0.95, 0.0]))
        right_math = MathTex(inverse, font_size=34, color=GREEN)
        right_math.scale_to_fit_width(5.3)
        right_math.move_to(np.array([3.5, -0.10, 0.0]))

        divider = Line(np.array([0.0, 1.40, 0.0]), np.array([0.0, -1.35, 0.0]), color=GREY_B)
        note = Text(
            "Elegant formulas — but elimination is usually the practical computational tool.",
            font_size=19,
            color=GREY_B,
        )
        note.scale_to_fit_width(10.5)
        note.move_to(np.array([0.0, -2.35, 0.0]))

        self.play(FadeIn(title), FadeIn(divider))
        self.play(FadeIn(left_title), Write(left_math))
        self.play(FadeIn(right_title), Write(right_math))
        self.play(FadeIn(note))
        self.wait(2.0)
        self.clear_stage((banner,))

    def show_jacobian_bridge(self, banner: Text) -> None:
        title = self.stage_title("The same idea survives beyond linear algebra")
        linear, nonlinear = jacobian_bridge()

        top = MathTex(linear, font_size=31, color=BLUE)
        top.scale_to_fit_width(10.0)
        top.move_to(np.array([0.0, 0.70, 0.0]))

        bottom = MathTex(nonlinear, font_size=34, color=GREEN)
        bottom.scale_to_fit_width(10.0)
        bottom.move_to(np.array([0.0, -0.75, 0.0]))

        arrow = MathTex(r"\Longrightarrow", font_size=42, color=YELLOW)
        arrow.move_to(np.array([0.0, 0.0, 0.0]))

        note = Text(
            "The Jacobian turns global linear scaling into local nonlinear scaling.",
            font_size=20,
            color=GREY_B,
        )
        note.move_to(np.array([0.0, -2.25, 0.0]))

        self.play(FadeIn(title), Write(top))
        self.play(Write(arrow), Write(bottom))
        self.play(FadeIn(note))
        self.wait(2.0)
        self.clear_stage((banner,))

    def show_final_map(self, banner: Text) -> None:
        title = self.stage_title("The big picture", size=29)
        det = MathTex(r"\det(A)", font_size=62, color=GREEN)
        det.move_to(np.array([0.0, 0.40, 0.0]))

        words = closing_words()
        left = Text(words[0], font_size=24, color=BLUE).move_to(np.array([-4.0, 0.40, 0.0]))
        right = Text(words[1], font_size=24, color=WHITE).move_to(np.array([4.0, 0.40, 0.0]))
        bottom = Text(words[2], font_size=24, color=YELLOW).move_to(np.array([0.0, -1.35, 0.0]))

        links = VGroup(
            Line(left.get_right(), det.get_left(), color=GREY_B),
            Line(det.get_right(), right.get_left(), color=GREY_B),
            Line(det.get_bottom(), bottom.get_top(), color=GREY_B),
        )

        closing = Text(
            "Recognize structure before you compute.",
            font_size=27,
            color=GREEN,
        )
        closing.move_to(np.array([0.0, -2.45, 0.0]))

        self.play(FadeIn(title), Write(det))
        self.play(FadeIn(left), FadeIn(right), FadeIn(bottom), FadeIn(links))
        self.play(FadeIn(closing))
        self.wait(2.4)
