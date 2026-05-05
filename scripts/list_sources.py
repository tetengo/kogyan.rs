# Lists the Rust program sources.
# Copyright (C) 2024-2026 kaoru  <https://www.tetengo.org>

from pathlib import Path

IGNORED_DIRECTORIES = {".git", "target"}


def list_rs_files(base_path: Path) -> list[Path]:
    return [
        path
        for path in base_path.rglob("*.rs")
        if path.is_file()
        and path.relative_to(base_path).parts[0] not in IGNORED_DIRECTORIES
    ]
