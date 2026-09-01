# Checkpoint 211 — Finite Elements: Turning Energy into a Matrix

This lesson introduces the finite element method from first principles. A
one-dimensional boundary-value problem is recast as energy minimization, the
unknown function is approximated by two piecewise-linear hat functions, and local
element contributions assemble into a positive-definite linear system.

## Numerical spine

- Solve `-u''(x)=1` on `0<x<1` with `u(0)=u(1)=0`.
- Here `x` is position along a taut string and `u(x)` is its downward
  displacement.
- Vertical force balance is `-T u''(x)=q(x)`. Normalizing the constant tension
  and uniform load to `T=1` and `q=1` gives `-u''=1`.
- Positive downward displacement is concave down under a positive load, explaining
  why the curvature appears with a minus sign.
- `u(0)=u(1)=0` fixes the string at both supports. These are spatial boundary
  conditions, not time-based initial conditions.
- The continuous energy is
  `J(u)=(1/2) integral (u')^2 dx - integral u dx`.
- Use the uniform mesh `0, 1/3, 2/3, 1` with three elements.
- The two interior nodes define hat functions `phi1` and `phi2`.
- Approximate `u` by `u_h=c1 phi1+c2 phi2`.
- Each element has length `h=1/3` and local stiffness matrix
  `(1/h)[[1,-1],[-1,1]]=[[3,-3],[-3,3]]`.
- Assembly followed by zero endpoint conditions gives
  `K=[[6,-3],[-3,6]]`.
- The area under either hat is `1/3`, so `f=(1/3,1/3)`.
- The discrete energy is `J(c)=(1/2)c^T K c-f^T c`.
- The stationarity condition is `Kc=f`, with solution `c=(1/9,1/9)`.
- The approximate nodal values are `(0,1/9,1/9,0)`.

## Story

1. Define position, downward displacement, string tension, and distributed load.
2. Derive `-T u''=q` from force balance and explain the minus sign.
3. Normalize to `T=1`, `q=1`, and explain the fixed-support boundary conditions.
4. State the energy minimized by the solution.
5. Divide the interval into three finite elements and identify the unknown nodes.
6. Draw the two piecewise-linear hat functions.
7. Replace the unknown function by two coefficients.
8. Compute the common local stiffness matrix.
9. Assemble the full stiffness matrix and impose the endpoint conditions.
10. Compute the load vector from hat-function areas.
11. Show that the continuous energy becomes a quadratic function of `c`.
12. Connect positive stiffness energy to a unique minimizer.
13. Pause and ask which equation the minimizing coefficients must satisfy.
14. Solve `Kc=f` and graph the piecewise-linear approximation alongside the exact
    curve.
15. Finish with `mesh -> basis -> assemble -> solve`.

## Scope boundary

The lesson does not introduce weak-form terminology, integration by parts,
Galerkin methods, higher-order elements, two-dimensional meshes, convergence rates,
or error estimates.

## Files

```text
engine/finite_element_energy.py
scenes/finite_element_energy_presentation.py
tests/test_finite_element_energy.py
tests/test_finite_element_energy_presentation.py
scripts/check_cp211_finite_element_energy.zsh
scripts/render_cp211_finite_element_energy.zsh
CHECKPOINT_211.md
apply_checkpoint_211.zsh
```

## Environment

Checkpoint 211 assumes Python 3.12 and Manim Community 0.21.0. Both scripts place
the repository root on `PYTHONPATH` before checking or rendering.

```zsh
conda activate seeingla-manim021
scripts/check_cp211_finite_element_energy.zsh
scripts/render_cp211_finite_element_energy.zsh
```

The render script intentionally produces only a low-quality preview.
