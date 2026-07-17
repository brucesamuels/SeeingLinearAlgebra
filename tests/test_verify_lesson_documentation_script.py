from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_verification_script_accepts_generated_files(tmp_path: Path) -> None:
    markdown_path = tmp_path / "LESSON_INVENTORY.md"
    json_path = tmp_path / "LESSON_INVENTORY.json"

    generate_markdown = subprocess.run(
        [
            sys.executable,
            str(Path.cwd() / "scripts/generate_lesson_inventory.py"),
            "--output",
            str(markdown_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert generate_markdown.returncode == 0

    generate_json = subprocess.run(
        [
            sys.executable,
            str(Path.cwd() / "scripts/generate_lesson_inventory_json.py"),
            "--output",
            str(json_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert generate_json.returncode == 0

    script = Path.cwd() / "scripts/verify_lesson_documentation.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
        env={
            **__import__("os").environ,
            "PYTHONPATH": str(Path.cwd()),
        },
    )

    assert result.returncode == 0
    assert "Lesson documentation verified" in result.stdout


def test_verification_script_rejects_stale_files(tmp_path: Path) -> None:
    (tmp_path / "LESSON_INVENTORY.md").write_text(
        "# stale\n",
        encoding="utf-8",
    )
    (tmp_path / "LESSON_INVENTORY.json").write_text(
        "{}\n",
        encoding="utf-8",
    )

    script = Path.cwd() / "scripts/verify_lesson_documentation.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
        env={
            **__import__("os").environ,
            "PYTHONPATH": str(Path.cwd()),
        },
    )

    assert result.returncode != 0
    assert "verification failed" in result.stderr
