# Checkpoint 200 — From Directional Energy to a Bowl

This lesson turns the directional experiment from Checkpoint 199 into a statement
about every nonzero vector, then gives positive definiteness a three-dimensional
geometric meaning.

## Numerical spine

- `A=[[2,1],[1,2]]`
- `q(x)=x^T A x`
- Every nonzero vector is written as `x=ru`, where `r>0` and `||u||=1`.
- `q(ru)=r^2 q(u)` connects unit-direction energy to arbitrary vectors.
- The graph uses quadratic energy as height: `(x,y) -> (x,y,q(x,y))`.

## Story

1. Recall that the quadratic energy is positive on every unit direction.
2. Grow and shrink a vector along a fixed ray while its live energy changes.
3. Reveal quadratic radial scaling and extend the directional observation to all
   nonzero vectors.
4. Lift one input point to its quadratic height, then reveal the full surface.
5. Ask what zero or negative energy would look like relative to the input plane.
6. Morph the bowl into a trough that touches the plane along a nonzero line, then
   into a saddle that crosses below the plane.
7. Restore the original bowl and show that it touches the plane only at the origin
   and otherwise stays strictly above it.
8. Finish with the equivalence between the defining inequality and this geometric
   signature.

Later algebraic criteria, coordinate directions, extrema, and factorizations remain
outside this checkpoint.

## Environment and commands

Use Python 3.12 with Manim Community 0.21.0. Both scripts set `PYTHONPATH` to the
repository root and reject a different active environment.

```zsh
conda activate seeingla-manim021
zsh scripts/check_cp200_positive_definite_quadratic_surface.zsh
zsh scripts/render_cp200_positive_definite_quadratic_surface.zsh
```

The render command produces only a low-quality preview.
