# Engine v0.3 - Checkpoint 31 axes-coordinate mapping repair

## Visual finding

The three vectors were constructed from raw Manim scene coordinates, while the
displayed `ThreeDAxes` used its own coordinate scaling. As a result, the arrows
did not visually begin at the coordinate-system origin even though their raw
start point was `(0, 0, 0)`.

## Repair

The scene now uses the axes as the single display-coordinate authority:

```python
axes_origin = axes.c2p(0, 0, 0)
vector_point = axes.c2p(*vector)
```

The same mapping is applied to:

- all three common-origin vectors;
- every parallelepiped edge;
- the yellow resultant endpoint.

The mathematical vectors remain unchanged. Only their conversion into Manim
scene points is corrected.
