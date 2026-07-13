# Engine v0.3 — Checkpoint 5

Adds a renderer-independent topology layer:

- `engine/rank_collapse_geometry.py`
- `tests/test_rank_collapse_geometry.py`
- `scripts/check_rank_collapse_geometry.zsh`

The layer stores arbitrary-dimensional source vertices, edges, and polylines.
A snapshot may use a different ambient dimension, but must preserve the vertex count.
This keeps topology independent of RankCollapsePath, display projection, and Manim.

Add this import block to `engine/__init__.py`:

```python
from .rank_collapse_geometry import (
    Edge,
    Polyline,
    RankCollapseGeometry,
    RankCollapseGeometrySnapshot,
)
```

If `engine/__init__.py` defines `__all__`, add these four names there as well.
