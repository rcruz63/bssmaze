import subprocess
from pathlib import Path

from check_gitignore_kiro import PROBE_PATHS


def test_repository_does_not_ignore_kiro() -> None:
    root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        ["git", "check-ignore", *PROBE_PATHS],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.stdout.strip() == ""
