"""Reusable boxed mathematical equation callout for Manim lessons.

This renderer-specific lesson component owns one fixed ``MathTex`` equation,
an optional fixed explanatory ``Text`` caption, and one surrounding panel.  It
performs only local Manim construction and layout.

No mathematical computation, snapshot interpretation, animation timing,
scene sequencing, or chapter orchestration is performed here.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import numpy as np
from manim import DOWN, MathTex, SurroundingRectangle, Text, VGroup

from engine.theme import GRID, MUTED, PANEL, TEXT


class ManimEquationCallout(VGroup):
    """Own a fixed boxed equation and optional explanatory caption.

    Parameters
    ----------
    equation:
        Nonempty TeX source for the displayed equation.
    caption:
        Optional nonempty plain-text explanation displayed below the equation.
    content_buff:
        Vertical spacing between the equation and caption.
    panel_buff:
        Padding between the content and surrounding panel.
    equation_kwargs:
        Optional keyword arguments copied and forwarded to ``MathTex``.
    caption_kwargs:
        Optional keyword arguments copied and forwarded to ``Text`` when a
        caption is present.
    panel_kwargs:
        Optional keyword arguments copied and forwarded to
        ``SurroundingRectangle``.

    Notes
    -----
    The equation, caption, and panel are structural and immutable.  Scene code
    remains responsible for placement, scaling, appearance timing, and removal.
    """

    def __init__(
        self,
        equation: str,
        *,
        caption: str | None = None,
        content_buff: float = 0.18,
        panel_buff: float = 0.22,
        equation_kwargs: Mapping[str, Any] | None = None,
        caption_kwargs: Mapping[str, Any] | None = None,
        panel_kwargs: Mapping[str, Any] | None = None,
    ) -> None:
        equation_source = _nonempty_string(equation, name="equation")
        caption_text = (
            None
            if caption is None
            else _nonempty_string(caption, name="caption")
        )
        content_spacing = _nonnegative_finite_float(
            content_buff,
            name="content_buff",
        )
        panel_padding = _nonnegative_finite_float(
            panel_buff,
            name="panel_buff",
        )

        equation_options = _copied_options(
            equation_kwargs,
            name="equation_kwargs",
            reserved_keys=("tex_strings",),
        )
        caption_options = _copied_options(
            caption_kwargs,
            name="caption_kwargs",
            reserved_keys=("text",),
        )
        panel_options = _copied_options(
            panel_kwargs,
            name="panel_kwargs",
            reserved_keys=("mobject", "buff"),
        )

        equation_defaults: dict[str, Any] = {
            "font_size": 34,
            "color": TEXT,
        }
        caption_defaults: dict[str, Any] = {
            "font_size": 22,
            "color": MUTED,
        }
        panel_defaults: dict[str, Any] = {
            "stroke_color": GRID,
            "stroke_width": 1.5,
            "fill_color": PANEL,
            "fill_opacity": 0.94,
        }
        equation_defaults.update(equation_options)
        caption_defaults.update(caption_options)
        panel_defaults.update(panel_options)

        equation_mobject = MathTex(
            equation_source,
            **dict(equation_defaults),
        )

        caption_mobject: Text | None = None
        panel_target = equation_mobject
        if caption_text is not None:
            caption_mobject = Text(
                caption_text,
                **dict(caption_defaults),
            )
            caption_mobject.next_to(
                equation_mobject,
                DOWN,
                buff=content_spacing,
            )
            panel_target = VGroup(equation_mobject, caption_mobject)

        panel_mobject = SurroundingRectangle(
            panel_target,
            buff=panel_padding,
            **dict(panel_defaults),
        )

        children = [panel_mobject, equation_mobject]
        if caption_mobject is not None:
            children.append(caption_mobject)
        super().__init__(*children)

        self._equation_mobject = equation_mobject
        self._caption_mobject = caption_mobject
        self._panel_mobject = panel_mobject
        self._equation_source = equation_source
        self._caption_text = caption_text
        self._content_buff = content_spacing
        self._panel_buff = panel_padding
        self._equation_kwargs = dict(equation_defaults)
        self._caption_kwargs = dict(caption_defaults)
        self._panel_kwargs = dict(panel_defaults)

    @property
    def mobject(self) -> VGroup:
        """Return this component's root Manim group."""

        return self

    @property
    def equation_mobject(self) -> MathTex:
        """Return the fixed equation mobject."""

        return self._equation_mobject

    @property
    def caption_mobject(self) -> Text | None:
        """Return the optional fixed caption mobject."""

        return self._caption_mobject

    @property
    def panel_mobject(self) -> SurroundingRectangle:
        """Return the fixed surrounding panel mobject."""

        return self._panel_mobject

    @property
    def content_mobjects(self) -> tuple[MathTex, ...] | tuple[MathTex, Text]:
        """Return the equation followed by the optional caption."""

        if self._caption_mobject is None:
            return (self._equation_mobject,)
        return (self._equation_mobject, self._caption_mobject)

    @property
    def equation_source(self) -> str:
        """Return the immutable equation TeX source."""

        return self._equation_source

    @property
    def caption_text(self) -> str | None:
        """Return the immutable optional caption text."""

        return self._caption_text

    @property
    def content_buff(self) -> float:
        """Return the equation-to-caption spacing."""

        return self._content_buff

    @property
    def panel_buff(self) -> float:
        """Return the content-to-panel padding."""

        return self._panel_buff

    @property
    def equation_kwargs(self) -> dict[str, Any]:
        """Return a copy of the resolved ``MathTex`` options."""

        return dict(self._equation_kwargs)

    @property
    def caption_kwargs(self) -> dict[str, Any]:
        """Return a copy of the resolved ``Text`` options."""

        return dict(self._caption_kwargs)

    @property
    def panel_kwargs(self) -> dict[str, Any]:
        """Return a copy of the resolved panel options."""

        return dict(self._panel_kwargs)


def _nonempty_string(value: str, *, name: str) -> str:
    """Return one validated nonempty string."""

    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value.strip():
        raise ValueError(f"{name} must not be empty")
    return value


def _nonnegative_finite_float(value: float, *, name: str) -> float:
    """Return one validated finite nonnegative float."""

    if isinstance(value, (bool, np.bool_)):
        raise TypeError(f"{name} must be a real number")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise TypeError(f"{name} must be a real number") from exc
    if not np.isfinite(result):
        raise ValueError(f"{name} must be finite")
    if result < 0.0:
        raise ValueError(f"{name} must be nonnegative")
    return result


def _copied_options(
    values: Mapping[str, Any] | None,
    *,
    name: str,
    reserved_keys: tuple[str, ...],
) -> dict[str, Any]:
    """Return copied constructor options without adapter-owned arguments."""

    if values is None:
        return {}
    if not isinstance(values, Mapping):
        raise TypeError(f"{name} must be a mapping")
    options = dict(values)
    conflicts = tuple(key for key in reserved_keys if key in options)
    if conflicts:
        conflict_list = ", ".join(conflicts)
        raise ValueError(
            f"{name} cannot override component-owned arguments: "
            f"{conflict_list}"
        )
    return options
