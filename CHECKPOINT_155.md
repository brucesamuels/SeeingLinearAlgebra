# Checkpoint 155 — Projection onto a Subspace

CP155 extends vector projection from a line to a higher-dimensional subspace while making the algebraic analogy explicit.

## Conceptual arc

1. Begin geometrically: projection onto a subspace is the point reached by a perpendicular drop.
2. Place the line and subspace formulas side by side:
   - `proj_a(x) = a (a^T x)/(a^T a)`
   - `proj_W(x) = A(A^T A)^(-1)A^T x`.
3. Emphasize the analogy: scalar division by `a^T a` becomes multiplication by the inverse Gram matrix `(A^T A)^(-1)`; matrix division itself is not defined.
4. Derive the general formula from the perpendicular residual condition `A^T(x-Ac)=0`, giving the normal equations `A^T A c=A^T x`.
5. Compute with a genuinely non-orthonormal basis matrix
   `A=[[1,1],[1,1],[0,2]]` and `x=(3,1,2)`, obtaining `c=(1,1)` and `p=(2,2,2)`.
6. Then introduce an orthonormal basis `Q` as the simplification: `Q^T Q=I`, so the general formula collapses to `QQ^T x`, equivalently the sum of the component projections.
7. Stress that the projection depends on the subspace `W`, not on which basis is used to describe it.
8. End with the residual in `W^perp`, preparing the orthogonal-complement lesson.

## Visual refinement in r2

Fixed-orientation world labels are now created invisible and revealed only with their corresponding vectors. In particular, `x`, `p`, and `r` no longer appear before the geometry animation begins.

## Files

- `engine/subspace_projection.py`
- `scenes/subspace_projection_presentation.py`
- `tests/test_subspace_projection.py`
- `tests/test_subspace_projection_presentation.py`
- `scripts/check_cp155_subspace_projection.zsh`
- `scripts/render_cp155_subspace_projection.zsh`


## r3 layout refinement

- Card 3 opens more vertical space in the derivation so the normal-equations line and coefficient line do not crowd each other.
- Card 4 lowers the computation block so the heading no longer collides with the first matrix line.


## r4 layout and transition refinement

- Card 3 moves the premise higher and the derivation block lower, with more separation between lines, to eliminate the remaining collision.
- World labels now use FadeIn/FadeOut transitions instead of opacity toggles for a smoother appearance and disappearance.
