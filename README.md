# GP2 Documentation

This folder contains the canonical documentation for the GP2 smart-helmet prototype.

## Docs

- Architecture overview: `docs/ARCHITECTURE.md`
- Component reference: `docs/COMPONENTS.md`
- Testing guide + expected outputs: `docs/TESTING.md`

## Report (SGP2)

- LaTeX report draft + checklist: `docs/report/`
  - Main file: `docs/report/sgp2-report.tex`
  - Rubric checklist: `docs/report/RUBRIC-CHECKLIST.md`

## Quick start (tests)

```bash
cd unit-tests
python -m unittest -v
```

If `numpy` is missing:

```bash
python -m pip install numpy
```
