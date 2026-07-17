from __future__ import annotations

import inspect

import pytest
from manim import MathTex, Text, VGroup

from engine.manim_perspective_pictograms import (
    PerspectivePictogram,
    PerspectivePictogramFactory,
)
from engine.why_vectors_content import WHY_VECTORS_SEQUENCE


def test_every_application_has_geometry_only_pictogram() -> None:
    for perspective in WHY_VECTORS_SEQUENCE.perspectives:
        for example in perspective.examples:
            pictogram = PerspectivePictogramFactory.build(example)

            assert isinstance(pictogram, PerspectivePictogram)
            assert isinstance(pictogram.group, VGroup)
            assert len(pictogram.group) > 0

            for mobject in pictogram.group.get_family():
                assert not isinstance(mobject, (Text, MathTex))


def test_music_pictogram_contains_no_unicode_or_tex() -> None:
    source = inspect.getsource(
        PerspectivePictogramFactory._music_recommendation
    )

    assert "MathTex" not in source
    assert "♪" not in source
    assert "Circle" in source
    assert "Line" in source
    assert "Arc" in source


def test_unknown_pictogram_is_rejected() -> None:
    with pytest.raises(KeyError, match="unknown perspective pictogram"):
        PerspectivePictogramFactory.build("unknown")
