
## Implementation
Script is running in two modes
- file mode: given file .gp
    - it runs script with one file 
- folder mode: given folder
    - it aggregates all files in given folder, and join them into one file

## Run
To run script we use:
```shell
python3 gp_to_fasta.py
```
With given flags
- org_style:
    - `full` it uses full organizm name (Homo Sapiens)
    - `abbreviate` (default) it uses abbreviate name (H. Sapiens)
    - `short` it uses short name (3 first letters) (Homsap)
- id:
    - `locus` (default) it uses locus index (without suffix)
    - `gi` it uses gi index
    - `none` it does not 
- separator:
    - we provide separator between name parts
    - `-` (default) 
- no_genename
    - boolean flag for reducing genename from name 


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
org style
```shell
python3 gp_to_fasta.py data/before_conversion data/after_conversion/org_style.fasta --org_style full
```
id - TODO
```shell
python3 gp_to_fasta.py data/before_conversion data/after_conversion/id.fasta --id gi
```
- here should be nothing return because in this file gi does not exists

separator
```shell
python3 gp_to_fasta.py data/before_conversion data/after_conversion/separator.fasta --separator '|'
```
no_genename
```shell
python3 gp_to_fasta.py data/before_conversion data/after_conversion/no_genename.fasta --no_genename
```




Wykład
- problemy komunikacji
- problem z realnymi problemami
- brak dobrej organizacji czasu
- uwaga z lepszymi wynikami (ciężko to wytłumaczyć)
- specjalizacja vs obszerna wiedza 
- pytania o fora 