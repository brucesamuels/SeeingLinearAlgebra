"""Safe scene utilities."""

from manim import FadeOut, Group, Rectangle, Scene, Text, VGroup, DOWN
from engine.theme import BACKGROUND, GRID, HIGHLIGHT, NORMAL, TEXT, TITLE_BAND_Y

def mixed_group(*mobjects):
    return Group(*[m for m in mobjects if m is not None])

def fade_out_all(scene: Scene, *mobjects, run_time: float = NORMAL):
    targets = mixed_group(*mobjects)
    if len(targets):
        scene.play(FadeOut(targets), run_time=run_time)

def clear_scene(scene: Scene, run_time: float = NORMAL):
    if scene.mobjects:
        fade_out_all(scene, *list(scene.mobjects), run_time=run_time)

def chapter_title(text: str):
    band = Rectangle(width=14.2, height=0.72, fill_color=BACKGROUND,
                     fill_opacity=0.96, stroke_color=GRID, stroke_width=1)
    label = Text(text, font_size=30, color=TEXT).move_to(band)
    group = VGroup(band, label)
    group.move_to([0, TITLE_BAND_Y, 0])
    return group

def pause_and_predict(prompt: str):
    heading = Text("Pause and Predict", font_size=34,
                   color=HIGHLIGHT, weight="SEMIBOLD")
    question = Text(prompt, font_size=24, color=TEXT, line_spacing=0.95)
    return VGroup(heading, question).arrange(DOWN, buff=0.35)

class SeeingScene(Scene):
    def setup(self):
        super().setup()
        self.camera.background_color = BACKGROUND

    def clear_all(self, run_time: float = NORMAL):
        clear_scene(self, run_time=run_time)
