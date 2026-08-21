"""Title card for Chapter 7: Eigenvalues and Eigenvectors."""
from manim import DOWN, GREY_B, Scene, Text, VGroup, WHITE, YELLOW


class ChapterSevenTitleCard(Scene):
    """Open the Eigenvalues and Eigenvectors chapter."""

    def construct(self) -> None:
        chapter = Text("CHAPTER 7", font_size=28, color=GREY_B, weight="BOLD")
        title = Text("Eigenvalues and Eigenvectors", font_size=48, color=YELLOW, weight="BOLD")
        subtitle = Text(
            "Special directions reveal hidden simplicity.",
            font_size=30,
            color=WHITE,
        )
        group = VGroup(chapter, title, subtitle).arrange(DOWN, buff=0.48)
        self.play(*[item.animate.set_opacity(1) for item in group], run_time=0.01)
        self.wait(2.2)
