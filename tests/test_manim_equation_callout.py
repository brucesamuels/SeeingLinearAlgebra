"""Focused tests for the reusable Manim equation callout."""

from __future__ import annotations

import numpy as np
import pytest

pytest.importorskip("manim")

from manim import MathTex, SurroundingRectangle, Text, VGroup  # noqa: E402

from engine.manim_equation_callout import ManimEquationCallout  # noqa: E402


def _assert_panel_surrounds(
    panel: SurroundingRectangle,
    *content: MathTex | Text,
) -> None:
    assert panel.get_left()[0] < min(item.get_left()[0] for item in content)
    assert panel.get_right()[0] > max(item.get_right()[0] for item in content)
    assert panel.get_bottom()[1] < min(item.get_bottom()[1] for item in content)
    assert panel.get_top()[1] > max(item.get_top()[1] for item in content)


def test_callout_is_a_vgroup_and_returns_itself_as_root() -> None:
    callout = ManimEquationCallout(r"\mathbf{w}=a\mathbf{u}+b\mathbf{v}")

    assert isinstance(callout, VGroup)
    assert callout.mobject is callout


def test_equation_only_callout_owns_fixed_public_children_in_order() -> None:
    callout = ManimEquationCallout(r"\mathbf{w}=a\mathbf{u}+b\mathbf{v}")

    assert isinstance(callout.equation_mobject, MathTex)
    assert isinstance(callout.panel_mobject, SurroundingRectangle)
    assert callout.caption_mobject is None
    assert callout.content_mobjects == (callout.equation_mobject,)
    assert tuple(callout.submobjects) == (
        callout.panel_mobject,
        callout.equation_mobject,
    )


def test_caption_callout_owns_equation_caption_and_panel_in_order() -> None:
    callout = ManimEquationCallout(
        r"\mathbf{w}=a\mathbf{u}+b\mathbf{v}",
        caption="Coefficients scale the two vectors.",
    )

    assert isinstance(callout.caption_mobject, Text)
    assert callout.content_mobjects == (
        callout.equation_mobject,
        callout.caption_mobject,
    )
    assert tuple(callout.submobjects) == (
        callout.panel_mobject,
        callout.equation_mobject,
        callout.caption_mobject,
    )


def test_sources_and_spacing_are_retained_exactly() -> None:
    equation = r"\mathbf{w}=a\mathbf{u}+b\mathbf{v}"
    caption = "The resultant is the sum of the scaled vectors."
    callout = ManimEquationCallout(
        equation,
        caption=caption,
        content_buff=0.31,
        panel_buff=0.27,
    )

    assert callout.equation_source == equation
    assert callout.caption_text == caption
    assert callout.content_buff == pytest.approx(0.31)
    assert callout.panel_buff == pytest.approx(0.27)


def test_caption_is_below_equation_and_panel_surrounds_all_content() -> None:
    callout = ManimEquationCallout(
        r"\mathbf{w}=a\mathbf{u}+b\mathbf{v}",
        caption="Coefficients scale the two vectors.",
        content_buff=0.24,
        panel_buff=0.20,
    )

    assert callout.caption_mobject is not None
    assert (
        callout.caption_mobject.get_top()[1]
        < callout.equation_mobject.get_bottom()[1]
    )
    _assert_panel_surrounds(
        callout.panel_mobject,
        callout.equation_mobject,
        callout.caption_mobject,
    )


def test_equation_only_panel_surrounds_the_equation() -> None:
    callout = ManimEquationCallout(r"\mathbf{w}=a\mathbf{u}+b\mathbf{v}")

    _assert_panel_surrounds(
        callout.panel_mobject,
        callout.equation_mobject,
    )


def test_custom_options_are_copied_resolved_and_observable() -> None:
    equation_options = {"font_size": 41.0}
    caption_options = {"font_size": 19.0}
    panel_options = {
        "stroke_width": 3.0,
        "fill_opacity": 0.72,
    }

    callout = ManimEquationCallout(
        r"\mathbf{w}=a\mathbf{u}+b\mathbf{v}",
        caption="Coefficients scale the two vectors.",
        equation_kwargs=equation_options,
        caption_kwargs=caption_options,
        panel_kwargs=panel_options,
    )

    equation_options["font_size"] = 99.0
    caption_options["font_size"] = 99.0
    panel_options["stroke_width"] = 99.0

    assert callout.equation_mobject.font_size == pytest.approx(41.0)
    assert callout.caption_mobject is not None
    assert callout.caption_mobject.font_size == pytest.approx(19.0)
    assert callout.panel_mobject.get_stroke_width() == pytest.approx(3.0)
    assert callout.panel_mobject.get_fill_opacity() == pytest.approx(0.72)
    assert callout.equation_kwargs["font_size"] == pytest.approx(41.0)
    assert callout.caption_kwargs["font_size"] == pytest.approx(19.0)
    assert callout.panel_kwargs["stroke_width"] == pytest.approx(3.0)


def test_returned_option_dictionaries_are_defensive_copies() -> None:
    callout = ManimEquationCallout(
        r"\mathbf{w}=a\mathbf{u}+b\mathbf{v}",
        caption="Coefficients scale the two vectors.",
    )

    equation_options = callout.equation_kwargs
    caption_options = callout.caption_kwargs
    panel_options = callout.panel_kwargs
    equation_options["font_size"] = 999
    caption_options["font_size"] = 999
    panel_options["stroke_width"] = 999

    assert callout.equation_kwargs["font_size"] != 999
    assert callout.caption_kwargs["font_size"] != 999
    assert callout.panel_kwargs["stroke_width"] != 999


def test_distinct_callouts_do_not_share_mobjects() -> None:
    first = ManimEquationCallout(r"\mathbf{w}=a\mathbf{u}+b\mathbf{v}")
    second = ManimEquationCallout(r"\mathbf{x}=c\mathbf{p}+d\mathbf{q}")

    assert id(first) != id(second)
    assert id(first.equation_mobject) != id(second.equation_mobject)
    assert id(first.panel_mobject) != id(second.panel_mobject)


@pytest.mark.parametrize("value", [None, 4, object()])
def test_equation_must_be_a_string(value: object) -> None:
    with pytest.raises(TypeError, match="equation must be a string"):
        ManimEquationCallout(value)  # type: ignore[arg-type]


@pytest.mark.parametrize("value", ["", "   ", "\n\t"])
def test_equation_must_not_be_empty(value: str) -> None:
    with pytest.raises(ValueError, match="equation must not be empty"):
        ManimEquationCallout(value)


@pytest.mark.parametrize("value", [4, object(), ["caption"]])
def test_caption_must_be_a_string_when_present(value: object) -> None:
    with pytest.raises(TypeError, match="caption must be a string"):
        ManimEquationCallout(
            r"x=y",
            caption=value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("value", ["", "   ", "\n\t"])
def test_caption_must_not_be_empty_when_present(value: str) -> None:
    with pytest.raises(ValueError, match="caption must not be empty"):
        ManimEquationCallout(r"x=y", caption=value)


@pytest.mark.parametrize("name", ["content_buff", "panel_buff"])
@pytest.mark.parametrize("value", [True, False, "wide", object()])
def test_spacing_must_be_real(name: str, value: object) -> None:
    with pytest.raises(TypeError, match=rf"{name} must be a real number"):
        ManimEquationCallout(r"x=y", **{name: value})


@pytest.mark.parametrize("name", ["content_buff", "panel_buff"])
@pytest.mark.parametrize("value", [np.nan, np.inf, -np.inf])
def test_spacing_must_be_finite(name: str, value: float) -> None:
    with pytest.raises(ValueError, match=rf"{name} must be finite"):
        ManimEquationCallout(r"x=y", **{name: value})


@pytest.mark.parametrize("name", ["content_buff", "panel_buff"])
def test_spacing_must_be_nonnegative(name: str) -> None:
    with pytest.raises(ValueError, match=rf"{name} must be nonnegative"):
        ManimEquationCallout(r"x=y", **{name: -0.01})


@pytest.mark.parametrize(
    "name",
    ["equation_kwargs", "caption_kwargs", "panel_kwargs"],
)
def test_constructor_options_must_be_mappings(name: str) -> None:
    with pytest.raises(TypeError, match=rf"{name} must be a mapping"):
        ManimEquationCallout(r"x=y", **{name: [("font_size", 20)]})


@pytest.mark.parametrize(
    ("name", "options", "reserved"),
    [
        ("equation_kwargs", {"tex_strings": ("bad",)}, "tex_strings"),
        ("caption_kwargs", {"text": "bad"}, "text"),
        ("panel_kwargs", {"mobject": object()}, "mobject"),
        ("panel_kwargs", {"buff": 1.0}, "buff"),
    ],
)
def test_constructor_options_cannot_override_owned_arguments(
    name: str,
    options: dict[str, object],
    reserved: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=rf"{name} cannot override component-owned arguments: {reserved}",
    ):
        ManimEquationCallout(r"x=y", **{name: options})
