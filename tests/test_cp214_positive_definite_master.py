import importlib.util
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_cp214_positive_definite_master.py"
SPEC = importlib.util.spec_from_file_location("positive_definite_master_builder", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
NARRATION = Path(__file__).parents[1] / "POSITIVE_DEFINITE_MATRICES_NARRATION.md"


def checkpoints():
    return [checkpoint for checkpoint, *_ in MODULE.MASTER_SCENES if checkpoint is not None]


def test_master_uses_eighty_percent_speed():
    assert MODULE.DEFAULT_SPEED == pytest.approx(0.80)
    assert MODULE.validate_speed(0.80) == pytest.approx(0.80)
    with pytest.raises(ValueError):
        MODULE.validate_speed(0.4)


def test_master_contains_title_and_cp199_through_cp212():
    assert MODULE.MASTER_SCENES[0][2] == "PositiveDefiniteMatricesTitleCard"
    assert checkpoints() == list(range(199, 213))
    assert MODULE.MASTER_SCENES[-1][2] == "PositiveDefinitenessSummaryPresentation"


def test_builder_renders_current_sources_at_1080p60():
    source = MODULE_PATH.read_text()
    assert '"--disable_caching", "-qh"' in source
    assert '"python", "-m", "manim"' in source
    assert '("h264", 1920, 1080, "yuv420p", "60/1")' in source


def test_builder_assembles_and_slows_with_high_quality_encoding():
    source = MODULE_PATH.read_text()
    assert '"-c", "copy"' in source
    assert "setpts=PTS/{speed:.6f},fps=60" in source
    assert '"-preset", "slow", "-crf", "16"' in source
    assert "PositiveDefiniteMatrices_1080p60_fullspeed.mp4" in source
    assert "PositiveDefiniteMatrices_1080p60_80pct.mp4" in source


def test_narration_explains_energy_terminology_at_onset():
    text = NARRATION.read_text()
    opening = text.split("## CP200", 1)[0]
    assert "quadratic energy" in opening
    assert "literal stored energy" in opening
    assert "variance" in opening
    assert "squared size" in opening
    assert "cost" in opening


def test_narration_covers_every_lesson_and_slowed_timeline():
    text = NARRATION.read_text()
    for checkpoint in range(199, 213):
        assert f"## CP{checkpoint}" in text
    assert "18:37" in text
