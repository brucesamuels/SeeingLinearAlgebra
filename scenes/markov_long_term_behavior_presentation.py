"""Manim presentation: powers, steady states, and absorbing states."""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow, BLACK, Circle, DOWN, Dot, FadeIn, FadeOut, GREEN_C, GREY_B,
    LEFT, Line, MathTex, Matrix, ORANGE, RIGHT, Scene, ShowPassingFlash,
    SurroundingRectangle, TEAL_C, Tex, Text, Transform, UP, VGroup, WHITE, YELLOW,
)

from engine.markov_long_term_behavior import MarkovLongTermBehavior


class MarkovLongTermBehaviorPresentation(Scene):
    CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"
    LESSON_TITLE = "Long-Term Probabilities and Steady States"
    FOUR_POSITIONS = {
        1: LEFT * 1.45 + UP * 1.05,
        2: RIGHT * 1.45 + UP * 1.05,
        3: LEFT * 1.45 + DOWN * 1.05,
        4: RIGHT * 1.45 + DOWN * 1.05,
    }

    def _heading(self, text):
        item = Text(text, font_size=27, color=WHITE)
        if item.width > 11.4:
            item.scale_to_fit_width(11.4)
        return item

    def _chrome(self, heading_text):
        banner = Tex(r"\textbf{GRAPHS, NETWORKS, AND THE LAPLACIAN}", font_size=23, color=GREY_B).to_edge(UP, buff=0.16)
        title = Tex(r"\textbf{Long-Term Probabilities and Steady States}", font_size=32, color=YELLOW).next_to(banner, DOWN, buff=0.11)
        heading = self._heading(heading_text).next_to(title, DOWN, buff=0.16)
        return banner, title, heading

    def _replace_heading(self, old, text):
        new = self._heading(text).move_to(old)
        self.play(FadeOut(old), run_time=0.18)
        self.play(FadeIn(new), run_time=0.22)
        return new

    @staticmethod
    def _matrix(entries, scale=0.67, h_buff=0.78, v_buff=0.67):
        return Matrix(entries, h_buff=h_buff, v_buff=v_buff).scale(scale)

    @staticmethod
    def _card(label, statement, note, color, width=4.15):
        content = VGroup(
            Text(label, font_size=22, color=color, weight="BOLD"),
            MathTex(statement, font_size=35, color=WHITE),
            Text(note, font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.15)
        if content.width > width - 0.34:
            content.scale_to_fit_width(width - 0.34)
        return VGroup(SurroundingRectangle(content, color=color, buff=0.19, stroke_width=2.0), content)

    @classmethod
    def _four_states(cls, shift=DOWN * 0.10):
        positions = {state: point + shift for state, point in cls.FOUR_POSITIONS.items()}
        guides = VGroup(
            Line(positions[1], positions[2], color=GREY_B, stroke_width=2.5),
            Line(positions[1], positions[3], color=GREY_B, stroke_width=2.5),
            Line(positions[2], positions[4], color=GREY_B, stroke_width=2.5),
            Line(positions[3], positions[4], color=GREY_B, stroke_width=2.5),
        ).set_opacity(0.55)
        dots = {state: Dot(positions[state], radius=0.18, color=YELLOW).set_z_index(3) for state in (1, 2, 3, 4)}
        labels = {
            state: MathTex(str(state), font_size=29, color=BLACK).move_to(positions[state]).set_z_index(5)
            for state in (1, 2, 3, 4)
        }
        return VGroup(guides, *dots.values(), *labels.values()), positions, dots

    @staticmethod
    def _probability_marks(positions, values, color=TEAL_C):
        marks = VGroup()
        for state, value in zip(sorted(positions), values):
            if value > 1e-10:
                marks.add(
                    Circle(
                        radius=0.24 + 0.50 * np.sqrt(value), color=color, stroke_width=3.0,
                        fill_color=color, fill_opacity=0.14 + 0.46 * value,
                    ).move_to(positions[state]).set_z_index(1)
                )
        return marks

    def construct(self):
        mixing = MarkovLongTermBehavior.mixing_chain()
        branching = MarkovLongTermBehavior.branching_chain()
        start = mixing.point_mass(1)
        trajectory = mixing.trajectory(start, 3)
        steady = mixing.uniform_distribution()
        if not np.allclose(trajectory[1], [5 / 8, 1 / 8, 1 / 8, 1 / 8]):
            raise RuntimeError("unexpected first probability step")
        if not np.allclose(trajectory[2], [7 / 16, 3 / 16, 3 / 16, 3 / 16]):
            raise RuntimeError("unexpected second probability step")
        if not np.allclose(trajectory[3], [11 / 32, 7 / 32, 7 / 32, 7 / 32]):
            raise RuntimeError("unexpected third probability step")
        if not mixing.is_stationary(steady) or mixing.fixed_space_dimension() != 1:
            raise RuntimeError("unexpected steady state")
        if mixing.first_positive_power() != 1 or not mixing.is_regular():
            raise RuntimeError("unexpected regularity")
        if not np.allclose(branching.absorption_probabilities([1, 0, 0, 0]), [1 / 2, 1 / 2]):
            raise RuntimeError("unexpected absorption probabilities")

        banner, title, heading = self._chrome("A probability vector in R⁴ records the chances of four possible states.")
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        # Card 1: probability vectors and the long-term question.
        vector = self._matrix([["x_1"], ["x_2"], ["x_3"], ["x_4"]], scale=0.68, v_buff=0.83)
        vector_group = VGroup(MathTex(r"x=", font_size=42, color=YELLOW), vector).arrange(RIGHT, buff=0.28).move_to(LEFT * 2.65)
        constraints = VGroup(
            MathTex(r"x_i\ge0", font_size=42, color=TEAL_C),
            MathTex(r"x_1+x_2+x_3+x_4=1", font_size=40, color=GREEN_C),
            Text("Each coordinate is a probability; together they contain all the probability.", font_size=23, color=WHITE),
        )
        constraints[2].scale_to_fit_width(5.05)
        constraints.arrange(DOWN, buff=0.32).to_edge(RIGHT, buff=0.43)
        question = MathTex(r"x_k=A^k x_0\quad\xrightarrow{k\to\infty}\quad ?", font_size=43, color=ORANGE).to_edge(DOWN, buff=0.70)
        self.play(FadeIn(vector_group), FadeIn(constraints), FadeIn(question))
        self.wait(3.0)

        # Card 2: state the numerical transition rule first.
        heading = self._replace_heading(heading, "At each step: stay with probability one half, or choose any state uniformly.")
        self.play(FadeOut(vector_group), FadeOut(constraints), FadeOut(question))
        states, positions, dots = self._four_states(shift=LEFT * 2.72 + DOWN * 0.10)
        rules = VGroup(
            self._card("STAY", r"\frac12", "remain at the current state", TEAL_C, width=4.72),
            self._card("CHOOSE UNIFORMLY", r"\frac12\cdot\frac14=\frac18", "for each of the four destinations", ORANGE, width=4.72),
            MathTex(r"\Pr(i\to i)=\frac12+\frac18=\frac58", font_size=39, color=YELLOW),
            Text("Moving to each different state has probability 1/8.", font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.28).scale(0.92).to_edge(RIGHT, buff=0.38).shift(DOWN * 0.08)
        self.play(FadeIn(states), FadeIn(rules[0]))
        self.play(*[ShowPassingFlash(Circle(radius=0.34, color=TEAL_C).move_to(dots[state]).set_stroke(width=6)) for state in dots])
        self.play(FadeIn(rules[1:]))
        self.wait(3.0)

        # Card 3: structural four-by-four transition matrix.
        heading = self._replace_heading(heading, "A Markov matrix maps probability vectors to probability vectors.")
        self.play(FadeOut(states), FadeOut(rules))
        transition = self._matrix(
            [[r"\frac58", r"\frac18", r"\frac18", r"\frac18"],
             [r"\frac18", r"\frac58", r"\frac18", r"\frac18"],
             [r"\frac18", r"\frac18", r"\frac58", r"\frac18"],
             [r"\frac18", r"\frac18", r"\frac18", r"\frac58"]],
            scale=0.61, h_buff=1.03, v_buff=1.50,
        ).move_to(LEFT * 1.28 + DOWN * 0.02)
        transition_label = MathTex(r"A=", font_size=42, color=YELLOW).next_to(transition, LEFT, buff=0.30)
        matrix_panel = VGroup(
            self._card("MARKOV MATRIX", r"x_{k+1}=Ax_k", "entries ≥ 0; column j starts at state j", GREEN_C, width=4.55),
            self._card("COLUMN-STOCHASTIC", r"\mathbf1^TA=\mathbf1^T", "every column sums to one", TEAL_C, width=4.55),
            Text("Here A is a transition matrix, not the earlier adjacency matrix.", font_size=21, color=YELLOW),
        )
        matrix_panel[2].scale_to_fit_width(4.15)
        matrix_panel.arrange(DOWN, buff=0.31).to_edge(RIGHT, buff=0.37).shift(DOWN * 0.05)
        self.play(FadeIn(transition_label), FadeIn(transition), FadeIn(matrix_panel))
        self.wait(3.2)

        # Card 4: x1 is the first column.
        heading = self._replace_heading(heading, "Starting at state 1, one multiplication reads the first column of A.")
        self.play(FadeOut(transition_label), FadeOut(transition), FadeOut(matrix_panel))
        states, positions, _ = self._four_states(shift=LEFT * 2.72 + DOWN * 0.10)
        marks = self._probability_marks(positions, trajectory[0], ORANGE)
        computation = VGroup(
            MathTex(r"x_0=e_1=(1,0,0,0)^T", font_size=38, color=ORANGE),
            MathTex(r"x_1=Ax_0=Ae_1", font_size=41, color=WHITE),
            MathTex(r"=\operatorname{column}_1(A)", font_size=39, color=TEAL_C),
            MathTex(r"=\left(\frac58,\frac18,\frac18,\frac18\right)^T", font_size=42, color=YELLOW),
        ).arrange(DOWN, buff=0.34).to_edge(RIGHT, buff=0.49)
        self.play(FadeIn(states), FadeIn(marks), FadeIn(computation[0]))
        self.play(Transform(marks, self._probability_marks(positions, trajectory[1], TEAL_C)), FadeIn(computation[1:]), run_time=1.35)
        self.wait(3.0)

        # Card 5: compute A^2 x0 coordinate by coordinate.
        heading = self._replace_heading(heading, "A second multiplication combines the columns using the probabilities in x₁.")
        self.play(FadeOut(states), FadeOut(marks), FadeOut(computation))
        multiplication = VGroup(
            MathTex(r"x_2=A x_1=A^2x_0", font_size=43, color=YELLOW),
            MathTex(r"(x_2)_1=\frac58\frac58+3\left(\frac18\frac18\right)=\frac{28}{64}=\frac7{16}", font_size=39, color=TEAL_C),
            MathTex(r"(x_2)_2=\frac18\frac58+\frac58\frac18+2\left(\frac18\frac18\right)=\frac{12}{64}=\frac3{16}", font_size=37, color=GREEN_C),
            MathTex(r"x_2=\left(\frac7{16},\frac3{16},\frac3{16},\frac3{16}\right)^T", font_size=43, color=WHITE),
        ).arrange(DOWN, buff=0.42).move_to(DOWN * 0.05)
        multiplication[1].scale_to_fit_width(10.4)
        multiplication[2].scale_to_fit_width(10.6)
        for line in multiplication:
            self.play(FadeIn(line), run_time=0.48)
        self.wait(3.1)

        # Card 6: continue the powers visually.
        heading = self._replace_heading(heading, "The large first probability shrinks while the other three rise toward one fourth.")
        self.play(FadeOut(multiplication))
        states, positions, _ = self._four_states(shift=LEFT * 2.72 + DOWN * 0.10)
        marks = self._probability_marks(positions, trajectory[1], TEAL_C)
        table = VGroup(
            MathTex(r"x_0=(1,0,0,0)^T", font_size=33, color=GREY_B),
            MathTex(r"x_1=\left(\frac58,\frac18,\frac18,\frac18\right)^T", font_size=36, color=TEAL_C),
            MathTex(r"x_2=\left(\frac7{16},\frac3{16},\frac3{16},\frac3{16}\right)^T", font_size=36, color=GREEN_C),
            MathTex(r"x_3=\left(\frac{11}{32},\frac7{32},\frac7{32},\frac7{32}\right)^T", font_size=36, color=YELLOW),
        ).arrange(DOWN, buff=0.37).to_edge(RIGHT, buff=0.46).shift(DOWN * 0.05)
        table[2].scale_to_fit_width(4.75)
        table[3].scale_to_fit_width(4.90)
        self.play(FadeIn(states), FadeIn(marks), FadeIn(table[0:2]))
        self.play(Transform(marks, self._probability_marks(positions, trajectory[2], GREEN_C)), FadeIn(table[2]), run_time=1.20)
        self.play(Transform(marks, self._probability_marks(positions, trajectory[3], YELLOW)), FadeIn(table[3]), run_time=1.20)
        self.wait(3.0)

        # Card 7: derive A^k and its limit.
        heading = self._replace_heading(heading, "Regular means some power is entirely positive; here A itself is positive.")
        self.play(FadeOut(states), FadeOut(marks), FadeOut(table))
        powers = VGroup(
            MathTex(r"U=\frac14\mathbf1\mathbf1^T", font_size=40, color=TEAL_C),
            MathTex(r"A=U+\frac12(I-U)", font_size=43, color=WHITE),
            MathTex(r"A^k=U+2^{-k}(I-U)", font_size=45, color=YELLOW),
            MathTex(r"2^{-k}\to0\quad\Longrightarrow\quad A^k\to U", font_size=42, color=GREEN_C),
        ).arrange(DOWN, buff=0.33).move_to(LEFT * 2.35)
        limit_panel = VGroup(
            MathTex(r"x_k=\frac14\mathbf1+2^{-k}\left(e_1-\frac14\mathbf1\right)", font_size=40, color=ORANGE),
            MathTex(r"(x_k)_1=\frac14+\frac{3}{4\cdot2^k},\qquad (x_k)_{2,3,4}=\frac14-\frac{1}{4\cdot2^k}", font_size=34, color=TEAL_C),
            MathTex(r"x_k\longrightarrow\left(\frac14,\frac14,\frac14,\frac14\right)^T", font_size=40, color=YELLOW),
            Text("For this regular chain, the initial imbalance is halved at every step.", font_size=21, color=WHITE),
        ).arrange(DOWN, buff=0.30).to_edge(RIGHT, buff=0.28)
        limit_panel[0].scale_to_fit_width(5.10)
        limit_panel[1].scale_to_fit_width(5.30)
        limit_panel[2].scale_to_fit_width(5.10)
        limit_panel.arrange(DOWN, buff=0.30).to_edge(RIGHT, buff=0.28).shift(DOWN * 0.28)
        for line in powers:
            self.play(FadeIn(line), run_time=0.43)
        self.play(FadeIn(limit_panel))
        self.wait(3.3)

        # Card 8: solve Ax=x directly.
        heading = self._replace_heading(heading, "The limiting vector is exactly the normalized solution of Ax=x.")
        self.play(FadeOut(powers), FadeOut(limit_panel))
        derivation = VGroup(
            MathTex(r"Ax=x", font_size=48, color=YELLOW),
            MathTex(r"A=\frac12I+\frac18\mathbf1\mathbf1^T", font_size=42, color=WHITE),
            MathTex(r"\mathbf1^Tx=1\quad\Longrightarrow\quad Ax=\frac12x+\frac18\mathbf1", font_size=39, color=TEAL_C),
            MathTex(r"x=\frac12x+\frac18\mathbf1", font_size=42, color=WHITE),
            MathTex(r"x=\frac14\mathbf1=\left(\frac14,\frac14,\frac14,\frac14\right)^T", font_size=44, color=GREEN_C),
        ).arrange(DOWN, buff=0.29)
        derivation[2].scale_to_fit_width(10.6)
        note = Text("The distribution is steady even though individual transitions continue.", font_size=23, color=ORANGE).to_edge(DOWN, buff=0.70)
        for line in derivation:
            self.play(FadeIn(line), run_time=0.45)
        self.play(FadeIn(note))
        self.wait(3.2)

        # Card 9: absorbing states create multiple steady distributions.
        heading = self._replace_heading(heading, "Absorbing states are a contrasting source of steady states—and the limit need not be unique.")
        self.play(FadeOut(derivation), FadeOut(note))
        fork_positions = {1: LEFT * 3.0, 2: LEFT * 1.0, 3: RIGHT * 1.45 + UP, 4: RIGHT * 1.45 + DOWN}
        arrows = VGroup(
            Arrow(fork_positions[1], fork_positions[2], buff=0.24, color=GREY_B, stroke_width=4.5),
            Arrow(fork_positions[2], fork_positions[3], buff=0.24, color=TEAL_C, stroke_width=4.5),
            Arrow(fork_positions[2], fork_positions[4], buff=0.24, color=ORANGE, stroke_width=4.5),
        )
        dots = VGroup(*[Dot(fork_positions[s], radius=0.19, color=YELLOW) for s in (1, 2, 3, 4)])
        labels = VGroup(*[MathTex(str(s), font_size=30, color=BLACK).move_to(fork_positions[s]).set_z_index(5) for s in (1, 2, 3, 4)])
        rings = VGroup(Circle(radius=0.43, color=TEAL_C).move_to(fork_positions[3]), Circle(radius=0.43, color=ORANGE).move_to(fork_positions[4]))
        edge_labels = VGroup(
            MathTex("1", font_size=25).move_to((fork_positions[1] + fork_positions[2]) / 2 + UP * 0.28),
            MathTex(r"\frac12", font_size=25, color=TEAL_C).move_to((fork_positions[2] + fork_positions[3]) / 2 + UP * 0.28),
            MathTex(r"\frac12", font_size=25, color=ORANGE).move_to((fork_positions[2] + fork_positions[4]) / 2 + DOWN * 0.28),
        )
        fork = VGroup(arrows, dots, labels, rings, edge_labels).shift(LEFT * 2.15)
        absorbing_panel = VGroup(
            MathTex(r"Be_3=e_3,\qquad Be_4=e_4", font_size=39, color=GREEN_C),
            MathTex(r"Bx=x\quad\text{for every}\quad x=(0,0,t,1-t)^T", font_size=35, color=TEAL_C),
            self._card("FROM STATE 1", r"B^2e_1=\left(0,0,\frac12,\frac12\right)^T", "half is absorbed at each final state", ORANGE, width=5.20),
            Text("The eventual steady distribution depends on the starting probabilities.", font_size=21, color=YELLOW),
        ).arrange(DOWN, buff=0.32).to_edge(RIGHT, buff=0.27)
        absorbing_panel[1].scale_to_fit_width(5.30)
        self.play(FadeIn(fork), FadeIn(absorbing_panel[0]))
        self.play(FadeIn(absorbing_panel[1:]))
        self.wait(3.2)

        # Card 10: distinguish steady-state and convergence questions.
        heading = self._replace_heading(heading, "The equation Ax=x identifies steady states; powers of A determine whether we reach one.")
        self.play(FadeOut(fork), FadeOut(absorbing_panel))
        synthesis = VGroup(
            self._card("REGULAR", r"A^kx_0\to q", "every start reaches the same steady vector", GREEN_C, width=3.55),
            self._card("ABSORBING", r"B^kx_0\to x(x_0)", "the limit can depend on the start", ORANGE, width=3.55),
            self._card("PERIODIC", r"Ce_1=e_2,\ Ce_2=e_1", "a steady state can exist without a limit", TEAL_C, width=3.55),
        ).arrange(RIGHT, buff=0.30).move_to(UP * 0.58)
        conclusion = VGroup(
            MathTex(r"Ax=x\quad\Longleftrightarrow\quad(A-I)x=0", font_size=43, color=YELLOW),
            Text("Steady states are normalized eigenvectors with eigenvalue 1.", font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 0.88)
        preview = Text("Next: PageRank modifies a directed walk to produce one stable long-term ranking.", font_size=23, color=GREY_B).to_edge(DOWN, buff=0.70)
        self.play(FadeIn(synthesis), FadeIn(conclusion), FadeIn(preview))
        self.wait(3.2)
        self.play(*[FadeOut(mobject) for mobject in self.mobjects])
