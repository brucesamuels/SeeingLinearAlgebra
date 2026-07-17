# Engine v0.3 - Checkpoint 42

## Goal

Prove directly that scalar multiplication is already represented by the
existing renderer-independent linear-combination pipeline as its one-term case.

Checkpoint 42 adds tests only. It adds no new engine class.

## Mathematical interpretation

For one fixed vector `v` and one coefficient `c`:

```text
LinearCombination([v]).snapshot([c])
```

should produce:

```text
coefficients = [c]
terms = [c v]
partial_sums = [0, c v]
result = c v
```

The corresponding geometry should contain:

```text
one term segment from 0 to c v
one resultant segment from 0 to c v
```

This is scalar multiplication without a duplicate mathematical abstraction.

## Direct cases

The focused tests verify:

```text
c > 1       stretching
0 < c < 1   shrinking
c = 0       collapse to zero
c < 0       reversal and scaling
```

They also verify:

- one-term coefficient arrays retain shape `(1,)`;
- interpolation remains exact;
- mathematical term arrays retain one row;
- partial sums contain exactly the origin and endpoint;
- geometry contains exactly one origin-anchored term segment;
- the resultant agrees with that term;
- the existing geometry-path layer accepts the one-term pipeline.

## API compatibility strategy

The external packaging environment did not contain the complete local source
tree. The test therefore uses Python signature inspection only to identify
established public constructor parameter names.

It does not:

- inspect private attributes;
- patch engine code;
- skip failed assertions;
- create substitute mathematics;
- treat incompatible behavior as success.

If the public constructor names differ from the recognized stable patterns, the
test fails with the exact signature so the test can be narrowed to the actual
API.

## Architectural boundary

Checkpoint 42 does not add:

- `ScalarMultiplication`;
- a scalar-specific snapshot;
- scalar-specific geometry;
- scalar-specific interpolation;
- Manim code;
- a scene;
- a lesson wrapper.

The architectural conclusion is:

```text
scalar multiplication = one-term linear combination
```

## Files

```text
CHECKPOINT_42.md
tests/test_scalar_multiplication_one_term.py
scripts/check_scalar_multiplication_one_term.zsh
```

All files are additive.

## Expected test count

Checkpoint 41 was expected to pass approximately 515 tests.

Checkpoint 42 adds nine collected test cases, for an expected total near:

```text
524 passed
```

The exact total depends on local parametrization.

## Render decision

No render is required. This checkpoint proves mathematics and geometry only.

## Next checkpoint

If these direct tests pass, Checkpoint 43 should create the smallest
renderer-independent scalar-multiplication lesson configuration by composing:

```text
one fixed vector
one coefficient sweep
existing linear-combination mathematics
existing geometry path
existing display projection
lesson-sequence metadata
```

That configuration should contain pedagogical constants and composition only,
not duplicate arithmetic.
