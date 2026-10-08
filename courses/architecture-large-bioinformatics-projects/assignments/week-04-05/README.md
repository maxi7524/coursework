# Protein Data Analysis: Labs 4–5

Complete PDB/UniProt analysis pipeline: acquisition, protein-length and amino-acid statistics, N-terminal analysis, PDB trends and report generation. The submitted implementation matches the repository implementation. This replaces the partial week-04 draft.

| Material | Entry point |
|---|---|
| Workflow | [create_report.smk](create_report.smk), [config.yaml](config.yaml) |
| Submitted analysis | [report.md](report.md) |
| Source and license | [Original repository](https://github.com/maxi7524/project_bioinformatics_tools_proteins_data_analyse), [LICENSE](LICENSE) |

Run from this assignment directory using the original environment (`requests`, Biopython, pandas, NumPy, SciPy, matplotlib, seaborn, Plotly, PyYAML and Snakemake):

```shell
python3 download_data.py
snakemake --snakefile create_report.smk --cores 1
```

Inputs and plots are untracked. The Markdown report is preserved; its generated images require restoration or regeneration. HTML/PDF reports and the interactive plot are available in the owner's archive. The scientific pipeline was not re-executed during organization.

[Input preparation](DATA.md) · [Course index](../../README.md)
