# Source Layout

Runtime package location:

- `gp2/`: main project package
  - `main.py`: orchestration loop
  - `sensors.py`: hardware abstraction (with dev-machine fallbacks)
  - `detection.py`: fatigue logic
  - `telemetry.py`: telemetry publishing
  - `planning/`: task-aligned planning models and placeholders

Run main module from repo root:

```bash
PYTHONPATH=src python -m gp2.main
```
