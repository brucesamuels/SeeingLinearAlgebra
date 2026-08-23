"""Manim presentation: From Standard Coordinates to Basis Coordinates."""
from manim import (
    BLUE_C, GREEN_C, GREY_B, ORANGE, WHITE, YELLOW,
    DOWN, LEFT, RIGHT, UP,
    Arrow, Create, FadeIn, FadeOut, Line, MathTex, NumberPlane,
    ReplacementTransform, Scene, Text, Transform, VGroup, smooth,
)


class StandardToBasisCoordinatesPresentation(Scene):
    CHAPTER_BANNER = "CHANGE OF BASIS"
    LESSON_TITLE = "From Standard Coordinates to Basis Coordinates"

    def _heading(self, text):
        item = Text(text, font_size=27, color=WHITE)
        if item.width > 11.6:
            item.scale_to_fit_width(11.6)
        return item

    def _chrome(self, heading_text):
        banner = Text(self.CHAPTER_BANNER, font_size=22, color=GREY_B, weight="BOLD").to_edge(UP, buff=0.16)
        title = Text(self.LESSON_TITLE, font_size=32, color=YELLOW, weight="BOLD").next_to(banner, DOWN, buff=0.12)
        title.scale_to_fit_width(min(title.width, 11.5)) if title.width > 11.5 else title
        heading = self._heading(heading_text).next_to(title, DOWN, buff=0.17)
        return banner, title, heading

    def _replace_heading(self, old, text):
        new = self._heading(text).move_to(old)
        self.play(ReplacementTransform(old, new), run_time=0.6)
        return new

    @staticmethod
    def _fit_full(group):
        if group.width > 11.2:
            group.scale_to_fit_width(11.2)
        if group.height > 4.65:
            group.scale_to_fit_height(4.65)
        group.move_to(DOWN * 0.42)
        return group

    @staticmethod
    def _standard_grid(plane):
        """Explicit grid lines, ordered to match `_basis_grid`."""
        lines = VGroup()
        for x in range(-2, 7):
            is_axis = x == 0
            lines.add(Line(
                plane.c2p(x, -3), plane.c2p(x, 5),
                color=WHITE if is_axis else GREY_B,
                stroke_width=3.2 if is_axis else 1.8,
                stroke_opacity=1.0 if is_axis else 0.88,
            ))
        for y in range(-3, 6):
            is_axis = y == 0
            lines.add(Line(
                plane.c2p(-2, y), plane.c2p(6, y),
                color=WHITE if is_axis else GREY_B,
                stroke_width=3.2 if is_axis else 1.8,
                stroke_opacity=1.0 if is_axis else 0.88,
            ))
        return lines

    @staticmethod
    def _basis_grid(plane):
        """Target endpoints obtained from (x,y) -> (x+y,x-y)."""
        lines = VGroup()
        for x in range(-2, 7):
            is_axis = x == 0
            lines.add(Line(
                plane.c2p(x - 3, x + 3), plane.c2p(x + 5, x - 5),
                color=BLUE_C,
                stroke_width=3.2 if is_axis else 1.8,
                stroke_opacity=1.0 if is_axis else 0.72,
            ))
        for y in range(-3, 6):
            is_axis = y == 0
            lines.add(Line(
                plane.c2p(-2 + y, -2 - y), plane.c2p(6 + y, 6 - y),
                color=GREEN_C,
                stroke_width=3.2 if is_axis else 1.8,
                stroke_opacity=1.0 if is_axis else 0.72,
            ))
        return lines

    def construct(self):
        banner, title, heading = self._chrome("What coordinate translation are we trying to perform?")
        self.play(FadeIn(banner), FadeIn(title), FadeIn(heading))

        question = VGroup(
            Text("How do we translate a vector's standard coordinates", font_size=35, color=WHITE),
            Text("into coordinates in a nonstandard basis?", font_size=35, color=WHITE),
        ).arrange(DOWN, buff=0.16)
        unknown_map = MathTex(r"[\mathbf v]_{\mathcal E}\xrightarrow{\qquad ?\qquad}[\mathbf v]_{\mathcal B}", font_size=70, color=YELLOW)
        invariant = Text("The geometric vector must remain unchanged.", font_size=32, color=ORANGE)
        opening = self._fit_full(VGroup(question, unknown_map, invariant).arrange(DOWN, buff=0.62))
        self.play(FadeIn(question)); self.play(FadeIn(unknown_map)); self.play(FadeIn(invariant)); self.wait(1.6)

        heading = self._replace_heading(heading, "Begin with one fixed vector on the standard coordinate grid.")
        self.play(FadeOut(opening))
        plane = NumberPlane(
            x_range=[-2, 6, 1], y_range=[-3, 5, 1], x_length=7.0, y_length=6.1,
            background_line_style={"stroke_color": GREY_B, "stroke_width": 1.8, "stroke_opacity": 0.88},
            axis_config={"stroke_color": WHITE, "stroke_width": 3.0},
        ).shift(DOWN * 0.38)
        standard_grid = self._standard_grid(plane)
        vector = Arrow(plane.c2p(0, 0), plane.c2p(4, 2), buff=0, color=ORANGE, stroke_width=9)
        standard_label = MathTex(r"[\mathbf v]_{\mathcal E}=(4,2)", font_size=39, color=ORANGE).next_to(vector.get_end(), UP + RIGHT, buff=0.10)
        b1 = Arrow(plane.c2p(0, 0), plane.c2p(1, 1), buff=0, color=GREEN_C, stroke_width=7)
        b2 = Arrow(plane.c2p(0, 0), plane.c2p(1, -1), buff=0, color=BLUE_C, stroke_width=7)
        basis_label = MathTex(r"\mathcal B=\{\mathbf b_1=(1,1),\ \mathbf b_2=(1,-1)\}", font_size=36, color=WHITE).to_edge(DOWN, buff=0.18)
        self.play(Create(standard_grid), FadeIn(vector), FadeIn(standard_label)); self.play(FadeIn(b1), FadeIn(b2), FadeIn(basis_label)); self.wait(1.5)

        heading = self._replace_heading(heading, "Change the coordinate grid and description—not the vector.")
        # Each source line has a corresponding target line with explicitly
        # transformed endpoints.  This guarantees visible line-by-line motion.
        basis_grid = self._basis_grid(plane)
        basis_coordinate_label = MathTex(r"[\mathbf v]_{\mathcal B}=(3,1)", font_size=42, color=YELLOW).move_to(standard_label)
        self.play(
            Transform(standard_grid, basis_grid, rate_func=smooth),
            ReplacementTransform(standard_label, basis_coordinate_label),
            run_time=4.0,
        )
        self.wait(1.8)

        heading = self._replace_heading(heading, "Undo the basis matrix to recover the coordinate instructions.")
        self.play(FadeOut(standard_grid), FadeOut(vector), FadeOut(b1), FadeOut(b2), FadeOut(basis_label), FadeOut(basis_coordinate_label))
        start = MathTex(r"[\mathbf v]_{\mathcal E}=P_{\mathcal B}[\mathbf v]_{\mathcal B}", font_size=58, color=WHITE)
        inverse_step = MathTex(r"P_{\mathcal B}^{-1}[\mathbf v]_{\mathcal E}=P_{\mathcal B}^{-1}P_{\mathcal B}[\mathbf v]_{\mathcal B}", font_size=52, color=WHITE)
        formula = MathTex(r"\boxed{[\mathbf v]_{\mathcal B}=P_{\mathcal B}^{-1}[\mathbf v]_{\mathcal E}}", font_size=66, color=YELLOW)
        derivation = self._fit_full(VGroup(start, inverse_step, formula).arrange(DOWN, buff=0.55))
        self.play(FadeIn(start)); self.play(FadeIn(inverse_step)); self.play(FadeIn(formula)); self.wait(1.7)

        heading = self._replace_heading(heading, "First compute the inverse of the basis matrix.")
        self.play(FadeOut(derivation))
        p_matrix = MathTex(r"P_{\mathcal B}=\begin{bmatrix}1&1\\1&-1\end{bmatrix},\qquad \det(P_{\mathcal B})=-2", font_size=53, color=WHITE)
        inverse = MathTex(r"P_{\mathcal B}^{-1}=\frac{1}{-2}\begin{bmatrix}-1&-1\\-1&1\end{bmatrix}=\frac12\begin{bmatrix}1&1\\1&-1\end{bmatrix}", font_size=55, color=YELLOW)
        inverse_card = self._fit_full(VGroup(p_matrix, inverse).arrange(DOWN, buff=0.72))
        self.play(FadeIn(p_matrix)); self.play(FadeIn(inverse)); self.wait(1.6)

        heading = self._replace_heading(heading, "Now apply the inverse to the standard coordinate column.")
        self.play(FadeOut(inverse_card))
        line1 = MathTex(r"[\mathbf v]_{\mathcal B}=\frac12\begin{bmatrix}1&1\\1&-1\end{bmatrix}\begin{bmatrix}4\\2\end{bmatrix}", font_size=55, color=WHITE)
        line2 = MathTex(r"=\frac12\begin{bmatrix}1(4)+1(2)\\1(4)+(-1)(2)\end{bmatrix}=\frac12\begin{bmatrix}6\\2\end{bmatrix}", font_size=52, color=WHITE)
        line3 = MathTex(r"\boxed{[\mathbf v]_{\mathcal B}=\begin{bmatrix}3\\1\end{bmatrix}}", font_size=65, color=YELLOW)
        computation = self._fit_full(VGroup(line1, line2, line3).arrange(DOWN, buff=0.42))
        self.play(FadeIn(line1)); self.play(FadeIn(line2)); self.play(FadeIn(line3)); self.wait(1.8)

        heading = self._replace_heading(heading, "The inverse matrix changes the description, not the geometric vector.")
        self.play(FadeOut(computation))
        direction = MathTex(r"[\mathbf v]_{\mathcal E}\xrightarrow{\quad P_{\mathcal B}^{-1}\quad}[\mathbf v]_{\mathcal B}", font_size=65, color=WHITE)
        final_formula = MathTex(r"\boxed{[\mathbf v]_{\mathcal B}=P_{\mathcal B}^{-1}[\mathbf v]_{\mathcal E}}", font_size=65, color=YELLOW)
        descriptions = MathTex(r"(4,2)_{\mathcal E}\quad\longleftrightarrow\quad(3,1)_{\mathcal B}", font_size=55, color=ORANGE)
        final = self._fit_full(VGroup(direction, final_formula, descriptions).arrange(DOWN, buff=0.52))
        self.play(FadeIn(direction)); self.play(FadeIn(final_formula)); self.play(FadeIn(descriptions)); self.wait(2.0)
