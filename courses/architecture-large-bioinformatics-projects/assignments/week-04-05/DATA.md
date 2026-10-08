# Input preparation

```shell
python3 download_data.py --list
python3 download_data.py
```

Paths are resolved relative to this assignment, regardless of the working directory. External inputs and generated artifacts are ignored by Git.

The downloader calls the original PDB and UniProt scripts. Its manifest matches the species, kingdoms and sample count in the preserved `config.yaml`; update both when changing the experiment. Install the existing `requests` dependency first. Kingdom samples retain the original unseeded sampling; exact historical inputs were not recovered.

Restore preserved outputs with `python3 download_data.py --archive-root /path/to/migration-archive --include-artifacts`. This also prepares the declared current inputs. The JSON manifest records checksums and exact archive paths.

[Data policy](../../../../DATA_POLICY.md) · [Assignment](README.md)
