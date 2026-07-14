# Seeing Mathematics Engine v0.3 - Checkpoint 8

## Goal

Add a renderer-independent geometry display layer that connects:

```text
RankCollapseGeometryPath
        |
        v
LinearDisplayProjector
        |
        v
display-ready RankCollapseGeometrySnapshot
        |
        v
ManimRankCollapseGeometry
```

The new layer projects transformed geometry into a chosen 1D, 2D, or 3D
display space while preserving topology. It contains no Manim code.

## New class

`engine/rank_collapse_geometry_display.py`

```python
RankCollapseGeometryDisplayAdapter(geometry_path, projector)
```

The constructor verifies that the projector input dimension equals the
rank-collapse codomain dimension.

The public frame methods are:

```python
snapshot(progress)
snapshots(progress_values)
```

Each result is an ordinary `RankCollapseGeometrySnapshot` whose vertices are
display coordinates and whose edges and polylines are unchanged.

## Smoke-scene refactor

The square-grid smoke scene now exercises the complete renderer-independent
pipeline:

```python
collapse = RankCollapse(np.eye(2), target_rank=1)
geometry_path = RankCollapseGeometryPath.from_collapse(geometry, collapse)
projector = LinearDisplayProjector(np.eye(2))
display_path = RankCollapseGeometryDisplayAdapter(
    geometry_path,
    projector,
)
```

The Manim adapter receives only display-ready snapshots:

```python
display_path.snapshot(progress)
```

No matrix, collapse path, or display projection is performed inside Manim.

## Install after Safari has extracted the download

From the repository root:

```zsh
cd "/Users/brucesamuels/Documents/School/Linear Algebra/SeeingLinearAlgebra_v2"

CHECKPOINT_DIR=$(find ~/Downloads -maxdepth 2 \
  -type d \
  -iname "seeing_linear_algebra_checkpoint_8*" \
  -print -quit)

[[ -n "$CHECKPOINT_DIR" ]] || {
  print "Extracted Checkpoint 8 folder was not found in Downloads."
  exit 1
}

cp -R "$CHECKPOINT_DIR"/. .

chmod +x scripts/check_rank_collapse_geometry_display.zsh
```

## Test

```zsh
./scripts/check_rank_collapse_geometry_display.zsh
```

The focused test file should report:

```text
6 passed
```

With the Checkpoint 7 baseline of 104 tests, the complete suite should report:

```text
110 passed
```

## Render and preview

The preview flag was added locally during Checkpoint 7. Confirm the existing
render script contains `-pql`, then run:

```zsh
./scripts/render_rank_collapse_geometry_smoke.zsh
```

The square grid should collapse continuously from a plane to a line.

## Files added

- `engine/rank_collapse_geometry_display.py`
- `tests/test_rank_collapse_geometry_display.py`
- `scripts/check_rank_collapse_geometry_display.zsh`
- `CHECKPOINT_8.md`

## Files intentionally updated

- `engine/__init__.py`
- `scenes/rank_collapse_geometry_smoke.py`

The existing mathematical model, geometry container, geometry-path layer,
display projector, and Manim adapter are not overwritten.
