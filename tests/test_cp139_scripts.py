from pathlib import Path


def test_check_script_targets_cp139_tests() -> None:
    text = Path("scripts/check_cp139_triangular.zsh").read_text(encoding="utf-8")
    assert 'repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"' in text
    assert 'export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"' in text
    assert "test_determinant_triangular.py" in text
    assert "test_determinant_triangular_presentation.py" in text


def test_render_script_targets_scene_and_disables_cache() -> None:
    text = Path("scripts/render_cp139_triangular.zsh").read_text(encoding="utf-8")
    assert '--disable_caching' in text
    assert "determinant_triangular_presentation.py" in text
    assert "DeterminantTriangularPresentation" in text
