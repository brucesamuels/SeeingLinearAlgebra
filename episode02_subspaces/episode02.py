from manim import *

from common.components import DimensionBadge, GlowArrow, SeriesTitle, equation_panel
from common.theme import (
    BLUE_VEC,
    CYAN,
    GREEN_VEC,
    GRID,
    MUTED,
    PURPLE,
    RED_VEC,
    SUCCESS,
    FAILURE,
    TEXT,
    YELLOW,
    apply_theme,
    soft_grid_2d,
)

apply_theme()


class Episode02Subspaces(ThreeDScene):
    """Episode 2: Span and Vector Subspaces -- complete continuous render."""

    def construct(self) -> None:
        self.camera.background_color = "#0B1020"
        self.opening_title()
        self.one_vector_span()
        self.origin_test()
        self.two_vector_span()
        self.dependence_collapse()
        self.three_dimensional_span()
        self.subspace_test()
        self.closing_summary()

    def opening_title(self) -> None:
        title = SeriesTitle(
            "Episode 2",
            "Span and Vector Subspaces",
            "Building spaces from linear combinations",
        )
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title, shift=UP * 0.18), run_time=1.2)
        self.wait(1.4)
        self.play(FadeOut(title))
        self.remove(title)

    def one_vector_span(self) -> None:
        plane = soft_grid_2d()
        self.add_fixed_in_frame_mobjects(plane)
        self.play(Create(plane), run_time=1.0)
        v_end = np.array([2.5, 1.25, 0])
        v = GlowArrow(v_end, color=BLUE_VEC, label=r"\mathbf v")
        self.add_fixed_in_frame_mobjects(v)
        self.play(GrowArrow(v.arrow), FadeIn(v.label))
        self.add(*v[:2])
        self.bring_to_front(v.arrow, v.label)

        tracker = ValueTracker(1.0)
        moving = always_redraw(
            lambda: Arrow(
                ORIGIN,
                tracker.get_value() * v_end,
                buff=0,
                color=YELLOW,
                stroke_width=5.5,
                max_tip_length_to_length_ratio=0.1,
            )
        )
        scalar = always_redraw(
            lambda: MathTex(
                rf"{tracker.get_value():.1f}\mathbf v",
                color=YELLOW,
                font_size=31,
            ).to_corner(UR, buff=0.35)
        )
        self.add_fixed_in_frame_mobjects(moving, scalar)
        self.play(FadeIn(moving), FadeIn(scalar))
        for value in [2.0, -1.5, 0.25, -2.2, 1.0]:
            self.play(tracker.animate.set_value(value), run_time=0.85, rate_func=smooth)
        span_line = Line(-7 * normalize(v_end), 7 * normalize(v_end), color=BLUE_VEC, stroke_width=7).set_opacity(0.45)
        span_glow = Line(-7 * normalize(v_end), 7 * normalize(v_end), color=BLUE_VEC, stroke_width=22).set_opacity(0.08)
        self.add_fixed_in_frame_mobjects(span_glow, span_line)
        self.play(Create(span_glow), Create(span_line), FadeOut(moving), FadeOut(scalar))
        formula = MathTex(r"\operatorname{span}(\mathbf v)=\{c\mathbf v:c\in\mathbb R\}", color=TEXT, font_size=39)
        formula.to_edge(DOWN)
        badge = DimensionBadge(1, "a line").to_corner(UR, buff=0.3)
        self.add_fixed_in_frame_mobjects(formula, badge)
        self.play(Write(formula), FadeIn(badge))
        self.wait(1.3)
        self.play(FadeOut(formula), FadeOut(badge), FadeOut(v), FadeOut(span_line), FadeOut(span_glow))
        self.remove(v, span_line, span_glow)
        self.plane2d = plane

    def origin_test(self) -> None:
        shifted = Line(LEFT * 7 + UP * 1.45, RIGHT * 7 + UP * 1.45, color=RED_VEC, stroke_width=7).set_opacity(0.65)
        origin = Dot(ORIGIN, color=TEXT, radius=0.065)
        zero = MathTex(r"\mathbf 0", font_size=32, color=TEXT).next_to(origin, DL, buff=0.08)
        prompt = Text("Does every line form a subspace?", font_size=34, color=TEXT).to_edge(UP)
        self.add_fixed_in_frame_mobjects(shifted, origin, zero, prompt)
        self.play(FadeIn(prompt), Create(shifted), FadeIn(origin), FadeIn(zero))
        self.wait(0.8)
        cross = Cross(shifted, stroke_color=FAILURE, stroke_width=10)
        reason = Text("No: it misses the zero vector.", font_size=31, color=FAILURE).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(cross, reason)
        self.play(Create(cross), Write(reason))
        self.wait(1.3)
        self.play(*[FadeOut(x) for x in [shifted, origin, zero, prompt, cross, reason]])
        self.remove(shifted, origin, zero, prompt, cross, reason)

    def two_vector_span(self) -> None:
        v_end = np.array([2.5, 0.8, 0])
        w_end = np.array([-0.8, 2.25, 0])
        v = GlowArrow(v_end, color=BLUE_VEC, label=r"\mathbf v")
        w = GlowArrow(w_end, color=RED_VEC, label=r"\mathbf w", label_direction=UL)
        self.add_fixed_in_frame_mobjects(v, w)
        self.play(GrowArrow(v.arrow), FadeIn(v.label), GrowArrow(w.arrow), FadeIn(w.label))
        self.add(*v[:2], *w[:2])

        a = ValueTracker(0.0)
        b = ValueTracker(0.0)
        combo = always_redraw(
            lambda: GlowArrow(
                a.get_value() * v_end + b.get_value() * w_end,
                color=YELLOW,
            )
        )
        combo_label = always_redraw(
            lambda: MathTex(
                rf"{a.get_value():.1f}\mathbf v+{b.get_value():.1f}\mathbf w",
                font_size=30,
                color=YELLOW,
            ).to_corner(UR, buff=0.28)
        )
        self.add_fixed_in_frame_mobjects(combo, combo_label)
        self.play(FadeIn(combo), FadeIn(combo_label))
        for av, bv in [(1, 1), (-1.4, 0.6), (0.5, -1.2), (1.5, -0.7), (0, 0)]:
            self.play(a.animate.set_value(av), b.animate.set_value(bv), run_time=0.75)

        # Fill the span with a lattice of combinations.
        dots = VGroup()
        for av in np.linspace(-2.3, 2.3, 13):
            for bv in np.linspace(-1.8, 1.8, 11):
                p = av * v_end + bv * w_end
                if abs(p[0]) < 7 and abs(p[1]) < 4:
                    dots.add(Dot(p, radius=0.028, color=PURPLE).set_opacity(0.75))
        self.add_fixed_in_frame_mobjects(dots)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.003), run_time=1.5)
        wash = Rectangle(width=14, height=8, fill_color=PURPLE, fill_opacity=0.09, stroke_opacity=0)
        self.add_fixed_in_frame_mobjects(wash)
        self.play(FadeIn(wash), FadeOut(combo), FadeOut(combo_label))
        formula = MathTex(r"\operatorname{span}(\mathbf v,\mathbf w)=\{a\mathbf v+b\mathbf w:a,b\in\mathbb R\}", font_size=34, color=TEXT).to_edge(DOWN)
        badge = DimensionBadge(2, "a plane").to_corner(UR, buff=0.28)
        self.add_fixed_in_frame_mobjects(formula, badge)
        self.play(Write(formula), FadeIn(badge))
        self.wait(1.3)
        self.play(FadeOut(formula), FadeOut(badge), FadeOut(dots), FadeOut(wash))
        self.remove(dots, wash)
        self.two_v = v
        self.two_w = w

    def dependence_collapse(self) -> None:
        v = self.two_v
        w = self.two_w
        title = Text("What if the directions become dependent?", font_size=31, color=TEXT).to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title))
        target_end = 1.35 * np.array([2.5, 0.8, 0])
        target_w = GlowArrow(target_end, color=RED_VEC, label=r"1.35\mathbf v", label_direction=UR)
        self.add_fixed_in_frame_mobjects(target_w)
        self.play(ReplacementTransform(w, target_w), run_time=1.4)
        collapse = Line(-7 * normalize(target_end), 7 * normalize(target_end), color=PURPLE, stroke_width=8).set_opacity(0.55)
        self.add_fixed_in_frame_mobjects(collapse)
        self.play(Create(collapse))
        message = Text("No new direction means no new dimension.", font_size=30, color=YELLOW).to_edge(DOWN)
        badge = DimensionBadge(1, "a line").to_corner(UR, buff=0.28)
        self.add_fixed_in_frame_mobjects(message, badge)
        self.play(Write(message), FadeIn(badge))
        self.wait(1.2)
        self.play(FadeOut(v), FadeOut(target_w), FadeOut(collapse), FadeOut(title), FadeOut(message), FadeOut(badge), FadeOut(self.plane2d))
        self.remove(v, target_w, collapse, title, message, badge, self.plane2d)

    def three_dimensional_span(self) -> None:
        axes = ThreeDAxes(
            x_range=(-4, 4, 1),
            y_range=(-4, 4, 1),
            z_range=(-3, 3, 1),
            x_length=7,
            y_length=7,
            z_length=5,
            axis_config={"color": GRID, "stroke_opacity": 0.65, "include_ticks": False},
        )
        self.set_camera_orientation(phi=68 * DEGREES, theta=-43 * DEGREES, zoom=0.9)
        self.play(Create(axes), run_time=1.2)
        self.begin_ambient_camera_rotation(rate=0.055)

        v = Arrow3D(ORIGIN, np.array([2.4, 0.5, 0.3]), color=BLUE_VEC, thickness=0.025)
        w = Arrow3D(ORIGIN, np.array([-0.4, 2.3, 0.5]), color=RED_VEC, thickness=0.025)
        u = Arrow3D(ORIGIN, np.array([0.2, -0.3, 2.2]), color=GREEN_VEC, thickness=0.025)
        self.play(Create(v))
        line = Line3D(-3 * normalize(v.get_end()), 3 * normalize(v.get_end()), color=BLUE_VEC, thickness=0.018).set_opacity(0.5)
        self.play(Create(line))

        self.play(Create(w))
        s, t = np.meshgrid(np.linspace(-2.2, 2.2, 12), np.linspace(-2.2, 2.2, 12))
        ve = np.array([2.4, 0.5, 0.3]); we = np.array([-0.4, 2.3, 0.5])
        plane = Surface(
            lambda a, b: a * normalize(ve) + b * normalize(we),
            u_range=(-2.5, 2.5),
            v_range=(-2.5, 2.5),
            resolution=(12, 12),
            fill_color=PURPLE,
            fill_opacity=0.22,
            stroke_color=PURPLE,
            stroke_opacity=0.18,
        )
        self.play(FadeIn(plane))

        self.play(Create(u))
        cloud = VGroup()
        for x in np.linspace(-2.0, 2.0, 6):
            for y in np.linspace(-2.0, 2.0, 6):
                for z in np.linspace(-1.6, 1.6, 5):
                    cloud.add(Dot3D(np.array([x, y, z]), radius=0.025, color=CYAN).set_opacity(0.34))
        self.play(LaggedStart(*[FadeIn(p) for p in cloud], lag_ratio=0.002), run_time=1.5)

        badge = DimensionBadge(3, r"all of R^3").to_corner(UR, buff=0.3)
        formula = MathTex(r"\operatorname{span}(\mathbf v,\mathbf w,\mathbf u)=\mathbb R^3", font_size=37, color=TEXT).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(badge, formula)
        self.play(FadeIn(badge), Write(formula))
        self.wait(1.6)
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(badge), FadeOut(formula), FadeOut(cloud), FadeOut(plane), FadeOut(v), FadeOut(w), FadeOut(u), FadeOut(line), FadeOut(axes))
        self.remove(badge, formula, cloud, plane, v, w, u, line, axes)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)

    def subspace_test(self) -> None:
        title = Text("The subspace test", font_size=45, color=TEXT, weight=BOLD).to_edge(UP)
        conditions = VGroup(
            MathTex(r"\mathbf 0\in W", font_size=38, color=CYAN),
            MathTex(r"\mathbf x,\mathbf y\in W\Rightarrow\mathbf x+\mathbf y\in W", font_size=35, color=CYAN),
            MathTex(r"c\in\mathbb R,\ \mathbf x\in W\Rightarrow c\mathbf x\in W", font_size=35, color=CYAN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        panel = equation_panel(*conditions, width=8.3).move_to(ORIGIN + UP * 0.15)
        self.add_fixed_in_frame_mobjects(title, panel)
        self.play(FadeIn(title), FadeIn(panel))
        self.wait(1.6)
        self.play(FadeOut(panel))

        examples = [
            (r"\{\mathbf 0\}", "zero subspace", True),
            (r"\{t(1,2):t\in\mathbb R\}", "line through the origin", True),
            (r"x+y+z=0", "plane through the origin", True),
            (r"x^2+y^2=1", "circle", False),
            (r"x+y+z=1", "shifted plane", False),
        ]
        cards = VGroup()
        for expr, name, valid in examples:
            card = RoundedRectangle(width=5.3, height=0.88, corner_radius=0.12, stroke_color=GRID, fill_color="#111A2D", fill_opacity=0.88)
            eq = MathTex(expr, font_size=29, color=TEXT)
            desc = Text(name, font_size=18, color=MUTED)
            icon = Text("✓" if valid else "✗", font_size=34, color=SUCCESS if valid else FAILURE, weight=BOLD)
            eq.move_to(card.get_center() + LEFT * 0.7 + UP * 0.1)
            desc.next_to(eq, DOWN, buff=0.06)
            icon.move_to(card.get_right() + LEFT * 0.35)
            cards.add(VGroup(card, eq, desc, icon))
        cards.arrange(DOWN, buff=0.15).scale(0.92)
        cards.next_to(title, DOWN, buff=0.32)
        self.add_fixed_in_frame_mobjects(cards)
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.18) for c in cards], lag_ratio=0.18), run_time=2.0)
        self.wait(1.8)
        self.play(FadeOut(cards), FadeOut(title))
        self.remove(cards, title)

    def closing_summary(self) -> None:
        q = Text("What is a subspace?", font_size=34, color=MUTED)
        answer = Text("Every linear combination you can build", font_size=44, color=TEXT, weight=BOLD)
        answer2 = Text("without ever leaving the set.", font_size=44, color=CYAN, weight=BOLD)
        final = VGroup(q, answer, answer2).arrange(DOWN, buff=0.2)
        self.add_fixed_in_frame_mobjects(final)
        self.play(FadeIn(q), Write(answer), Write(answer2), run_time=2.0)
        self.wait(1.8)
        next_ep = Text("Next: Linear Independence", font_size=23, color=MUTED).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(next_ep)
        self.play(FadeIn(next_ep))
        self.wait(1.2)
        self.play(FadeOut(final), FadeOut(next_ep))
