from pathlib import Path
import ast

BUILD = Path("scripts/build_cp184_chapter_seven.py")
TITLE = Path("scenes/chapter_seven_title_card.py")


def build_source() -> str:
    return BUILD.read_text(encoding="utf-8")


def test_title_card_is_chapter_seven_eigenvalues_and_eigenvectors() -> None:
    text = TITLE.read_text(encoding="utf-8")
    assert "ChapterSevenTitleCard" in text
    assert '"CHAPTER 7"' in text
    assert '"Eigenvalues and Eigenvectors"' in text


def test_assembly_contains_every_approved_checkpoint_in_order() -> None:
    module = ast.parse(build_source())
    lessons = next(
        node for node in module.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "LESSONS" for target in node.targets)
    )
    checkpoints = [elt.elts[0].value for elt in lessons.value.elts]
    assert checkpoints == list(range(168, 184))


def test_key_scene_files_are_present_in_manifest() -> None:
    text = build_source()
    for filename in (
        "eigenvector_special_directions_presentation.py",
        "computing_eigenvectors_presentation.py",
        "eigenvector_basis_presentation.py",
        "diagonalization_presentation.py",
        "powers_of_diagonalizable_matrix_presentation.py",
        "repeated_eigenvalues_presentation.py",
        "symmetric_orthogonal_eigenvectors_presentation.py",
        "spectral_theorem_presentation.py",
        "dominant_eigenvector_presentation.py",
        "first_order_system_eigenvectors_presentation.py",
        "fibonacci_difference_equation_presentation.py",
        "eigenvalues_chapter_review_presentation.py",
    ):
        assert filename in text


def test_preview_uses_low_quality_and_ffmpeg_concat() -> None:
    render = Path("scripts/render_cp184_chapter_seven_assembly.zsh").read_text(encoding="utf-8")
    text = build_source()
    assert "--quality l" in render
    assert '"ffmpeg"' in text
    assert '"concat"' in text
    assert '"-c", "copy"' in text


def test_output_name_is_explicit() -> None:
    assert "ChapterSeven_EigenvaluesAndEigenvectors_preview.mp4" in build_source()
