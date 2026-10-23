# Denver park and street tree inventory - Machine Readable brief

Denver's park and street tree inventory records 33,479 ash trees (genus Fraxinus) among 305,295 inventoried trees, 11.0 percent. In Marston, 29.6 percent of inventoried trees are ash (815 of 2,757); in Indian Creek, 27.6 percent (924 of 3,349). Emerald ash borer was confirmed in Denver in June 2025.

Part of Machine Readable: https://adowlen.github.io/machine-readable/

## Contents

- brief-draft.md - the brief (publishable text)
- stats.json - every figure used in the brief, produced by code/build_stats.py
- verification.md - Section 10 pre-flight audit record, methods checklist, sync gate
- verification-ledger-independent.md - the independent verifier's recomputation ledger
- reviewer-notes.md - claims most likely challenged, checks not completed, flags
- sources.md - dataset citations and the per-figure source audit
- social-drafts.md - LinkedIn draft (held for a future Friday synthesis under the Friday-only rule)
- hero.png - hero graphic (generated illustration, headline figure composited; code/hero_composite.py)
- charts/ - chart_neighborhood_rates.png, chart_ash_diameter.png, chart_condition.png
- data/ - neighborhood_panel_trees.csv (aggregate panel), audit_output.txt, raw_aggregates.json (the server-side aggregate query output the figures are built from; the source dataset itself is published by the City of Denver)
- code/ - pull_data.py, build_stats.py, audit_section10.py, charts.py, hero_composite.py

## Dependencies (match code imports)

Python 3 standard library; matplotlib (charts); Pillow (hero composite). No other third-party imports.

## Reuse and citation

Licensed CC-BY-4.0 (see LICENSE). Cite as: Machine Readable, "Denver's inventoried ash, counted tree by tree" (2026), https://github.com/adowlen/denver-tree-inventory-data-brief
