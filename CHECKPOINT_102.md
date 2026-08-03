# Checkpoint 102 — Matrix Transposition

## Chapter role

CP102 follows the trace lesson and precedes the conceptual capstone on order,
identity, and undoing.

The lesson introduces transposition as exchanging rows and columns and develops
the properties needed later for symmetric matrices, orthogonality, least
squares, and eigenvalue theory.

## Storyboard

1. Animate the rows of a matrix becoming columns.
2. Introduce the notation \(A^T\).
3. State the entry rule:
   \[
   (A^T)_{ij}=a_{ji}.
   \]
4. Show that dimensions reverse:
   \[
   m\times n\longrightarrow n\times m.
   \]
5. Show that \((A^T)^T=A\).
6. Establish
   \[
   (A+B)^T=A^T+B^T,
   \qquad
   (cA)^T=cA^T.
   \]
7. Show that product order reverses:
   \[
   (AB)^T=B^TA^T.
   \]
8. Introduce symmetric matrices with \(A^T=A\).
9. Include a Pause-and-Predict dimension question.
10. Bridge to Order, Identity, and Undoing.

## Apply

```zsh
chmod +x ~/Downloads/seeing_linear_algebra_cp102/apply_checkpoint_102.zsh
~/Downloads/seeing_linear_algebra_cp102/apply_checkpoint_102.zsh
```

## Check

```zsh
./scripts/check_cp102_matrix_transposition.zsh
```

## Render

```zsh
./scripts/render_cp102_matrix_transposition.zsh
```

Do not commit until the render has been reviewed and approved.
