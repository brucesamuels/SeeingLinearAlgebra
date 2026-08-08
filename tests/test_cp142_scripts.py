from pathlib import Path


def test_check_script_sets_repo_root_and_pythonpath() -> None:
    text = Path("scripts/check_cp142_adjugate_inverse.zsh").read_text(encoding="utf-8")
    assert 'repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"' in text
    assert 'cd "$repo_root"' in text
    assert 'export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"' in text
    assert "test_cp142_scripts.py" in text


def test_render_script_sets_repo_root_and_disables_cache() -> None:
    text = Path("scripts/render_cp142_adjugate_inverse.zsh").read_text(encoding="utf-8")
    assert 'repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"' in text
    assert 'cd "$repo_root"' in text
    assert 'export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"' in text
    assert "--disable_caching" in text
    assert "DeterminantAdjugateInversePresentation" in text
