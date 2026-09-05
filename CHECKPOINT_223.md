# Checkpoint 223 — Singular Values, Rank, and Approximation: The Big Picture

This checkpoint closes the instructional sequence by synthesizing the chapter
rather than adding a new theorem. Its organizing principle is that the
singular-value spectrum reveals what a matrix preserves, loses, amplifies, and
approximates.

## Numerical anchor

Use the rectangular matrix

```text
A = [[3,0],[0,1/2],[0,0]].
```

Its singular values are `3` and `1/2`, its rank is two, and its condition
number is six. The pseudoinverse reverses the positive stretches with values
`1/3` and `2`. Its rank-one approximation discards `1/2`, so the Frobenius
error is exactly `1/2`.

## Presentation sequence

1. Reassemble `A=U Sigma V^T` as input directions, stretches, and output directions.
2. Interpret zero, small, and large singular values.
3. Organize the four fundamental subspaces using positive and zero singular values.
4. Review the pseudoinverse with image and pre-image language.
5. Distinguish invertibility from conditioning and inverse amplification.
6. Review truncated SVD and best rank-`k` approximation.
7. Compare image compression with PCA as two uses of the same low-rank idea.
8. Give a four-way recognition guide for inverse, pseudoinverse, truncated SVD, and PCA.
9. Conclude that singular values reveal what is preserved, lost, amplified, and approximated.

## Files

- `engine/svd_chapter_synthesis.py`
- `scenes/svd_chapter_synthesis_presentation.py`
- `tests/test_svd_chapter_synthesis.py`
- `tests/test_svd_chapter_synthesis_presentation.py`
- `scripts/check_cp223_svd_chapter_synthesis.zsh`
- `scripts/render_cp223_svd_chapter_synthesis.zsh`
- `apply_checkpoint_223.zsh`

## Review workflow

```zsh
./scripts/check_cp223_svd_chapter_synthesis.zsh
./scripts/render_cp223_svd_chapter_synthesis.zsh
```

Review the 480p preview before committing. Chapter preview assembly and the
final high-definition master remain separate checkpoints.

## Pacing revision

The review pass lengthens each completed-card hold by approximately 1.5 seconds
and softens the heading transitions. The source scene now runs near 77 seconds,
giving the dense synthesis formulas and recognition cards more reading time
without slowing their internal build animations.
