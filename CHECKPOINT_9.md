# Engine v0.3 - Checkpoint 9

## Architectural goal

Begin the engine's second reusable animation family at the mathematical layer.
Checkpoint 8 completed the end-to-end rank-collapse pipeline.  The next family,
coefficient sweeps, needs a stable definition of a linear-combination state
before it needs interpolation, display projection, or renderer code.

Checkpoint 9 adds that foundation:

```text
fixed vectors + coefficients
            |
            v
    LinearCombination
            |
            v
LinearCombinationSnapshot
```

A snapshot contains:

- the coefficient vector;
- each scaled term `c_i v_i`;
- cumulative tip-to-tail partial sums, beginning at the origin;
- the final resultant vector.

## Why this belongs in the engine

Linear combinations recur throughout the project: span, basis coordinates,
column space, change of basis, projections, and later coefficient-sweep
animations.  Encoding the mathematics once prevents future scenes from
reimplementing coefficient arithmetic or tip-to-tail geometry.

The class is:

- renderer independent;
- display independent;
- dimension independent;
- independent of the number of vectors;
- immutable at its public array boundaries;
- suitable for later path and adapter layers.

## Existing stable classes left unchanged

Checkpoint 9 does not modify the completed rank-collapse stack:

- `RankCollapse`
- `RankCollapsePath`
- `RankCollapseGeometry`
- `RankCollapseGeometryPath`
- `LinearDisplayProjector`
- `RankCollapseGeometryDisplayAdapter`
- `ManimRankCollapseGeometry`

No Manim file or smoke scene changes in this checkpoint.

## New files

- `engine/linear_combination.py`
- `tests/test_linear_combination.py`
- `scripts/check_linear_combination.zsh`
- `CHECKPOINT_9.md`

The installer also adds this public import to `engine/__init__.py`:

```python
from .linear_combination import LinearCombination, LinearCombinationSnapshot
```

## Focused test coverage

The ten tests cover:

1. a two-vector combination in `R^2`;
2. independence of vector count and ambient dimension;
3. cumulative tip-to-tail partial sums;
4. zero coefficients;
5. a single vector with a scalar coefficient;
6. coefficient-count validation;
7. vector-shape validation;
8. finite-number validation;
9. defensive copying and read-only public arrays;
10. rejection of internally inconsistent snapshots.

Expected focused result:

```text
10 passed
```

Expected full-suite result after the Checkpoint 8 baseline of 110 tests:

```text
120 passed
```

## Commands

From the repository root:

```zsh
./scripts/check_linear_combination.zsh
python -m pytest -q
```

## Next logical checkpoint

Checkpoint 10 should add a renderer-independent `CoefficientSweepPath` that
interpolates between coefficient vectors and returns
`LinearCombinationSnapshot` objects.  That path should delegate all linear-
combination mathematics to the class introduced here rather than duplicating
it.
