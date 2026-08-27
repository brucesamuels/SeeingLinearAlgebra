# Checkpoint 199 — Why Positive Definiteness?

This lesson opens the Positive Definite Matrices sequence by giving the defining
inequality a directional, numerical meaning.

## Numerical spine

- `A=[[2,1],[1,2]]`
- `x(theta)=(cos(theta), sin(theta))`
- `q(x)=x^T A x`
- The numerical model is renderer-independent and accepts any finite symmetric
  2-by-2 matrix.

## Story

1. Introduce the fixed matrix, a unit direction, and its scalar quadratic energy.
2. Rotate the vector through several directions while a live readout tracks the
   value of `x^T A x`.
3. Pause and ask whether a nonzero direction can make the value zero or negative.
4. Sweep through additional directions, then reveal the defining inequality and
   the term **positive definite**.

This checkpoint intentionally does not introduce geometric surfaces, spectral
tests, elimination tests, factorizations, or determinant criteria.

## Environment and commands

Use Python 3.12 with Manim Community 0.21.0. Both scripts set `PYTHONPATH` to the
repository root and stop with a clear message if the active environment differs.

```zsh
conda activate seeingla-manim021
zsh scripts/check_cp199_positive_definite_why.zsh
zsh scripts/render_cp199_positive_definite_why.zsh
```

The render command produces only a low-quality preview.
