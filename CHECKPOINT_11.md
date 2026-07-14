# Engine v0.3 - Checkpoint 11

## Architectural goal

Add renderer-independent arrow geometry for the linear-combination family.

```text
LinearCombinationSnapshot
          |
          v
LinearCombinationGeometry
          |
          v
LinearCombinationGeometrySnapshot
```

Each scaled term becomes a mathematical segment whose tail is the preceding
partial sum and whose tip is the following partial sum.  The resultant is a
separate segment from the origin to the final sum.

## Why this belongs in the engine

Tip-to-tail placement is mathematical geometry, not Manim behavior.  Every
renderer should receive the same segment endpoints.  Centralizing this layer
also prevents scenes from reconstructing partial sums or embedding linear-
combination logic in drawing code.

The geometry is:

- renderer independent;
- display independent;
- dimension independent;
- independent of vector count;
- immutable at its public array boundaries;
- traceable to the exact `LinearCombinationSnapshot` that produced it.

## Data conventions

`term_segments` has shape:

```text
(vector_count, 2, dimension)
```

For each term, index `0` is the tail and index `1` is the tip.

`resultant_segment` has shape:

```text
(2, dimension)
```

It begins at the origin and ends at the final linear combination.

## Scope deliberately excluded

Checkpoint 11 does not add:

- coefficient interpolation;
- a combined geometry path;
- display projection;
- arrow styling;
- Manim adapters;
- a smoke scene.

Those remain separate layers.

## Existing stable classes left unchanged

The checkpoint does not modify:

- `LinearCombination`
- `LinearCombinationSnapshot`
- `CoefficientSweepPath`
- the complete rank-collapse pipeline
- any Manim class or scene

Only the public export in `engine/__init__.py` is extended by the installer.

## New files

- `engine/linear_combination_geometry.py`
- `tests/test_linear_combination_geometry.py`
- `scripts/check_linear_combination_geometry.zsh`
- `CHECKPOINT_11.md`

The installer adds:

```python
from .linear_combination_geometry import LinearCombinationGeometry, LinearCombinationGeometrySnapshot
```

## Public interface

```python
mathematical_snapshot = linear_combination.snapshot(coefficients)

geometry_converter = LinearCombinationGeometry()
geometry_snapshot = geometry_converter.snapshot(mathematical_snapshot)
# equivalent:
geometry_snapshot = geometry_converter(mathematical_snapshot)
```

Useful geometry fields are:

```python
geometry_snapshot.term_segments
geometry_snapshot.term_starts
geometry_snapshot.term_ends
geometry_snapshot.resultant_segment
geometry_snapshot.resultant_start
geometry_snapshot.resultant_end
```

## Focused test coverage

The twelve tests cover:

1. two-term tip-to-tail placement;
2. segment displacement equality with scaled terms;
3. negative and zero terms;
4. origin-based resultant geometry;
5. independence of vector count and ambient dimension;
6. the single-vector case;
7. exact mathematical-snapshot traceability;
8. converter type validation;
9. owned, read-only public arrays;
10. inconsistent term-segment rejection;
11. inconsistent resultant rejection;
12. callable shorthand behavior.

Expected focused result:

```text
12 passed
```

Expected complete-suite result after the Checkpoint 10 baseline of 131 tests:

```text
143 passed
```

## Commands

From the repository root:

```zsh
./scripts/check_linear_combination_geometry.zsh
python -m pytest -q
```

## Next logical checkpoint

Checkpoint 12 should add `LinearCombinationGeometryPath`.  It should compose
`CoefficientSweepPath` with `LinearCombinationGeometry`, producing a complete
geometry snapshot at any progress value without duplicating either coefficient
interpolation or segment construction.
