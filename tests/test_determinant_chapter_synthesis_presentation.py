from pathlib import Path

SCENE = Path("scenes/determinant_chapter_synthesis_presentation.py")


def source() -> str:
    return SCENE.read_text(encoding="utf-8")


def test_scene_class_exists() -> None:
    text = source()
    assert "class DeterminantChapterSynthesisPresentation(Scene):" in text


def test_scene_uses_eight_card_sequence() -> None:
    text = source()
    for call in (
        "self.show_overview(banner)",
        "self.show_computation(banner)",
        "self.show_invertibility(banner)",
        "self.show_geometry(banner)",
        "self.show_algebraic_rules(banner)",
        "self.show_systems(banner)",
        "self.show_jacobian_bridge(banner)",
        "self.show_final_map(banner)",
    ):
        assert call in text


def test_overview_centers_determinant() -> None:
    text = source()
    assert r'MathTex(r"\det(A)", font_size=58, color=GREEN)' in text
    assert "Different questions kept leading back to the same scalar." in text


def test_invertibility_card_uses_two_chains() -> None:
    text = source()
    assert "invertibility_chain()" in text
    assert "singular_chain()" in text


def test_systems_card_contains_cramer_and_adjugate_titles() -> None:
    text = source()
    assert 'Text("Cramer\'s Rule"' in text
    assert 'Text("Adjugate inverse"' in text


def test_jacobian_card_connects_global_to_local() -> None:
    text = source()
    assert "The same idea survives beyond linear algebra" in text
    assert "jacobian_bridge()" in text


def test_final_map_closes_with_recognition_message() -> None:
    text = source()
    assert "Recognize structure before you compute." in text
    assert 'MathTex(r"\\det(A)", font_size=62, color=GREEN)' in text


def test_scene_uses_safe_clear_pattern() -> None:
    text = source()
    assert '*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve]' in text
    assert "VGroup(*self.mobjects)" not in text
