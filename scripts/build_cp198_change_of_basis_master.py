#!/usr/bin/env python3
"""Assemble and slow the 1080p60 Change of Basis master."""
from __future__ import annotations

import argparse
import importlib.util
import shutil
import subprocess
from pathlib import Path


DEFAULT_SPEED = 0.85


def load_preview_builder(repo_root: Path):
    builder_path = repo_root / "scripts" / "build_cp197_change_of_basis_preview.py"
    if not builder_path.is_file():
        raise FileNotFoundError(f"Missing CP197 builder: {builder_path}")
    spec = importlib.util.spec_from_file_location("change_of_basis_preview_builder", builder_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def has_audio(ffprobe: str, source: Path) -> bool:
    command = [
        ffprobe, "-v", "error", "-select_streams", "a:0",
        "-show_entries", "stream=index", "-of", "csv=p=0", str(source),
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return bool(result.stdout.strip())


def slow_master(source: Path, output: Path, speed: float = DEFAULT_SPEED) -> Path:
    if not 0.5 <= speed <= 1.0:
        raise ValueError("speed must be between 0.5 and 1.0")
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if ffmpeg is None or ffprobe is None:
        raise RuntimeError("ffmpeg and ffprobe are required")
    output.parent.mkdir(parents=True, exist_ok=True)
    video_filter = f"setpts=PTS/{speed:.6f}"
    common = [
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", "60", "-movflags", "+faststart",
    ]
    if has_audio(ffprobe, source):
        command = [
            ffmpeg, "-y", "-i", str(source),
            "-filter_complex", f"[0:v]{video_filter}[v];[0:a]atempo={speed:.6f}[a]",
            "-map", "[v]", "-map", "[a]", *common,
            "-c:a", "aac", "-b:a", "192k", str(output),
        ]
    else:
        command = [
            ffmpeg, "-y", "-i", str(source), "-vf", video_filter,
            "-an", *common, str(output),
        ]
    subprocess.run(command, check=True)
    return output


def build_master(repo_root: Path, quality: str, speed: float) -> tuple[Path, Path]:
    builder = load_preview_builder(repo_root)
    media_root = repo_root / "media"
    normal_master = media_root / "change_of_basis_master.mp4"
    slowed_master = media_root / "change_of_basis_master_85pct.mp4"
    builder.assemble(media_root, normal_master, quality)
    slow_master(normal_master, slowed_master, speed)
    print(f"Normal-speed master: {normal_master.resolve()}")
    print(f"{speed:.0%}-speed classroom master: {slowed_master.resolve()}")
    return normal_master, slowed_master


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--quality", default="1080p60")
    parser.add_argument("--speed", type=float, default=DEFAULT_SPEED)
    args = parser.parse_args()
    build_master(args.repo_root.resolve(), args.quality, args.speed)


if __name__ == "__main__":
    main()

