"""Brooklyn Tech and series branding."""

from pathlib import Path
from manim import Group, ImageMobject, Rectangle, Text, VGroup, DOWN, UP
from engine.theme import BACKGROUND, GRID, MUTED, TEXT, TITLE_SIZE, SUBTITLE_SIZE, VECTOR_1

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SEAL = PROJECT_ROOT / "assets" / "BTHSseal.jpeg"

def _seal_or_placeholder(path: Path, height: float = 1.35):
    if path.exists():
        return ImageMobject(str(path)).set(height=height)
    box = Rectangle(width=height, height=height, stroke_color=GRID,
                    fill_color=BACKGROUND, fill_opacity=1.0)
    initials = Text("BTHS", font_size=22, color=MUTED)
    return VGroup(box, initials)

class BrooklynTechIntro(Group):
    """General Group is required because the seal is an ImageMobject."""

    def __init__(self, episode_number: int, episode_title: str,
                 instructor: str = "Mr. Bruce Samuels",
                 seal_path: str | Path | None = None):
        super().__init__()
        seal = _seal_or_placeholder(Path(seal_path) if seal_path else DEFAULT_SEAL)
        school = Text("Brooklyn Technical High School", font_size=24, color=MUTED)
        series = Text("Seeing Linear Algebra", font_size=TITLE_SIZE,
                      color=TEXT, weight="SEMIBOLD")
        episode = Text(f"Episode {episode_number}: {episode_title}",
                       font_size=SUBTITLE_SIZE, color=VECTOR_1)
        credit = Text(instructor, font_size=20, color=MUTED)
        stack = VGroup(school, series, episode, credit).arrange(DOWN, buff=0.18)
        seal.next_to(stack, UP, buff=0.35)
        self.add(seal, stack)

class EpisodeEndCard(VGroup):
    def __init__(self, next_title: str | None = None):
        parts = [Text("Seeing Linear Algebra", font_size=38, color=TEXT)]
        if next_title:
            parts += [
                Text("Next episode", font_size=20, color=MUTED),
                Text(next_title, font_size=28, color=VECTOR_1),
            ]
        super().__init__(*parts)
        self.arrange(DOWN, buff=0.22)
