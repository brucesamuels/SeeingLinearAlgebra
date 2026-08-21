from pathlib import Path
import ast

BUILD = Path("scripts/build_cp186_chapter_seven_master.py")
RENDER = Path("scripts/render_cp186_chapter_seven_master.zsh")


def source() -> str:
    return BUILD.read_text(encoding="utf-8")


def test_master_contains_every_approved_checkpoint_in_order() -> None:
    module = ast.parse(source())
    lessons = next(
        node for node in module.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "LESSONS" for target in node.targets)
    )
    checkpoints = [elt.elts[0].value for elt in lessons.value.elts]
    assert checkpoints == list(range(168, 184))


def test_master_renders_with_manim_high_quality_1080p60() -> None:
    text = source()
    assert '"-qh"' in text
    assert '"-ql"' not in text


def test_master_applies_approved_85_percent_speed() -> None:
    text = source()
    assert "SPEED = 0.85" in text
    assert 'f"setpts=PTS/{SPEED},fps=60"' in text


def test_master_uses_high_quality_h264_output() -> None:
    text = source()
    assert '"libx264"' in text
    assert '"-crf", "16"' in text
    assert '"yuv420p"' in text
    assert '"+faststart"' in text


def test_master_output_names_are_explicit() -> None:
    text = source()
    assert "ChapterSeven_EigenvaluesAndEigenvectors_1080p60_fullspeed.mp4" in text
    assert "ChapterSeven_EigenvaluesAndEigenvectors_1080p60_85pct.mp4" in text


def test_current_repository_scenes_are_rendered() -> None:
    text = source()
    assert 'scenes_dir = repo_root / "scenes"' in text
    assert "chapter_seven_title_card.py" in text
    assert "symmetric_orthogonal_eigenvectors_presentation.py" in text
    assert "characteristic_equation_presentation.py" in text


def test_render_wrapper_invokes_master_builder() -> None:
    text = RENDER.read_text(encoding="utf-8")
    assert "python scripts/build_cp186_chapter_seven_master.py" in text
