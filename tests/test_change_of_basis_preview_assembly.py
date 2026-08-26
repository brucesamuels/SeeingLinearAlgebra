from pathlib import Path
import importlib.util
import os


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_cp197_change_of_basis_preview.py"
SPEC = importlib.util.spec_from_file_location("change_of_basis_preview_builder", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def scene_names():
    return [name for name, _ in MODULE.CHAPTER_CLIPS]


def test_chapter_order_places_linear_combination_bridge_early():
    names = scene_names()
    assert names.index("CoordinatesRelativeToBasisPresentation") < names.index("CoordinateLinearCombinationsPresentation")
    assert names.index("CoordinateLinearCombinationsPresentation") < names.index("BasisMatrixPresentation")


def test_transformation_translation_precedes_good_basis_payoff():
    names = scene_names()
    assert names.index("TransformationBetweenBasesPresentation") < names.index("GoodBasisPresentation")
    assert names[-1] == "ChangeOfBasisReviewPresentation"


def test_every_scene_name_is_unique():
    names = scene_names()
    assert len(names) == len(set(names))


def test_find_rendered_clip_prefers_requested_quality_and_newest(tmp_path):
    low = tmp_path / "videos" / "lesson" / "480p15"
    high = tmp_path / "videos" / "lesson" / "1080p60"
    low.mkdir(parents=True)
    high.mkdir(parents=True)
    old = low / "ExamplePresentation.mp4"
    newer = low / "nested" / "ExamplePresentation.mp4"
    other_quality = high / "ExamplePresentation.mp4"
    old.write_bytes(b"old")
    newer.parent.mkdir()
    newer.write_bytes(b"new")
    other_quality.write_bytes(b"high")
    os.utime(old, (100, 100))
    os.utime(newer, (200, 200))
    os.utime(other_quality, (300, 300))
    assert MODULE.find_rendered_clip(tmp_path, "ExamplePresentation", "480p15") == newer


def test_default_output_is_preview_not_final_master():
    source = MODULE_PATH.read_text()
    assert "media/change_of_basis_preview.mp4" in source
    assert "final_master" not in source
