# Checkpoint 207 — Why Covariance Is Positive Semidefinite

This lesson introduces covariance from first principles before connecting it to
positive semidefiniteness. It moves from raw observations to their mean, centered
data, covariance entries, directional variance, and finally the scaled Gram-matrix
identity.

## Numerical spine

- Raw observations are `(1,1)`, `(3,1)`, `(3,3)`, and `(5,3)`.
- Their mean is `mu=(3,2)`.
- The centered data matrix is
  `C=[[-2,-1],[0,-1],[0,1],[2,1]]`.
- Population covariance uses `Sigma=(1/4) C^T C`.
- `C^T C=[[8,4],[4,4]]`, so `Sigma=[[2,1],[1,1]]`.
- For `v=(1,0)`, the centered projections are `(-2,0,0,2)` and
  `v^T Sigma v=2`.
- In general, `v^T Sigma v=(1/m)||Cv||^2>=0`.
- The singular example starts with raw points `(2,3)`, `(3,5)`, `(4,7)`.
- Its centered rows lie on `y=2x`; for `v=(-2,1)`, every projection is zero.

## Story

1. Plot the raw observations and identify their mean.
2. Subtract the mean and show the centered point cloud.
3. Stack centered observations as rows of `C`.
4. Define population covariance as both an average of outer products and
   `(1/m)C^T C`.
5. Explain diagonal variances and off-diagonal joint variation.
6. Compute the example covariance structurally.
7. Project the centered observations onto one direction and interpret
   `v^T Sigma v` as directional variance.
8. Derive the squared-norm identity and positive semidefiniteness.
9. Pause and ask when a nonzero direction can have zero variance.
10. Use line data to show all projections collapsing to zero.
11. Finish with the full-column-rank condition for positive definiteness.

The final note distinguishes the population factor `1/m` from the sample factor
`1/(m-1)` and explains that positive scaling does not change definiteness. PCA,
correlation, whitening, and statistical inference remain outside this checkpoint.

## Environment and commands

Use Python 3.12 with Manim Community 0.21.0. Both scripts set `PYTHONPATH` to the
repository root and reject a different active environment.

```zsh
conda activate seeingla-manim021
zsh scripts/check_cp207_covariance_definiteness.zsh
zsh scripts/render_cp207_covariance_definiteness.zsh
```

The render command produces only a low-quality preview.
