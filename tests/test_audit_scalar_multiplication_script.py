from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_script_generates_repository_audit(tmp_path: Path) -> None:
    output = tmp_path / "audit.md"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/audit_scalar_multiplication.py",
            "--repo-root",
            ".",
            "--output",
            str(output),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output.is_file()
    assert "Scalar Multiplication Reuse Audit" in output.read_text(
        encoding="utf-8"
    )
    assert "core_pipeline_symbols" in result.stdout
