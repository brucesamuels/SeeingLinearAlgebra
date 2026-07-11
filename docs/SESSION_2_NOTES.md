# Session 2 Notes

The core `Vector` and `Subspace` classes work in arbitrary ambient dimension.
Only their direct geometric displays are restricted to R^2 and R^3.

Examples:

```python
v = Vector([2, -1, 4, 3])
e4 = BasisVector(index=4, dimension=7)
W = Subspace([Vector([1,0,1,0]), Vector([0,1,0,1])])
```

The engine therefore distinguishes “not directly drawable” from “not representable.”

Next milestone:
- coefficient sweeps,
- dimension badges,
- 3D planes and volumes,
- rank-collapse animations.
