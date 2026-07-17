"""Reusable minimalist Manim pictograms built from geometry, not typography."""

from __future__ import annotations

from dataclasses import dataclass

from manim import (
    Arc,
    Arrow,
    Circle,
    Dot,
    Line,
    Polygon,
    Rectangle,
    RoundedRectangle,
    Square,
    Triangle,
    VGroup,
)


@dataclass(frozen=True, slots=True)
class PerspectivePictogram:
    """One pictogram and the mobjects intended for simple scene animation."""

    group: VGroup
    animated_parts: tuple

    def __post_init__(self) -> None:
        if not isinstance(self.group, VGroup):
            raise TypeError("group must be a VGroup")


class PerspectivePictogramFactory:
    """Construct pictograms entirely from Manim geometry primitives."""

    @staticmethod
    def build(label: str) -> PerspectivePictogram:
        builders = {
            "velocity": PerspectivePictogramFactory._velocity,
            "force": PerspectivePictogramFactory._force,
            "acceleration": PerspectivePictogramFactory._acceleration,
            "gravity": PerspectivePictogramFactory._gravity,
            "Netflix recommendations": PerspectivePictogramFactory._movie_recommendation,
            "Spotify suggestions": PerspectivePictogramFactory._music_recommendation,
            "Google Maps coordinates": PerspectivePictogramFactory._gps,
            "RGB color values": PerspectivePictogramFactory._rgb,
            "bridge loads": PerspectivePictogramFactory._bridge,
            "robot arms": PerspectivePictogramFactory._robot_arm,
            "aircraft motion": PerspectivePictogramFactory._aircraft,
            "satellite trajectories": PerspectivePictogramFactory._satellite,
            "vector addition": PerspectivePictogramFactory._addition,
            "scalar multiplication": PerspectivePictogramFactory._scalar,
            "closure under both operations": PerspectivePictogramFactory._closure,
            "vector spaces": PerspectivePictogramFactory._vector_space,
        }
        try:
            pictogram = builders[label]()
        except KeyError as exc:
            raise KeyError(f"unknown perspective pictogram: {label!r}") from exc

        pictogram.group.scale_to_fit_height(0.55)
        return pictogram

    @staticmethod
    def _velocity() -> PerspectivePictogram:
        ball = Circle(radius=0.14)
        arrow = Arrow([-0.1, 0, 0], [0.75, 0, 0], buff=0.02)
        group = VGroup(ball, arrow)
        return PerspectivePictogram(group, (arrow,))

    @staticmethod
    def _force() -> PerspectivePictogram:
        block = Square(side_length=0.32)
        arrow = Arrow([-0.7, 0, 0], [-0.2, 0, 0], buff=0.02)
        group = VGroup(block, arrow)
        return PerspectivePictogram(group, (arrow,))

    @staticmethod
    def _acceleration() -> PerspectivePictogram:
        dot = Dot()
        short = Arrow([0.0, 0.0, 0.0], [0.35, 0.0, 0.0], buff=0.02)
        long = Arrow([0.0, -0.22, 0.0], [0.7, -0.22, 0.0], buff=0.02)
        group = VGroup(dot, short, long)
        return PerspectivePictogram(group, (short, long))

    @staticmethod
    def _gravity() -> PerspectivePictogram:
        earth = Circle(radius=0.22)
        falling = Dot([0.0, 0.45, 0.0])
        arrow = Arrow([0.0, 0.35, 0.0], [0.0, -0.05, 0.0], buff=0.02)
        group = VGroup(earth, falling, arrow)
        return PerspectivePictogram(group, (arrow,))

    @staticmethod
    def _movie_recommendation() -> PerspectivePictogram:
        frame = RoundedRectangle(width=0.68, height=0.42, corner_radius=0.05)
        play = Triangle().scale(0.10).rotate(-1.5708)
        sprockets = VGroup(
            *[
                Square(side_length=0.05).move_to([x, y, 0])
                for x in (-0.26, 0.26)
                for y in (-0.15, 0.15)
            ]
        )
        recommendation_arrow = Arrow(
            [0.38, 0.0, 0.0],
            [0.72, 0.0, 0.0],
            buff=0.02,
        )
        group = VGroup(frame, play, sprockets, recommendation_arrow)
        return PerspectivePictogram(group, (recommendation_arrow,))

    @staticmethod
    def _music_recommendation() -> PerspectivePictogram:
        # Geometry-only eighth note: head, stem, and curved flag.
        head = Circle(radius=0.09).shift([-0.08, -0.12, 0.0])
        stem = Line([0.0, -0.08, 0.0], [0.0, 0.38, 0.0])
        flag = Arc(
            radius=0.20,
            start_angle=0.0,
            angle=1.3,
        ).shift([0.18, 0.22, 0.0])

        sound_wave_1 = Arc(
            radius=0.27,
            start_angle=-0.55,
            angle=1.10,
        ).shift([0.37, 0.05, 0.0])
        sound_wave_2 = Arc(
            radius=0.40,
            start_angle=-0.52,
            angle=1.04,
        ).shift([0.40, 0.05, 0.0])

        group = VGroup(head, stem, flag, sound_wave_1, sound_wave_2)
        return PerspectivePictogram(
            group,
            (sound_wave_1, sound_wave_2),
        )

    @staticmethod
    def _gps() -> PerspectivePictogram:
        pin_circle = Circle(radius=0.13).shift([0.0, 0.08, 0.0])
        pin_point = Triangle().scale(0.12).rotate(3.14159).shift(
            [0.0, -0.10, 0.0]
        )
        route = VGroup(
            Dot([-0.38, -0.18, 0.0], radius=0.04),
            Line([-0.34, -0.16, 0.0], [0.28, 0.10, 0.0]),
            Dot([0.32, 0.12, 0.0], radius=0.04),
        )
        group = VGroup(pin_circle, pin_point, route)
        return PerspectivePictogram(group, (route[1],))

    @staticmethod
    def _rgb() -> PerspectivePictogram:
        red = Square(side_length=0.24).shift([-0.22, 0.0, 0.0])
        green = Square(side_length=0.24)
        blue = Square(side_length=0.24).shift([0.22, 0.0, 0.0])
        group = VGroup(red, green, blue)
        return PerspectivePictogram(group, (red, green, blue))

    @staticmethod
    def _bridge() -> PerspectivePictogram:
        deck = Line([-0.65, 0.1, 0], [0.65, 0.1, 0])
        left = Line([-0.55, 0.1, 0], [-0.25, -0.3, 0])
        right = Line([0.55, 0.1, 0], [0.25, -0.3, 0])
        load = Arrow([0.0, 0.55, 0.0], [0.0, 0.15, 0.0], buff=0.02)
        group = VGroup(deck, left, right, load)
        return PerspectivePictogram(group, (load,))

    @staticmethod
    def _robot_arm() -> PerspectivePictogram:
        base = Rectangle(width=0.35, height=0.15)
        joint1 = Dot([0.0, 0.12, 0.0], radius=0.06)
        arm1 = Line([0.0, 0.12, 0.0], [0.32, 0.42, 0.0])
        joint2 = Dot([0.32, 0.42, 0.0], radius=0.06)
        arm2 = Line([0.32, 0.42, 0.0], [0.62, 0.18, 0.0])
        group = VGroup(base, joint1, arm1, joint2, arm2)
        return PerspectivePictogram(group, (arm1, arm2))

    @staticmethod
    def _aircraft() -> PerspectivePictogram:
        body = Line([-0.55, 0, 0], [0.55, 0, 0])
        wings = Line([-0.1, -0.28, 0], [0.1, 0.28, 0])
        tail = Line([-0.42, -0.15, 0], [-0.42, 0.15, 0])
        arrow = Arrow([0.25, 0, 0], [0.8, 0, 0], buff=0.02)
        group = VGroup(body, wings, tail, arrow)
        return PerspectivePictogram(group, (arrow,))

    @staticmethod
    def _satellite() -> PerspectivePictogram:
        body = Rectangle(width=0.28, height=0.22)
        panels = VGroup(
            Rectangle(width=0.35, height=0.14).shift([-0.34, 0, 0]),
            Rectangle(width=0.35, height=0.14).shift([0.34, 0, 0]),
        )
        orbit = Arc(radius=0.6, start_angle=0.2, angle=2.6)
        group = VGroup(body, panels, orbit)
        return PerspectivePictogram(group, (orbit,))

    @staticmethod
    def _addition() -> PerspectivePictogram:
        first = Arrow([-0.5, -0.2, 0], [0.0, 0.2, 0], buff=0.02)
        second = Arrow([0.0, 0.2, 0], [0.5, -0.05, 0], buff=0.02)
        resultant = Arrow(
            [-0.5, -0.2, 0],
            [0.5, -0.05, 0],
            buff=0.02,
        )
        group = VGroup(first, second, resultant)
        return PerspectivePictogram(group, (resultant,))

    @staticmethod
    def _scalar() -> PerspectivePictogram:
        short = Arrow([-0.55, -0.15, 0], [-0.05, -0.15, 0], buff=0.02)
        long = Arrow([-0.55, 0.15, 0], [0.55, 0.15, 0], buff=0.02)
        group = VGroup(short, long)
        return PerspectivePictogram(group, (long,))

    @staticmethod
    def _closure() -> PerspectivePictogram:
        boundary = Circle(radius=0.3)
        vector_a = Arrow(
            [-0.15, -0.05, 0],
            [0.08, 0.12, 0],
            buff=0.02,
        )
        vector_b = Arrow(
            [0.05, -0.08, 0],
            [0.18, 0.05, 0],
            buff=0.02,
        )
        group = VGroup(boundary, vector_a, vector_b)
        return PerspectivePictogram(group, (vector_a, vector_b))

    @staticmethod
    def _vector_space() -> PerspectivePictogram:
        axes = VGroup(
            Line([-0.45, 0, 0], [0.45, 0, 0]),
            Line([0, -0.35, 0], [0, 0.35, 0]),
        )
        arrows = VGroup(
            Arrow([0, 0, 0], [0.32, 0.22, 0], buff=0.02),
            Arrow([0, 0, 0], [-0.25, 0.18, 0], buff=0.02),
        )
        group = VGroup(axes, arrows)
        return PerspectivePictogram(group, tuple(arrows))
