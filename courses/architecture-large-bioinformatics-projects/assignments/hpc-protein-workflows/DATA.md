# Input preparation

```shell
python3 download_data.py --list
python3 download_data.py
```

Paths are resolved relative to this assignment, regardless of the working directory. External inputs and bulk generated datasets are ignored by Git. Preserved reports, figures and compact submitted result tables are tracked documentation.

| Local input | Source |
|---|---|
| `data/raw/E_coli.fasta` | [Download](https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Bacteria/UP000000625/UP000000625_83333.fasta.gz) |
| `data/raw/H_sapiens.fasta` | [Download](https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Eukaryota/UP000005640/UP000005640_9606.fasta.gz) |
| `data/raw/SwissProt.fasta` | [Download](https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz) |
| `DisProt_human_fragments_flat.csv` | [Download](https://www.mimuw.edu.pl/~lukaskoz/teaching/adp/labs/lab_hpc3/DisProt_human_fragments_flat.csv) |

Gzip resources are streamed to their unpacked destination. Mutable upstream data are not claimed to reproduce the historical snapshot.

Restore preserved outputs with `python3 download_data.py --archive-root /path/to/migration-archive --include-artifacts`. This also prepares the declared current inputs. The JSON manifest records checksums and exact archive paths.

[Data policy](../../../../DATA_POLICY.md) · [Assignment](README.md)

Committed reports and figures are already included; viewing them requires no data download. Their manifest retrieval URLs point to this collection rather than a retired source repository.
