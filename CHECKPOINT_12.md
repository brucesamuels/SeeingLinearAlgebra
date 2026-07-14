# Engine v0.3 - Checkpoint 12

## Architectural goal

Add the renderer-independent orchestration layer for coefficient-sweep
geometry.

```text
CoefficientSweepPath
         |
         v
LinearCombinationSnapshot
         |
         v
LinearCombinationGeometry
         |
         v
LinearCombinationGeometrySnapshot
```

`LinearCombinationGeometryPath` composes the two existing layers and returns
complete mathematical segment geometry for any progress value in `[0, 1]`.

## Why this belongs in the engine

A scene should not know how coefficients are interpolated, how scaled terms
are accumulated, or how tip-to-tail segments are constructed.  Those are
renderer-independent responsibilities already owned by tested classes.

This orchestration layer provides one stable entry point for future display
adapters and renderers while preserving those boundaries.

## Composition rule

For progress `t`, the class performs exactly two delegated operations:

```python
mathematical_snapshot = coefficient_sweep_path.snapshot(t)
geometry_snapshot = geometry.snapshot(mathematical_snapshot)
```

It does not reproduce either operation internally.

## Scope deliberately excluded

Checkpoint 12 does not add:

- display projection;
- display-coordinate snapshots;
- arrow styling;
- Manim objects;
- easing or animation timing;
- a smoke scene.

## Existing stable classes left unchanged

The checkpoint does not modify:

- `LinearCombination`
- `LinearCombinationSnapshot`
- `CoefficientSweepPath`
- `LinearCombinationGeometry`
- `LinearCombinationGeometrySnapshot`
- the complete rank-collapse pipeline
- any Manim class or scene

Only the public export in `engine/__init__.py` is extended by the installer.

## New files

- `engine/linear_combination_geometry_path.py`
- `tests/test_linear_combination_geometry_path.py`
- `scripts/check_linear_combination_geometry_path.zsh`
- `CHECKPOINT_12.md`

The installer adds:

```python
from .linear_combination_geometry_path import LinearCombinationGeometryPath
```

## Public interface

```python
combination = LinearCombination(vectors)
coefficient_path = CoefficientSweepPath(
    combination,
    start_coefficients,
    end_coefficients,
)
geometry_path = LinearCombinationGeometryPath(coefficient_path)

snapshot = geometry_path.snapshot(0.5)
# equivalent:
snapshot = geometry_path(0.5)
```

A custom converter may be injected:

```python
geometry_path = LinearCombinationGeometryPath(
    coefficient_path,
    LinearCombinationGeometry(),
)
```

Useful properties are:

```python
geometry_path.coefficient_sweep_path
geometry_path.geometry
geometry_path.linear_combination
geometry_path.vector_count
geometry_path.dimension
```

## Focused test coverage

The eleven tests cover:

1. start-state composition;
2. midpoint interpolation and geometry;
3. end-state composition;
4. exactly one delegation to each existing layer;
5. exact component retention and metadata delegation;
6. default geometry-converter construction;
7. independent vector count and ambient dimension;
8. the single-vector scalar-endpoint case;
9. constructor type validation;
10. propagation of coefficient-path progress validation;
11. callable shorthand behavior.

Expected focused result:

```text
11 passed
```

Expected complete-suite result after the Checkpoint 11 baseline of 143 tests:

```text
154 passed
```

## Commands

From the repository root:

```zsh
./scripts/check_linear_combination_geometry_path.zsh
python -m pytest -q
```

## Next logical checkpoint

Checkpoint 13 should add the display layer for linear-combination geometry.  It
should use the existing `LinearDisplayProjector` and introduce a thin
`LinearCombinationGeometryDisplayAdapter` that projects all segment endpoints
without changing mathematical topology or recomputing any linear combination.
