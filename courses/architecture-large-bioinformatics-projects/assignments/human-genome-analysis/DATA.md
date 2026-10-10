# Input preparation

```shell
python3 download_data.py --list
python3 download_data.py
```

Paths are resolved relative to this assignment, regardless of the working directory. External inputs and bulk generated datasets are ignored by Git. Preserved reports, figures and compact submitted result tables are tracked documentation.

| Local input | Source |
|---|---|
| `data/genome/hs1.fa` | [Download](https://hgdownload.soe.ucsc.edu/goldenPath/hs1/bigZips/hs1.fa.gz) |
| `data/genome/hs1.annotation.fasta` | [Download](https://www.mimuw.edu.pl/~lukaskoz/teaching/adp/labs/lab_human_genome/chm13.draft_v1.1.gene_annotation.protein.fasta) |
| `data/genome/chr1.fa` | [Download](https://www.mimuw.edu.pl/~lukaskoz/teaching/adp/labs/lab_human_genome/chr1.fa) |
| `data/genome/chrM.fa` | [Download](https://www.mimuw.edu.pl/~lukaskoz/teaching/adp/labs/lab_human_genome/chrM.fa) |

Gzip resources are streamed to their unpacked destination. Mutable upstream data are not claimed to reproduce the historical snapshot.

Restore preserved outputs with `python3 download_data.py --archive-root /path/to/migration-archive --include-artifacts`. This also prepares the declared current inputs. The JSON manifest records checksums and exact archive paths.

[Data policy](../../../../DATA_POLICY.md) · [Assignment](README.md)

Committed reports and figures are already included; viewing them requires no data download. Their manifest retrieval URLs point to this collection rather than a retired source repository.
