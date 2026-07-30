# Seeing Linear Algebra — Checkpoint 82

## Goal

Begin the Linear Transformations chapter with a geometry-first standalone lesson:

> What Does a Linear Transformation Do?

The lesson surveys several actions on a complete coordinate stage before defining
linearity formally or introducing a matrix.

## Pedagogical arc

The same grid, basis vectors, vector, asymmetric figure, and origin marker undergo:

1. rotation;
2. reflection through a line through the origin;
3. shear;
4. orthogonal projection;
5. translation.

The lesson asks:

> Which of these preserve the linear structure?

The first visible test is whether the origin remains fixed. Translation is isolated
as a non-example because its origin moves. The lesson closes with:

> A linear transformation must fix the origin.

and then leaves the formal definition unresolved:

> What additional properties must it preserve?

CP82 intentionally does not introduce homogeneity, additivity, basis images,
matrix columns, or matrix multiplication.

## Architecture

`PlanarAffineTransformation` is renderer independent and models

```text
x -> A x + b
```

rather than assuming every candidate is linear. This lets the same engine represent
both linear candidates and translation.

`PlanarTransformationGeometry` owns the mathematical stage:

- basis endpoints;
- vector endpoints;
- polygon vertices;
- grid segments;
- origin.

It returns immutable snapshots containing every transformed component.

`TransformationStage` is a thin Manim adapter. It owns visual mobjects and updates
them from one renderer-independent snapshot.

## Files

All files are additive:

```text
CHECKPOINT_82.md
engine/planar_affine_transformation.py
scenes/what_does_a_linear_transformation_do_presentation.py
tests/test_planar_affine_transformation.py
tests/test_what_does_a_linear_transformation_do_presentation.py
scripts/check_what_does_a_linear_transformation_do.zsh
scripts/render_what_does_a_linear_transformation_do.zsh
```

## Focused tests

The checkpoint verifies:

- exact rotation, reflection, projection, shear, and translation behavior;
- the translation origin test;
- interpolation from identity to the target action;
- coherent transformation of the grid, basis, vectors, polygon, and origin;
- the required candidate sequence;
- matrix notation and formal linearity equations are absent from this lesson;
- the prediction and closing questions are present.

## Visual review

Please check:

- grid and figure remain comfortably inside the frame during every action;
- deformation is smooth enough to read;
- basis colors remain distinct;
- labels do not compete with the moving geometry;
- projection collapse is legible;
- translation makes the moving origin unmistakable;
- reading time feels natural;
- the lesson does not imply that fixing the origin is sufficient for linearity.

No chapter number is assigned.
