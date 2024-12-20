#! /usr/bin/env python
# Check the use declaration order.
# Copyright (C) 2024 kaoru  <https://www.tetengo.org>

import re
import sys
from pathlib import Path

import list_sources


def main(args: list[str]) -> None:
    if len(args) < 1:
        print("Usage: check_use_order.py base_directory_path", file=sys.stderr)
        sys.exit(0)

    paths = list_sources.list_rs_files(Path(sys.argv[1]))
    failure = False
    for path in paths:
        if not check_use_order(path):
            failure = True

    if failure:
        sys.exit(1)


USE_PATTERN = re.compile(r"\s*use\s+([^;]+);\s*")


def check_use_order(path: Path) -> bool:
    use_declarations = make_use_declarations(path)

    for d in use_declarations:
        if d[1].count(9999) > 0:
            print("Unexpected use declaration: {}".format(path), file=sys.stderr)
            return False
        if len(d[1]) > 0 and d[1] != len(d[1]) * [d[1][0]]:
            print("Mixed use declaration: {}".format(path), file=sys.stderr)
            return False

    sorted_use_declarations = sorted(use_declarations)
    if use_declarations != sorted_use_declarations:
        print("Unsorted use declaration: {}".format(path), file=sys.stderr)
        return False

    return True


def make_use_declarations(path: Path) -> list[tuple[int, list[int]]]:
    use_declarations: list[tuple[int, list[int]]] = [(0, [])]
    with path.open(mode="r", encoding="UTF-8") as file:
        for line in file:
            line = line.rstrip("\r\n")

            matched = USE_PATTERN.fullmatch(line)
            if matched:
                id = to_id(matched.group(1))
                use_declarations[-1][1].append(id)
                continue

            if len(line) == 0:
                if len(use_declarations[-1][1]) > 0:
                    section_index = use_declarations[-1][0]
                    use_declarations.append((section_index, []))
                continue

            section_index = use_declarations[-1][0]
            if len(use_declarations[-1][1]) == 0:
                use_declarations[-1] = (section_index + 1, use_declarations[-1][1])
            else:
                use_declarations.append((section_index + 1, []))
    if len(use_declarations[-1][1]) == 0:
        use_declarations.pop()
    return use_declarations


TETENGO_CRATE_PATTERN = re.compile(r"tetengo_[a-z0-9_]+::.*")

LOCAL_CRATE_PATTERN = re.compile(r"crate::[a-z0-9_]+.*")

OTHER_CRATE_PATTERN = re.compile(r"[a-z0-9_]+.*")


def to_id(name: str) -> int:
    if name.startswith("std::"):
        return 0

    if name.startswith("super::"):
        return 4

    matched = TETENGO_CRATE_PATTERN.fullmatch(name)
    if matched:
        return 2

    matched = LOCAL_CRATE_PATTERN.fullmatch(name)
    if matched:
        return 3

    matched = OTHER_CRATE_PATTERN.fullmatch(name)
    if matched and not name.startswith("crate::"):
        return 1

    return 9999


if __name__ == "__main__":
    main(sys.argv[1:])
