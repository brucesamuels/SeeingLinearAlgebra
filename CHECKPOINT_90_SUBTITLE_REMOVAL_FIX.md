# CP90 Subtitle Removal Fix

This revision resolves the remaining collision between the cofactor-section
heading and the persistent introductory subtitle.

## Visual/code revision

- Removes the subtitle
  **"We know what it represents. Now let us calculate it."**
  immediately before the cofactor / cross-hatch section begins.
- Keeps the lowered section headings:
  - **"Where Do the Cofactors Come From?"** at `DOWN * 0.65`
  - **"The Cross-Hatch Shortcut"** at `DOWN * 1.05`
- Keeps the lowered symbolic vector form at `DOWN * 1.00`.

## Test updates

- Updates every affected focused presentation test in the same package.
- Removes stale and duplicate layout assertions from earlier revisions.
- Adds a focused test confirming the subtitle is removed before the cofactor
  section is shown.
