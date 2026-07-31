"""Render the current Chapter 1 lessons and concatenate them into one video."""

from __future__ import annotations

import argparse
import ast
import subprocess
from pathlib import Path

from engine.chapter_one_lesson_manifest import CHAPTER_ONE_LESSONS, locate_scene_file


QUALITY_FOLDERS = {
    "l": "480p15",
    "m": "720p30",
    "h": "1080p60",
    "p": "1440p60",
    "k": "2160p60",
}


def discover_scene_class(scene_file: Path) -> str:
    tree = ast.parse(scene_file.read_text(encoding="utf-8"))
    candidates = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        base_names = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                base_names.append(base.id)
            elif isinstance(base, ast.Attribute):
                base_names.append(base.attr)
        if any(name.endswith("Scene") for name in base_names):
            candidates.append(node.name)

    presentation_candidates = [
        name for name in candidates if name.endswith("Presentation")
    ]
    if len(presentation_candidates) == 1:
        return presentation_candidates[0]
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        raise RuntimeError(f"No Manim Scene subclass found in {scene_file}")
    raise RuntimeError(
        f"Ambiguous Manim scene classes in {scene_file}: {', '.join(candidates)}"
    )


def rendered_video_path(media_dir: Path, scene_file: Path, class_name: str, quality: str) -> Path:
    return (
        media_dir
        / "videos"
        / scene_file.stem
        / QUALITY_FOLDERS[quality]
        / f"{class_name}.mp4"
    )


def render_scene(repo: Path, media_dir: Path, scene_file: Path, class_name: str, quality: str) -> Path:
    subprocess.run(
        [
            "manim",
            f"-q{quality}",
            "--media_dir",
            str(media_dir),
            str(scene_file),
            class_name,
        ],
        cwd=repo,
        check=True,
    )
    video = rendered_video_path(media_dir, scene_file, class_name, quality)
    if not video.exists():
        raise FileNotFoundError(f"Expected rendered video not found: {video}")
    return video


def concatenate(videos: list[Path], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    concat_file = output.parent / "cp91_concat.txt"
    concat_file.write_text(
        "".join(f"file '{video.resolve()}'\n" for video in videos),
        encoding="utf-8",
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_file), "-c", "copy", str(output),
        ],
        check=True,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--quality", choices=tuple(QUALITY_FOLDERS), default="l")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo = args.repo_root.resolve()
    media_dir = repo / "media"
    scenes_dir = repo / "scenes"

    subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.DEVNULL)

    title_file = scenes_dir / "chapter_one_title_card.py"
    title_class = "ChapterOneTitleCard"
    videos = [render_scene(repo, media_dir, title_file, title_class, args.quality)]

    print("Chapter 1 lesson files:")
    for index, lesson in enumerate(CHAPTER_ONE_LESSONS, start=1):
        scene_file = locate_scene_file(scenes_dir, lesson)
        class_name = discover_scene_class(scene_file)
        print(f"  {index:02d}. {lesson.title}: {scene_file.name} / {class_name}")
        videos.append(render_scene(repo, media_dir, scene_file, class_name, args.quality))

    output = (
        media_dir
        / "videos"
        / "chapter_one_assembly"
        / QUALITY_FOLDERS[args.quality]
        / "ChapterOneAssembly.mp4"
    )
    concatenate(videos, output)
    print(f"Complete Chapter 1 video: {output}")


if __name__ == "__main__":
    main()
