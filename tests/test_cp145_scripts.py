from pathlib import Path


def test_check_script_includes_all_cp145_tests() -> None:
    text = Path("scripts/check_cp145_determinant_geometry.zsh").read_text(encoding="utf-8")
    assert 'repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"' in text
    assert 'test_determinant_geometry.py' in text
    assert 'test_determinant_geometry_presentation.py' in text
    assert 'test_cp145_scripts.py' in text


def test_render_script_targets_correct_scene() -> None:
    text = Path("scripts/render_cp145_determinant_geometry.zsh").read_text(encoding="utf-8")
    assert '--disable_caching' in text
    assert 'determinant_geometry_presentation.py' in text
    assert 'DeterminantGeometryPresentation' in text
