# Runtime Layout (`unit-tests/`)

This folder contains the executable GP2 prototype modules and tests.

## Active modules

- `main.py` - orchestration loop (sensor read -> detect -> publish)
- `sensors.py` - IMU, camera, and IR abstractions with dev-machine fallbacks
- `detection.py` - EAR/PERCLOS fatigue logic
- `telemetry.py` - MQTT status/alert publishing
- `tests.py` - unit tests and integration-style logic tests

## Planning scaffolding

- `placeholders/` - task-aligned configuration/data-model placeholders used to guide implementation phases

## Legacy archive

- `legacy/` - retired or superseded files kept only for historical reference

## Execution

```bash
cd unit-tests
/Users/binghzal/Developer/gp2/.venv/bin/python -m unittest -v
```
