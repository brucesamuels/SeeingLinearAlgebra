"""Renderer-independent mathematics for CP119: elementary matrices."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class ElementaryMatrixCase:
    """One elementary row operation and its matrix representation."""

    name: str
    operation_tex: str
    explanation: str
    elementary_matrix: FloatArray
    source_matrix: FloatArray
    product_matrix: FloatArray
    inverse_matrix: FloatArray
    inverse_operation_tex: str
    changed_rows: tuple[int, ...]


@dataclass(frozen=True)
class RowReductionStep:
    """One stage in a complete row reduction."""

    index: int
    operation_tex: str
    inverse_operation_tex: str
    elementary_matrix: FloatArray
    inverse_matrix: FloatArray
    source_matrix: FloatArray
    product_matrix: FloatArray
    changed_rows: tuple[int, ...]


@dataclass(frozen=True)
class ElementaryMatricesSnapshot:
    """Immutable data consumed by the CP119 presentation."""

    identity: FloatArray
    source_matrix: FloatArray
    swap: ElementaryMatrixCase
    scale: ElementaryMatrixCase
    replacement: ElementaryMatrixCase
    definition_tex: str
    left_multiplication_tex: str
    inverse_tex: str
    reduction_source: FloatArray
    reduction_steps: tuple[RowReductionStep, ...]
    cumulative_products: tuple[FloatArray, ...]
    reduction_matrix: FloatArray
    reverse_steps: tuple[RowReductionStep, ...]


class ElementaryMatrices:
    """Construct and apply elementary matrices in R^3."""

    DEFAULT_SOURCE = np.array(
        [
            [1.0, 2.0, 0.0],
            [3.0, 1.0, 1.0],
            [2.0, -1.0, 4.0],
        ],
        dtype=float,
    )

    REDUCTION_SOURCE = np.array(
        [
            [1.0, 2.0, 1.0],
            [0.0, 1.0, 3.0],
            [0.0, 0.0, 2.0],
        ],
        dtype=float,
    )

    def __init__(self, source_matrix: Iterable[Iterable[float]] | FloatArray | None = None) -> None:
        matrix = np.array(
            self.DEFAULT_SOURCE if source_matrix is None else source_matrix,
            dtype=float,
            copy=True,
        )
        if matrix.shape != (3, 3):
            raise ValueError("source_matrix must have shape (3, 3).")
        if not np.isfinite(matrix).all():
            raise ValueError("source_matrix entries must be finite.")
        self._source = matrix

    @property
    def source_matrix(self) -> FloatArray:
        return self._source.copy()

    @staticmethod
    def identity(size: int = 3) -> FloatArray:
        if not isinstance(size, int) or size <= 0:
            raise ValueError("size must be a positive integer.")
        return np.eye(size, dtype=float)

    @staticmethod
    def row_swap_matrix(size: int, first: int, second: int) -> FloatArray:
        ElementaryMatrices._validate_row_indices(size, first, second)
        if first == second:
            raise ValueError("row swap requires two distinct rows.")
        result = np.eye(size, dtype=float)
        result[[first, second]] = result[[second, first]]
        return result

    @staticmethod
    def row_scale_matrix(size: int, row: int, factor: float) -> FloatArray:
        ElementaryMatrices._validate_row_indices(size, row)
        if not np.isfinite(factor) or abs(float(factor)) < 1e-12:
            raise ValueError("scale factor must be finite and nonzero.")
        result = np.eye(size, dtype=float)
        result[row, row] = float(factor)
        return result

    @staticmethod
    def row_replacement_matrix(
        size: int,
        target: int,
        source: int,
        multiple: float,
    ) -> FloatArray:
        ElementaryMatrices._validate_row_indices(size, target, source)
        if target == source:
            raise ValueError("target and source rows must be distinct.")
        if not np.isfinite(multiple):
            raise ValueError("replacement multiple must be finite.")
        result = np.eye(size, dtype=float)
        result[target, source] = float(multiple)
        return result

    @staticmethod
    def apply(elementary_matrix: FloatArray, matrix: FloatArray) -> FloatArray:
        e = np.array(elementary_matrix, dtype=float, copy=True)
        a = np.array(matrix, dtype=float, copy=True)
        if e.ndim != 2 or e.shape[0] != e.shape[1]:
            raise ValueError("elementary_matrix must be square.")
        if a.ndim != 2 or a.shape[0] != e.shape[0]:
            raise ValueError("matrix must have the same number of rows as elementary_matrix.")
        if not np.isfinite(e).all() or not np.isfinite(a).all():
            raise ValueError("matrix entries must be finite.")
        return e @ a

    def case(self, name: str) -> ElementaryMatrixCase:
        cases = self._cases()
        try:
            case = cases[name]
        except KeyError as exc:
            raise KeyError(f"unknown elementary-matrix case: {name}") from exc
        return ElementaryMatrixCase(
            name=case.name,
            operation_tex=case.operation_tex,
            explanation=case.explanation,
            elementary_matrix=case.elementary_matrix.copy(),
            source_matrix=case.source_matrix.copy(),
            product_matrix=case.product_matrix.copy(),
            inverse_matrix=case.inverse_matrix.copy(),
            inverse_operation_tex=case.inverse_operation_tex,
            changed_rows=case.changed_rows,
        )

    def reduction_steps(self) -> tuple[RowReductionStep, ...]:
        current = self.REDUCTION_SOURCE.copy()
        specs = (
            (
                r"R_3\leftarrow \tfrac12R_3",
                r"R_3\leftarrow 2R_3",
                self.row_scale_matrix(3, 2, 0.5),
                self.row_scale_matrix(3, 2, 2.0),
                (2,),
            ),
            (
                r"R_2\leftarrow R_2-3R_3",
                r"R_2\leftarrow R_2+3R_3",
                self.row_replacement_matrix(3, 1, 2, -3.0),
                self.row_replacement_matrix(3, 1, 2, 3.0),
                (1,),
            ),
            (
                r"R_1\leftarrow R_1-R_3",
                r"R_1\leftarrow R_1+R_3",
                self.row_replacement_matrix(3, 0, 2, -1.0),
                self.row_replacement_matrix(3, 0, 2, 1.0),
                (0,),
            ),
            (
                r"R_1\leftarrow R_1-2R_2",
                r"R_1\leftarrow R_1+2R_2",
                self.row_replacement_matrix(3, 0, 1, -2.0),
                self.row_replacement_matrix(3, 0, 1, 2.0),
                (0,),
            ),
        )
        steps: list[RowReductionStep] = []
        for index, (operation, inverse_operation, e, e_inverse, changed_rows) in enumerate(specs, start=1):
            product = self.apply(e, current)
            steps.append(
                RowReductionStep(
                    index=index,
                    operation_tex=operation,
                    inverse_operation_tex=inverse_operation,
                    elementary_matrix=e.copy(),
                    inverse_matrix=e_inverse.copy(),
                    source_matrix=current.copy(),
                    product_matrix=product.copy(),
                    changed_rows=changed_rows,
                )
            )
            current = product
        return tuple(steps)

    def cumulative_products(self) -> tuple[FloatArray, ...]:
        cumulative = np.eye(3, dtype=float)
        products: list[FloatArray] = []
        for step in self.reduction_steps():
            cumulative = step.elementary_matrix @ cumulative
            products.append(cumulative.copy())
        return tuple(products)

    def reverse_steps(self) -> tuple[RowReductionStep, ...]:
        result: list[RowReductionStep] = []
        for reverse_index, step in enumerate(reversed(self.reduction_steps()), start=1):
            result.append(
                RowReductionStep(
                    index=step.index,
                    operation_tex=step.inverse_operation_tex,
                    inverse_operation_tex=step.operation_tex,
                    elementary_matrix=step.inverse_matrix.copy(),
                    inverse_matrix=step.elementary_matrix.copy(),
                    source_matrix=step.product_matrix.copy(),
                    product_matrix=step.source_matrix.copy(),
                    changed_rows=step.changed_rows,
                )
            )
        return tuple(result)

    def snapshot(self) -> ElementaryMatricesSnapshot:
        steps = self.reduction_steps()
        cumulative = self.cumulative_products()
        return ElementaryMatricesSnapshot(
            identity=self.identity(3),
            source_matrix=self.source_matrix,
            swap=self.case("swap"),
            scale=self.case("scale"),
            replacement=self.case("replacement"),
            definition_tex=(
                r"E\text{ is obtained by performing one elementary row operation on }I"
            ),
            left_multiplication_tex=(
                r"(EA)_{i*}=e_{i1}R_1+e_{i2}R_2+e_{i3}R_3"
            ),
            inverse_tex=r"E^{-1}(EA)=A",
            reduction_source=self.REDUCTION_SOURCE.copy(),
            reduction_steps=steps,
            cumulative_products=cumulative,
            reduction_matrix=cumulative[-1].copy(),
            reverse_steps=self.reverse_steps(),
        )

    def _cases(self) -> dict[str, ElementaryMatrixCase]:
        source = self.source_matrix

        swap_e = self.row_swap_matrix(3, 0, 1)
        scale_e = self.row_scale_matrix(3, 1, -2)
        replacement_e = self.row_replacement_matrix(3, 2, 0, 2)

        return {
            "swap": ElementaryMatrixCase(
                name="swap",
                operation_tex=r"R_1\leftrightarrow R_2",
                explanation="Interchange rows 1 and 2.",
                elementary_matrix=swap_e,
                source_matrix=source,
                product_matrix=self.apply(swap_e, source),
                inverse_matrix=swap_e.copy(),
                inverse_operation_tex=r"R_1\leftrightarrow R_2",
                changed_rows=(0, 1),
            ),
            "scale": ElementaryMatrixCase(
                name="scale",
                operation_tex=r"R_2\leftarrow -2R_2",
                explanation="Multiply row 2 by -2.",
                elementary_matrix=scale_e,
                source_matrix=source,
                product_matrix=self.apply(scale_e, source),
                inverse_matrix=self.row_scale_matrix(3, 1, -0.5),
                inverse_operation_tex=r"R_2\leftarrow -\tfrac12R_2",
                changed_rows=(1,),
            ),
            "replacement": ElementaryMatrixCase(
                name="replacement",
                operation_tex=r"R_3\leftarrow R_3+2R_1",
                explanation="Add twice row 1 to row 3.",
                elementary_matrix=replacement_e,
                source_matrix=source,
                product_matrix=self.apply(replacement_e, source),
                inverse_matrix=self.row_replacement_matrix(3, 2, 0, -2),
                inverse_operation_tex=r"R_3\leftarrow R_3-2R_1",
                changed_rows=(2,),
            ),
        }

    @staticmethod
    def _validate_row_indices(size: int, *rows: int) -> None:
        if not isinstance(size, int) or size <= 0:
            raise ValueError("size must be a positive integer.")
        for row in rows:
            if not isinstance(row, int) or not 0 <= row < size:
                raise ValueError("row index is out of range.")
