\
    # Checkpoint 60 — Commutativity of Vector Addition

    ## Objective

    Add a standalone lesson showing geometrically that

    \[
    \mathbf u+\mathbf v=\mathbf v+\mathbf u.
    \]

    The lesson reuses

    \[
    \mathbf u=(3,1),
    \qquad
    \mathbf v=(1,2),
    \]

    so both orders reach

    \[
    (4,3).
    \]

    ## Pedagogical sequence

    1. Show \(\mathbf u\) and \(\mathbf v\) in standard position.
    2. Ask what changes when their order is reversed.
    3. Construct \(\mathbf u+\mathbf v\).
    4. Preserve that route and construct \(\mathbf v+\mathbf u\).
    5. Observe that the two paths form the parallelogram and reach the same
       endpoint.
    6. State the commutative property.

    ## Architecture

    CP60 introduces no new vector arithmetic.

    The scene evaluates the existing renderer-independent `VectorAddition`
    model twice:

    ```python
    VectorAddition(u, v).snapshot()
    VectorAddition(v, u).snapshot()
    ```

    The Manim scene owns only the two route constructions, labels, screen
    layout, and pacing.

    ## Added files

    - `engine/vector_addition_commutativity_lesson.py`
    - `scenes/vector_addition_commutativity_presentation.py`
    - `tests/test_vector_addition_commutativity_lesson.py`
    - `tests/test_vector_addition_commutativity_presentation.py`
    - `scripts/check_vector_addition_commutativity.zsh`
    - `scripts/render_vector_addition_commutativity_presentation.zsh`
    - `CHECKPOINT_60.md`

    No existing repository file or Chapter 1 ordering file is modified.

    ## Verification

    ```zsh
    ./scripts/check_vector_addition_commutativity.zsh
    ```

    ## Render

    ```zsh
    ./scripts/render_vector_addition_commutativity_presentation.zsh
    ```

    ## Next step

    After visual approval, CP61 should introduce vector subtraction as adding
    the negative vector.
