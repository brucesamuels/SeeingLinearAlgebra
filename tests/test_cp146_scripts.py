from pathlib import Path


def test_check_script_includes_all_cp146_tests() -> None:
    text = Path("scripts/check_cp146_jacobian_preview.zsh").read_text(encoding="utf-8")
    assert 'repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"' in text
    assert "test_determinant_jacobian_preview.py" in text
    assert "test_determinant_jacobian_preview_presentation.py" in text
    assert "test_cp146_scripts.py" in text


def test_render_script_renders_correct_scene() -> None:
    text = Path("scripts/render_cp146_jacobian_preview.zsh").read_text(encoding="utf-8")
    assert "--disable_caching" in text
    assert "determinant_jacobian_preview_presentation.py" in text
    assert "DeterminantJacobianPreviewPresentation" in text
