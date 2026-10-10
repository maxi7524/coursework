# HPC Protein Feature Prediction: Labs 1–3

IUPred disorder prediction, ProtBert secondary structure, proteome comparisons, runtime and memory measurements, Slurm batching and RAM-disk execution.

| Material | Entry point |
|---|---|
| Submitted analysis | [Report with four original structure illustrations](report_refined.md) |
| Submitted result tables | [Disorder and structure comparisons](report/results/), [runtime/cost measurements](report/results/cost_estimation/) |
| Original command sequence | [SCRIPTS_RUN_HISTORY.md](SCRIPTS_RUN_HISTORY.md) |
| Preparation recovered from email | [download_data.sh](scripts/data/download_data.sh), [normalize_fasta.py](scripts/data/normalize_fasta.py), [split_fasta.py](scripts/data/split_fasta.py) |
| License | [LICENSE](LICENSE) |

Run `python3 download_data.py` to fetch E. coli, human and SwissProt FASTA files into `data/raw/`, plus the course DisProt reference. Follow the original command sequence for normalization, splitting, predictions and analysis. Python packages used by the source include pandas, scikit-learn, torch, transformers, sentencepiece and tabulate; execution also requires Slurm, IUPred and ProtBert model weights.

The three preparation scripts were present only in the submitted archive and are now included. Repository versions are used for the remaining implementation. Both exact versions remain in the owner's archive.

The report, all four figures and compact submitted result tables are committed and can be read without running predictions. The original submission contains a Markdown report; no original PDF or HTML report was found. Proteome inputs, prediction datasets and model weights remain untracked.

## Deferred maintenance

The wrappers and Slurm scripts retain the original absolute cluster paths. Update the installation paths before executing on another machine. The original ProtBert setup used `Rostlab/prot_bert_bfd_ss3`; weights and downloaded IUPred code belong outside Git. [Original installation notes](ORIGINAL_GUIDE.md).

`scripts/analysis/make_report.py` contains a pre-existing unterminated string at line 69 in both source versions. The final Markdown report is retained; this generator is not currently runnable. Algorithm changes, dependency updates and this repair are deferred to the later modernization pass.

[Original experiment/setup guide](ORIGINAL_GUIDE.md) · [Input preparation](DATA.md) · [Course index](../../README.md)
