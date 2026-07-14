# Engine v0.3 — Checkpoint 14

## Thin Manim adapter for linear-combination geometry

Checkpoint 14 adds the final renderer-specific layer for the current
linear-combination pipeline:

```text
LinearCombination
↓
CoefficientSweepPath
↓
LinearCombinationGeometry
↓
LinearCombinationGeometryPath
↓
LinearDisplayProjector
↓
LinearCombinationGeometryDisplayAdapter
↓
ManimLinearCombinationGeometry
```

The new adapter receives a completed
`LinearCombinationGeometryDisplaySnapshot`. It performs no vector arithmetic,
coefficient interpolation, tip-to-tail construction, or projection.

## Why the adapter belongs here

Manim requires concrete `Mobject` instances and in-place mutation methods.
Those concerns are renderer-specific and therefore belong after the display
snapshot has already been computed. Keeping this boundary last preserves the
renderer-independent mathematical pipeline and allows a future renderer to
consume the same display snapshots without depending on Manim.

## Added files

- `engine/manim_linear_combination_geometry.py`
- `tests/test_manim_linear_combination_geometry.py`
- `scripts/check_manim_linear_combination_geometry.zsh`
- `CHECKPOINT_14.md`

No smoke scene is included. The first scene using this adapter remains
Checkpoint 15.

## Public adapter behavior

`ManimLinearCombinationGeometry` is a Manim `VGroup` that:

1. creates one `Arrow` for each displayed term;
2. creates one `Arrow` for the displayed resultant;
3. keeps those exact `Arrow` instances for the adapter lifetime;
4. updates their endpoints through `update_from_snapshot(...)`;
5. rejects later snapshots whose term count differs;
6. embeds two-coordinate display points into Manim's three-coordinate scene
   space by appending `z = 0`;
7. forces `buff = 0` so Manim does not shorten already projected endpoints;
8. keeps coincident endpoints renderable through a visually negligible
   epsilon-length arrow, preserving object identity across zero and nonzero
   states.

The method is named `update_from_snapshot(...)` deliberately. It does not
replace Manim's own `Mobject.update(...)` lifecycle method.

## Snapshot boundary

The canonical Checkpoint 13 snapshot shape is:

- `term_arrows`: a fixed sequence of displayed arrows;
- `resultant_arrow`: one displayed arrow;
- each displayed arrow exposes `start` and `end`.

The module also accepts equivalent endpoint-only names at this final boundary.
This is compatibility handling only; it does not recompute any upstream
mathematics or geometry.

## Existing classes left unchanged

Checkpoint 14 does not modify:

- `LinearCombination`
- `CoefficientSweepPath`
- `LinearCombinationGeometry`
- `LinearCombinationGeometryPath`
- `LinearDisplayProjector`
- `LinearCombinationGeometryDisplayAdapter`
- rank-collapse mathematics, geometry, display adapters, or Manim adapters
- any existing smoke scene or render script

The adapter is imported directly from
`engine.manim_linear_combination_geometry`, avoiding an unnecessary edit to the
stable package initializer in this checkpoint overlay.

## Focused tests

The focused tests verify:

- correct creation of term and resultant arrows;
- two-dimensional point embedding;
- preservation of root, term-arrow, and resultant-arrow identity;
- in-place endpoint updates;
- atomic rejection of changed term count;
- zero-length to nonzero transitions without mobject replacement;
- style mapping isolation and exact endpoint preservation;
- rejection of invalid display dimensions.

## Verification

Run:

```zsh
./scripts/check_manim_linear_combination_geometry.zsh
```

The script adds the repository root to `PYTHONPATH`, runs the focused test file,
and then runs the complete suite.
