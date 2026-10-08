import os
import re
import time
import argparse
import logging
import subprocess
from pathlib import Path



# ------------------------
# helpers
# ------------------------

def parse_fasta(file_path: Path):
    header = ""
    seq = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header:
                    yield header, "".join(seq)
                header = line
                seq = []
            else:
                seq.append(line)
        if header:
            yield header, "".join(seq)

def clean_header_to_filename(header: str) -> str:
    clean_header = header.strip().lstrip('>')
    safe_name = re.sub(r'[^A-Za-z0-9_\-]', '_', clean_header)
    return f"{safe_name}_esmfold_v1.pdb"

# ------------------------
#  main functions
# ------------------------

def run_esm_for_sequence(seq: str, rtn_path: Path, prefix: str) -> bool:
    command = [
        "curl", "-s", "-f", "-X", "POST",
        "--data", seq,
        "https://api.esmatlas.com/foldSequence/v1/pdb/",
        "--output", str(rtn_path)
    ]
    try:
        subprocess.run(command, capture_output=True, text=True, check=True)
        logging.info(f"[PREDICT ESM {prefix}] Successfully downloaded: {rtn_path.name}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"[PREDICT ESM {prefix}] Error for {rtn_path.name}. Code: {e.returncode}. Details: {e.stderr}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Runs ESM API for a single FASTA file.')
    parser.add_argument('fasta_file', type=str, help="Path to input .fasta/.fas file")
    parser.add_argument('output_folder', type=str, help="Exact path to the output part folder")
    args = parser.parse_args()

    file_path = Path(args.fasta_file)
    output_folder = Path(args.output_folder)

    if not file_path.exists():
        print(f"[PREDICT ESM] File not found: {file_path}")
        return

    output_folder.mkdir(parents=True, exist_ok=True)

    # Set up local logging inside the specific part folder
    log_file = output_folder / "predict.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    # Extract base prefix for cleaner logging (e.g., from 'Mycgen_000-019' to 'Mycgen')
    full_stem = file_path.stem
    if '_' in full_stem:
        base_prefix = '_'.join(full_stem.split('_')[:-1])
    else:
        base_prefix = full_stem

    logging.info(f"[PREDICT ESM {base_prefix}] --- Started processing file: {file_path.name} ---")
    
    for header, seq in parse_fasta(file_path):
        safe_filename = clean_header_to_filename(header)
        rtn_path = output_folder / safe_filename
        
        if rtn_path.exists():
            logging.info(f"[PREDICT ESM {base_prefix}] File {rtn_path.name} already exists. Skipping.")
            continue
            
        success = run_esm_for_sequence(seq, rtn_path, base_prefix)
        if success:
            time.sleep(5) 

    # When the entire file is successfully processed, create the '.done' marker
    done_marker = output_folder / ".done"
    done_marker.touch()
    logging.info(f"[PREDICT ESM {base_prefix}] --- Finished processing file. Part marker created. ---")

if __name__ == "__main__":
    main()