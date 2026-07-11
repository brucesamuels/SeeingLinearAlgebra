# Git Workflow

Keep one permanent repository on the desktop Mac.

```zsh
git status
git add .
git commit -m "Meaningful description"
git push
```

Commit source, narration, documentation, scripts, tests, and small image assets.

Do not commit Manim cache or large rendered videos.

Approved milestones may be tagged:

```zsh
git tag -a v0.1-engine -m "Initial reusable engine foundation"
git push origin v0.1-engine
```
