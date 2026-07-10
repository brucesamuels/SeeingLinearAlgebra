# Git workflow for Seeing Linear Algebra

Run Git commands from the project root:

```zsh
cd ~/Documents/School/'Linear Algebra'/SeeingLinearAlgebra
```

## Before replacing files

Save the current working version:

```zsh
git status
git add .
git commit -m "Save working version before Episode 1 v2"
```

## After copying in Episode 1 v2

Review what changed:

```zsh
git status
git diff --stat
git diff
```

Commit the new version:

```zsh
git add common/branding.py assets/BTHSseal.jpeg episode01_vectors README.md GIT_WORKFLOW.md
git commit -m "Rebuild Episode 1 from lesson progression with Brooklyn Tech branding"
```

## Push to GitHub

If a remote already exists:

```zsh
git push
```

To check the remote:

```zsh
git remote -v
```

If no remote exists, create an empty GitHub repository named `SeeingLinearAlgebra`, then run the commands GitHub provides. They will look similar to:

```zsh
git branch -M main
git remote add origin git@github.com:YOUR-USER-NAME/SeeingLinearAlgebra.git
git push -u origin main
```

## A useful checkpoint after a successful render

```zsh
git add .
git commit -m "Episode 1 v2 preview renders successfully"
git push
```

## Do not commit Manim's generated cache

The project's `.gitignore` excludes `media/`. Keep approved videos in `media_exports/`, but large MP4 files are best stored in cloud storage or GitHub Releases rather than normal Git history.

## Recover an older version

See the history:

```zsh
git log --oneline --decorate --graph
```

Restore one file from a previous commit without changing the rest of the project:

```zsh
git restore --source COMMIT_HASH -- episode01_vectors/episode01.py
```
