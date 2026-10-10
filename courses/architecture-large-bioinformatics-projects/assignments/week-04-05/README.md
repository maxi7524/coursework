# Protein Data Analysis: Labs 4–5

Complete PDB/UniProt analysis pipeline: acquisition, protein-length and amino-acid statistics, N-terminal analysis, PDB trends and report generation. The submitted implementation matches the repository implementation. This replaces the partial week-04 draft.

| Material | Entry point |
|---|---|
| Workflow | [create_report.smk](create_report.smk), [config.yaml](config.yaml) |
| Submitted report | [PDF](report.pdf), [interactive HTML](report.html), [Markdown](report.md) |
| Interactive timeline | [PDB trends with year slider](results/plots/pdb_trends_interactive.html) |
| Figures | [Report figures and animations](results/plots/), [earlier figure versions](results/plots/historical/) |
| License | [LICENSE](LICENSE) |

Run from this assignment directory using the original environment (`requests`, Biopython, pandas, NumPy, SciPy, matplotlib, seaborn, Plotly, PyYAML and Snakemake):

```shell
python3 download_data.py
snakemake --snakefile create_report.smk --cores 1
```

The original PDF, HTML and interactive timeline are committed with the report figures. Eighteen figures and GIF animations were recovered directly from the original HTML; no analysis was rerun. Downloaded protein data remain untracked.

To view the interactive report, download this assignment directory and open `report.html` in a browser, or serve the directory with `python3 -m http.server 8000`. GitHub displays HTML source; the local browser runs the year slider and animations. Viewing these reports requires no dataset download or scientific environment.

[Original experiment/setup guide](ORIGINAL_GUIDE.md) · [Input preparation](DATA.md) · [Course index](../../README.md)
