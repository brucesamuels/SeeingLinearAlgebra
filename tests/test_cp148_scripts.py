from pathlib import Path


def test_check_script_targets_cp148_tests() -> None:
    source = Path("scripts/check_cp148_determinant_chapter.zsh").read_text(encoding="utf-8")
    assert "test_cp148_determinant_chapter_assembly.py" in source
    assert "test_cp148_scripts.py" in source
    assert "test_cp148_elimination_banner.py" in source
    assert "compileall" in source


def test_assembly_rerenders_corrected_elimination_scene() -> None:
    source = Path("scripts/assemble_cp148_determinant_chapter.zsh").read_text(encoding="utf-8")
    assert "DeterminantEliminationPresentation" in source
    assert "determinant_elimination_presentation.py" in source


def test_final_hd_script_renders_all_scenes_at_high_quality() -> None:
    source = Path("scripts/finalize_cp148_determinant_chapter_hd.zsh").read_text(encoding="utf-8")
    assert "-qh" in source
    assert "--quality-dir 1080p60" in source
    assert "Chapter5_Determinants_Final_1080p.mp4" in source
    assert "DeterminantEliminationPresentation" in source


def test_banner_patch_script_is_installed_and_verifies_exact_heading() -> None:
    source = Path("scripts/patch_cp148_elimination_banner.py").read_text(encoding="utf-8")
    assert 'OLD = "Properties of the Determinant"' in source
    assert 'NEW = "Methods of Computation"' in source
    assert "CP134 banner patch verification failed." in source


def test_banner_patcher_targets_exact_stale_heading() -> None:
    source = Path("scripts/patch_cp148_elimination_banner.py").read_text(encoding="utf-8")
    assert 'OLD = "Properties of the Determinant"' in source
    assert 'NEW = "Methods of Computation"' in source
    assert "determinant_elimination_presentation.py" in source
