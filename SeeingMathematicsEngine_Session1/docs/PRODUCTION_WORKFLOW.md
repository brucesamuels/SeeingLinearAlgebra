# Production Workflow

## Portable-device phase

1. Upload lesson notes, sketches, HTML models, or references.
2. Define learning objectives.
3. Plan scenes and narration.
4. Identify reusable engine components.
5. Generate focused file updates.

## Desktop phase

1. Enter the permanent repository.
2. Copy or pull the focused update.
3. Run the project checker.
4. Render a low-quality preview.
5. Review mathematics, pacing, and layout.
6. Commit the working revision.
7. Render HD only after approval.

## Standard commands

```zsh
git status
./scripts/check_project.zsh
python3 -m manim -pql tests/test_engine.py EngineSmokeTest
```
