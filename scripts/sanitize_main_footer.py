#!/usr/bin/env python3
"""Sanitize src/gp2/main.py by enforcing a single valid __main__ footer."""

from __future__ import annotations

from pathlib import Path

TARGET = Path("src/gp2/main.py")
MAIN_GUARD = 'if __name__ == "__main__":'


def sanitize(text: str) -> str:
    """Normalize source text to exactly one final __main__ block."""
    marker = text.find(MAIN_GUARD)
    if marker == -1:
        return text.rstrip() + "\n\n" + MAIN_GUARD + "\n    main()\n"

    head = text[:marker].rstrip()
    return head + "\n\n" + MAIN_GUARD + "\n    main()\n"


def main() -> int:
    """Apply footer normalization to target file and return a shell exit code."""
    if not TARGET.exists():
        print(f"{TARGET} not found")
        return 1

    original = TARGET.read_text(encoding="utf-8")
    updated = sanitize(original)

    if updated != original:
        TARGET.write_text(updated, encoding="utf-8")
        print("sanitized main footer")
    else:
        print("main footer already clean")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
