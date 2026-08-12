"""CP148 title card for Chapter 5: Determinants."""
from manim import FadeIn, GREY_B, Scene, Text, VGroup, WHITE, YELLOW


class DeterminantChapterTitleCard(Scene):
    """Opening card for the assembled determinant chapter."""

    def construct(self) -> None:
        chapter = Text("Chapter 5", font_size=34, color=GREY_B)
        title = Text("Determinants", font_size=58, color=WHITE)
        subtitle = Text(
            "Scale • orientation • invertibility • structure",
            font_size=27,
            color=YELLOW,
        )

        group = VGroup(chapter, title, subtitle).arrange(direction=[0, -1, 0], buff=0.34)
        group.move_to([0, 0.15, 0])

        self.play(FadeIn(chapter), FadeIn(title), FadeIn(subtitle))
        self.wait(3.0)
