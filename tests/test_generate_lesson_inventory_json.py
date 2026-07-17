from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_json_generator_writes_and_checks_export(tmp_path: Path) -> None:
    output = tmp_path / "inventory.json"

    write_result = subprocess.run(
        [
            sys.executable,
            "scripts/generate_lesson_inventory_json.py",
            "--output",
            str(output),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert write_result.returncode == 0
    assert output.is_file()

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["schema_version"] == 1
    assert payload["is_valid"] is True

    check_result = subprocess.run(
        [
            sys.executable,
            "scripts/generate_lesson_inventory_json.py",
            "--output",
            str(output),
            "--check",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert check_result.returncode == 0
    assert "JSON inventory is current" in check_result.stdout


def test_json_generator_detects_stale_export(tmp_path: Path) -> None:
    output = tmp_path / "inventory.json"
    output.write_text("{}\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/generate_lesson_inventory_json.py",
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
