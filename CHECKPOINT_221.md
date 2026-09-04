# Checkpoint 221 — Image Compression with the SVD

This lesson applies truncated SVD to a deterministic grayscale image. It treats
pixel brightness as matrix data, compares rank-one, rank-four, and rank-eight
reconstructions, and makes the storage-versus-fidelity tradeoff explicit.

## Numerical spine

Use a generated `32 x 32` grayscale landscape with values in `[0,1]`.

- The original image stores `32*32=1024` brightness values.
- Rank-`k` reconstruction keeps the first `k` singular image layers.
- Retained energy is the fraction of squared singular values kept.
- Relative Frobenius error is the square root of the discarded energy fraction.
- Rank four stores `4(32+32+1)=260` values.
- Rank-four storage is about `25.4%` of the original, a compression ratio of
  about `3.94` to one.
- Rank-one, rank-four, and rank-eight images show progressively greater fidelity.

## Story

1. Interpret a grayscale image as a matrix of pixel brightness values.
2. Decompose the image into ordered rank-one patterns.
3. Display the singular-value spectrum.
4. Show the rank-one reconstruction and its broad structure.
5. Show the rank-four reconstruction and its storage count.
6. Show the rank-eight reconstruction and its reduced error.
7. Define Frobenius error and retained energy from discarded singular values.
8. Compare original storage with rank-four SVD storage.
9. Place the original and three reconstructions side by side.
10. Finish with rank selection as a balance between compression and fidelity.

## Architecture

`SVDImageCompression` composes the CP220 `TruncatedSVDApproximation` model. It
provides a deterministic synthetic image, reconstructions, singular values,
Frobenius error, retained energy, storage counts, storage fractions, and
compression ratios without depending on Manim.

## Scope boundary

This checkpoint uses one grayscale matrix. RGB channel handling, external image
assets, PCA, and covariance remain outside its scope.

## Commands

```zsh
conda activate seeingla-manim021
scripts/check_cp221_svd_image_compression.zsh
scripts/render_cp221_svd_image_compression.zsh
```

The render command produces only a low-quality preview.

## Files

```text
engine/svd_image_compression.py
scenes/svd_image_compression_presentation.py
tests/test_svd_image_compression.py
tests/test_svd_image_compression_presentation.py
scripts/check_cp221_svd_image_compression.zsh
scripts/render_cp221_svd_image_compression.zsh
CHECKPOINT_221.md
apply_checkpoint_221.zsh
```
