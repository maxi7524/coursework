# Merge project part 

## Documentation

### fasta_splitter.py

#### Implementation
The script processes FASTA sequences and splits them into fixed sized (`--size`) chunks dynamically based on the provided paths and parameters:
- **Inputs**: You can provide one or more paths. These can be specific `.fasta` files, directories (which will aggregate all `.fasta` files within), or wildcards (e.g., `*.fasta`). The LAST provided path is always treated as the final output directory.
- **Output - Separate Mode (Default)**: Maintains the distinction between input files. Output files are saved in the output directory with the original file prefix and a dynamically zero-padded index range (e.g., `prefix_000-019.fasta`).
- **Output - Merge Mode**: Aggregates all valid sequences from all provided input files and splits them into globally indexed chunks without original prefixes (e.g., `merged_000-019.fasta`).

#### Run
To run the script, use the following base command:
'''shell
python3 fasta_splitter.py <input_paths...> <output_path>
'''
Available Flags:
- `-m`, `--max_length`: Maximum sequence length (longer sequences will be skipped). Set to `0` for no limit (default: `0`).
- `-s`, `--size`: Number of sequences to include in a single output file chunk (default: `20`).
- `--mode`: Determines how input files are handled.
  - `separate` (default): Distinguishes input files and retains their original prefixes.
  - `merge`: Merges all sequences together into consolidated `merged_...` files.

***

### predictESM.py
#### Implementation
The script takes a target output folder and a single `.fasta` file, processing its sequences through the ESMAtlas FoldSequence v1 API to predict protein structures:
- **Header Cleaning**: It sanitizes FASTA headers by removing special characters and whitespaces to generate safe and valid output filenames (e.g., replacing spaces and symbols to format as `Clean|Name -> Clean_Name`).
- **API Interaction**: Sends sequences via POST request to the ESM API (`https://api.esmatlas.com/foldSequence/v1/pdb/`) and saves the resulting `.pdb` files directly into the part folder.
- **Completion Marker**: Upon successfully processing all sequences in the file, it generates an empty `.done` marker file in the output folder. This signals completion to the scanner script.

#### Run
To run the script, use the following base command:
'''shell
python3 predictESM.py <fasta_file> <output_folder>
'''
*(Note: This script uses positional arguments for the input file and output directory, and does not require additional flags).*

***

### scan_fasta4ESM.py
#### Implementation
This script acts as a pipeline manager that scans for unprocessed FASTA files, triggers the prediction script, and handles the final organization of results and logs:
- **Scanning**: Checks the output directory for unprocessed chunks by looking for the absence of the `.done` marker file or checking if the final merged folder already exists for a given prefix.
- **Execution**: If an unprocessed file is found, it triggers `predictESM.py` for that specific file and then exits (designed to execute one process per run).
- **Merging and Cleanup**: When all parts are processed and the script is executed in `merge` mode, it combines all temporary part folders into final, prefix-named folders. 
- **Log Management**: During the merge operation, temporary logs from part folders are concatenated into a single `main_predict.log` file in the main output directory. This ensures the final log is preserved for error analysis while keeping the project structure clean (highly practical since aggregated logs around ~60MB remain manageable).

#### Run
To run the script, use the following base command:
'''shell
python3 scan_fasta4ESM.py <input_folder> <output_folder>
'''
Available Flags:
- `--mode`: Determines the post-processing behavior once all files are marked as done.
  - `separate` (default): Leaves the processed `.pdb` files and individual logs in their respective part folders.
  - `merge`: Consolidates `.pdb` files into final prefix folders, merges all temporary logs into `main_predict.log`, and removes the empty part folders.

*** 

# Ćwiczenia 

## Do prowadzącego

### Odniesienie się do uwag z poprzedniego zadania:
#### uwaga 1:

"nie ma potrzeby nowej lini miedzy sekwencja a nastepnym headerem"

Przerwa między sekwencjami była świadomym wyborem w celu zwiększenia czytelności, przy minimalnym zwiększeniu rozmiaru pliku. Po namyśle zgadzam się że jest nie potrzebna - usunąłem ją. 


### Zmiany w implementacji (względem instrukcji) 
Względem uwagi z poprzednich ćwiczeń zamieszczam ten żeby móc otrzymać komentarz dotyczący moich zmian w implementacji. 

#### Struktura folderów:
oryginalnie:
```shell
├── (pliki z sekwencjami w formacie .gp) 
├── (pliki z sekwencjami w formacie .fasta)
├── fastas (folder z )
│   ├── (rozdzielone pliki .fasta - fasta_splitter.py output)
│   ├── (wyniki po predictESM.py)
```

Moja konwencja 
```shell
├── (logi + skrypty - one powinny iść do osobnego folderu)
├── data
│   ├── nazwa zbioru danych ('mycoplasmoides_genitalium_G37' | 'hsp23')
│   │   ├── raw (surowe pliki w formacie .gp - można zebrać kilka) 
│   │   ├── clean_fasta (wyniki gp_to_fasta.py)
│   │   ├── separated (wyniki fasta_splitter.py)
│   │   ├── 4ESM (wyniki predictESM.py)
│   │   │   ├── folder dla każdego pliku z separated osobno z odpowiadającym logiem
```

#### Nazwy plików
W nazwach pliku zostawiłem skróconą nazwę żeby łatwiej nawigować w logach (przypadek wielu różnych zestawów sekwencji, ponieważ w takim trybie też można ten pipeline uruchomić). Można oczywiście to usunąć, ale ponieważ nie mamy tutaj do czynienia z dużą ilością sekwencji to uznałem że nei jest to duża strata pamięci.

## Wywołania 

### Zmiany względem instrukcji
Musiałem nałożyć dwie instrukcje pobierania, starałem się to zrobić na jak najkrótszym interwale czasu (8-12), oraz w okresach gdzie domyślnie inni studenci nie powinni zajmować czasu (23, 53). Wynikało to z konieczności wyjazdu i braku możliwości stałego uruchomienia komputera oraz możliwość powrotu dopiero w niedziele późnym wieczorem. 

### Część 1-3 
Download data:
```shell
wget -P data/mycoplasmoides_genitalium_G37/raw  http://gp2fasta.mlhpc.org/Mycoplasmoides_genitalium_G37.gp
```
Transform download `gp` into `fasta`:
```shell
python3 gp_to_fasta.py data/mycoplasmoides_genitalium_G37/raw data/mycoplasmoides_genitalium_G37/clean_fasta --id locus --no_genename
```

Split data
```shell
python3 fasta_splitter.py -m 400 -s 20 data/mycoplasmoides_genitalium_G37/clean_fasta data/mycoplasmoides_genitalium_G37/separated
```

Crontab command (album last number is 3) 
```shell
3,33 * * * * /home/maxi7524/.pyenv/shims/python3 /home/maxi7524/repositories/private/semester_2025-2026_summer/ADPB/week_2/scan_fasta4ESM.py /home/maxi7524/repositories/private/semester_2025-2026_summer/ADPB/week_2/data/mycoplasmoides_genitalium_G37/separated/ /home/maxi7524/repositories/private/semester_2025-2026_summer/ADPB/week_2/data/mycoplasmoides_genitalium_G37/4ESM/ >> /home/maxi7524/repositories/private/semester_2025-2026_summer/ADPB/week_2/cron_general_mycoplasmoides.log 2>&1
```

### Część 4 
Download data:
```shell
wget -P data/hsp23/raw  http://gp2fasta.mlhpc.org/hsp23.gp
```

Transform download `gp` into `fasta`:
```shell
python3 gp_to_fasta.py data/hsp23/raw data/hsp23/clean_fasta --id locus --no_genename
```

Split data
```shell
python3 fasta_splitter.py data/hsp23/clean_fasta data/hsp23/separated --max_length 400 --size 20
```
Last file is only 2 sequences long so i merged it with the last one


Crontab command
```shell
23,53 * * * * /home/maxi7524/.pyenv/shims/python3 /home/maxi7524/repositories/private/semester_2025-2026_summer/ADPB/week_2/scan_fasta4ESM.py /home/maxi7524/repositories/private/semester_2025-2026_summer/ADPB/week_2/data/hsp23/separated/ /home/maxi7524/repositories/private/semester_2025-2026_summer/ADPB/week_2/data/hsp23/4ESM/ >> /home/maxi7524/repositories/private/semester_2025-2026_summer/ADPB/week_2/cron_general_hsp.log 2>&1
```
- Później został zmieniony na 3, 33 (domyślnie dla albumu) 




