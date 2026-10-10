# Human Genome Analysis & 6-Frame ORF Finding Pipeline

## Introduction
This project was developed as part of the Architecture of Large Projects in Bioinformatics (ADP) course. The primary objective was to design and implement high-throughput computational pipelines for whole-genome characterization and benchmark 6-frame Open Reading Frame (ORF) extraction algorithms across different cellular compartments.

The project focused on:
* **Memory-Optimized Genome Statistics:** Compiling structural profiles (nucleotide frequencies, sequence length, and GC content) for the complete T2T-CHM13 v2.0 assembly using stream-parsing strategies to minimize RAM overhead.
* **6-Frame ORF Extraction Benchmarking:** Developing and comparing three decoupled algorithmic approaches (BioPython wrappers, EMBOSS suite integrations, and dependency-free Pure Python engines) under distinct codon tables.
* **Proteomic Reference Mapping:** Cross-referencing predicted translational outputs against official UniProt database annotations to calculate mapping efficiency rates and systematically analyze biological discrepancies.

## Project Directory Structure
```
.
├── data
│   ├── genome
│   │   ├── chr1.fa                  # Human Chromosome 1 genomic sequence
│   │   ├── chrM.fa                  # Human Mitochondrial chromosome sequence
│   │   ├── GRCh38.p14.genome.fa     # GRCh38 reference assembly file
│   │   ├── hs1.annotation.fasta     # T2T-CHM13 official proteome annotations
│   │   └── hs1.fa                   # Complete T2T-CHM13 v2.0 genome assembly
│   └── results
│       ├── GRCh38.p14_stats.csv     # Computed nucleotide metrics for GRCh38
│       ├── map_chrM_vs_ref.csv      # Reference alignment output for Mitochondrial ORFs
│       ├── orf_chr1.csv             # Extracted 6-frame ORFs for Chromosome 1
│       ├── orf_chrM.csv             # Extracted 6-frame ORFs for Mitochondrial DNA
│       └── T2T_stats.csv            # Computed nucleotide metrics for T2T-CHM13
├── genome_analysis_report.md        # Dynamically compiled markdown analysis report
├── GRCh38.p14.log                   # Pipeline execution logs for GRCh38
├── orf_map_chr1.log                 # Translation and mapping logs for Chromosome 1
├── orf_map_chrM.log                 # Translation and mapping logs for Mitochondrial DNA
├── README.md                        # Project documentation overview
├── scripts
│   ├── generate_report.py           # Aggregates log metrics into the final markdown report
│   ├── genome_analyzer.py           # Stream-based incremental sequence statistic parser
│   ├── orf_analyzer.py              # Multi-engine execution script for 6-frame translation
│   └── orf_map_exact.py             # Exact matching alignment tool against reference proteomes
├── T2T.log                          # Pipeline execution logs for T2T-CHM13
```

---

## Replication Guide

### 1. Dataset Acquisition

#### T2T Genome Data Retrieval
To download the complete T2T genome data and testing subsets, use:
```shell
# Download complete T2T reference genome and proteome annotations
wget https://hgdownload.soe.ucsc.edu/goldenPath/hs1/bigZips/hs1.fa.gz
wget https://www.mimuw.edu.pl/~lukaskoz/teaching/adp/labs/lab_human_genome/chm13.draft_v1.1.gene_annotation.protein.fasta

# Download specific chromosome fasta subsets for testing
wget https://www.mimuw.edu.pl/~lukaskoz/teaching/adp/labs/lab_human_genome/chr1.fa
wget https://www.mimuw.edu.pl/~lukaskoz/teaching/adp/labs/lab_human_genome/chrM.fa
```

### 2. Pipeline Execution
Run the 6-frame translation and reference mapping workflows in the background using the commands below:
```shell
# Nuclear Genome Processing: Chromosome 1 (Standard Genetic Code 1)
nohup bash -c "export PATH='/home/ms488923/micromamba/envs/bio_env/bin:\$PATH' && export EMBOSS_ACDROOT='/home/ms488923/micromamba/envs/bio_env/share/EMBOSS/acd' && python3 scripts/orf_analyzer.py -I data/genome/chr1.fa -O data/results/orf_chr1.csv --genetic-code 1 --min-aa 100 && python3 scripts/orf_map_exact.py --orfs data/results/orf_chr1.csv --reference data/genome/hs1.annotation.fasta -O data/results/map_chr1_vs_ref.csv" > orf_map_chr1.log 2>&1 &

# Mitochondrial Genome Processing: Chromosome M (Vertebrate Mitochondrial Code 2)
nohup bash -c "export PATH='/home/ms488923/micromamba/envs/bio_env/bin:\$PATH' && export EMBOSS_ACDROOT='/home/ms488923/micromamba/envs/bio_env/share/EMBOSS/acd' && python3 scripts/orf_analyzer.py -I data/genome/chrM.fa -O data/results/orf_chrM.csv --genetic-code 2 --min-aa 100 && python3 scripts/orf_map_exact.py --orfs data/results/orf_chrM.csv --reference data/genome/hs1.annotation.fasta -O data/results/map_chrM_vs_ref.csv" > orf_map_chrM.log 2>&1 &
```