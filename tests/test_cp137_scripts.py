from pathlib import Path


def test_render_script_exports_repo_root_on_pythonpath() -> None:
    text = Path("scripts/render_cp137_cofactor_expansion.zsh").read_text(encoding="utf-8")
    assert 'repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"' in text
    assert 'cd "$repo_root"' in text
    assert 'export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"' in text


def test_check_script_exports_repo_root_on_pythonpath() -> None:
    text = Path("scripts/check_cp137_cofactor_expansion.zsh").read_text(encoding="utf-8")
    assert 'repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"' in text
    assert 'cd "$repo_root"' in text
    assert 'export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"' in text
