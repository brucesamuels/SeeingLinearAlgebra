"""Manim presentation: Image Compression with the SVD."""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    FadeIn,
    FadeOut,
    GREEN_C,
    GREY_B,
    Group,
    ImageMobject,
    LEFT,
    MathTex,
    Matrix,
    ORANGE,
    Rectangle,
    RESAMPLING_ALGORITHMS,
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

from engine.svd_image_compression import SVDImageCompression


class SVDImageCompressionPresentation(Scene):
    CHAPTER_BANNER = "SINGULAR VALUES, RANK, AND APPROXIMATION"
    LESSON_TITLE = "Image Compression with the SVD"

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
            r"\textbf{Image Compression with the SVD}",
            font_size=34,
            color=YELLOW,
        ).next_to(banner, DOWN, buff=0.11)
        heading = self._heading(heading_text).next_to(title, DOWN, buff=0.16)
        return banner, title, heading

    def _replace_heading(self, old, text):
        new = self._heading(text).move_to(old)
        self.play(FadeOut(old), run_time=0.18)
        self.play(FadeIn(new), run_time=0.22)
        return new

    @staticmethod
    def _matrix(entries, scale=0.52, h_buff=1.05, v_buff=0.88):
        return Matrix(entries, h_buff=h_buff, v_buff=v_buff).scale(scale)

    @staticmethod
    def _pixel_array(values):
        gray = np.rint(np.clip(values, 0.0, 1.0) * 255).astype(np.uint8)
        return np.repeat(gray[:, :, np.newaxis], 3, axis=2)

    def _image_panel(self, values, label, note, color, width=3.35):
        image = ImageMobject(self._pixel_array(values))
        image.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        image.set(width=width)
        border = SurroundingRectangle(image, color=color, buff=0.04, stroke_width=2.4)
        title = Text(label, font_size=25, color=color, weight="BOLD").next_to(
            image, UP, buff=0.13
        )
        caption = Text(note, font_size=21, color=GREY_B).next_to(image, DOWN, buff=0.13)
        return Group(image, border, title, caption)

    @staticmethod
    def _card(label, formula, note, color):
        body = VGroup(
            Text(label, font_size=23, color=color, weight="BOLD"),
            MathTex(formula, font_size=36, color=WHITE),
            Text(note, font_size=21, color=GREY_B),
        ).arrange(DOWN, buff=0.17)
        border = SurroundingRectangle(body, color=color, buff=0.17, stroke_width=2.0)
        return VGroup(border, body)

    @staticmethod
    def _spectrum(values):
        colors = (TEAL_C, GREEN_C, YELLOW, ORANGE, GREY_B, GREY_B, GREY_B, GREY_B)
        bars = VGroup()
        for index, (value, color) in enumerate(zip(values[:8], colors, strict=True), start=1):
            height = max(0.10, 2.65 * value / values[0])
            bar = Rectangle(
                width=0.62,
                height=height,
                color=color,
                fill_color=color,
                fill_opacity=0.55,
            )
            label = MathTex(rf"\sigma_{{{index}}}", font_size=25, color=color)
            bars.add(VGroup(bar, label).arrange(DOWN, buff=0.12))
        bars.arrange(RIGHT, buff=0.30, aligned_edge=DOWN)
        return bars

    def construct(self):
        model = SVDImageCompression()
        if model.shape != (32, 32):
            raise RuntimeError("unexpected image dimensions")
        if model.compressed_storage(4) != 260:
            raise RuntimeError("unexpected rank-four storage")
        if not (
            model.frobenius_error(1)
            > model.frobenius_error(4)
            > model.frobenius_error(8)
        ):
            raise RuntimeError("compression error must decrease with rank")

        original = model.original()
        reconstructions = {rank: model.reconstruction(rank, clip=True) for rank in (1, 4, 8)}
        energies = {rank: model.retained_energy(rank) for rank in (1, 4, 8)}
        relative_errors = {rank: model.relative_frobenius_error(rank) for rank in (1, 4, 8)}

        banner, title, heading = self._chrome(
            "A grayscale image is a matrix whose entries record pixel brightness."
        )
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        original_panel = self._image_panel(original, "32 x 32 IMAGE", "one number per pixel", TEAL_C)
        symbolic = self._matrix(
            [
                [r"a_{1,1}", r"\cdots", r"a_{1,32}"],
                [r"\vdots", r"\ddots", r"\vdots"],
                [r"a_{32,1}", r"\cdots", r"a_{32,32}"],
            ],
            scale=0.44,
            h_buff=1.32,
            v_buff=1.03,
        )
        matrix_explanation = VGroup(
            VGroup(MathTex(r"A=", font_size=40), symbolic).arrange(RIGHT, buff=0.12),
            MathTex(r"A\in\mathbb R^{32\times32}", font_size=38, color=GREEN_C),
            MathTex(r"0\le a_{ij}\le1", font_size=37, color=WHITE),
            Text("1024 brightness values", font_size=28, color=YELLOW, weight="BOLD"),
        ).arrange(DOWN, buff=0.24)
        opening = Group(original_panel, matrix_explanation).arrange(RIGHT, buff=0.85).move_to(
            DOWN * 0.02
        )
        self.play(FadeIn(original_panel))
        self.play(FadeIn(matrix_explanation))
        self.wait(2.3)

        heading = self._replace_heading(
            heading, "The SVD decomposes the image into ordered rank-one patterns."
        )
        self.play(FadeOut(opening))
        layers = VGroup(
            MathTex(
                r"A=\sum_{i=1}^{32}\sigma_i u_i v_i^T",
                font_size=51,
                color=YELLOW,
            ),
            VGroup(
                self._card("PATTERN", r"u_i v_i^T", "one rank-one image layer", TEAL_C),
                self._card("STRENGTH", r"\sigma_i", "importance of that layer", GREEN_C),
            ).arrange(RIGHT, buff=0.72),
            Text(
                "Large singular values carry broad structure; small ones carry finer detail.",
                font_size=28,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.43).move_to(DOWN * 0.03)
        self.play(FadeIn(layers[0]))
        self.play(FadeIn(layers[1]))
        self.play(FadeIn(layers[2]))
        self.wait(2.4)

        heading = self._replace_heading(
            heading, "Most of this image's energy is concentrated in its first few singular values."
        )
        self.play(FadeOut(layers))
        spectrum = self._spectrum(model.singular_values()).move_to(DOWN * 0.02)
        spectrum_formula = MathTex(
            r"\sigma_1\ge\sigma_2\ge\cdots\ge\sigma_{32}\ge0",
            font_size=40,
            color=WHITE,
        ).to_edge(DOWN, buff=0.86)
        self.play(FadeIn(spectrum))
        self.play(FadeIn(spectrum_formula))
        self.wait(2.4)

        heading = self._replace_heading(
            heading, "Rank one keeps only the strongest image pattern."
        )
        self.play(FadeOut(spectrum), FadeOut(spectrum_formula))
        rank_one_panel = self._image_panel(
            reconstructions[1],
            "RANK 1",
            f"retained energy {100 * energies[1]:.1f}%",
            ORANGE,
            width=4.25,
        ).move_to(DOWN * 0.03)
        rank_one_formula = MathTex(
            r"A_1=\sigma_1u_1v_1^T",
            font_size=42,
            color=YELLOW,
        ).to_edge(RIGHT, buff=0.80).shift(DOWN * 0.02)
        rank_one_panel.shift(LEFT * 2.15)
        rank_one_note = Text(
            "Broad brightness and the dominant silhouette survive.",
            font_size=27,
            color=WHITE,
        ).to_edge(DOWN, buff=0.84)
        self.play(FadeIn(rank_one_panel))
        self.play(FadeIn(rank_one_formula), FadeIn(rank_one_note))
        self.wait(2.4)

        heading = self._replace_heading(
            heading, "Four singular layers restore the main shapes while using far fewer values."
        )
        self.play(FadeOut(rank_one_panel), FadeOut(rank_one_formula), FadeOut(rank_one_note))
        rank_four_panel = self._image_panel(
            reconstructions[4],
            "RANK 4",
            f"retained energy {100 * energies[4]:.1f}%",
            GREEN_C,
            width=4.25,
        ).move_to(DOWN * 0.03)
        rank_four_panel.shift(LEFT * 2.15)
        rank_four_formula = VGroup(
            MathTex(r"A_4=\sum_{i=1}^{4}\sigma_i u_i v_i^T", font_size=41, color=YELLOW),
            Text("260 stored values", font_size=29, color=GREEN_C, weight="BOLD"),
            Text("instead of 1024", font_size=27, color=WHITE),
        ).arrange(DOWN, buff=0.30).to_edge(RIGHT, buff=0.52).shift(DOWN * 0.02)
        self.play(FadeIn(rank_four_panel))
        self.play(FadeIn(rank_four_formula))
        self.wait(2.4)

        heading = self._replace_heading(
            heading, "Eight layers recover finer boundaries and tonal variation."
        )
        self.play(FadeOut(rank_four_panel), FadeOut(rank_four_formula))
        rank_eight_panel = self._image_panel(
            reconstructions[8],
            "RANK 8",
            f"retained energy {100 * energies[8]:.1f}%",
            TEAL_C,
            width=4.25,
        ).move_to(DOWN * 0.03)
        rank_eight_panel.shift(LEFT * 2.15)
        rank_eight_formula = VGroup(
            MathTex(r"A_8=\sum_{i=1}^{8}\sigma_i u_i v_i^T", font_size=41, color=YELLOW),
            Text(
                f"relative error {100 * relative_errors[8]:.1f}%",
                font_size=29,
                color=TEAL_C,
                weight="BOLD",
            ),
            Text("closer to the original", font_size=27, color=WHITE),
        ).arrange(DOWN, buff=0.30).to_edge(RIGHT, buff=0.52).shift(DOWN * 0.02)
        self.play(FadeIn(rank_eight_panel))
        self.play(FadeIn(rank_eight_formula))
        self.wait(2.4)

        heading = self._replace_heading(
            heading, "Discarded singular values determine both error and retained energy."
        )
        self.play(FadeOut(rank_eight_panel), FadeOut(rank_eight_formula))
        metrics = VGroup(
            MathTex(
                r"\|A-A_k\|_F^2=\sum_{i>k}\sigma_i^2",
                font_size=46,
                color=ORANGE,
            ),
            MathTex(
                r"E_k=\frac{\sum_{i=1}^{k}\sigma_i^2}{\sum_i\sigma_i^2}",
                font_size=47,
                color=GREEN_C,
            ),
            VGroup(
                self._card(
                    "RANK 1",
                    rf"E_1={100 * energies[1]:.1f}\%",
                    rf"relative error {100 * relative_errors[1]:.1f}%",
                    ORANGE,
                ),
                self._card(
                    "RANK 4",
                    rf"E_4={100 * energies[4]:.1f}\%",
                    rf"relative error {100 * relative_errors[4]:.1f}%",
                    GREEN_C,
                ),
                self._card(
                    "RANK 8",
                    rf"E_8={100 * energies[8]:.1f}\%",
                    rf"relative error {100 * relative_errors[8]:.1f}%",
                    TEAL_C,
                ),
            ).arrange(RIGHT, buff=0.34),
        ).arrange(DOWN, buff=0.34).move_to(DOWN * 0.02)
        self.play(FadeIn(metrics[0]))
        self.play(FadeIn(metrics[1]))
        self.play(FadeIn(metrics[2]))
        self.wait(2.5)

        heading = self._replace_heading(
            heading, "Compression replaces all pixels with a small set of singular vectors and values."
        )
        self.play(FadeOut(metrics))
        storage = VGroup(
            self._card("ORIGINAL", r"mn=32\cdot32=1024", "one value per pixel", ORANGE),
            MathTex(r"\Longrightarrow", font_size=46, color=YELLOW),
            self._card(
                "RANK 4 SVD",
                r"k(m+n+1)=4(32+32+1)=260",
                "four left vectors, values, and right vectors",
                GREEN_C,
            ),
        ).arrange(RIGHT, buff=0.42).move_to(DOWN * 0.02)
        storage_note = VGroup(
            Text(
                f"{100 * model.storage_fraction(4):.1f}% of the original storage",
                font_size=28,
                color=TEAL_C,
                weight="BOLD",
            ),
            Text(
                f"compression ratio {model.compression_ratio(4):.2f} to 1",
                font_size=28,
                color=WHITE,
            ),
        ).arrange(RIGHT, buff=0.70).to_edge(DOWN, buff=0.84)
        self.play(FadeIn(storage[0]))
        self.play(FadeIn(storage[1]), FadeIn(storage[2]))
        self.play(FadeIn(storage_note))
        self.wait(2.5)

        heading = self._replace_heading(
            heading, "Increasing rank trades storage for progressively greater fidelity."
        )
        self.play(FadeOut(storage), FadeOut(storage_note))
        comparison = Group(
            self._image_panel(original, "ORIGINAL", "1024 values", YELLOW, width=2.35),
            self._image_panel(
                reconstructions[1], "RANK 1", f"energy {100 * energies[1]:.1f}%", ORANGE, width=2.35
            ),
            self._image_panel(
                reconstructions[4], "RANK 4", f"energy {100 * energies[4]:.1f}%", GREEN_C, width=2.35
            ),
            self._image_panel(
                reconstructions[8], "RANK 8", f"energy {100 * energies[8]:.1f}%", TEAL_C, width=2.35
            ),
        ).arrange(RIGHT, buff=0.34).move_to(DOWN * 0.03)
        self.play(FadeIn(comparison[0]))
        self.play(FadeIn(comparison[1]))
        self.play(FadeIn(comparison[2]))
        self.play(FadeIn(comparison[3]))
        self.wait(2.6)

        heading = self._replace_heading(
            heading, "Choose the truncation rank to balance simplicity and visual fidelity."
        )
        self.play(FadeOut(comparison))
        conclusion = VGroup(
            MathTex(
                r"\boxed{A_k=\sum_{i=1}^{k}\sigma_i u_i v_i^T}",
                font_size=53,
                color=YELLOW,
            ),
            VGroup(
                self._card("SMALL k", r"\text{fewer stored values}", "stronger compression", ORANGE),
                self._card("LARGE k", r"\text{smaller approximation error}", "greater fidelity", GREEN_C),
            ).arrange(RIGHT, buff=0.62),
            Text(
                "Keep the strongest image patterns; discard detail according to the available budget.",
                font_size=27,
                color=WHITE,
            ),
        ).arrange(DOWN, buff=0.40).move_to(DOWN * 0.04)
        self.play(FadeIn(conclusion[0]))
        self.play(FadeIn(conclusion[1]))
        self.play(FadeIn(conclusion[2]))
        self.wait(3.0)
