# Seeing Linear Algebra — Checkpoint 169

## Goal

Continue Chapter 7 with **Eigenvectors and Eigenvalues**.

CP168 established the geometric phenomenon: some transformations have special
directions whose images remain on the same line through the origin. CP169 now
formalizes that observation as

\[
A\mathbf v=\lambda\mathbf v,\qquad \mathbf v\ne\mathbf 0.
\]

The pedagogical order remains geometry first, algebra second.

## Mathematical sequence

1. Reuse CP168's symmetric transformation
   \[
   A=\begin{bmatrix}5&3\\3&5\end{bmatrix}.
   \]
2. Start with the invariant direction
   \[
   \mathbf v=\begin{bmatrix}1\\-1\end{bmatrix}.
   \]
3. Animate its image while retaining a dashed original reference.
4. Compute
   \[
   A\mathbf v=\begin{bmatrix}2\\-2\end{bmatrix}=2\mathbf v.
   \]
5. Only then introduce
   \[
   A\mathbf v=\lambda\mathbf v.
   \]
6. Identify \(\mathbf v\) as the eigenvector direction and \(\lambda\) as the
   scale factor along that direction.
7. Reuse the second CP168 invariant direction and show
   \[
   A\mathbf w=8\mathbf w.
   \]
8. Classify the qualitative meaning of \(\lambda\): stretch, shrink, reverse,
   fixed, or collapse to the origin.
9. End with the synthesis: eigenvectors identify invariant directions;
   eigenvalues describe scaling on those directions.

## Scope discipline

CP169 deliberately does **not** introduce:

- eigenspaces;
- \((A-\lambda I)\mathbf v=0\);
- characteristic polynomials;
- determinant conditions;
- eigenvalue computation procedures.

Those belong to subsequent lessons.

## Layout

- fixed 2D camera;
- coordinate grid behind geometric cards;
- viewer-left geometry and viewer-right equations on the worked example;
- one concise heading at a time;
- no checkpoint number in the student-facing scene;
- no crowded stacked explanatory bands.

## Files

```text
engine/eigenvectors_eigenvalues.py
scenes/eigenvectors_eigenvalues_presentation.py
tests/test_eigenvectors_eigenvalues.py
tests/test_eigenvectors_eigenvalues_presentation.py
scripts/check_cp169_eigenvectors_eigenvalues.zsh
scripts/render_cp169_eigenvectors_eigenvalues.zsh
CHECKPOINT_169.md
```

## Visual approval target

The preview should make three ideas clear without narration:

1. the eigenvector image remains on the same line;
2. \(\lambda\) measures scaling along that line;
3. changing the sign or size of \(\lambda\) changes stretch/shrink/reversal behavior.

Source tests cannot establish collision-free rendering. Visual approval of the
`-pql` preview is required before CP169 is committed.

## Visual refinement

- Card 2 right-hand worked-example equations now use rendered bounding-box spacing rather than fixed vertical coordinates.
- The blue vector definition and white transformed-vector equation have a generous explicit gap to prevent matrix-bracket collisions across font metrics.
- No mathematical content, pacing, or later-card structure was changed.
