# Checkpoint 146 — Determinants and Change of Variables

## Central idea

A determinant is not only an algebraic invariant. It is the geometric scale factor that tells how a transformation changes area or volume.

For a linear map,
\[
\text{area after}=|\det(A)|\,\text{area before}.
\]

For a nonlinear map, the transformation changes from point to point. Its best local linear approximation is the Jacobian matrix
\[
J_F(u,v)=
\begin{bmatrix}
\frac{\partial x}{\partial u} & \frac{\partial x}{\partial v}\\
\frac{\partial y}{\partial u} & \frac{\partial y}{\partial v}
\end{bmatrix}.
\]

Thus a small area element scales approximately by
\[
dA_{xy}\approx |\det J_F(u,v)|\,dA_{uv}.
\]

## Linear example

For
\[
F(u,v)=(2u,u+3v),
\]
we have
\[
J_F=
\begin{bmatrix}
2&0\\
1&3
\end{bmatrix},
\qquad
\det(J_F)=6.
\]
Every area is scaled by 6.

## Polar coordinates

With
\[
x=r\cos\theta,
\qquad
y=r\sin\theta,
\]
the Jacobian determinant is
\[
\det(J)=r.
\]
Therefore
\[
dA=r\,dr\,d\theta.
\]
This explains geometrically why the factor \(r\) appears in polar-coordinate area integrals.

## Pedagogical goal

This checkpoint is a preview, not a full multivariable-calculus lesson. Its purpose is to show that the determinant's area-scaling meaning survives beyond linear maps through the Jacobian determinant.

## Layout rule

The scene uses the fixed-zone layout adopted after CP144:
- heading band at the top,
- geometry/formula band in the center,
- explanatory prose in a separate lower band,
- the largest formula reserved for the final takeaway.

## Files

- `engine/determinant_jacobian_preview.py`
- `scenes/determinant_jacobian_preview_presentation.py`
- `tests/test_determinant_jacobian_preview.py`
- `tests/test_determinant_jacobian_preview_presentation.py`
- `tests/test_cp146_scripts.py`
- `scripts/check_cp146_jacobian_preview.zsh`
- `scripts/render_cp146_jacobian_preview.zsh`


## Layout and visualization refinement R2

This refinement enlarges the mathematics on the Jacobian card so the central formulas are easier to read. It also redesigns the nonlinear-map card so the lesson now explicitly visualizes the idea of zooming into a nonlinear map: a highlighted local patch on the left is paired with a zoomed-in view on the right showing a curved patch together with a nearly linear approximation. Finally, the polar-coordinate card raises the title and lowers the formulas slightly to eliminate the heading collision.


## Packaging correction R3

R2 contained the intended scene revisions, but its installer was accidentally serialized with literal `\n` sequences instead of real line breaks. As a result, running the installer did not reliably replace the repository files. R3 corrects the installer and adds a regression test that verifies the installer begins with a valid zsh shebang followed by actual line breaks.


## Layout refinement R4

This refinement targets the crowding visible around 39 seconds on the polar area-element card. The card title is slightly reduced and moved higher, while the explanatory formula stack on the right is shifted lower, given more vertical spacing, and scaled down modestly. This creates a clearer separation between the explanatory text and the green area-element formula without changing the mathematical content.


## Structural layout refinement R5

The 36-44 second region is redesigned rather than nudged. The polar-coordinate card no longer carries a bottom explanatory sentence; it displays only the coordinate/Jacobian mathematics with generous vertical spacing. The following polar-area card replaces the prose-heavy three-line stack with two large dimension labels, \(dr\) and \(r\,d\theta\), followed later by a separate large green area formula. This removes the source of the collisions by giving each mathematical idea its own region and animation step.


## Layout refinement R6

After inspecting the uploaded preview frames from 36 to 44 seconds, the remaining collision was identified as the yellow stage title overlapping the large polar-coordinate formulas. This refinement moves the title higher, lowers the formula stack substantially, narrows its width slightly, and increases the vertical spacing between the displayed equations. The following polar-area card title is also raised a bit for consistency and clearance.


## Test packaging correction R7

The R6 scene and render are unchanged. The focused check failed only because `tests/test_cp146_scripts.py` contained a packaging-only assertion that tried to read `apply_checkpoint_146.zsh` from the repository root. The installer itself is intentionally not copied into the repository, so that assertion was stale after installation. R7 removes that stale assertion while retaining the script tests that verify the installed check and render scripts.


## Layout refinement R8

This refinement rebalances the "Polar coordinates give a nonlinear change of variables" card. The first line, $x=r\cos\theta,\ y=r\sin\theta$, is shifted downward to clear the title more comfortably, while the green determinant statement, $\det(J)=r$, is moved upward to sit closer to the Jacobian line and create a better-balanced page. The three displayed formulas are now positioned individually rather than as a single evenly arranged stack.


## Layout refinement R9

The previous R8 adjustment over-corrected the polar-coordinate card by manually placing each line too aggressively. This refinement restores the stable stacked layout from earlier revisions, then applies only small nudges: the white $x=r\cos\theta,\ y=r\sin\theta$ line is shifted slightly downward, and the green $\det(J)=r$ line is shifted slightly upward. This preserves spacing and size while improving the page balance without introducing new overlaps.


## Conceptual refinement R10

The polar-area card is rebuilt to answer its own question rather than merely display the final formula. Two arcs with the same small angle $d\theta$ are shown at different radii so students can see that the farther arc is longer: arc length is proportional to radius. A thin polar cell is then paired with a local rectangular approximation whose dimensions are $dr$ and $r\,d\theta$. The area formula $dA\approx(dr)(r\,d\theta)=r\,dr\,d\theta$ now emerges visually from those dimensions.


## Layout refinement R11

The explanatory polar-area card has been rebalanced for a cleaner page. The title is raised slightly, the arc labels on the left are separated more clearly, the explanatory sentence is moved upward and narrowed so it sits with the left-hand picture, and the right-hand rectangle cluster is spread vertically. The approximation sentence is raised, the rectangle dimensions are tucked closer to the shape, and the final green area formula is lowered slightly. The goal is a more balanced distribution of text and formulas across the full card.


## Layout refinement R12

Further tuned the two later cards in the Jacobian preview. On the polar-coordinate card, the title is raised and the formula stack is shifted upward slightly for a more balanced distribution of text and mathematics. On the polar-area explanation card, the outer-arc label $(r+dr)\,d\theta$ is moved farther from the sector vertex so it reads clearly against the geometry.


## Layout refinement R13

The outer-arc label is moved well away from the sector and enlarged slightly so the final `d\theta` is unmistakable. A short green leader line now connects the label to the outer arc. This avoids the previous visual merging with the nearby blue `r\,d\theta` label and the sector vertex.


## Content refinement R14

The polar-sector explanatory card has been removed from the lesson stack. Although mathematically valid, it added visual and conceptual complexity without improving the clarity of the Jacobian preview. The lesson now moves directly from the polar-coordinate Jacobian card to the final takeaway, keeping CP146 focused on the determinant as a local area-scale factor rather than developing the polar area element in detail.


## Conceptual refinement R15

Card 2 now makes the meaning of the two right-hand shapes explicit. The blue shape is labeled as the actual nonlinear image of the tiny highlighted patch, while the green parallelogram is labeled as the Jacobian's linear approximation. The zoom is also animated: a copy of the yellow focus patch grows into the enlarged blue image on the right, after which the green linear approximation appears on top of it. This makes the local-linearization idea dynamic rather than merely asserted.


## Conceptual refinement R16

Card 2 now separates magnification from deformation. The highlighted yellow patch is first copied and enlarged on the right without changing shape. Only after the zoom completes does the label "apply the nonlinear map" appear and the enlarged yellow patch deform into the blue nonlinear image. The green Jacobian parallelogram then appears as the local linear approximation. This prevents the misleading impression that zooming itself changes shape.
