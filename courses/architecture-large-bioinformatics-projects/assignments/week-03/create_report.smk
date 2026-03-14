# --- Configuration  ---

# ASSUMPTIONS
## we assume that after using cerating filters we will obtain file in format:
## `probe_clean.fasta` (and those files need to exists )

## Define methods to compare structure
### We split them because they are giving different information, later we use it to create sequence dfs and structure df
SEQUENCE_METHODS = ['blast']
STRUCTURE_METHODS =  ['tmalign', 'reseek', 'foldseek']
METHODS = SEQUENCE_METHODS + STRUCTURE_METHODS


## Define the names of our experiments (subfolders in the data/ directory)
EXPERIMENTS = ["synthethic_bacterium"]  # 
## Define the names of our probes (fasta files in data/experiment/clean/)
PROBES = ['CP014940.1']

## GLOBAL PARAMS
TARGET_DB = ['data/blastdb/CP014940/CPO149940']

# --- SNAKEMAKE RULES ---

## Target rule 
rule all:
    input:
        expand("reports/{experiment}/{probe}_report.md", experiment=EXPERIMENTS, probe=PROBES)

## Rule for running individual methods
## This rule is generic. It will run the appropriate Python script (e.g., run_blast.py, run_foldseek.py)
rule run_method:
    input:
        ### We assume that file is merged that is 4ESM/
        fasta_file="data/{experiment}/clean/{probe}_clean.fasta",
        pdb_dir="data/{experiment}/4ESM/{probe}/"
    output:
        ### We require the wrapper to create these two standardized files
        results="results/{experiment}/report/{probe}/{method}_output.csv",
        metadata="results/{experiment}/report/{probe}/{method}_metadata.csv"
    log:
        "logs/{experiment}/{probe}/report/{method}_run.log"
    shell:
        ### Run your script dedicated to a specific method
        """
        python3 scripts/sequence_comparison/run_{wildcards.method}.py \
            --query_fasta {input.fasta_file} \
            --target_fasta data/{wildcards.experiment}/clean/{wildcards.probe}_clean.fasta \
            --query_pdb_dir {input.pdb_dir} \
            --target_pdb_dir data/{wildcards.experiment}/4ESM/{wildcards.probe}/ \
            --binary_db_dir data/{wildcards.experiment}/binary_datasets/{wildcards.probe}/{wildcards.method}/{wildcards.probe} \
            --out_results {output.results} \
            --out_meta {output.metadata} \
            > {log} 2>&1
        """

# 3. Rule generating the final Markdown report
rule generate_report:
    input:
        # TODO - w przypadku pliku config trzeba by go tutaj dać (jak zmieniają się ustawienia)) 
        # Collect all results and metadata for a given experiment 
        all_results=expand("results/{{experiment}}/report/{{probe}}/{method}_output.csv", method=METHODS),
        all_meta=expand("results/{{experiment}}/report/{{probe}}/{method}_metadata.csv", method=METHODS)
    output:
        report="reports/{experiment}/{probe}_report.md"
    log:
        "logs/{experiment}/{probe}/report/generate_report.log"
    shell:
        """
        python3 scripts/sequence_comparison/generate_md_report.py \\
            --experiment {wildcards.experiment} \\
            --probe {wildcards.probe} \\
            --fasta_sequence_file data/{wildcards.experiment}/clean/{wildcards.probe}_clean.fasta \\
            --methods_sequence {','.join(SEQUENCE_METHODS)} \\
            --methods_structure {','.join(STRUCTURE_METHODS)} \\}
            --results_dir results/{wildcards.experiment}/report/{wildcards.probe} \\
            --out_report {output.report} \\
            > {log} 2>&1
        """