from pathlib import Path


def test_check_script_exists_and_mentions_cp147_tests() -> None:
    source = Path("scripts/check_cp147_determinant_synthesis.zsh").read_text(encoding="utf-8")
    assert "test_determinant_chapter_synthesis.py" in source
    assert "test_determinant_chapter_synthesis_presentation.py" in source
    assert "test_cp147_scripts.py" in source


def test_render_script_targets_synthesis_scene() -> None:
    source = Path("scripts/render_cp147_determinant_synthesis.zsh").read_text(encoding="utf-8")
    assert "determinant_chapter_synthesis_presentation.py" in source
    assert "DeterminantChapterSynthesisPresentation" in source
    assert "--disable_caching" in source
