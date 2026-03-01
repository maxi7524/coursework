
## Implementation
The script operates in two modes:
- **File mode**: When provided with a specific `.gp` file, it processes only that single file.
- **Folder mode**: When provided with a directory, it aggregates all `.gp` files within that folder and joins them into a single output file.

## Run
To run the script, use the following base command:
```shell
python3 gp_to_fasta.py <input_path> <output_path>
```
Available Flags:
- `--org_style`: Determines the format of the organism's name.
    - `full`: Uses the complete organism name (e.g., Homo sapiens).
    - `abbreviate` (default): Uses the abbreviated name (e.g., Homo Sapiens $\rightarrow$ H. sapiens).
    - `short`: Uses a short name consisting of the first 3 letters of the genus and species (e.g., *Hom*o *Sap*iens $\rightarrow$ Homsap).
- `--id`: Determines which identifier to include in the FASTA header.
    - `locus` (default): Uses the locus index.
    - `gi`: Uses the GI index
    - `none`: Excludes the identifier entirely.
- `--separator`: Specifies the character used to separate parts of the header.
    - Default is `-`.
- `--no_genename`: A boolean flag that omits the gene name (definition) from the header when passed.

## example runs

### File vs folder

file run
```shell
python3 gp_to_fasta.py data/before_conversion/sequence.gp data/after_conversion/run_file.fasta
```
folder run
```shell
python3 gp_to_fasta.py data/before_conversion data/after_conversion/run_folder.fasta
```

### Flags
org style - full
```shell
python3 gp_to_fasta.py data/before_conversion data/after_conversion/org_style_full.fasta --org_style full
```
org style - abbreviate
```shell
python3 gp_to_fasta.py data/before_conversion data/after_conversion/org_style_abbreviate.fasta 
```
rg style - short
```shell
python3 gp_to_fasta.py data/before_conversion data/after_conversion/org_style_short.fasta --org_style short
```

id - gi
```shell
python3 gp_to_fasta.py data/before_conversion data/after_conversion/id_gi.fasta --id gi --no_genename
```
id - locus
```shell
python3 gp_to_fasta.py data/before_conversion data/after_conversion/id_locus.fasta --id locus --no_genename
```

separator
```shell
python3 gp_to_fasta.py data/before_conversion data/after_conversion/separator.fasta --separator '|' --id gi
```
- if there are not gi values we do not get double separator

no_genename
```shell
python3 gp_to_fasta.py data/before_conversion data/after_conversion/no_genename.fasta --no_genename
```