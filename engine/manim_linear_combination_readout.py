"""Thin Manim readout for one linear-combination snapshot.

This renderer-specific module consumes the existing renderer-independent
``LinearCombinationSnapshot`` interface.  It displays the coefficient vector
and resulting vector as decimal column matrices and updates the same numeric
mobjects in place for later snapshots.

No vector scaling, summation, coefficient interpolation, geometry, or display
projection is performed here.  All mathematical values are supplied upstream.
"""

from __future__ import annotations

from collections.abc import Mapping
from numbers import Integral, Real
from typing import Any, Protocol

import numpy as np
from manim import DOWN, LEFT, RIGHT, DecimalMatrix, DecimalNumber, MathTex, VGroup


class _LinearCombinationSnapshotLike(Protocol):
    """Canonical mathematical fields consumed by the readout adapter."""

    coefficients: np.ndarray
    result: np.ndarray


class ManimLinearCombinationReadout(VGroup):
    """Display and update coefficients and the resulting vector.

    Parameters
    ----------
    snapshot
        A renderer-independent linear-combination snapshot exposing the
        canonical one-dimensional ``coefficients`` and ``result`` arrays.
    coefficient_label
        MathTex source shown beside the coefficient column vector.
    result_label
        MathTex source shown beside the result column vector.
    num_decimal_places
        Fixed number of digits shown after the decimal point.
    include_sign
        Whether positive values and zero display an explicit plus sign.
        Keeping sign width fixed is useful during coefficient sweeps.
    label_kwargs
        Optional style arguments copied and passed to both ``MathTex`` labels.
    matrix_kwargs
        Optional style and layout arguments copied and passed to both
        ``DecimalMatrix`` objects.  Matrix data and entry construction remain
        owned by this adapter.
    row_buff
        Horizontal space between each label and its column vector.
    block_buff
        Vertical space between the coefficient and result rows.

    Notes
    -----
    The coefficient count and result dimension are structural.  Later
    snapshots must retain both sizes so every Manim mobject can be created
    exactly once and updated in place.
    """

    def __init__(
        self,
        snapshot: _LinearCombinationSnapshotLike,
        *,
        coefficient_label: str = r"\mathbf{c} =",
        result_label: str = r"\mathbf{r} =",
        num_decimal_places: int = 2,
        include_sign: bool = True,
        label_kwargs: Mapping[str, Any] | None = None,
        matrix_kwargs: Mapping[str, Any] | None = None,
        row_buff: float = 0.25,
        block_buff: float = 0.30,
    ) -> None:
        coefficients, result = _snapshot_values(snapshot)
        decimal_places = _decimal_places(num_decimal_places)
        horizontal_buff = _nonnegative_finite(row_buff, name="row_buff")
        vertical_buff = _nonnegative_finite(block_buff, name="block_buff")
        coefficient_tex = _nonempty_label(coefficient_label, name="coefficient_label")
        result_tex = _nonempty_label(result_label, name="result_label")
        labels = dict(label_kwargs or {})
        matrices = _matrix_kwargs(matrix_kwargs)

        super().__init__()

        entry_config = {
            "num_decimal_places": decimal_places,
            "include_sign": bool(include_sign),
        }

        self._coefficient_label_mobject = MathTex(coefficient_tex, **labels)
        self._result_label_mobject = MathTex(result_tex, **labels)
        self._coefficient_matrix = DecimalMatrix(
            coefficients.reshape(-1, 1),
            element_to_mobject_config=entry_config,
            **matrices,
        )
        self._result_matrix = DecimalMatrix(
            result.reshape(-1, 1),
            element_to_mobject_config=entry_config,
            **matrices,
        )

        self._coefficient_entries = tuple(self._coefficient_matrix.get_entries())
        self._result_entries = tuple(self._result_matrix.get_entries())
        _validate_decimal_entries(
            self._coefficient_entries,
            expected_count=coefficients.size,
            name="coefficient",
        )
        _validate_decimal_entries(
            self._result_entries,
            expected_count=result.size,
            name="result",
        )

        self._coefficient_row = VGroup(
            self._coefficient_label_mobject,
            self._coefficient_matrix,
        ).arrange(RIGHT, buff=horizontal_buff)
        self._result_row = VGroup(
            self._result_label_mobject,
            self._result_matrix,
        ).arrange(RIGHT, buff=horizontal_buff)

        self.add(self._coefficient_row, self._result_row)
        self.arrange(DOWN, aligned_edge=LEFT, buff=vertical_buff)

        self._snapshot = snapshot
        self._vector_count = int(coefficients.size)
        self._dimension = int(result.size)

    @property
    def mobject(self) -> ManimLinearCombinationReadout:
        """Return the root Manim mobject represented by this adapter."""

        return self

    @property
    def snapshot(self) -> _LinearCombinationSnapshotLike:
        """Return the exact mathematical snapshot currently displayed."""

        return self._snapshot

    @property
    def vector_count(self) -> int:
        """Return the structural number of coefficients."""

        return self._vector_count

    @property
    def dimension(self) -> int:
        """Return the structural dimension of the resulting vector."""

        return self._dimension

    @property
    def coefficient_label_mobject(self) -> MathTex:
        """Return the fixed coefficient label."""

        return self._coefficient_label_mobject

    @property
    def result_label_mobject(self) -> MathTex:
        """Return the fixed result label."""

        return self._result_label_mobject

    @property
    def coefficient_matrix(self) -> DecimalMatrix:
        """Return the fixed coefficient column matrix."""

        return self._coefficient_matrix

    @property
    def result_matrix(self) -> DecimalMatrix:
        """Return the fixed result column matrix."""

        return self._result_matrix

    @property
    def coefficient_entries(self) -> tuple[DecimalNumber, ...]:
        """Return the fixed coefficient ``DecimalNumber`` objects."""

        return self._coefficient_entries

    @property
    def result_entries(self) -> tuple[DecimalNumber, ...]:
        """Return the fixed result ``DecimalNumber`` objects."""

        return self._result_entries

    def update_from_snapshot(
        self,
        snapshot: _LinearCombinationSnapshotLike,
    ) -> ManimLinearCombinationReadout:
        """Update all numeric entries in place from a later snapshot.

        The complete incoming state is validated before any displayed number
        is mutated.  Changed coefficient count or result dimension raises
        ``ValueError`` because either change would violate the create-once
        mobject contract.
        """

        coefficients, result = _snapshot_values(snapshot)
        if coefficients.size != self.vector_count:
            raise ValueError(
                "coefficient count changed: "
                f"expected {self.vector_count}, received {coefficients.size}"
            )
        if result.size != self.dimension:
            raise ValueError(
                "result dimension changed: "
                f"expected {self.dimension}, received {result.size}"
            )

        _update_entries(self._coefficient_entries, coefficients)
        _update_entries(self._result_entries, result)
        self._snapshot = snapshot
        return self


def _snapshot_values(
    snapshot: object,
) -> tuple[np.ndarray, np.ndarray]:
    if not hasattr(snapshot, "coefficients") or not hasattr(snapshot, "result"):
        raise TypeError("snapshot must expose coefficients and result")

    coefficients = _finite_vector(
        getattr(snapshot, "coefficients"),
        name="coefficients",
    )
    result = _finite_vector(getattr(snapshot, "result"), name="result")
    return coefficients, result


def _finite_vector(values: object, *, name: str) -> np.ndarray:
    array = np.asarray(values, dtype=float)
    if array.ndim != 1:
        raise ValueError(f"{name} must be a one-dimensional array")
    if array.size < 1:
        raise ValueError(f"{name} must contain at least one value")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")
    return array.astype(float, copy=True)


def _decimal_places(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, Integral):
        raise TypeError("num_decimal_places must be an integer")
    result = int(value)
    if result < 0:
        raise ValueError("num_decimal_places must be nonnegative")
    return result


def _nonnegative_finite(value: float, *, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real scalar")
    result = float(value)
    if not np.isfinite(result):
        raise ValueError(f"{name} must be finite")
    if result < 0.0:
        raise ValueError(f"{name} must be nonnegative")
    return result


def _nonempty_label(value: str, *, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value.strip():
        raise ValueError(f"{name} must not be empty")
    return value


def _matrix_kwargs(values: Mapping[str, Any] | None) -> dict[str, Any]:
    kwargs = dict(values or {})
    reserved = {
        "matrix",
        "element_to_mobject",
        "element_to_mobject_config",
    }
    conflicting = sorted(reserved.intersection(kwargs))
    if conflicting:
        joined = ", ".join(conflicting)
        raise ValueError(
            "matrix_kwargs cannot override adapter-owned arguments: " + joined
        )
    return kwargs


def _validate_decimal_entries(
    entries: tuple[object, ...],
    *,
    expected_count: int,
    name: str,
) -> None:
    if len(entries) != expected_count:
        raise RuntimeError(
            f"{name} matrix produced {len(entries)} entries; "
            f"expected {expected_count}"
        )
    if not all(isinstance(entry, DecimalNumber) for entry in entries):
        raise TypeError(f"{name} matrix entries must be DecimalNumber objects")


def _update_entries(
    entries: tuple[DecimalNumber, ...],
    values: np.ndarray,
) -> None:
    for entry, value in zip(entries, values, strict=True):
        center = entry.get_center().copy()
        entry.set_value(float(value))
        entry.move_to(center)
