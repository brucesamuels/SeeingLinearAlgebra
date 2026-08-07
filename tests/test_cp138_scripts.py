from pathlib import Path


def test_render_script_sets_pythonpath_and_disables_caching() -> None:
    text = Path("scripts/render_cp138_cofactor_efficiency.zsh").read_text(encoding="utf-8")
    assert 'export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"' in text
    assert "--disable_caching" in text


def test_check_script_runs_cp138_tests() -> None:
    text = Path("scripts/check_cp138_cofactor_efficiency.zsh").read_text(encoding="utf-8")
    assert "test_determinant_cofactor_efficiency.py" in text
    assert "test_determinant_cofactor_efficiency_presentation.py" in text
    assert "test_cp138_scripts.py" in text
