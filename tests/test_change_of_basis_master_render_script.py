from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "render_cp198_change_of_basis_master.zsh"
TEXT = SCRIPT.read_text()


def test_every_render_is_high_quality_and_cache_free():
    assert 'manim --disable_caching -qh' in TEXT
    assert '--quality 1080p60' in TEXT


def test_cp195_is_directly_after_cp188_and_before_cp189():
    classes = [line.split()[-1] for line in TEXT.splitlines() if line.startswith("render_scene scenes/")]
    start = classes.index("CoordinatesRelativeToBasisPresentation")
    assert classes[start:start + 3] == [
        "CoordinatesRelativeToBasisPresentation",
        "CoordinateLinearCombinationsPresentation",
        "BasisMatrixPresentation",
    ]


def test_render_order_ends_with_review():
    assert TEXT.index("GoodBasisPresentation") < TEXT.index("ChangeOfBasisReviewPresentation")


def test_render_script_requests_eighty_five_percent_speed():
    assert "--speed 0.85" in TEXT
    assert "change_of_basis_master_85pct.mp4" in TEXT
