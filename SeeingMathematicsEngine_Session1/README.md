# Seeing Mathematics Engine

Reusable Manim framework for **Seeing Linear Algebra** and future
**Seeing Calculus** projects.

## Session 1 milestone

This package establishes the design philosophy, visual standards, repository
layout, production workflow, Git guidance, initial engine modules, a validation
script, and the Episode 2 production brief.

## Validate

```zsh
./scripts/check_project.zsh
```

## Smoke test

```zsh
python3 -m manim -pql tests/test_engine.py EngineSmokeTest
```

Place the Brooklyn Tech seal at `assets/BTHSseal.jpeg`. A placeholder is used
when the seal is absent.
