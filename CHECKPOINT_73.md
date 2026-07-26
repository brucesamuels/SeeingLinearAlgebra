# Checkpoint 73 — The Subspace Test

## Goal
Introduce the formal subspace test through a direct geometric contrast:

- a plane through the origin, which is a subspace;
- the same plane shifted away from the origin, which is not.

## Mathematical structure
The renderer-independent `SubspaceTest` model verifies three conditions:

1. the set contains the zero vector;
2. the set is closed under vector addition;
3. the set is closed under scalar multiplication.

For the plane through the origin, all three conditions hold. For the parallel shifted plane, all three fail in the chosen examples.

## Presentation sequence
1. Display a plane through the origin.
2. Mark the zero vector as belonging to the plane.
3. Draw two vectors in the plane and show that their sum remains in the plane.
4. Scale one vector and show that the scalar multiple remains in the plane.
5. Conclude that the plane passes the subspace test.
6. Replace it with a parallel shifted plane.
7. Show that the origin is missing.
8. Show that adding two points in the shifted plane leaves it.
9. Show that scaling a point in the shifted plane leaves it.
10. End with the formal three-part subspace test.

## Files added
- `engine/subspace_test.py`
- `scenes/subspace_test_presentation.py`
- `tests/test_subspace_test.py`
- `tests/test_subspace_test_presentation.py`
- `scripts/check_subspace_test.zsh`
- `scripts/render_subspace_test.zsh`
- `CHECKPOINT_73.md`

## Validation
The checkpoint package passes its focused test suite before installation.
