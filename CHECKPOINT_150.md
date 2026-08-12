# Checkpoint 150 - Dot Product and Perpendicularity

## Purpose

Answer the question raised by CP149: **how do we recognize perpendicularity
algebraically?** This checkpoint introduces the dot product in both coordinate
and geometric forms, then uses the angle formula to derive the perpendicularity
test

\[
\mathbf{u}\perp\mathbf{v}\iff \mathbf{u}\cdot\mathbf{v}=0.
\]

## Mathematical narrative

1. Recall the CP149 question about detecting perpendicularity.
2. Introduce the coordinate formula
   `u · v = u1v1 + u2v2`.
3. Connect it to the geometric formula
   `u · v = ||u|| ||v|| cos(theta)`.
4. Specialize to the right-angle case to obtain `u · v = 0`.
5. Show the sign interpretation:
   acute `> 0`, right `= 0`, obtuse `< 0`.
6. End with the chapter bridge toward projection.

## Architecture

- `engine/dot_product_perpendicularity.py` owns all numerical vector data and
  sign/angle calculations.
- `scenes/dot_product_perpendicularity_presentation.py` is a thin 2D Manim
  presentation using the established header hierarchy and separate vertical
  zones for title, mathematics/geometry, and explanatory text.
- No camera motion or 3D geometry is used.
- The sign interpretation is shown with three clean mini-panels rather than a
  crowded derivation card.

## Files

- `engine/dot_product_perpendicularity.py`
- `scenes/dot_product_perpendicularity_presentation.py`
- `tests/test_dot_product_perpendicularity.py`
- `tests/test_dot_product_perpendicularity_presentation.py`
- `scripts/check_cp150_dot_product_perpendicularity.zsh`
- `scripts/render_cp150_dot_product_perpendicularity.zsh`
- `CHECKPOINT_150.md`

## Install

From the repository root:

```zsh
unzip -q ~/Downloads/seeing_linear_algebra_cp150.zip -d /tmp/seeing_linear_algebra_cp150
zsh /tmp/seeing_linear_algebra_cp150/apply_checkpoint_150.zsh
```

The installer rejects unrelated repository changes but permits replacement of
CP150 files so a revised package can be applied before commit.

## Check

```zsh
zsh scripts/check_cp150_dot_product_perpendicularity.zsh
```

## Preview render

```zsh
zsh scripts/render_cp150_dot_product_perpendicularity.zsh -pql
```

Do not commit until the low-quality render has been visually approved.

## Visual review

- Banner, yellow lesson title, central mathematics/geometry, and explanatory
  prose remain in separate vertical zones.
- The coordinate formula and angle formula are not crowded onto one card.
- The right-angle derivation is readable and paced deliberately.
- The sign interpretation panels read cleanly side by side.
- No prose approaches the frame edges.
- The final theorem card has visual weight and a deliberate hold.
- The closing bridge clearly motivates the upcoming projection lesson.


## Revision r4 verification

This package carries the scene marker `r5_verified_split_layout_installer_fix`. The installer
verifies that marker after copying the scene into the repository, and the render
script writes a uniquely named preview, `CP150_r4_verified_preview.mp4`, so an
older CP150 render cannot be mistaken for this revision.


## r5 installer correction

The installer no longer uses the variable name `path` while parsing `git status`.
In zsh, `path` is a special array tied to `PATH`; assigning to it can make later
commands such as `mktemp` unavailable. CP150 r5 uses `candidate_path` instead.


## Revision r6

- Retains the verified split layout for card 4.
- Removes the stale repository test that incorrectly expected the download-only
  `apply_checkpoint_150.zsh` installer to be copied into the repository.
- Adds repository-valid checks for the installed check/render scripts.
- Names the preview output `CP150_r6_verified_preview.mp4`.
