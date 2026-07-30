from pathlib import Path


SCENE = Path("scenes/what_does_a_linear_transformation_do_presentation.py")


def test_transformation_caption_is_grouped_and_shifted_below_title() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "transformation_caption = VGroup(label, origin_note)" in source
    assert "transformation_caption.to_corner(LEFT + UP, buff=0.55)" in source
    assert "transformation_caption.shift(0.55 * DOWN)" in source
    assert "FadeIn(transformation_caption)" in source
    assert "FadeOut(transformation_caption)" in source
