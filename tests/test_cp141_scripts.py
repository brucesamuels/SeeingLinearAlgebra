from pathlib import Path


def test_check_script_runs_all_cp141_tests() -> None:
    text = Path("scripts/check_cp141_cramers_rule.zsh").read_text(encoding="utf-8")
    assert 'repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"' in text
    assert 'export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"' in text
    assert "test_determinant_cramers_rule.py" in text
    assert "test_determinant_cramers_rule_presentation.py" in text
    assert "test_cp141_scripts.py" in text


def test_render_script_is_portable_and_disables_cache() -> None:
    text = Path("scripts/render_cp141_cramers_rule.zsh").read_text(encoding="utf-8")
    assert 'repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"' in text
    assert 'export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"' in text
    assert "--disable_caching" in text
    assert "DeterminantCramersRulePresentation" in text
