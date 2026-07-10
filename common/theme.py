from manim import *

# Seeing Linear Algebra visual language
BACKGROUND = "#0B1020"
GRID = "#26324A"
GRID_FAINT = "#182238"
TEXT = "#F4F7FB"
MUTED = "#A8B3C7"
BLUE_VEC = "#4EA1FF"
RED_VEC = "#FF6577"
GREEN_VEC = "#58D68D"
YELLOW = "#FFD166"
PURPLE = "#B388FF"
CYAN = "#66E3FF"
SUCCESS = "#55D187"
FAILURE = "#FF5D73"

TITLE_FONT_SIZE = 58
SUBTITLE_FONT_SIZE = 30
BODY_FONT_SIZE = 30
LABEL_FONT_SIZE = 28

FAST = 0.55
MEDIUM = 1.0
SLOW = 1.6


def apply_theme() -> None:
    config.background_color = BACKGROUND


def soft_grid_2d(x_range=(-7, 7, 1), y_range=(-4, 4, 1)) -> NumberPlane:
    plane = NumberPlane(
        x_range=x_range,
        y_range=y_range,
        background_line_style={
            "stroke_color": GRID,
            "stroke_width": 1.2,
            "stroke_opacity": 0.45,
        },
        axis_config={
            "stroke_color": MUTED,
            "stroke_width": 1.6,
            "include_ticks": False,
        },
    )
    return plane
