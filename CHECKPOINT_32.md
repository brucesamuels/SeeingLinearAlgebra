# Engine v0.3 - Checkpoint 32 continuous-arrow-growth repair

## Visual finding

The vectors appeared to draw in two segments because each vector was first
animated as a `Line3D` shaft and then replaced by a completed `Arrow3D`.

## Revised construction

Each vector is now represented by one updater-driven `Arrow3D` throughout the
scene.

Two trackers control each arrow:

- a draw-progress tracker;
- its coefficient tracker.

The displayed endpoint is:

```text
draw_progress * coefficient * vector
```

## Arrowhead behavior

The arrowhead begins effectively invisible and grows smoothly between:

```text
HEAD_REVEAL_START = 0.18
HEAD_REVEAL_END = 0.45
```

The shaft and arrowhead therefore develop as one continuous object.

## Coefficient sweep

The same three arrows remain in the scene when the coefficients change from:

```text
(1,1,1)
```

to:

```text
(1.80,0.45,1.60)
```

There is no shaft-to-arrow replacement and no second draw phase.

The matrix synchronization, camera zoom, parallelepiped, resultant, and final
180-degree camera rotation are preserved.
