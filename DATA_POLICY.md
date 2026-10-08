# Data policy

External input datasets and processed copies are never tracked, including in imported history. Use the assignment's `download_data.py`; inspect `DATA.md` for availability and `data_sources.json` for pinned hashes and source references. Do not use `git add -f` for datasets.

Keep the local migration archive until all unavailable inputs and historical results are independently secured. Original repositories are not a permanent download service after deletion. Legacy scientific reproduction remains separate from this organization pass.

Download scripts require Python 3.10+; analysis environments retain their original dependency declarations. Support checks: `python -m unittest discover -s tests -v` from the collection root.
