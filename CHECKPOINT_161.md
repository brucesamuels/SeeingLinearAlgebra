# Checkpoint 161 - Least Squares as Orthogonal Projection

## Purpose

Connect least squares directly to the geometry of orthogonal projection and make the normal equation the central algebraic consequence.

## Example

Use

\[
A=\begin{bmatrix}
1&0\\
0&1\\
1&1
\end{bmatrix},
\qquad
b=\begin{bmatrix}2\\2\\1\end{bmatrix}.
\]

The columns span the plane \(z=x+y\), while \(b\) lies outside that plane. The least-squares solution is

\[
\widehat x=\begin{bmatrix}1\\1\end{bmatrix},
\qquad
A\widehat x=\begin{bmatrix}1\\1\\2\end{bmatrix},
\qquad
r=b-A\widehat x=\begin{bmatrix}1\\1\\-1\end{bmatrix}.
\]

The residual is orthogonal to both columns of \(A\), hence

\[
A^Tr=0.
\]

Substituting \(r=b-A\widehat x\) gives the highlighted normal equation

\[
\boxed{A^TA\widehat x=A^Tb}.
\]

For this example,

\[
A^TA=\begin{bmatrix}2&1\\1&2\end{bmatrix},
\qquad
A^Tb=\begin{bmatrix}3\\3\end{bmatrix}.
\]

## Card sequence

1. Show that \(Ax=b\) has no exact solution because \(b\notin\operatorname{Col}(A)\).
2. Show the closest vector \(A\widehat x\) as the projection of \(b\) onto the column space.
3. Show the residual perpendicular to the column space with a right-angle marker.
4. Package the columnwise dot-product conditions into \(A^Tr=0\).
5. Dedicated **THE NORMAL EQUATION** card deriving and strongly highlighting \(A^TA\widehat x=A^Tb\).
6. Solve the small integer normal equation and recover the same projection and residual.
7. Connect to QR: \(R\widehat x=Q^Tb\), emphasizing that QR reaches the same least-squares solution without forming \(A^TA\).

## Revision

`cp161_initial_least_squares_normal_equation`


## r2 projection-view refinement

- Cards 1-3 now use a flatter camera view so the column space reads more like a broad tilted sheet than a steep wall.
- The column-space patch is enlarged slightly to strengthen the visual interpretation of projection onto the plane.
- Later algebra cards return to the original default view.


## r3 reference-style projection geometry

- Cards 1-3 now use a much stronger camera roll and opposite-side view so the column-space plane reads as a shallow, nearly horizontal sheet.
- The two spanning directions visually bracket the horizontal, while the residual from $A\hat{x}$ to $b$ rises nearly vertically.
- The 3D axes are deliberately deemphasized and the column-space patch is slightly stronger, matching the visual hierarchy of the supplied least-squares reference diagram.
- The original camera view is correctly restored after Card 3 for the later algebra cards.


## r4 framing correction

- Kept the improved projection orientation from r3.
- Raised the shared 3D construction on the opening geometry cards so the plane and projection picture remain fully inside the frame.


## r5 opening-geometry positioning

- Kept the improved projection orientation from r4.
- Raised the opening 3D construction substantially and moved it slightly viewer-left so the geometry stays on screen and uses the frame more effectively.


## r6 camera-aware framing and axis-tip cleanup

- The previous world-coordinate shift was nearly horizontal in the rolled camera view, so it did not raise the geometry appreciably on screen.
- The opening geometry now uses a world-space shift chosen to correspond to a substantial viewer-up move and a smaller viewer-left move under the r3/r4 camera orientation.
- Cards 1-3 now FadeIn the ThreeDAxes instead of Create-ing them, preventing an isolated axis arrowhead from appearing before the axes are visibly established.


## r7 framing and orthogonality refinement

- Raised the opening 3D geometry further so the lowest arrowhead begins fully inside the frame.
- On Cards 2 and 3, added stronger right-angle cues so the projection onto the column space reads more clearly as an orthogonal drop.


## r8 Card 2 marker bug fix

- Fixed a Card 2 runtime regression: the card defines one right-angle marker named `marker`, so its animation now creates `marker` rather than the Card 3 names `marker_a1` and `marker_a2`.
- Strengthened the focused presentation test so Card 2 and Card 3 marker names are checked independently.


## r9 raised geometry and perpendicular drop

- Raised the opening 3D geometry again so the bottom arrowhead begins inside the frame.
- On Cards 2 and 3, the residual is now shown as a dashed perpendicular drop from $b$ to the column space, with larger right-angle markers to make the $90^\circ$ meeting at the projection point visually apparent.


## r12 isotropic projection geometry

- Restored one continuous visual language across Cards 1-3: the same axes, plane, scale, and camera are used throughout.
- Corrected the 3D axes to equal coordinate scale in x, y, and z so Euclidean orthogonality is not visually distorted.
- Chose one camera direction perpendicular to the projection vector $A\hat{x}=(1,1,2)$ and rolled the view so $A\hat{x}$ appears horizontal while the residual appears vertical.
- Cards 2 and 3 now use one small right-angle marker between the projection direction and residual at their meeting point, with the extra multi-marker/guide constructions removed.


## r13 axis-tip artifact cleanup

- Disabled the 3D axis tips on the opening geometry cards to remove the stray white arrowhead artifact in the middle of the image.
- Preserved the current orientation and least-squares geometry.


## r14 penultimate-card spacing

- On the penultimate card, kept the subheading in place and lowered the computation block, verification block, and divider to clear the heading more comfortably.
- Mathematical content and timing are unchanged.
