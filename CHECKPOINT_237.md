# Checkpoint 237 — Long-Term Probabilities and Steady States

This checkpoint develops steady states through a complete numerical example in
`R^4`. Students compute successive probability vectors `x_k=A^k x_0`, identify
their limiting pattern, derive a formula for every power of `A`, and then solve
`Ax=x` directly. Absorbing states appear afterward as a contrast: they can
produce several steady distributions whose eventual mixture depends on the
starting probabilities.

## Source basis

The lesson's conceptual order and terminology are adapted from Howard Anton and
Chris Rorres, *Elementary Linear Algebra: Applications Version*, 11th edition,
Section 10.4, "Markov Chains" (pp. 551-559), supplied for this checkpoint. In
particular, the lesson follows the source's progression from transition
probabilities and column-stochastic Markov matrices to probability vectors,
`x_{k+1}=Ax_k`, powers `A^k x_0`, regularity, convergence, and the normalized
fixed-point equation `Aq=q`. The presentation paraphrases the source and uses an
original four-state example and original graphics rather than reproducing its
examples or page design.

The absorbing-state contrast is an extension requested for this course; it is
not developed in the supplied excerpt. The two-state periodic contrast follows
the source's nonconvergent switching example.

## Exact four-state spine

At each step, the chain stays at its current state with probability `1/2` or
chooses uniformly among all four states with probability `1/2`. Thus staying has
total probability `1/2+(1/2)(1/4)=5/8`, while moving to each different state has
probability `1/8`. With column probability vectors,

```text
    [5/8 1/8 1/8 1/8]
A = [1/8 5/8 1/8 1/8]
    [1/8 1/8 5/8 1/8]
    [1/8 1/8 1/8 5/8].
```

Here `A` is explicitly identified as a transition matrix, not the adjacency
matrix denoted by `A` earlier in the graph chapter.

Starting at state 1 gives

```text
x0 = (1,0,0,0)^T
x1 = A x0   = (5/8,1/8,1/8,1/8)^T
x2 = A^2 x0 = (7/16,3/16,3/16,3/16)^T
x3 = A^3 x0 = (11/32,7/32,7/32,7/32)^T.
```

The scene computes coordinates of `x2` directly from the matrix-vector product,
then uses

```text
U = (1/4) 1 1^T,
A = U + (1/2)(I-U),
A^k = U + 2^(-k)(I-U).
```

Therefore

```text
x_k = (1/4)1 + 2^(-k)(e1-(1/4)1)
    -> (1/4,1/4,1/4,1/4)^T.
```

Solving the steady-state equation independently gives the same vector. Since
`1^T x=1`,

```text
Ax = (1/2)x + (1/8)1 = x
```

implies `x=(1/4)1`.

## Absorbing-state contrast

A second four-state chain sends state 1 to state 2, then splits equally between
absorbing states 3 and 4. Both `e3` and `e4` are steady, and every normalized
mixture

```text
x=(0,0,t,1-t)^T
```

satisfies `Bx=x`. Starting at state 1 yields

```text
B^2 e1 = (0,0,1/2,1/2)^T.
```

This example makes the distinction explicit: `Ax=x` finds steady states, while
powers of the transition matrix determine whether a chosen initial distribution
converges and which steady distribution it reaches.

## Story

1. Define a probability vector in `R^4` and pose the question `x_k=A^k x_0`.
2. State the numerical transition rule before showing its matrix.
3. Build the structural four-by-four column-stochastic matrix `A`.
4. Compute `x1=Ae1` as the first column of `A`.
5. Compute coordinates of `x2=A^2e1` through matrix-vector multiplication.
6. Animate `x1`, `x2`, and `x3` and identify the emerging limit.
7. Define a regular Markov matrix, observe that this positive `A` is regular,
   and derive `A^k=U+2^(-k)(I-U)` and the exact formula for `x_k`.
8. Solve `Ax=x` with the probability normalization `1^T x=1`.
9. Contrast the unique mixing steady state with multiple absorbing steady states.
10. Separate regular convergence, absorbing behavior, and periodic behavior;
    distinguish the fixed-point question from the convergence question; and
    preview PageRank.

## Architecture

`MarkovLongTermBehavior` is renderer-independent. It validates finite
column-stochastic matrices and probability distributions; creates point masses;
computes steps, powers, and trajectories; tests stationarity; detects absorbing
states; identifies regularity by searching for a positive matrix power;
evaluates the exact four-state mixing power formula; approximates
absorption probabilities; computes fixed-space dimensions; and measures
total-variation distance. Class constructors provide the mixing, absorbing,
alternating, and branching examples.

The scene follows the established chapter chrome and pacing. Structural matrices
use generous fraction spacing, standalone entries align with fraction bars,
vertex numerals remain black inside yellow states, probability mass is shown by
halos, and bottom captions maintain safe margins.

## Scope boundary

This checkpoint develops finite, time-homogeneous Markov chains through one
fully worked convergent example and one compact absorbing contrast. It does not
introduce canonical block form, the fundamental matrix, expected absorption
times, irreducibility, formal recurrence theory, or general classification
theorems. Its purpose is to establish the distinction between fixed points and
long-term convergence before PageRank in CP238.

## Files

```text
engine/markov_long_term_behavior.py
scenes/markov_long_term_behavior_presentation.py
tests/test_markov_long_term_behavior.py
tests/test_markov_long_term_behavior_presentation.py
scripts/check_cp237_markov_long_term_behavior.zsh
scripts/render_cp237_markov_long_term_behavior.zsh
CHECKPOINT_237.md
apply_checkpoint_237.zsh
```

## Commands

Use Python 3.12 and Manim Community 0.21.0:

```zsh
conda activate seeingla-manim021
scripts/check_cp237_markov_long_term_behavior.zsh
scripts/render_cp237_markov_long_term_behavior.zsh
```

The render command produces only an uncached low-quality preview for review.
