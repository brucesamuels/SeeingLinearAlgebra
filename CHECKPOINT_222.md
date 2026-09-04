# Checkpoint 222 — Principal Component Analysis through the SVD

This lesson interprets truncated SVD as dimensionality reduction for centered
data. It connects the right singular vectors to directions in feature space,
the products `sigma_i u_i` to principal-component scores, and squared singular
values to captured variation.

## Numerical spine

Use the six already-centered observations

```text
(3,2), (2,3), (-3,-2), (-2,-3), (1,1), (-1,-1).
```

With observations stored as rows,

```text
X^T X = [[28,26],[26,28]].
```

The ordered eigenpairs are

```text
lambda_1=54, v_1=(1,1)/sqrt(2)
lambda_2= 2, v_2=(1,-1)/sqrt(2).
```

Therefore `sigma_1^2=54`, `sigma_2^2=2`, and one principal component
preserves `54/(54+2)=96.4%` of the total variation. The rank-one
reconstruction projects every observation onto `y=x`.

## Presentation sequence

1. Ask whether two coordinates can be replaced faithfully by one.
2. Define the mean as the coordinate-wise average and balance point, then center
   each observation by recording its displacement from that average. Note that
   this symmetric example already has zero mean, so `X_c=X`.
3. Identify rows as observations and columns as features.
4. Use `X=U Sigma V^T` to identify scores and feature-space directions.
5. Compute `X^T X` and its two exact eigenpairs.
6. Draw the major and minor principal axes through the data cloud.
7. Form the one-dimensional score vector `z=Xv_1=sigma_1u_1`.
8. Animate the rank-one reconstruction `X_1=(Xv_1)v_1^T`.
9. Compute the retained variation and the two-coordinate to one-score reduction.
10. Conclude that PCA is truncated SVD applied to centered data.

## Files

- `engine/pca_svd.py`
- `scenes/pca_svd_presentation.py`
- `tests/test_pca_svd.py`
- `tests/test_pca_svd_presentation.py`
- `scripts/check_cp222_pca_svd.zsh`
- `scripts/render_cp222_pca_svd.zsh`
- `apply_checkpoint_222.zsh`

## Review workflow

```zsh
./scripts/check_cp222_pca_svd.zsh
./scripts/render_cp222_pca_svd.zsh
```

Review the 480p preview before committing. This checkpoint does not assemble
the chapter or begin the chapter synthesis lesson.

The centering card assumes no statistics prerequisite: it explains why the mean
represents the data's typical location and why PCA measures spread relative to
that location rather than relative to an arbitrary coordinate origin.
