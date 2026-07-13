# Seeing Mathematics Engine v0.3 - Checkpoint 7

## Goal

Add a renderer-independent `RankCollapseGeometryPath` orchestration layer that:

- combines `RankCollapseGeometry` with `RankCollapsePath`;
- transforms every geometry vertex through the rank-collapse model;
- preserves edges and polylines unchanged;
- returns `RankCollapseGeometrySnapshot` objects;
- supports maps from `R^n` to `R^m`;
- keeps Manim confined to the existing thin adapter.

## Implementation

### New engine class

`engine/rank_collapse_geometry_path.py`

The class supports two construction forms:

```python
RankCollapseGeometryPath(geometry, path)
RankCollapseGeometryPath.from_collapse(geometry, collapse)
```

The explicit form verifies that the path's input points match the geometry
vertices. The convenience constructor creates the `RankCollapsePath` directly
from `geometry.vertices`, preventing accidental source mismatch.

The public frame methods are:

```python
snapshot(progress)
snapshots(progress_values)
```

Both return topology-preserving `RankCollapseGeometrySnapshot` objects.

### Smoke-scene refactor

`scenes/rank_collapse_geometry_smoke.py` now uses:

```python
collapse = RankCollapse(np.eye(2), target_rank=1)
geometry_path = RankCollapseGeometryPath.from_collapse(geometry, collapse)
```

The scene no longer contains its own matrix-path function. The updater requests
a geometry snapshot from the renderer-independent engine and passes that
snapshot to `ManimRankCollapseGeometry`.

### Focused tests

`tests/test_rank_collapse_geometry_path.py` covers:

1. all-vertex transformation;
2. edge and polyline preservation;
3. rectangular maps with different domain and codomain dimensions;
4. ordered snapshot sampling;
5. explicit composition with matching vertices;
6. rejection of mismatched vertices and invalid component types.

## Install from the repository root

```zsh
cd "/Users/brucesamuels/Documents/School/Linear Algebra/SeeingLinearAlgebra_v2"

unzip -o ~/Downloads/seeing_linear_algebra_checkpoint_7.zip -d .

chmod +x scripts/check_rank_collapse_geometry_path.zsh
```

## Test

```zsh
./scripts/check_rank_collapse_geometry_path.zsh
```

The focused test file should report:

```text
6 passed
```

With the previously reported 98-test baseline, the complete suite should report:

```text
104 passed
```

## Render the refactored smoke scene

```zsh
./scripts/render_rank_collapse_geometry_smoke.zsh
```

The grid should begin as a square plane and collapse continuously onto a line.

## Files added

- `engine/rank_collapse_geometry_path.py`
- `tests/test_rank_collapse_geometry_path.py`
- `scripts/check_rank_collapse_geometry_path.zsh`
- `CHECKPOINT_7.md`

## Files intentionally updated

- `engine/__init__.py`
- `scenes/rank_collapse_geometry_smoke.py`

No existing mathematical model, geometry container, display projector, or Manim
adapter is overwritten.
