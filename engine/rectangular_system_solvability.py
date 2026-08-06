"""Renderer-independent mathematics for CP126.

Checkpoint 126 studies solvability for overdetermined and underdetermined
systems.  Matrix shape limits what is possible, while rank and the location of
the right-hand side decide what actually happens.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


MatrixData = tuple[tuple[int, ...], ...]
VectorData = tuple[int, ...]


@dataclass(frozen=True)
class OverdeterminedSystemSnapshot:
    """Worked full-column-rank 3-by-2 example."""

    matrix: MatrixData
    compatible_rhs: VectorData
    incompatible_rhs: VectorData
    compatible_solution: VectorData
    matrix_tex: str
    compatible_augmented_tex: str
    compatible_reduced_tex: str
    incompatible_augmented_tex: str
    incompatible_reduced_tex: str
    column_space_condition_tex: str
    full_column_rank_tex: str


@dataclass(frozen=True)
class UnderdeterminedSystemSnapshot:
    """Worked full-row-rank 2-by-3 example and a rank-deficient contrast."""

    matrix: MatrixData
    rhs: VectorData
    particular_solution: VectorData
    null_vector: VectorData
    matrix_tex: str
    augmented_tex: str
    parameter_equations_tex: str
    complete_solution_tex: str
    full_row_rank_tex: str
    deficient_matrix: MatrixData
    deficient_rhs: VectorData
    deficient_augmented_tex: str
    deficient_reduced_tex: str


@dataclass(frozen=True)
class RectangularSystemSolvabilitySnapshot:
    """Complete immutable data used by the CP126 presentation."""

    common_consistency_tex: str
    augmented_rank_tex: str
    solution_count_tex: str
    overdetermined: OverdeterminedSystemSnapshot
    underdetermined: UnderdeterminedSystemSnapshot


class RectangularSystemSolvability:
    """Classify rectangular systems by consistency, rank, and nullity."""

    OVER_MATRIX: MatrixData = (
        (1, 0),
        (0, 1),
        (1, 1),
    )
    OVER_COMPATIBLE_RHS: VectorData = (2, -1, 1)
    OVER_INCOMPATIBLE_RHS: VectorData = (2, -1, 0)
    OVER_SOLUTION: VectorData = (2, -1)

    UNDER_MATRIX: MatrixData = (
        (1, 0, 1),
        (0, 1, 1),
    )
    UNDER_RHS: VectorData = (2, -1)
    UNDER_PARTICULAR: VectorData = (2, -1, 0)
    UNDER_NULL_VECTOR: VectorData = (-1, -1, 1)

    DEFICIENT_WIDE_MATRIX: MatrixData = (
        (1, 0, 1),
        (2, 0, 2),
    )
    DEFICIENT_WIDE_RHS: VectorData = (1, 0)

    @staticmethod
    def common_consistency_tex() -> str:
        return (
            r"A\mathbf{x}=\mathbf{b}\text{ is consistent}"
            r"\iff\mathbf{b}\in\operatorname{Col}(A)"
        )

    @staticmethod
    def augmented_rank_tex() -> str:
        return r"\operatorname{rank}(A)=\operatorname{rank}([A\mid\mathbf{b}])"

    @staticmethod
    def solution_count_tex() -> str:
        return (
            r"\text{if consistent, solution dimension}"
            r"=\dim N(A)=n-\operatorname{rank}(A)"
        )

    @staticmethod
    def nullity(columns: int, rank: int) -> int:
        RectangularSystemSolvability._validate_rank(columns, rank)
        return columns - rank

    @staticmethod
    def solvable_for_every_rhs(rows: int, rank: int) -> bool:
        RectangularSystemSolvability._validate_positive(rows, "rows")
        RectangularSystemSolvability._validate_rank(rows, rank)
        return rank == rows

    @staticmethod
    def unique_when_consistent(columns: int, rank: int) -> bool:
        RectangularSystemSolvability._validate_positive(columns, "columns")
        RectangularSystemSolvability._validate_rank(columns, rank)
        return rank == columns

    @staticmethod
    def solution_class(*, columns: int, rank: int, consistent: bool) -> str:
        """Return ``none``, ``unique``, or ``infinitely many``."""

        RectangularSystemSolvability._validate_positive(columns, "columns")
        RectangularSystemSolvability._validate_rank(columns, rank)
        if not consistent:
            return "none"
        if columns - rank == 0:
            return "unique"
        return "infinitely many"

    @staticmethod
    def matvec(matrix: MatrixData, vector: Sequence[int]) -> VectorData:
        if not matrix or not matrix[0]:
            raise ValueError("matrix must be nonempty")
        width = len(matrix[0])
        if any(len(row) != width for row in matrix):
            raise ValueError("matrix rows must have equal length")
        if len(vector) != width:
            raise ValueError("vector length must equal the number of columns")
        return tuple(sum(entry * value for entry, value in zip(row, vector)) for row in matrix)

    @classmethod
    def snapshot(cls) -> RectangularSystemSolvabilitySnapshot:
        over = OverdeterminedSystemSnapshot(
            matrix=cls.OVER_MATRIX,
            compatible_rhs=cls.OVER_COMPATIBLE_RHS,
            incompatible_rhs=cls.OVER_INCOMPATIBLE_RHS,
            compatible_solution=cls.OVER_SOLUTION,
            matrix_tex=r"A=\begin{bmatrix}1&0\\0&1\\1&1\end{bmatrix}",
            compatible_augmented_tex=(
                r"\left[\begin{array}{cc|c}1&0&2\\0&1&-1\\1&1&1\end{array}\right]"
            ),
            compatible_reduced_tex=(
                r"\left[\begin{array}{cc|c}1&0&2\\0&1&-1\\0&0&0\end{array}\right]"
            ),
            incompatible_augmented_tex=(
                r"\left[\begin{array}{cc|c}1&0&2\\0&1&-1\\1&1&0\end{array}\right]"
            ),
            incompatible_reduced_tex=(
                r"\left[\begin{array}{cc|c}1&0&2\\0&1&-1\\0&0&-1\end{array}\right]"
            ),
            column_space_condition_tex=r"b_3=b_1+b_2",
            full_column_rank_tex=(
                r"\operatorname{rank}(A)=n=2,\qquad N(A)=\{\mathbf{0}\}"
            ),
        )
        under = UnderdeterminedSystemSnapshot(
            matrix=cls.UNDER_MATRIX,
            rhs=cls.UNDER_RHS,
            particular_solution=cls.UNDER_PARTICULAR,
            null_vector=cls.UNDER_NULL_VECTOR,
            matrix_tex=r"A=\begin{bmatrix}1&0&1\\0&1&1\end{bmatrix}",
            augmented_tex=(
                r"\left[\begin{array}{ccc|c}1&0&1&2\\0&1&1&-1\end{array}\right]"
            ),
            parameter_equations_tex=r"z=t,\qquad x=2-t,\qquad y=-1-t",
            complete_solution_tex=(
                r"\mathbf{x}=\begin{bmatrix}2\\-1\\0\end{bmatrix}"
                r"+t\begin{bmatrix}-1\\-1\\1\end{bmatrix}"
                r"=\mathbf{x}_p+t\mathbf{v}"
            ),
            full_row_rank_tex=(
                r"\operatorname{rank}(A)=m=2,\qquad\dim N(A)=3-2=1"
            ),
            deficient_matrix=cls.DEFICIENT_WIDE_MATRIX,
            deficient_rhs=cls.DEFICIENT_WIDE_RHS,
            deficient_augmented_tex=(
                r"\left[\begin{array}{ccc|c}1&0&1&1\\2&0&2&0\end{array}\right]"
            ),
            deficient_reduced_tex=(
                r"\left[\begin{array}{ccc|c}1&0&1&1\\0&0&0&-2\end{array}\right]"
            ),
        )
        return RectangularSystemSolvabilitySnapshot(
            common_consistency_tex=cls.common_consistency_tex(),
            augmented_rank_tex=cls.augmented_rank_tex(),
            solution_count_tex=cls.solution_count_tex(),
            overdetermined=over,
            underdetermined=under,
        )

    @staticmethod
    def _validate_positive(value: int, name: str) -> None:
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer")

    @staticmethod
    def _validate_rank(maximum: int, rank: int) -> None:
        RectangularSystemSolvability._validate_positive(maximum, "maximum")
        if isinstance(rank, bool) or not isinstance(rank, int) or not 0 <= rank <= maximum:
            raise ValueError("rank must be an integer between zero and the dimension bound")
