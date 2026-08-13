# Checkpoint 151 - Orthogonal Sets

## Purpose

Extend the dot-product test from a single pair of vectors to a **whole set** of
vectors. This lesson defines an orthogonal set, shows a genuine 3D orthogonal
example, shows a 3D nonexample where one pair breaks the condition, and proves
that orthogonal nonzero vectors are linearly independent.

## Mathematical narrative

1. Begin with the familiar condition that two vectors are perpendicular when their dot product is zero.
2. Define an orthogonal set by the pairwise condition
   `v_i · v_j = 0` whenever `i ≠ j`.
3. Show a true orthogonal set in `R^3`.
4. Show a 3D nonexample where one nonzero dot product breaks orthogonality.
5. Prove that orthogonal nonzero vectors are linearly independent.
6. Bridge naturally to CP152 by asking what happens when the vectors are also
   unit length.

## Architecture

- `engine/orthogonal_sets.py` owns the vector data and pairwise dot products.
- `scenes/orthogonal_sets_presentation.py` is a thin Manim presentation with
  fixed banner/title and a 3D middle sequence for the set examples.
- The 3D camera motion is slow and deliberate.
- The theorem proof is staged in a separate algebra card with one idea per line.

## Files

- `engine/orthogonal_sets.py`
- `scenes/orthogonal_sets_presentation.py`
- `tests/test_orthogonal_sets.py`
- `tests/test_orthogonal_sets_presentation.py`
- `scripts/check_cp151_orthogonal_sets.zsh`
- `scripts/render_cp151_orthogonal_sets.zsh`
- `CHECKPOINT_151.md`

## Install

Because macOS Safari auto-unzips downloads, install from the extracted folder:

```zsh
zsh ~/Downloads/seeing_linear_algebra_cp151/apply_checkpoint_151.zsh
```

## Check

```zsh
zsh scripts/check_cp151_orthogonal_sets.zsh
```

## Preview render

```zsh
zsh scripts/render_cp151_orthogonal_sets.zsh -pql
```

Do not commit until the low-quality render has been visually approved.

## Visual review

- The definition card should stay clean and uncrowded.
- The orthogonal 3D example should clearly show three mutually perpendicular
  directions.
- The nonexample should make it obvious that one bad pair destroys
  orthogonality.
- The right-side algebra in the 3D cards must not collide with the geometry.
- The theorem card should read one logical step at a time.
- The final bridge should clearly motivate orthonormal sets.


## r7 visual refinement

- Enlarged both 3D coordinate displays from 3.0 to 3.6 scene units.
- Lowered the 3D displays to improve balance under the lesson heading.
- Raised the final yellow question, “What if the vectors are also unit length?”,
  to balance the final card more effectively.
- Cleaned stale revision labels in the check and render scripts.

- The 3D example and nonexample are lowered further on the screen to reduce blank space above the geometry.

- The 3D example and nonexample are moved much lower and made slightly larger so the central region is used more fully and the vertical change is unmistakable.

- After reviewing the rendered r6 video, the 3D example and nonexample are shifted substantially farther down (DOWN * 3.15) while the algebra column remains fixed.

- In r8 the 3D geometry is moved noticeably to the right and further down, based on rendered-video review, so the left-middle blank space is reduced and the geometry occupies the central visual field more naturally.

- r9 interprets "right" explicitly as screen-right from the viewer perspective. Because the 3D camera projection reverses the apparent effect of the earlier world-coordinate adjustment, the world shift is changed in the opposite direction and lowered further.

## r10 rendered-camera correction

The r9 preview showed that lowering a 3D object with the rotated camera also drove it toward screen-left. r10 therefore uses a compensating world-right shift while lowering the geometry slightly further. The intent is explicitly viewer-screen placement: the 3D graphic should sit lower and farther to the viewer's right, fully inside the frame, while the fixed algebra remains on the right.

- In r11 the 3D geometry is raised from the r10 bottom-edge placement and shifted substantially farther toward the viewer's right, while the fixed equations remain unchanged.


## r12 visual refinement

- Raise the 3D axes slightly so the initial axis tips remain on screen.
- Use a less oblique camera orientation (`phi=58°, theta=-30°`) so the projected xy-plane is closer to horizontal.
- Keep the slow camera motion, but end at milder azimuths (`theta=-22°` and `-18°`) to preserve spatial depth without the strong negative screen slope.

- r13 starts the 3D camera at theta = -15 degrees, raises the 3D block from r12 so all axes begin on-screen, and uses gentler later theta changes.

## r14 visual refinement

- Preserve the r13 starting frame at `theta=-15 degrees`.
- Increase the camera sweep substantially: the orthogonal example rotates to `theta=28 degrees`, and the nonexample to `theta=25 degrees`.
- Lengthen each camera move to 2.6 seconds so students can watch the spatial directions separate more clearly.
- Keep the r13 position and safer initial zoom so the larger rotation begins fully on-screen.
