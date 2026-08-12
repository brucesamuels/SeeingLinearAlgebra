from pathlib import Path

SCENE = Path("scenes/determinant_elimination_presentation.py")


def test_elimination_banner_is_methods_of_computation() -> None:
    source = SCENE.read_text(encoding="utf-8")
    assert 'banner = Text("Methods of Computation", font_size=38)' in source
    assert "Properties of the Determinant" not in source
