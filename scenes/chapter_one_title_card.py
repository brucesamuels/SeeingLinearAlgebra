"""Opening title card for the assembled Chapter 1 video."""

from manim import DOWN, FadeIn, FadeOut, Scene, Text, VGroup, YELLOW


class ChapterOneTitleCard(Scene):
    def construct(self) -> None:
        title = Text("Chapter 1", font_size=58, color=YELLOW)
        subtitle = Text("Vectors", font_size=48)
        question = Text(
            "How can direction and magnitude become mathematics?",
            font_size=28,
        )
        card = VGroup(title, subtitle, question).arrange(DOWN, buff=0.32)
        self.play(FadeIn(card))
        self.wait(2.8)
        self.play(FadeOut(card))
