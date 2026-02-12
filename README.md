# GP2 – Smart Helmet (Fatigue + Crash Telemetry)

Documentation is in `docs/`.

- Start here: `docs/README.md`
- Structure guide: `docs/PROJECT_STRUCTURE.md`

## Quick start (tests)

```bash
python3 -m unittest tests/test_runtime.py -v
```

If `numpy` is missing:

```bash
python3 -m pip install numpy
```

## Workspace consistency

Install dev tooling:

```bash
python3 -m pip install -r requirements-dev.txt
pre-commit install
```

Run local quality checks:

```bash
ruff check .
ruff format .
black .
pylint src tests
pyright
```

Markdown linting uses repository config in `.markdownlint.json`.
Nested unordered list items use a 4-space indent (`MD007`).
