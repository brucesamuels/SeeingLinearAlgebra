# Checkpoint 190 — From Standard Coordinates to Basis Coordinates

This lesson reverses the basis-matrix conversion developed in the preceding lesson.

## Mathematical focus

- Keep the geometric vector fixed while changing its coordinate description.
- Derive `[v]_B = P_B^{-1}[v]_E` from `[v]_E = P_B[v]_B`.
- Compute the inverse of `P_B = [[1,1],[1,-1]]` explicitly.
- Convert `(4,2)_E` into `(3,1)_B` with complete row arithmetic.

## Visual focus

- Every line and both axes of the pronounced standard grid visibly transform into the oblique basis grid.
- The orange geometric vector is created once and never transformed during the grid change.
- Its endpoint readout changes from `[v]_E=(4,2)` to `[v]_B=(3,1)`.
- Algebra cards use large `MathTex` and safe full-frame fitting.

## Review workflow

1. Run the focused checks.
2. Render the low-quality preview.
3. Review geometry, labels, margins, font sizes, and pacing.
4. Revise before committing.

Revision 2 replaces the grid crossfade with a continuous whole-grid matrix transformation.

Revision 3 uses Manim's matrix animation directly on the existing `NumberPlane`,
giving the grid a clearly visible three-second deformation into the nonstandard grid.

Revision 4 replaces the `NumberPlane` transformation with paired, explicit source
and target line segments. Every grid line now interpolates between calculated
endpoints over four seconds, making the motion unambiguous in the rendered preview.

Revision 5 uses a unique package name, verifies the animated-grid source during
installation, and disables Manim caching in the preview script.
