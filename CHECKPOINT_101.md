# Checkpoint 101 — The Trace of a Matrix

## Chapter role

This checkpoint introduces trace before the chapter's final conceptual lesson
on order, identity, and undoing.

Trace is presented as a scalar-valued function on square matrices. Its deeper
connection to eigenvalues is previewed but deferred.

## Storyboard

1. Highlight the main diagonal of a 3×3 matrix.
2. Add its entries to compute the trace.
3. State
   \[
   \operatorname{tr}(A)=\sum_{i=1}^{n}a_{ii}.
   \]
4. Contrast matrix-valued operations with the scalar-valued trace.
5. Explain that trace is defined only for square matrices.
6. Show linearity:
   \[
   \operatorname{tr}(A+B)=\operatorname{tr}(A)+\operatorname{tr}(B),
   \]
   \[
   \operatorname{tr}(cA)=c\,\operatorname{tr}(A).
   \]
7. Compare \(AB\) and \(BA\):
   \[
   AB\ne BA,\qquad
   \operatorname{tr}(AB)=\operatorname{tr}(BA).
   \]
8. Include a Pause-and-Predict calculation.
9. Preview the future relationship between trace and eigenvalues.
10. Bridge to CP102: Order, Identity, and Undoing.

## Apply

```zsh
chmod +x ~/Downloads/seeing_linear_algebra_cp101_trace/apply_checkpoint_101.zsh
~/Downloads/seeing_linear_algebra_cp101_trace/apply_checkpoint_101.zsh
```

## Check

```zsh
./scripts/check_cp101_matrix_trace.zsh
```

## Render

```zsh
./scripts/render_cp101_matrix_trace.zsh
```

Do not commit until the render has been reviewed and approved.
