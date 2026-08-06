#!/bin/zsh
set -euo pipefail

REPO="${0:A:h:h}"
cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

for command_name in python ffmpeg ffprobe; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    print -u2 -- "Required command is not available: $command_name"
    exit 1
  fi
done

if [[ -n "${1:-}" && "${1:-}" != "--preview" ]]; then
  print -u2 -- "Usage: $0 [--preview]"
  exit 1
fi

print -- "Preparing all Chapter 4 clips at 1080p60..."
print -- "Any missing high-quality lesson renders will be created automatically."
python scripts/build_cp127_chapter_four.py --render-missing

OUTPUT="$REPO/media/ChapterFourSolvingLinearSystems.mp4"
print
print -- "Complete chapter:"
print -- "  $OUTPUT"

if [[ "${1:-}" == "--preview" ]]; then
  open "$OUTPUT"
fi
