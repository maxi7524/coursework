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
EXPERIMENTS = ["Mycgen"]  # 
## Define the names of our probes (fasta files in data/experiment/clean/)
PROBES = ['Mycoplasmoides_genitalium_G37']

## Define reference base (TARGET)
TARGET_FASTA = 'data/synthethic_bacterium/clean/CP014940.1_clean.fasta'
TARGET_PDB_DIR = 'data/synthethic_bacterium/4ESM/CP014940.1/'
BINARY_DB_DIR = 'data/synthethic_bacterium/binary_datasets/CP014940.1'


# readme i licencja ()