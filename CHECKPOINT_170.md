# Checkpoint 170 — Eigenspaces

## Purpose

Continue Chapter 7 immediately after the defining equation `A v = lambda v` by showing that one eigenvector belongs to an entire family of scalar multiples on the same invariant line.

## Student-facing arc

1. Reuse the CP168/CP169 matrix `A = [[5,3],[3,5]]` and the lambda=2 direction `[1,-1]`.
2. Animate several nonzero scalar multiples and show algebraically that `A(cv)=lambda(cv)`.
3. Name the invariant line as the eigenspace `E_2 = span{[1,-1]}`.
4. Explicitly distinguish the zero vector: zero belongs to the eigenspace because it is a subspace, but zero is not an eigenvector.
5. Derive `(A-lambda I)v=0` from `Av=lambda v`.
6. Compute `A-2I=[[3,3],[3,3]]`, giving `x+y=0`, and identify `E_2 = Null(A-2I)`.
7. Finish by showing both eigenspaces for the same matrix: `E_2` and `E_8`.

The characteristic equation and determinants are intentionally deferred to the next lesson.

## Layout discipline

- Fixed 2D camera and coordinate grid for every geometric card.
- Viewer-left geometry and viewer-right mathematics remain independent zones.
- Stacked equations use `next_to` and rendered bounding boxes with explicit buffers rather than fixed y-coordinate guesses.
- The bottom caption band is reserved for the final zero/eigenvector distinction and does not compete with the calculation column.

## Files

- `engine/eigenspaces.py`
- `scenes/eigenspaces_presentation.py`
- `tests/test_eigenspaces.py`
- `tests/test_eigenspaces_presentation.py`
- `scripts/check_cp170_eigenspaces.zsh`
- `scripts/render_cp170_eigenspaces.zsh`
- `CHECKPOINT_170.md`

## Commands

```zsh
zsh scripts/check_cp170_eigenspaces.zsh
zsh scripts/render_cp170_eigenspaces.zsh
```
