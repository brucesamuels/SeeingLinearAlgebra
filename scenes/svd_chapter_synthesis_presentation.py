"""Manim presentation: Singular Values, Rank, and Approximation synthesis."""

from __future__ import annotations

from manim import (
    BLUE_C,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN_C,
    GREY_B,
    LEFT,
    MathTex,
    ORANGE,
    Rectangle,
    RIGHT,
    Scene,
    SurroundingRectangle,
    TEAL_C,
    Tex,
    Text,
    UP,
    VGroup,
    WHITE,
    YELLOW,
)

from engine.svd_chapter_synthesis import SVDChapterSynthesis


class SVDChapterSynthesisPresentation(Scene):
    CHAPTER_BANNER = "SINGULAR VALUES, RANK, AND APPROXIMATION"
    LESSON_TITLE = "Singular Values, Rank, and Approximation: The Big Picture"

    def _heading(self, text):
        item = Text(text, font_size=27, color=WHITE)
        if item.width > 11.4:
            item.scale_to_fit_width(11.4)
        return item

    def _chrome(self, heading_text):
        banner = Tex(
            r"\textbf{SINGULAR VALUES, RANK, AND APPROXIMATION}",
            font_size=23,
            color=GREY_B,
        ).to_edge(UP, buff=0.16)
        title = Tex(
            r"\textbf{Singular Values, Rank, and Approximation: The Big Picture}",
            font_size=31,
            color=YELLOW,
        ).next_to(banner, DOWN, buff=0.11)
        if title.width > 11.7:
            title.scale_to_fit_width(11.7)
        heading = self._heading(heading_text).next_to(title, DOWN, buff=0.16)
        return banner, title, heading

    def _replace_heading(self, old, text):
        new = self._heading(text).move_to(old)
        self.play(FadeOut(old), run_time=0.28)
        self.play(FadeIn(new), run_time=0.32)
        return new

    @staticmethod
    def _card(label, formula, note, color, formula_size=35, width=None):
        body = VGroup(
            Text(label, font_size=22, color=color, weight="BOLD"),
            MathTex(formula, font_size=formula_size, color=WHITE),
            Text(note, font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.16)
        if width is not None and body.width > width - 0.34:
            body.scale_to_fit_width(width - 0.34)
        border = SurroundingRectangle(body, color=color, buff=0.17, stroke_width=2.0)
        return VGroup(border, body)

    @staticmethod
    def _text_card(label, lines, color, width=4.9):
        body = VGroup(
            Text(label, font_size=23, color=color, weight="BOLD"),
            *[Text(line, font_size=21, color=WHITE if i == 0 else GREY_B) for i, line in enumerate(lines)],
        ).arrange(DOWN, buff=0.17)
        if body.width > width - 0.34:
            body.scale_to_fit_width(width - 0.34)
        border = SurroundingRectangle(body, color=color, buff=0.18, stroke_width=2.0)
        return VGroup(border, body)

    def construct(self):
        model = SVDChapterSynthesis()
        if len(model.topics()) != 8 or len(model.recognition_rules()) != 4:
            raise RuntimeError("unexpected chapter synthesis structure")
        if model.rank() != 2 or model.condition_number() != 6:
            raise RuntimeError("unexpected synthesis numerical anchor")

        banner, title, heading = self._chrome(
            "The SVD separates every matrix into input directions, stretches, and output directions."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        input_box = self._card("INPUT DIRECTIONS", r"V^T", "choose orthonormal coordinates", TEAL_C, 43)
        stretch_box = self._card("STRETCHES", r"\Sigma", "scale or collapse each direction", ORANGE, 48)
        output_box = self._card("OUTPUT DIRECTIONS", r"U", "place orthonormal images", GREEN_C, 48)
        flow = VGroup(
            input_box,
            MathTex(r"\longrightarrow", font_size=36, color=GREY_B),
            stretch_box,
            MathTex(r"\longrightarrow", font_size=36, color=GREY_B),
            output_box,
        ).arrange(RIGHT, buff=0.24)
        opening = VGroup(
            MathTex(r"A=U\Sigma V^T", font_size=55, color=YELLOW),
            flow,
            Text(
                "The singular values reveal how strongly A acts in its preferred directions.",
                font_size=27,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.46).move_to(DOWN * 0.03)
        self.play(FadeIn(opening[0]))
        self.play(FadeIn(flow))
        self.play(FadeIn(opening[2]))
        self.wait(4.0)

        heading = self._replace_heading(
            heading, "The singular-value spectrum summarizes the matrix's directional behavior."
        )
        self.play(FadeOut(opening))
        bars = VGroup()
        for value, label, color in ((3.0, r"\sigma_1=3", GREEN_C), (0.5, r"\sigma_2=\frac12", ORANGE)):
            bar = Rectangle(
                width=0.82,
                height=0.72 * value,
                color=color,
                fill_color=color,
                fill_opacity=0.55,
            )
            bars.add(VGroup(bar, MathTex(label, font_size=28, color=color)).arrange(DOWN, buff=0.13))
        bars.arrange(RIGHT, buff=0.55, aligned_edge=DOWN)
        spectrum_meanings = VGroup(
            self._text_card("ZERO", ("direction is lost", "rank decreases"), ORANGE, 3.2),
            self._text_card("SMALL", ("inverse is sensitive", "errors are amplified"), BLUE_C, 3.2),
            self._text_card("LARGE", ("effect is dominant", "structure is retained first"), GREEN_C, 3.2),
        ).arrange(RIGHT, buff=0.35)
        spectrum = VGroup(
            VGroup(bars, MathTex(r"\sigma_1\ge\sigma_2\ge\cdots\ge0", font_size=39, color=WHITE)).arrange(DOWN, buff=0.30),
            spectrum_meanings,
        ).arrange(DOWN, buff=0.48).move_to(DOWN * 0.02)
        self.play(FadeIn(spectrum[0]))
        self.play(FadeIn(spectrum[1]))
        self.wait(4.1)

        heading = self._replace_heading(
            heading, "Positive and zero singular values organize all four fundamental subspaces."
        )
        self.play(FadeOut(spectrum))
        domain = VGroup(
            self._card("ROW SPACE", r"\operatorname{span}(v_1,\ldots,v_r)", "input directions that survive", GREEN_C, 31, 4.8),
            self._card("NULL SPACE", r"\operatorname{span}(v_{r+1},\ldots)", "input directions sent to zero", ORANGE, 31, 4.8),
        ).arrange(DOWN, buff=0.34)
        codomain = VGroup(
            self._card("COLUMN SPACE", r"\operatorname{span}(u_1,\ldots,u_r)", "reachable outputs: the image", TEAL_C, 31, 4.8),
            self._card("LEFT NULL SPACE", r"\operatorname{span}(u_{r+1},\ldots)", "outputs perpendicular to the image", BLUE_C, 31, 4.8),
        ).arrange(DOWN, buff=0.34)
        subspaces = VGroup(
            MathTex(r"r=\#\{i:\sigma_i>0\}=\operatorname{rank}(A)", font_size=43, color=YELLOW),
            VGroup(domain, codomain).arrange(RIGHT, buff=0.54),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.04)
        self.play(FadeIn(subspaces[0]))
        self.play(FadeIn(domain), FadeIn(codomain))
        self.wait(4.2)

        heading = self._replace_heading(
            heading, "The pseudoinverse finds the closest image and its shortest pre-image."
        )
        self.play(FadeOut(subspaces))
        target = self._card("TARGET", r"\mathbf b", "may lie outside the image", ORANGE, 39, 3.15)
        reachable = self._card(
            "CLOSEST IMAGE",
            r"AA^+\mathbf b\in\operatorname{Col}(A)",
            "remove the unreachable part",
            TEAL_C,
            31,
            3.65,
        )
        preimage = self._card(
            "SHORTEST PRE-IMAGE",
            r"\mathbf x^+=A^+\mathbf b",
            "discard null-space additions",
            GREEN_C,
            33,
            3.55,
        )
        pseudo_flow = VGroup(
            target,
            MathTex(r"\longrightarrow", font_size=34, color=GREY_B),
            reachable,
            MathTex(r"\longrightarrow", font_size=34, color=GREY_B),
            preimage,
        ).arrange(RIGHT, buff=0.19)
        pseudoinverse = VGroup(
            MathTex(r"A^+=V\Sigma^+U^T", font_size=51, color=YELLOW),
            pseudo_flow,
            Text(
                "Reverse positive singular values; leave every zero singular value at zero.",
                font_size=27,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.44).move_to(DOWN * 0.03)
        self.play(FadeIn(pseudoinverse[0]))
        self.play(FadeIn(pseudo_flow))
        self.play(FadeIn(pseudoinverse[2]))
        self.wait(4.2)

        heading = self._replace_heading(
            heading, "The smallest positive singular value controls the worst inverse amplification."
        )
        self.play(FadeOut(pseudoinverse))
        conditioning = VGroup(
            MathTex(
                r"\sigma_1=3,\qquad\sigma_2=\frac12,\qquad\kappa_2(A)=\frac{\sigma_1}{\sigma_2}=6",
                font_size=44,
                color=YELLOW,
            ),
            VGroup(
                self._card("FORWARD MAP", r"\frac12", "compresses the weak direction", ORANGE, 43, 4.7),
                self._card("INVERSE MAP", r"2", "amplifies that direction", BLUE_C, 43, 4.7),
            ).arrange(RIGHT, buff=0.58),
            Text(
                "Invertible does not necessarily mean numerically stable.",
                font_size=29,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.43).move_to(DOWN * 0.03)
        self.play(FadeIn(conditioning[0]))
        self.play(FadeIn(conditioning[1]))
        self.play(FadeIn(conditioning[2]))
        self.wait(4.1)

        heading = self._replace_heading(
            heading, "Truncated SVD keeps the strongest layers and gives the best rank-k approximation."
        )
        self.play(FadeOut(conditioning))
        approximation = VGroup(
            MathTex(r"A_k=\sum_{i=1}^{k}\sigma_i u_i v_i^T", font_size=49, color=YELLOW),
            VGroup(
                self._card("KEEP", r"\sigma_1,\ldots,\sigma_k", "dominant structure", GREEN_C, 36, 4.7),
                self._card("DISCARD", r"\sigma_{k+1},\ldots", "controlled residual", ORANGE, 36, 4.7),
            ).arrange(RIGHT, buff=0.58),
            MathTex(r"\|A-A_k\|_F^2=\sum_{i>k}\sigma_i^2", font_size=43, color=WHITE),
            Text("No other rank-k matrix has smaller approximation error.", font_size=27, color=TEAL_C),
        ).arrange(DOWN, buff=0.34).move_to(DOWN * 0.02)
        self.play(FadeIn(approximation[0]))
        self.play(FadeIn(approximation[1]))
        self.play(FadeIn(approximation[2]))
        self.play(FadeIn(approximation[3]))
        self.wait(4.2)

        heading = self._replace_heading(
            heading, "Image compression and PCA use the same low-rank idea in different settings."
        )
        self.play(FadeOut(approximation))
        applications = VGroup(
            self._card(
                "IMAGE COMPRESSION",
                r"A_k=U_k\Sigma_kV_k^T",
                "keep dominant pixel patterns",
                TEAL_C,
                38,
                5.0,
            ),
            self._card(
                "PCA",
                r"X_c\approx U_k\Sigma_kV_k^T",
                "keep dominant variation directions",
                GREEN_C,
                36,
                5.0,
            ),
        ).arrange(RIGHT, buff=0.62)
        application_notes = VGroup(
            Text("pixels become a matrix", font_size=25, color=WHITE),
            MathTex(r"\Longleftrightarrow", font_size=42, color=YELLOW),
            Text("observations become a centered matrix", font_size=25, color=WHITE),
        ).arrange(RIGHT, buff=0.48)
        app_group = VGroup(
            applications,
            application_notes,
            Text(
                "Large singular values identify the structure worth preserving.",
                font_size=29,
                color=YELLOW,
            ),
        ).arrange(DOWN, buff=0.48).move_to(DOWN * 0.03)
        self.play(FadeIn(applications))
        self.play(FadeIn(application_notes))
        self.play(FadeIn(app_group[2]))
        self.wait(4.2)

        heading = self._replace_heading(
            heading, "Choose what to do with each singular value according to the problem."
        )
        self.play(FadeOut(app_group))
        recognition = VGroup(
            VGroup(
                self._text_card("INVERSE", ("all singular values positive", "reverse every stretch"), GREEN_C, 4.7),
                self._text_card("PSEUDOINVERSE", ("zero singular values allowed", "reverse positives; keep zeros"), TEAL_C, 4.7),
            ).arrange(RIGHT, buff=0.52),
            VGroup(
                self._text_card("TRUNCATED SVD", ("a simpler matrix is wanted", "keep the largest k layers"), ORANGE, 4.7),
                self._text_card("PCA", ("centered data need fewer coordinates", "keep the strongest directions"), BLUE_C, 4.7),
            ).arrange(RIGHT, buff=0.52),
        ).arrange(DOWN, buff=0.42).move_to(DOWN * 0.02)
        self.play(FadeIn(recognition[0]))
        self.play(FadeIn(recognition[1]))
        self.wait(4.3)

        heading = self._replace_heading(
            heading, "The singular values reveal what a matrix preserves, loses, amplifies, and approximates."
        )
        self.play(FadeOut(recognition))
        four_questions = VGroup(
            Text("PRESERVES", font_size=26, color=GREEN_C, weight="BOLD"),
            Text("LOSES", font_size=26, color=ORANGE, weight="BOLD"),
            Text("AMPLIFIES", font_size=26, color=BLUE_C, weight="BOLD"),
            Text("APPROXIMATES", font_size=26, color=TEAL_C, weight="BOLD"),
        ).arrange(RIGHT, buff=0.72)
        conclusion = VGroup(
            MathTex(r"\boxed{A=U\Sigma V^T}", font_size=58, color=YELLOW),
            four_questions,
            Text(
                "Read the spectrum, then choose the representation that matches the question.",
                font_size=28,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.55).move_to(DOWN * 0.02)
        self.play(FadeIn(conclusion[0]))
        self.play(FadeIn(conclusion[1]))
        self.play(FadeIn(conclusion[2]))
        self.wait(4.6)
