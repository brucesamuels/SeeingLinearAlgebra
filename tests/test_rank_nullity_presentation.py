from pathlib import Path

SCENE = Path("scenes/rank_nullity_presentation.py")


def test_v3_label_is_not_registered_before_v3_vector_is_drawn() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "self.add_fixed_orientation_mobjects(labels[0], labels[1])" in source
    assert "self.add_fixed_orientation_mobjects(*labels)" not in source


def test_v3_label_is_registered_immediately_before_its_fade_in() -> None:
    source = SCENE.read_text(encoding="utf-8")
    expected = (
        "self.add_fixed_orientation_mobjects(labels[2])\n"
        "        self.play(Create(v3_arrow), FadeIn(labels[2]), run_time=1.2)"
    )
    assert expected in source


def test_final_screen_still_reveals_equations_before_explanation() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert "self.play(FadeIn(theorem_intro), FadeIn(theorem), FadeIn(example), run_time=1.4)" in source
    assert "self.play(FadeIn(interpretation), run_time=1.4)" in source
