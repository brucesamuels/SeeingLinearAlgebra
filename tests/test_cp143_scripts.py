from pathlib import Path


def test_check_script_includes_all_cp143_tests() -> None:
    text = Path("scripts/check_cp143_determinant_products.zsh").read_text(encoding="utf-8")
    assert 'repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"' in text
    assert 'export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"' in text
    assert "test_determinant_product_rule.py" in text
    assert "test_determinant_product_rule_presentation.py" in text
    assert "test_cp143_scripts.py" in text


def test_render_script_renders_correct_scene() -> None:
    text = Path("scripts/render_cp143_determinant_products.zsh").read_text(encoding="utf-8")
    assert "--disable_caching" in text
    assert "determinant_product_rule_presentation.py" in text
    assert "DeterminantProductRulePresentation" in text
