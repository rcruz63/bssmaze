from pathlib import Path

from check_file_length import HARD_LIMIT, find_violations


def write_lines(path: Path, total: int) -> None:
    path.write_text("x = 1\n" * total, encoding="utf-8")


def test_file_at_limit_is_accepted(tmp_path: Path) -> None:
    write_lines(tmp_path / "ok.py", HARD_LIMIT)
    assert find_violations(tmp_path) == {}


def test_file_over_limit_is_reported(tmp_path: Path) -> None:
    write_lines(tmp_path / "big.py", HARD_LIMIT + 1)
    assert find_violations(tmp_path) == {tmp_path / "big.py": HARD_LIMIT + 1}


def test_generated_and_cache_files_are_ignored(tmp_path: Path) -> None:
    write_lines(tmp_path / "uv.lock", HARD_LIMIT + 50)
    (tmp_path / ".venv").mkdir()
    write_lines(tmp_path / ".venv" / "lib.py", HARD_LIMIT + 50)
    assert find_violations(tmp_path) == {}
