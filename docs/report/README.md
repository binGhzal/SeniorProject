# SGP2 Report (LaTeX)

Main file: `sgp2-report.tex`

## Files

- `sgp2-report.tex` – filled report draft based on the UAEU CIT template structure
- `references.bib` – BibTeX references used by the report
- `acro.tex` – acronym file loaded when present
- `Figures/` – put images here (optional)
- `../references/` – external template assets and forms (normalized path)

## Compile (local)

From `docs/report/`:

```bash
pdflatex sgp2-report.tex
bibtex sgp2-report
pdflatex sgp2-report.tex
pdflatex sgp2-report.tex
```

## Compile (Overleaf)

Upload the entire `docs/report/` folder to Overleaf as a project, then set `sgp2-report.tex` as the main file.

## What to edit

- Cover page metadata (project id, student names/IDs, advisor)
- Contribution table + signatures
- Optional: replace the architecture diagram placeholder with an exported figure
