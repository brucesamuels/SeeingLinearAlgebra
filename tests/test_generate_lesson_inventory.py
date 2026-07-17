from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_generator_writes_and_checks_inventory(tmp_path: Path) -> None:
    output = tmp_path / "inventory.md"

    write_result = subprocess.run(
        [
            sys.executable,
            "scripts/generate_lesson_inventory.py",
            "--output",
            str(output),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert write_result.returncode == 0
    assert output.is_file()

    check_result = subprocess.run(
        [
            sys.executable,
            "scripts/generate_lesson_inventory.py",
            "--output",
            str(output),
            "--check",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert check_result.returncode == 0
    assert "Inventory is current" in check_result.stdout


def test_generator_detects_stale_inventory(tmp_path: Path) -> None:
    output = tmp_path / "inventory.md"
    output.write_text("stale\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/generate_lesson_inventory.py",
            "--output",
            str(output),
            "--check",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "out of date" in result.stderr
