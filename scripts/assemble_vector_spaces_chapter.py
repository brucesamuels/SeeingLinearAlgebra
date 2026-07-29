"""Assemble rendered chapter segments without requiring a system ffmpeg binary."""
from __future__ import annotations

import argparse
from fractions import Fraction
from pathlib import Path
import sys

try:
    import av
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit(
        "PyAV is required for chapter assembly. It is normally installed with Manim."
    ) from exc


def read_concat_file(path: Path) -> list[Path]:
    segments: list[Path] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if not (line.startswith("file '") and line.endswith("'")):
            raise ValueError(f"Unsupported concat entry: {raw_line}")
        encoded = line[6:-1]
        decoded = encoded.replace("'\\''", "'")
        segment = Path(decoded)
        if not segment.is_file():
            raise FileNotFoundError(f"Rendered segment not found: {segment}")
        segments.append(segment)
    if not segments:
        raise ValueError("No rendered segments were listed for assembly")
    return segments


def _frame_rate(stream: av.video.stream.VideoStream) -> Fraction:
    rate = stream.average_rate or stream.guessed_rate or Fraction(15, 1)
    return Fraction(rate)


def assemble(segments: list[Path], output_path: Path, duration_factor: float = 1.0) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with av.open(str(segments[0])) as first_container:
        first_stream = first_container.streams.video[0]
        width = first_stream.codec_context.width
        height = first_stream.codec_context.height
        rate = _frame_rate(first_stream)

    output = av.open(str(output_path), mode="w")
    try:
        try:
            output_stream = output.add_stream("libx264", rate=rate)
        except av.AVError:
            output_stream = output.add_stream("mpeg4", rate=rate)
        output_stream.width = width
        output_stream.height = height
        output_stream.pix_fmt = "yuv420p"
        output_stream.options = {"crf": "18", "preset": "medium"}

        frame_index = 0
        source_frame_index = 0
        for segment in segments:
            with av.open(str(segment)) as container:
                video_stream = container.streams.video[0]
                for frame in container.decode(video_stream):
                    if frame.width != width or frame.height != height:
                        frame = frame.reformat(width=width, height=height, format="yuv420p")
                    target_total = int(round((source_frame_index + 1) * duration_factor))
                    copies = max(1, target_total - frame_index)
                    for _ in range(copies):
                        output_frame = frame.reformat(width=width, height=height, format="yuv420p")
                        output_frame.pts = frame_index
                        output_frame.time_base = Fraction(rate.denominator, rate.numerator)
                        frame_index += 1
                        for packet in output_stream.encode(output_frame):
                            output.mux(packet)
                    source_frame_index += 1

        for packet in output_stream.encode():
            output.mux(packet)
    finally:
        output.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("concat_file", type=Path)
    parser.add_argument("output_file", type=Path)
    parser.add_argument(
        "--duration-factor",
        type=float,
        default=1.0,
        help="Multiply the chapter duration without rerendering scenes (for example, 1.25 makes it 25%% longer).",
    )
    args = parser.parse_args()
    if args.duration_factor < 1.0:
        parser.error("--duration-factor must be at least 1.0")

    try:
        segments = read_concat_file(args.concat_file)
        assemble(segments, args.output_file, duration_factor=args.duration_factor)
    except Exception as exc:
        print(f"Chapter assembly failed: {exc}", file=sys.stderr)
        return 1

    print(f"Chapter assembly complete: {args.output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
