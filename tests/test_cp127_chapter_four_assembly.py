from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest


REPO = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = REPO / "scripts/build_cp127_chapter_four.py"
TITLE_SOURCE = REPO / "scenes/chapter_four_title_card.py"
SHELL_SOURCE = REPO / "scripts/build_cp127_chapter_four.zsh"


def load_build_module():
    spec = importlib.util.spec_from_file_location("cp127_build", BUILD_SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_chapter_contains_title_and_twenty_two_approved_lessons() -> None:
    module = load_build_module()
    assert len(module.CHAPTER_CLIPS) == 23
    assert module.CHAPTER_CLIPS[0].scene_class == "ChapterFourTitleCard"
    assert module.CHAPTER_CLIPS[-1].scene_class == "PivotingPALUPresentation"


def test_chapter_lesson_order_places_rectangular_systems_after_rank_consistency() -> None:
    module = load_build_module()
    expected = [
        "ChapterFourTitleCard",
        "LinearSystemMeaningPresentation",
        "AugmentedMatrixEncodingPresentation",
        "ElementaryRowOperationsPresentation",
        "RowReplacementPreservesSolutionsPresentation",
        "GaussianEliminationToEchelonPresentation",
        "BackSubstitutionPresentation",
        "EliminationAlgorithmPresentation",
        "GaussJordanRREFPresentation",
        "RREFSolutionSetsPresentation",
        "PivotAndFreeVariablesPresentation",
        "HomogeneousNullSpacePresentation",
        "NullSpaceBasisPresentation",
        "CompleteSolutionPresentation",
        "RankPivotsConsistencyPresentation",
        "RectangularMatricesPresentation",
        "RectangularSystemSolvabilityPresentation",
        "ElementaryMatricesPresentation",
        "EliminationMatrixMultiplicationPresentation",
        "MultipleRightHandSidesPresentation",
        "GaussJordanInversePresentation",
        "NoninvertibleMatrixPresentation",
        "PivotingPALUPresentation",
    ]
    assert [clip.scene_class for clip in module.CHAPTER_CLIPS] == expected


def test_every_lesson_scene_source_exists_and_defines_its_class() -> None:
    module = load_build_module()
    for clip in module.CHAPTER_CLIPS:
        source_path = REPO / clip.relative_scene_path()
        assert source_path.is_file(), source_path
        source = source_path.read_text(encoding="utf-8")
        assert f"class {clip.scene_class}(" in source


def test_every_existing_lesson_has_its_render_script() -> None:
    module = load_build_module()
    for clip in module.CHAPTER_CLIPS[1:]:
        render_script = REPO / clip.render_script
        assert render_script.is_file(), render_script


def test_title_card_uses_separate_text_and_math_objects() -> None:
    source = TITLE_SOURCE.read_text(encoding="utf-8")
    assert 'Text("CHAPTER 4"' in source
    assert 'Text("Solving Linear Systems"' in source
    assert r'r"A\mathbf{x}=\mathbf{b}"' in source
    assert "MathTex(" in source
    assert "maximum_width" in source


def test_title_card_has_deliberate_reading_time_and_fades_out() -> None:
    source = TITLE_SOURCE.read_text(encoding="utf-8")
    assert "self.wait(3.2)" in source
    assert "FadeOut(main_group)" in source
    assert "FadeOut(series)" in source


def test_expected_video_path_uses_manim_scene_directory() -> None:
    module = load_build_module()
    clip = module.CHAPTER_CLIPS[1]
    assert clip.relative_video_path("1080p60") == Path(
        "media/videos/linear_system_meaning_presentation/1080p60/"
        "LinearSystemMeaningPresentation.mp4"
    )


def test_quality_directory_maps_to_high_quality_manim_flag() -> None:
    module = load_build_module()
    assert module.manim_quality_flag("1080p60") == "-qh"
    assert module.manim_quality_flag("480p15") == "-ql"


def test_missing_clips_report_high_quality_render_commands(tmp_path: Path) -> None:
    module = load_build_module()
    with pytest.raises(module.AssemblyError) as error_info:
        module.collect_clip_paths(tmp_path, "1080p60")
    message = str(error_info.value)
    assert "approved renders are missing" in message
    assert (
        "python -m manim --disable_caching -qh "
        "scenes/linear_system_meaning_presentation.py LinearSystemMeaningPresentation"
    ) in message
    assert "build_cp127_chapter_four.zsh" in message


def test_render_clip_uses_selected_quality_and_python_module(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = load_build_module()
    clip = module.CHAPTER_CLIPS[1]
    scene_path = tmp_path / clip.relative_scene_path()
    scene_path.parent.mkdir(parents=True)
    scene_path.write_text("class LinearSystemMeaningPresentation: pass\n", encoding="utf-8")
    expected_output = tmp_path / clip.relative_video_path("1080p60")
    calls: list[tuple[list[str], Path, dict[str, str]]] = []

    def fake_run(command, *, cwd, env, check):
        assert check is True
        calls.append((command, cwd, env))
        expected_output.parent.mkdir(parents=True)
        expected_output.write_bytes(b"video")
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(module.subprocess, "run", fake_run)
    result = module.render_clip(tmp_path, "1080p60", clip)

    assert result == expected_output
    command, cwd, env = calls[0]
    assert command[:3] == [sys.executable, "-m", "manim"]
    assert "--disable_caching" in command
    assert "-qh" in command
    assert str(clip.relative_scene_path()) in command
    assert clip.scene_class in command
    assert cwd == tmp_path
    assert str(tmp_path) in env["PYTHONPATH"].split(":")


def test_format_duration_uses_hour_minute_second_notation() -> None:
    module = load_build_module()
    assert module.format_duration(0.0) == "0:00:00"
    assert module.format_duration(3661.2) == "1:01:01"


def test_assembly_uses_stream_copy_and_writes_two_stable_outputs() -> None:
    source = BUILD_SCRIPT.read_text(encoding="utf-8")
    assert '"-c",\n            "copy"' in source
    assert '"media/videos/chapter_four_assembly"' in source
    assert 'repo_root / "media" / OUTPUT_FILENAME' in source
    assert 'OUTPUT_FILENAME = "ChapterFourSolvingLinearSystems.mp4"' in source


def test_shell_driver_renders_missing_then_assembles() -> None:
    source = SHELL_SOURCE.read_text(encoding="utf-8")
    assert 'export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"' in source
    assert "python scripts/build_cp127_chapter_four.py --render-missing" in source
    assert "Any missing high-quality lesson renders will be created automatically." in source
    assert 'if [[ "${1:-}" == "--preview" ]]' in source


def test_rectangular_lessons_follow_rank_consistency_and_precede_elementary_matrices() -> None:
    module = load_build_module()
    classes = [clip.scene_class for clip in module.CHAPTER_CLIPS]
    rank_index = classes.index("RankPivotsConsistencyPresentation")
    rectangular_index = classes.index("RectangularMatricesPresentation")
    solvability_index = classes.index("RectangularSystemSolvabilityPresentation")
    elementary_index = classes.index("ElementaryMatricesPresentation")
    assert rank_index < rectangular_index < solvability_index < elementary_index


def test_rectangular_lessons_use_their_approved_render_scripts() -> None:
    module = load_build_module()
    by_class = {clip.scene_class: clip for clip in module.CHAPTER_CLIPS}
    assert by_class["RectangularMatricesPresentation"].render_script == (
        "scripts/render_cp125_rectangular_matrices.zsh"
    )
    assert by_class["RectangularSystemSolvabilityPresentation"].render_script == (
        "scripts/render_cp126_rectangular_system_solvability.zsh"
    )
