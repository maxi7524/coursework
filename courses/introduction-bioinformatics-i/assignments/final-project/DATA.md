# External inputs

Run `python3 download_data.py` from this assignment directory before opening the notebook. The script always writes into this assignment, including when invoked from another directory. `--list` lists inputs; `--archive-root` accepts the local migration archive. Inputs, downloaded reference datasets and generated outputs are ignored by Git. Sources and checksums are declared in [data_sources.json](data_sources.json).

GenBank records are pinned to the versioned accessions visible in the original notebook output. GenBank annotations and UniProt responses can change independently of sequence versions; checksums verify the inspected snapshots. If a live response no longer matches, use `--archive-root <migration-archive>` to restore the verified local snapshot. The original Bombyx mori query had no results; no replacement sequence was added.
