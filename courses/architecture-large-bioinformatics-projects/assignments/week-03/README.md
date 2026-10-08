# Sequence versus Structure Search

[Snakemake workflow](create_report.smk), [exercise notebook](exercise_3.ipynb) and [submitted report](returned_report.md). The latest submitted archive contained the report, comparison examples and result tables; the implementation comes from the original workspace.

Run `python3 download_data.py` to retrieve the course FASTA inputs under `data/raw/` and the supplied structure archives under `data/structures/`. Extract and arrange these inputs according to the [original lab instructions](lab3_instructions.md) and workflow configuration before running `snakemake --snakefile create_report.smk --cores 1` from this directory. BLAST, TM-align, Reseek and Foldseek must be installed separately.

Archived figures and result tables can be restored with `python3 download_data.py --archive-root /path/to/migration-archive --include-artifacts`. The report is retained as submitted; linked figures are restored locally rather than tracked in Git.

[Input preparation](DATA.md) · [Course index](../../README.md)
