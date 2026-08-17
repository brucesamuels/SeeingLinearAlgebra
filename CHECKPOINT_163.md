# CP163 - Rotations and Reflections: Orthogonal Transformations

## Purpose

CP162 established the general principle that orthogonal matrices preserve Euclidean geometry. CP163 now makes the two geometric possibilities concrete: **rotations** and **reflections**.

The lesson is intentionally geometry-forward. Most cards use a large coordinate grid on the left and a reserved mathematics column on the right, avoiding graph-label/equation collisions.

## Mathematical examples

### Rotation

The lesson begins from the images of the standard basis vectors:

\[
R_\theta \mathbf e_1=(\cos\theta,\sin\theta),
\qquad
R_\theta \mathbf e_2=(-\sin\theta,\cos\theta).
\]

Therefore

\[
R_\theta=
\begin{bmatrix}
\cos\theta&-\sin\theta\\
\sin\theta&\cos\theta
\end{bmatrix}.
\]

The concrete animation uses \(\theta=60^\circ\), with a vector and an asymmetric triangle rotating rigidly about the origin.

The inverse relationship is then emphasized:

\[
R_\theta^{-1}=R_{-\theta}=R_\theta^T.
\]

### Reflection

The reflection example is across the x-axis:

\[
H=
\begin{bmatrix}
1&0\\
0&-1
\end{bmatrix}.
\]

The geometry makes explicit that

\[
H\mathbf e_1=\mathbf e_1,
\qquad
H\mathbf e_2=-\mathbf e_2.
\]

Reflecting twice restores the original vector or figure:

\[
H^2=I,
\qquad
H^{-1}=H=H^T.
\]

## Six-card structure

1. **Build a rotation matrix from basis images.**
2. **Animate a rigid 60-degree rotation** of a vector and asymmetric triangle.
3. **Undo the rotation** and connect opposite angle, inverse, and transpose.
4. **Build a reflection geometrically** from a fixed direction and reversed perpendicular direction.
5. **Reflect twice** to show that a reflection is its own inverse.
6. **Compare orientation:** \(\det R_\theta=+1\) versus \(\det H=-1\).

## Files

- `engine/rotations_reflections.py`
- `scenes/rotations_reflections_presentation.py`
- `tests/test_rotations_reflections.py`
- `tests/test_rotations_reflections_presentation.py`
- `scripts/check_cp163_rotations_reflections.zsh`
- `scripts/render_cp163_rotations_reflections.zsh`
- `CHECKPOINT_163.md`
- `apply_checkpoint_163.zsh`

## Review focus

Please check the low-quality preview for:

- clarity of the dynamic 60-degree rotation on Card 2,
- separation between geometry and the right-hand mathematics column,
- whether the reflection across the x-axis is immediately readable on Card 4,
- whether Card 5 clearly communicates "reflect twice = return",
- and whether the final determinant/orientation comparison feels like a satisfying synthesis of CP162 and CP163.


## r2 final-card balance

- Nudged the white closing explanatory text upward slightly on the final card for better visual balance.
- All other content, timing, and layout remain unchanged.


## r3 orthogonality explanation and final-card balance

- Added a new card that explains why both the rotation and the reflection are orthogonal: their columns form orthonormal sets, so A^TA = I.
- On the final comparison card, moved the white explanatory text from the bottom to a position midway between the heading and the two box labels.
- Preserved the existing animation flow on the other cards.


## r4 last-two-cards spacing refinement

- Penultimate card: lowered the two boxed panels, reduced the criterion line slightly, and eased the density of the box text to avoid crowding with the heading and box titles.
- Final card: lowered the two comparison boxes and positioned the white explanatory sentence using the midpoint of the actual gap between the heading and the title band, instead of the midpoint of their centers.
- All other animation flow and content remain unchanged.


## r5 ending restructure

- Simplified the generic "Why are these transformations orthogonal?" card so it states the criterion cleanly without crowding.
- Added a new follow-up card that checks the actual rotation and reflection matrices from the lesson, verifying orthogonality and unit length directly. The rotation example explicitly uses the Pythagorean identity; the reflection example uses direct arithmetic.
- Reworked the final card so the standalone sentence "Rotation and reflection are both orthogonal" sits between the top heading and the lower comparison boxes.


## r6 final spacing cleanup

- Final card: raised the heading "Orientation distinguishes them" slightly for better vertical balance.
- Penultimate specific-example card: constrained the Pythagorean explanatory note to the interior width of the rotation box, preventing it from extending past the box boundary.
- All mathematical content and animation timing remain unchanged.
