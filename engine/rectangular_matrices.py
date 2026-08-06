"""Renderer-independent mathematics for CP125.

Checkpoint 125 introduces rectangular matrices through the map
A : R^n -> R^m.  The lesson separates matrix shape from rank and uses the
column space and null space to describe what can be reached and how uniquely.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RectangularShapeCase:
    """One canonical matrix shape used in the classroom comparison."""

    name: str
    rows: int
    columns: int
    relation_tex: str
    map_tex: str
    rank_bound_tex: str
    full_rank_tex: str
    full_rank_nullity: int
    can_be_onto: bool
    can_be_one_to_one: bool
    full_rank_reachability: str
    full_rank_uniqueness: str
    geometry_summary: str


@dataclass(frozen=True)
class RectangularMatricesSnapshot:
    """Immutable mathematical data used by the CP125 presentation."""

    dimension_equation_tex: str
    map_tex: str
    equation_count_tex: str
    column_combination_tex: str
    consistency_tex: str
    rank_bound_tex: str
    nullity_tex: str
    augmented_rank_tex: str
    cases: tuple[RectangularShapeCase, ...]


class RectangularMatrices:
    """Describe square, tall, and wide systems without assuming invertibility."""

    def __init__(self, *, rows: int = 3, columns: int = 2) -> None:
        self._validate_dimension(rows, "rows")
        self._validate_dimension(columns, "columns")
        self._rows = rows
        self._columns = columns
        self._cases = self._build_cases()

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def columns(self) -> int:
        return self._columns

    @staticmethod
    def dimension_equation_tex() -> str:
        return r"A_{m\times n}\mathbf{x}_{n\times 1}=\mathbf{b}_{m\times 1}"

    @staticmethod
    def map_tex() -> str:
        return r"A:\mathbb{R}^n\longrightarrow\mathbb{R}^m"

    @staticmethod
    def equation_count_tex() -> str:
        return r"m\ \text{rows}=m\ \text{equations},\qquad n\ \text{columns}=n\ \text{unknowns}"

    @staticmethod
    def column_combination_tex() -> str:
        return r"A\mathbf{x}=x_1\mathbf{a}_1+\cdots+x_n\mathbf{a}_n=\mathbf{b}"

    @staticmethod
    def consistency_tex() -> str:
        return r"A\mathbf{x}=\mathbf{b}\ \text{is solvable}\iff \mathbf{b}\in\operatorname{Col}(A)"

    @staticmethod
    def rank_bound_tex() -> str:
        return r"r=\operatorname{rank}(A)\le \min(m,n)"

    @staticmethod
    def nullity_tex() -> str:
        return r"\dim N(A)=n-r"

    @staticmethod
    def augmented_rank_tex() -> str:
        return r"\operatorname{rank}(A)=\operatorname{rank}([A\mid\mathbf{b}])"

    @staticmethod
    def maximum_rank(rows: int, columns: int) -> int:
        RectangularMatrices._validate_dimension(rows, "rows")
        RectangularMatrices._validate_dimension(columns, "columns")
        return min(rows, columns)

    @staticmethod
    def full_rank_nullity(rows: int, columns: int) -> int:
        return columns - RectangularMatrices.maximum_rank(rows, columns)

    @staticmethod
    def can_be_onto(rows: int, columns: int) -> bool:
        RectangularMatrices._validate_dimension(rows, "rows")
        RectangularMatrices._validate_dimension(columns, "columns")
        return columns >= rows

    @staticmethod
    def can_be_one_to_one(rows: int, columns: int) -> bool:
        RectangularMatrices._validate_dimension(rows, "rows")
        RectangularMatrices._validate_dimension(columns, "columns")
        return rows >= columns

    @property
    def cases(self) -> tuple[RectangularShapeCase, ...]:
        return self._cases

    def snapshot(self) -> RectangularMatricesSnapshot:
        return RectangularMatricesSnapshot(
            dimension_equation_tex=self.dimension_equation_tex(),
            map_tex=self.map_tex(),
            equation_count_tex=self.equation_count_tex(),
            column_combination_tex=self.column_combination_tex(),
            consistency_tex=self.consistency_tex(),
            rank_bound_tex=self.rank_bound_tex(),
            nullity_tex=self.nullity_tex(),
            augmented_rank_tex=self.augmented_rank_tex(),
            cases=self.cases,
        )

    @classmethod
    def _build_cases(cls) -> tuple[RectangularShapeCase, ...]:
        return (
            RectangularShapeCase(
                name="Square",
                rows=2,
                columns=2,
                relation_tex=r"m=n",
                map_tex=r"\mathbb{R}^2\to\mathbb{R}^2",
                rank_bound_tex=r"r\le2",
                full_rank_tex=r"r=2",
                full_rank_nullity=cls.full_rank_nullity(2, 2),
                can_be_onto=cls.can_be_onto(2, 2),
                can_be_one_to_one=cls.can_be_one_to_one(2, 2),
                full_rank_reachability="Every output is reachable.",
                full_rank_uniqueness="Each output has exactly one input.",
                geometry_summary="Full rank can be both onto and one-to-one.",
            ),
            RectangularShapeCase(
                name="Tall",
                rows=3,
                columns=2,
                relation_tex=r"m>n",
                map_tex=r"\mathbb{R}^2\to\mathbb{R}^3",
                rank_bound_tex=r"r\le2",
                full_rank_tex=r"r=n=2",
                full_rank_nullity=cls.full_rank_nullity(3, 2),
                can_be_onto=cls.can_be_onto(3, 2),
                can_be_one_to_one=cls.can_be_one_to_one(3, 2),
                full_rank_reachability="Only a plane in the output space is reachable.",
                full_rank_uniqueness="A reachable output has at most one input.",
                geometry_summary="Full column rank can be one-to-one, but not onto.",
            ),
            RectangularShapeCase(
                name="Wide",
                rows=2,
                columns=3,
                relation_tex=r"m<n",
                map_tex=r"\mathbb{R}^3\to\mathbb{R}^2",
                rank_bound_tex=r"r\le2",
                full_rank_tex=r"r=m=2",
                full_rank_nullity=cls.full_rank_nullity(2, 3),
                can_be_onto=cls.can_be_onto(2, 3),
                can_be_one_to_one=cls.can_be_one_to_one(2, 3),
                full_rank_reachability="Every output can be reachable.",
                full_rank_uniqueness="Each reachable output has infinitely many inputs.",
                geometry_summary="Full row rank can be onto, but not one-to-one.",
            ),
        )

    @staticmethod
    def _validate_dimension(value: int, name: str) -> None:
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer.")
