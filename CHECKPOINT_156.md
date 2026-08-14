# Checkpoint 156 - Orthogonal Complements

## Purpose

Introduce the orthogonal complement of a subspace and connect it directly to
projection and orthogonal decomposition.

The lesson emphasizes the idea that projection does more than find the nearest
point in a subspace: it also reveals a complementary perpendicular direction.
This leads naturally to the definition of `W^\perp`, to examples in `\mathbb R^2`
and `\mathbb R^3`, and to the structural result

\[
\mathbb R^n = W \oplus W^\perp.
\]

## Mathematical narrative

1. Motivate the idea with a projection split `x = p + r` and `r \perp W`.
2. Define
   `W^\perp = {v : v\cdot w = 0 for every w in W}`.
3. Show a line in `\mathbb R^2` and its orthogonal complement line.
4. Show a plane in `\mathbb R^3` and its orthogonal complement line.
5. State the decomposition and dimension payoffs:
   - `\mathbb R^n = W \oplus W^\perp`
   - `\dim W + \dim W^\perp = n`
6. Bridge to constructing orthogonal directions spanning a subspace.

## Files

- `engine/orthogonal_complements.py`
- `scenes/orthogonal_complements_presentation.py`
- `tests/test_orthogonal_complements.py`
- `tests/test_orthogonal_complements_presentation.py`
- `scripts/check_cp156_orthogonal_complements.zsh`
- `scripts/render_cp156_orthogonal_complements.zsh`
- `CHECKPOINT_156.md`

## Install

macOS Safari auto-unzips the download, so install from the extracted folder:

```zsh
zsh ~/Downloads/seeing_linear_algebra_cp156/apply_checkpoint_156.zsh
```

## Check

```zsh
zsh scripts/check_cp156_orthogonal_complements.zsh
```

## Preview render

```zsh
zsh scripts/render_cp156_orthogonal_complements.zsh -pql
```

The preview file is named:

```text
CP156_r2_layout_and_reveal_refinement_preview.mp4
```

Do not commit until the preview has been visually approved.

## Visual review notes

- The first geometric card should clearly identify `W`, `x`, `p`, and `r`.
- The `\mathbb R^2` card should label both `W` and `W^\perp` explicitly.
- The `\mathbb R^3` card should make the plane and its normal complement line easy to read.
- The decomposition card should remain spacious; the direct-sum and dimension lines should not crowd.
- The bridge should clearly set up Gram-Schmidt without introducing it prematurely.


## r2 visual refinement

- Fixed-in-frame text is registered only when its reveal animation begins, preventing formula/caption text from appearing in the first video frame.
- Card 3 shifts the 2D graph world-right and slightly upward.
- Card 4 enlarges the 3D geometry and shifts it down and world-left, with labels repositioned to match.
- Card 6 raises the yellow bridge question for a more balanced page.


## r3 geometry refinement

- Card 3 now uses a square coordinate plane so the two complement lines read as visibly perpendicular, and both labels are moved off the lines.
- Card 4 shifts the 3D graphic farther down and slightly world-left, enlarges it slightly, and attaches the W / W^perp labels to the 3D geometry so they move with the graphic.


## r4 card-4 placement repair

- Card 4 moves the 3D graphic substantially farther down and slightly world-left.
- The 3D labels W and W^perp are kept as world objects rather than fixed-in-frame overlays so they remain visible with the 3D geometry.


## r5 framing refinement

- Card 3 moves the W label away from the title area so it is no longer obscured.
- Card 4 lowers the 3D graphic further, shortens the normal direction slightly, and uses a gentler camera rotation so the figure stays within frame after rotating.


## r6 residual and 3D layout refinement

- Card 1 now uses equal horizontal and vertical scaling so the residual displays as truly perpendicular to W, and it adds a small right-angle marker at the projection point.
- Card 1 labels are moved farther away from the vectors and line.
- The 3D plane card begins lower on screen, uses a slightly shorter normal arrow, a smaller camera sweep, and a slightly wider zoom to keep the entire graphic inside frame.
- The 3D labels W and W^perp are attached to the geometry and added as fixed-orientation mobjects so they remain readable during the camera motion.


## r7 card-4 safe framing and label side

- Card 4 now uses a dedicated wider initial camera framing and a smaller camera sweep.
- The complete 3D construction is shifted substantially lower and slightly toward screen center so it begins in the lower-left/center region and has more safe margin throughout the rotation.
- The normal arrow is slightly shorter to reduce the risk of entering the title/banner region.
- W and W^perp remain world-positioned fixed-orientation labels. W^perp is positioned on the negative-x side of the normal so that, during the approved camera sweep, it can read to the viewer's left of the rotated vector.
- All r6 residual-geometry changes are preserved unchanged.


## r8 targeted layout refinement

- Card 1 moves the W label well below and away from the heading so the label cannot overlap “Projection leaves a perpendicular residual.”
- Card 4 places the complete 3D construction substantially lower in the lower-left/center region and widens the camera view slightly so the existing rotation remains inside the frame.
- All other content, timing, camera sweep, and label-attachment behavior are preserved.


## r9 card-4 recomposition

- Card 4 uses more of the lower-left/center blank region by enlarging the 3D construction slightly and moving the right-side equations upward.
- The camera sweep remains restrained and the normal is slightly shorter to protect frame clearance.
- W^perp begins offset from the normal and animates farther toward the viewer-left side during the camera rotation so the label does not remain hidden behind the vector.


## r10 card-4 viewer-right shift

- Moves the complete 3D Card 4 construction toward the viewer-right while preserving its approved vertical placement, scale, camera sweep, equations, and label behavior.


## r11 proportional viewer-right shift

- Card 4 moves the complete 3D construction approximately half of its current width toward the viewer-right.
- Vertical placement, scale, camera motion, equations, and W / W^perp label behavior are unchanged.


## r12 card-4 centering refinement

- Card 4 repositions the entire 3D construction toward the viewer-right so the complete visual center sits closer to the lower-middle region rather than deep in the lower-left.
- All other card-4 behaviors are preserved: scale, vertical placement, camera sweep, equations, and W / W^perp label behavior.


## r13 screen-space centering correction

- The r12 render showed that the raw world-coordinate shift moved the 3D construction farther viewer-left.
- Card 4 now uses a camera-projection-calibrated initial world shift chosen to place the visual center near the lower-middle of the screen.
- During the camera sweep, the 3D geometry receives a small compensating world translation so its rendered screen position stays approximately fixed instead of drifting left.
- W and W^perp remain geometry-attached, fixed-orientation labels; W^perp continues to move to the viewer-left side of the rotated normal.


## r14 card-4 slight upward shift

- Card 4 moves the complete 3D construction slightly upward while preserving its current centered composition, scale, camera sweep, equations, and W / W^perp label behavior.


## r15 card-4 full start in frame

- Card 4 moves the complete 3D construction upward just enough so the entire figure begins fully on screen at the start of the card.
- The current centered composition, scale, camera motion, equations, and W / W^perp label behavior are otherwise preserved.


## r16 card-4 safe-margin start

- Card 4 moves the complete 3D construction upward slightly more and zooms out slightly so the entire figure begins fully inside the frame with a small safety margin.
- The overall lower-middle composition, camera motion, equations, and W / W^perp label behavior are otherwise preserved.


## r17 card-4 first-frame clearance

- Based on the r16 rendered first frame, Card 4 moves the complete 3D construction upward by a small additional amount so the lower edge of the construction begins with visible clearance from the frame boundary.
- The current lower-middle composition, scale, zoom, camera motion, equations, and W / W^perp label behavior are otherwise unchanged.


## r18 card-4 first-frame safe margin

- Based on the r17 first-frame render, Card 4 moves the complete 3D construction upward by one small additional increment so the lowest arrowhead begins clearly inside the frame rather than touching the bottom edge.
- Scale, zoom, camera motion, equations, centered composition, and W / W^perp label behavior are unchanged.


## r19 card-4 start and label cleanup

- Card 4 moves the full 3D construction slightly upward again so the starting frame is fully inside the screen.
- The initial W^perp label is moved farther to the viewer-left so it is not obscured behind the normal at the start.
- The explanatory text block moves to the open blank area on the viewer-left.


## r20 card-4 caption and start clearance

- Card 4 raises the complete 3D construction by one additional small increment so the lowest arrowhead begins fully inside the frame.
- The bottom explainer caption moves into the lower viewer-left blank region and is wrapped across three lines for readability.
- The current equation placement, scale, zoom, camera motion, and W / W^perp label behavior are preserved.


## r21 restore card-4 equation block

- Card 4 restores the equation block to its r18 position on the viewer-right.
- The bottom caption remains in the viewer-left blank area, and the raised 3D construction and current label behavior are preserved.


## r22 card-4 caption left shift and raise

- Card 4 moves the viewer-left bottom caption farther left to avoid collision with the 3D geometry.
- Card 4 raises the full 3D construction by one more small increment so it clears the bottom boundary more reliably at the start.
- The equation block remains in its r18 position on the viewer-right.
