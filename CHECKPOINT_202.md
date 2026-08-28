# Checkpoint 202 — The Elimination Test

This lesson follows the eigenvalue test with an elimination-based route to positive
definiteness. It shows that elimination pivots reappear as the coefficients in a
completed-square expression, then connects those pivots to leading principal minors.

## Numerical spine

- `A=[[2,1],[1,2]]`
- Elimination without row exchanges gives pivots `p1=2` and `p2=3/2`.
- `x^T A x=2(x1+x2/2)^2+(3/2)x2^2`.
- The leading principal minors are `Delta1=2` and `Delta2=det(A)=3`.
- For `B=[[4,2,0],[2,3,1],[0,1,2]]`, the nested upper-left blocks give
  leading principal minors `4`, `8`, and `12`.
- With `Delta0=1`, the pivots satisfy `pk=Delta_k/Delta_(k-1)`.

## Story

1. Recall that positive eigenvalues test positive definiteness and ask whether
   elimination can see the same positivity without computing eigenvalues.
2. Perform one elimination step and reveal the two positive pivots.
3. Pause before interpreting the second pivot: what would a zero or negative pivot
   mean for the quadratic energy?
4. Complete the square and show that the pivot values are exactly the coefficients
   of the independent squares.
5. Read the first two leading principal minors from the upper-left blocks.
6. Define the leading `k`-by-`k` block and its determinant using a structural 3-by-3
   example with three nested blocks.
7. Connect pivot values to ratios of consecutive leading principal minors.
8. Finish with the positive-pivot test and Sylvester's criterion for symmetric
   matrices.

Only leading principal minors are used. Matrix decompositions remain outside this
checkpoint.

## Environment and commands

Use Python 3.12 with Manim Community 0.21.0. Both scripts set `PYTHONPATH` to the
repository root and reject a different active environment.

```zsh
conda activate seeingla-manim021
zsh scripts/check_cp202_positive_definite_elimination_test.zsh
zsh scripts/render_cp202_positive_definite_elimination_test.zsh
```

The render command produces only a low-quality preview.
