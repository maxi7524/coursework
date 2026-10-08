# CRON and API: Protein Structure Prediction

The [exercise notebook](exercise_2.ipynb) combines GenPept conversion, FASTA splitting and scheduled ESM API requests. Supporting scripts: [converter](gp_to_fasta.py), [splitter](fasta_splitter.py), [prediction client](predictESM.py), [batch scanner](scan_fasta4ESM.py).

Run `python3 download_data.py` from any directory. Course inputs are written to the notebook's `data/Mycgen/raw/`, `data/hsp23/raw/` and `data/` paths; follow the notebook's conversion and filtering steps before prediction. Prediction outputs and completion markers are generated locally.

ESM API availability and the original CRON/cluster environment were not revalidated. No separate lab-2 email submission was found; this is the recovered repository implementation.

[Input preparation](DATA.md) · [Course index](../../README.md)
