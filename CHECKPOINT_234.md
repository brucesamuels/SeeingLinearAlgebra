# Checkpoint 234 — The Fiedler Vector and Spectral Partitioning

This checkpoint turns the second Laplacian eigenvector into a proposed division
of the graph. The Fiedler coordinates provide a continuous ordering of the
vertices. Thresholding that ordering produces candidate two-way partitions,
which can then be compared with a balance-aware cut score.

## Numerical spine

For the recurring graph, use the exact Fiedler direction

```text
v_2 = (1,1,0,-2)^T.
```

Assign the zero coordinate to the nonnegative side for the first candidate:

```text
S = {1,2,3},    T = {4}.
```

Only the bridge `{3,4}` crosses this partition, so `cut(S,T)=1`. The alternative
partition `{1,2}|{3,4}` cuts both `{1,3}` and `{2,3}`, so its cut size is two.

Use the balance-aware score

```text
RatioCut(S,T) = cut(S,T) (1/|S| + 1/|T|).
```

The two candidates score

```text
{1,2,3}|{4}:  1(1/3+1)     = 4/3,
{1,2}|{3,4}:  2(1/2+1/2)   = 2.
```

The first partition can be encoded by the mean-zero vector

```text
z = (1/3,1/3,1/3,-1)^T,
```

whose Rayleigh quotient is `RatioCut=4/3`. Allowing all real mean-zero vectors
relaxes the discrete cut search; its minimizer is the Fiedler vector, with
quotient `lambda_2=1`.

Sorting the exact coordinates gives

```text
v_4=-2 < v_3=0 < v_1=v_2=1.
```

Only thresholds between distinct values are tested. Their RatioCut scores are
`4/3` and `2`, so the best sweep cut is `{4}|{1,2,3}`.

## Story

1. Recall the exact Fiedler coordinates on the recurring graph.
2. Threshold at zero, explicitly assigning the zero coordinate to the
   nonnegative side, to obtain one candidate partition.
3. Define a cut edge from first principles and highlight the single crossing
   bridge.
4. Show an alternative two-two grouping with two crossing edges.
5. Define RatioCut and compute both candidates with legible fractions.
6. Encode the first discrete cut with a mean-zero, two-level vector and recover
   RatioCut as its Rayleigh quotient.
7. Explain spectral partitioning as a continuous relaxation of the discrete
   search.
8. Sort the Fiedler coordinates, sweep only between distinct values, and select
   the best candidate.
9. Synthesize the solve–sweep–score method, state its scope honestly, and
   preview electrical potentials on graphs.

## Architecture

`SpectralGraphPartition` is renderer-independent and composes CP233's
`GraphLaplacianSpectrum`. It exposes canonical Fiedler coordinates, threshold
and sign partitions, crossing edges, cut size, RatioCut, mean-zero partition
signals, the partition-signal Rayleigh identity, distinct-coordinate sweep
partitions, sweep scores, and the best sweep candidate.

The scene retains the chapter's banner, title, heading, color, spacing, and
pacing conventions. It uses prominent crossing-edge flashes, structural column
vectors, legible fractions, explicit zero-threshold handling, and black
numerals inside colored vertices.

## Scope boundary

This checkpoint presents a two-way unnormalized spectral partition and makes no
claim that the returned cut is optimal for every graph or every cut objective.
It does not introduce normalized Laplacians, multiway clustering, weighted
graphs, statistical clustering assumptions, or electrical laws. Electrical
networks and Laplacian systems begin in CP235.

## Files

```text
engine/spectral_graph_partition.py
scenes/spectral_graph_partition_presentation.py
tests/test_spectral_graph_partition.py
tests/test_spectral_graph_partition_presentation.py
scripts/check_cp234_spectral_graph_partition.zsh
scripts/render_cp234_spectral_graph_partition.zsh
CHECKPOINT_234.md
apply_checkpoint_234.zsh
```

## Commands

Use Python 3.12 and Manim Community 0.21.0:

```zsh
conda activate seeingla-manim021
scripts/check_cp234_spectral_graph_partition.zsh
scripts/render_cp234_spectral_graph_partition.zsh
```

The render command produces only an uncached low-quality preview for review.
