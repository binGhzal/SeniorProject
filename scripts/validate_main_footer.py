#!/usr/bin/env python3
"""Validate Python files for duplicated __main__ guards and bad footer patterns."""

from __future__ import annotations

import re
import sys
from pathlib import Path

MAIN_GUARD = 'if __name__ == "__main__":'


def validate_file(path: Path) -> list[str]:
    """Return validation errors for duplicated or malformed __main__ footer blocks."""
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")

    main_guard_count = text.count(MAIN_GUARD)
    if main_guard_count > 1:
        errors.append(
            f"{path}: duplicated __main__ guard blocks detected ({main_guard_count} occurrences)."
        )

    bad_indented_cleanup = re.search(
        r"\n\s{8,}ir\.cleanup\(\)\n\n\nif __name__ == \"__main__\":",
        text,
    )
    if bad_indented_cleanup:
        errors.append(f"{path}: suspicious indented ir.cleanup() before __main__ guard.")

    return errors


def main(argv: list[str]) -> int:
    """Validate one or more Python files and return a shell-compatible exit code."""
    targets = [Path(arg) for arg in argv[1:]]
    if not targets:
        targets = [Path("src/gp2/main.py")]

    all_errors: list[str] = []
    for target in targets:
        if target.exists() and target.is_file() and target.suffix == ".py":
            all_errors.extend(validate_file(target))

    if all_errors:
        for error in all_errors:
            print(error)
        return 1

    print("main-footer validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
