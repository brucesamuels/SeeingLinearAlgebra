# Engine v0.3 — Checkpoint 6

Adds the thin Manim topology adapter and its first smoke scene:

- `manim_adapters/rank_collapse_geometry.py`
- `scenes/rank_collapse_geometry_smoke.py`
- `tests/test_manim_rank_collapse_geometry.py`
- `scripts/check_manim_rank_collapse_geometry.zsh`
- `scripts/render_rank_collapse_geometry_smoke.zsh`

## Architectural boundary

`ManimRankCollapseGeometry` accepts only a display-ready
`RankCollapseGeometrySnapshot`. It does not know about:

- `RankCollapse`
- `RankCollapsePath`
- matrices
- interpolation policy
- arbitrary-dimensional display projection

The renderer-independent layers decide all of those. The Manim adapter only:

1. pads 1D or 2D display coordinates to Manim's 3D point format;
2. creates one persistent `VMobject` per edge or polyline;
3. updates coordinates while preserving topology and object identity.

Snapshots above three display dimensions are rejected with an instruction to
apply `LinearDisplayProjector` before rendering.

## Smoke scene

`RankCollapseGeometrySmoke` creates a shared square lattice in `R^2`, stores its
horizontal and vertical grid lines as polylines, and follows a continuous matrix
path to the rank-one map

```text
[x]       [1  0.35] [x]
[y]  -->  [0  0   ] [y]
```

The grid therefore collapses continuously from a plane to a line.
