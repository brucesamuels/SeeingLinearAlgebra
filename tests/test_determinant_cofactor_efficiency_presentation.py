from pathlib import Path

SCENE = Path("scenes/determinant_cofactor_efficiency_presentation.py")


def source() -> str:
    return SCENE.read_text(encoding="utf-8")


def test_scene_exists() -> None:
    assert "class DeterminantCofactorEfficiencyPresentation(Scene):" in source()


def test_scene_asks_students_to_choose_row_or_column() -> None:
    text = source()
    assert "Which row or column should we use?" in text
    assert "Row 2 has three zeros" in text


def test_scene_shows_first_cofactor_expansion() -> None:
    text = source()
    assert "Expand along the row with the most zeros" in text
    assert r"(-1)^{2+2}=+1" in text
    assert "Delete row 2 and column 2." in text


def test_scene_shows_recursive_expansion() -> None:
    text = source()
    assert "Cofactor expansion is recursive" in text
    assert "recursive_expansion_tex()" in text
    assert "The zero entry contributes nothing." in text


def test_scene_finishes_numerically_and_with_strategy() -> None:
    text = source()
    assert "Now the arithmetic is small" in text
    assert "arithmetic_lines()" in text
    assert "Choose the expansion that creates the least work" in text
    assert "strategy_lines()" in text


def test_scene_uses_safe_clear_pattern() -> None:
    text = source()
    assert "*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve]" in text
