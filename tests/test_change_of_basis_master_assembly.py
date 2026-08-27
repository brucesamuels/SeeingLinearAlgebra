from pathlib import Path
import importlib.util

import pytest


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_cp198_change_of_basis_master.py"
SPEC = importlib.util.spec_from_file_location("change_of_basis_master_builder", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_default_speed_is_eighty_five_percent():
    assert MODULE.DEFAULT_SPEED == pytest.approx(0.85)


def test_slowdown_rejects_unreasonable_speed(tmp_path):
    with pytest.raises(ValueError):
        MODULE.slow_master(tmp_path / "input.mp4", tmp_path / "output.mp4", 0.4)


def test_builder_reuses_cp197_order(tmp_path):
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    source = Path(__file__).parents[1] / "scripts" / "build_cp197_change_of_basis_preview.py"
    target = scripts / source.name
    target.write_text(source.read_text())
    preview = MODULE.load_preview_builder(tmp_path)
    names = [name for name, _ in preview.CHAPTER_CLIPS]
    assert names.index("CoordinatesRelativeToBasisPresentation") + 1 == names.index("CoordinateLinearCombinationsPresentation")
    assert names.index("CoordinateLinearCombinationsPresentation") + 1 == names.index("BasisMatrixPresentation")
    assert names[-1] == "ChangeOfBasisReviewPresentation"


def test_output_names_distinguish_normal_and_slowed_masters():
    source = MODULE_PATH.read_text()
    assert '"change_of_basis_master.mp4"' in source
    assert '"change_of_basis_master_85pct.mp4"' in source
    assert 'default="1080p60"' in source

