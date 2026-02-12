# Project Structure Guide

This guide defines where to place code and documentation so the repository stays consistent and easy to maintain.

## Top-level layout

- `docs/` - canonical project documentation
- `src/gp2/` - active Python runtime package
- `tests/` - test suite
- `archive/` - archived legacy code kept for reference

## Documentation layout

- Core technical docs live directly under `docs/` (architecture, power, connectivity, etc.).
- Task tracking lives under `docs/todo/`.
- SGP2 report source lives under `docs/report/`.
- External report template assets live under `docs/references/`.

## Runtime code layout

- Active runtime modules stay in `src/gp2/`.
- Planning placeholders live in `src/gp2/planning/`.
- Retired files move to `archive/legacy/`.

## Naming rules

- Use `snake_case` for Python files.
- Use clear, correctly spelled folder names (for example `references`, not `refrences`).
- Keep one responsibility per file when possible.

## Change management rules

- Update related docs in `docs/` when module behavior changes.
- Add or update tests in `tests/test_runtime.py` for any new behavior.
- Do not place new runtime code in `legacy/` or top-level root files.
