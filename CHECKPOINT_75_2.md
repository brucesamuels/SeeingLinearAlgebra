# Checkpoint 75.2 — Robust Null-Sweep Origin Crossing

The previous fix still allowed Manim's moving `Arrow` to retain a degenerate internal subpath when the null input crossed the origin.

This refinement:
- removes the moving Arrow entirely,
- replaces it with a flat `Line`,
- keeps a tiny nonzero hidden segment near the origin,
- animates the dot while explicitly updating the line,
- prevents Cairo's 3D projection from receiving malformed one-dimensional point data.
