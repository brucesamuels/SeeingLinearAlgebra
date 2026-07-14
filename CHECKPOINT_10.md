# Engine v0.3 - Checkpoint 10

## Architectural goal

Add a renderer-independent path through coefficient space for the linear-
combination family introduced in Checkpoint 9.

```text
fixed vectors
     +
start/end coefficient vectors
             |
             v
    CoefficientSweepPath
             |
             v
 LinearCombinationSnapshot
```

For progress `t` in `[0, 1]`, the path computes

```text
c(t) = (1 - t)c_start + t c_end
```

and delegates the resulting coefficient vector to `LinearCombination`.

## Why this belongs in the engine

Coefficient sweeps are mathematical paths, not renderer behavior.  They will
support future scenes about span, basis coordinates, column space, dependence,
and change of basis.  Keeping interpolation in the engine gives every renderer
the same coefficient states and prevents scenes from reimplementing the
mathematics.

The path is:

- renderer independent;
- display independent;
- dimension independent;
- independent of vector count;
- immutable at its public array boundaries;
- composable with the Checkpoint 9 mathematical model.

## Scope deliberately excluded

Checkpoint 10 does not add:

- display projection;
- arrow or polyline geometry;
- easing or timing policies;
- Manim adapters;
- a smoke scene.

Those belong in later layers after the mathematical path is stable.

## Existing stable classes left unchanged

The checkpoint does not modify:

- `LinearCombination`
- `LinearCombinationSnapshot`
- `RankCollapse`
- `RankCollapsePath`
- `RankCollapseGeometry`
- `RankCollapseGeometryPath`
- `LinearDisplayProjector`
- `RankCollapseGeometryDisplayAdapter`
- `ManimRankCollapseGeometry`

## New files

- `engine/coefficient_sweep_path.py`
- `tests/test_coefficient_sweep_path.py`
- `scripts/check_coefficient_sweep_path.zsh`
- `CHECKPOINT_10.md`

The installer adds this public import to `engine/__init__.py`:

```python
from .coefficient_sweep_path import CoefficientSweepPath
```

## Public interface

```python
path = CoefficientSweepPath(
    linear_combination,
    start_coefficients,
    end_coefficients,
)

coefficients = path.coefficients_at(progress)
snapshot = path.snapshot(progress)
snapshot = path(progress)
```

The endpoint vectors and returned public coefficient arrays are owned,
read-only copies.

## Focused test coverage

The eleven tests cover:

1. exact start and end states;
2. midpoint interpolation;
3. full scaled-term and tip-to-tail state at an interior point;
4. independence of vector count and ambient dimension;
5. scalar endpoints for a one-vector family;
6. delegation of snapshot construction to `LinearCombination`;
7. endpoint validation through the existing mathematical model;
8. progress validation;
9. defensive copying and read-only public arrays;
10. independent arrays returned by `coefficients_at`;
11. callable shorthand behavior.

Expected focused result:

```text
11 passed
```

Expected complete-suite result after the Checkpoint 9 baseline of 120 tests:

```text
131 passed
```

## Commands

From the repository root:

```zsh
./scripts/check_coefficient_sweep_path.zsh
python -m pytest -q
```

## Next logical checkpoint

Checkpoint 11 should add renderer-independent linear-combination geometry.  It
should convert a `LinearCombinationSnapshot` into explicit arrow segments for
scaled terms, cumulative tip-to-tail placement, and the resultant, while
remaining in mathematical coordinates and leaving display projection for the
following checkpoint.
