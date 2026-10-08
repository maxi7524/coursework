# Human Genome Analysis

Streaming T2T-CHM13 genome statistics, six-frame ORF extraction with Biopython, EMBOSS and a pure-Python implementation, timing comparisons and reference-protein mapping. All four repository scripts match the submitted scripts.

| Material | Entry point |
|---|---|
| Genome statistics | [genome_analyzer.py](scripts/genome_analyzer.py) |
| ORF extraction and mapping | [orf_analyzer.py](scripts/orf_analyzer.py), [orf_map_exact.py](scripts/orf_map_exact.py) |
| Report | [genome_analysis_report.md](genome_analysis_report.md), [generate_report.py](scripts/generate_report.py) |
| Source and license | [Original repository](https://github.com/maxi7524/project_bioinformatics_tools_human_genome_analysis), [LICENSE](LICENSE) |

Run `python3 download_data.py` from any directory to retrieve the genome, protein annotation and chromosome subsets into this assignment's `data/genome/`. The complete genome requires several gigabytes of disk space after decompression. Use the original Biopython/EMBOSS environment.

Example from this assignment directory:

```shell
python3 scripts/orf_analyzer.py -I data/genome/chrM.fa -O data/results/orf_chrM.csv --genetic-code 2 --min-aa 100
python3 scripts/orf_map_exact.py --orfs data/results/orf_chrM.csv --reference data/genome/hs1.annotation.fasta -O data/results/map_chrM_vs_ref.csv
```

Chromosome 1 uses genetic code 1. The optional historical GRCh38.p14 comparison input was not supplied and is not silently replaced with another assembly. Original log-derived measurements are preserved, not independently reproduced. The submitted archive adds ORF result tables, kept outside Git.

[Input preparation](DATA.md) · [Course index](../../README.md)
