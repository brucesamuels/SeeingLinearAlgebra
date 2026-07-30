# Seeing Linear Algebra — Checkpoint 82.2

## Purpose

Refine the opening Linear Transformations lesson in two focused ways.

## Changes

### Pause and Predict placement

The complete Pause-and-Predict block is shifted downward by `0.55 * DOWN`
to maintain comfortable separation from the lesson title.

### Translation presentation

During the translation example, the coordinate grid remains fixed while the
following objects translate together:

- the origin marker;
- the basis vectors;
- the sample vector;
- the asymmetric geometric figure.

Rotation, reflection, shear, and projection continue to deform the entire stage,
including the grid.

This visual distinction reinforces that translation moves the geometric objects
relative to the original coordinate system and does not fix the origin.

## Architecture

`TransformationStage.update_objects_from_snapshot()` was added as a thin
presentation-layer helper. It updates transformed objects without changing the
grid. The renderer-independent mathematical engine is unchanged.

## Visual review

Please confirm that:

- Pause and Predict no longer collides with the title;
- the translation grid remains completely stationary;
- the figure, basis vectors, sample vector, and origin marker move together;
- the red origin marker clearly leaves `(0, 0)`;
- all other transformations still deform the grid;
- the translation reset returns cleanly to the initial stage.
