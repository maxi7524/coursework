import os
import shutil
import argparse
import logging
import subprocess
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[
        logging.FileHandler("scan_manager.log"),
        logging.StreamHandler()
    ]
)

def merge_results(output_dir: Path, fasta_files: list):
    """
    Merges results from subfolders into main prefix folders and concatenates logs.
    """
    logging.info("[SCAN FASTA 4ESM: MERGE] All processes finished. Starting merge operation...")
    
    main_log_path = output_dir / "main_predict.log"

    # Extract prefixes (assuming format: Mycoplasma_genitalium_part_1 -> Mycoplasma_genitalium)
    prefixes = set()
    for f in fasta_files:
        if '_part_' in f.stem:
            prefix = f.stem.split('_part_')[0]
        elif '_' in f.stem:
            prefix = '_'.merge(f.stem.split('_')[:-1])
        else:
            prefix = f.stem
        prefixes.add(prefix)

    for prefix in prefixes:
        final_folder = output_dir / prefix
        final_folder.mkdir(parents=True, exist_ok=True)
        
        # Find folders that belong to this prefix and are finished (contain .done file)
        part_folders = [d for d in output_dir.iterdir() if d.is_dir() and d.name.startswith(prefix) and (d / ".done").exists()]
        
        if not part_folders:
            continue
            
        logging.info(f"[SCAN FASTA 4ESM: MERGE] Merging {len(part_folders)} folders into {final_folder.name}/")
        
        for folder in part_folders:
            # Merge logs
            part_log = folder / "predict.log"
            if part_log.exists():
                with open(main_log_path, 'a') as main_log, open(part_log, 'r') as p_log:
                    main_log.write(f"\n--- Log from {folder.name} ---\n")
                    main_log.write(p_log.read())

            # Move PDB files
            for pdb_file in folder.glob("*.pdb"):
                destination = final_folder / pdb_file.name
                if not destination.exists():
                    shutil.move(str(pdb_file), str(destination))
                else:
                    pdb_file.unlink()
            
            # Remove the empty part folder
            shutil.rmtree(folder)
            logging.info(f"[SCAN FASTA 4ESM: MERGE] Removed temporary folder {folder.name}")

    logging.info("[SCAN FASTA 4ESM: MERGE] Merge complete. Project organized.")


def main():
    parser = argparse.ArgumentParser(description='Scans for unprocessed FASTA files to run ESM prediction.')
    parser.add_argument('input_folder', type=str, help="Folder with separated .fasta files")
    parser.add_argument('output_folder', type=str, help="Folder for output data")
    parser.add_argument('--mode', choices=['separate', 'merge'], default='merge', 
                        help="'separate' leaves part folders, 'merge' merges them (default).")
    args = parser.parse_args()

    input_dir = Path(args.input_folder)
    output_dir = Path(args.output_folder)

    if not input_dir.exists() or not input_dir.is_dir():
        logging.error(f"[SCAN FASTA 4ESM: SCANNER] Input directory '{input_dir}' not found.")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    fasta_files = sorted(list(input_dir.glob("*.fasta")) + list(input_dir.glob("*.fas")))
    if not fasta_files:
        logging.info("[SCAN FASTA 4ESM: SCANNER] No FASTA files found.")
        return

    unprocessed_files = []
    
    # Check status using the .done marker file in the target folder
    for fasta in fasta_files:
        part_folder = output_dir / fasta.stem
        done_marker = part_folder / ".done"
        
        if not done_marker.exists():
            unprocessed_files.append((fasta, part_folder))

    if unprocessed_files:
        # Run only one process per execution
        fasta_to_run, folder_to_run = unprocessed_files[0]
        logging.info(f"[SCAN FASTA 4ESM: SCANNER] Found unprocessed file: {fasta_to_run.name}. Triggering predictESM...")
        
        import sys
        # Provide the final path to predictESM.py
        subprocess.run([sys.executable, "predictESM.py", str(fasta_to_run), str(folder_to_run)])
        
        logging.info(f"[SCAN FASTA 4ESM: SCANNER] Exiting after processing {fasta_to_run.name}.")
    else:
        logging.info("[SCAN FASTA 4ESM: SCANNER] All files processed.")
        
        if args.mode == 'merge':
            # Check if there are any folders with `.done` that need merging
            part_folders_exist = any((d / ".done").exists() for d in output_dir.iterdir() if d.is_dir())
            if part_folders_exist:
                merge_results(output_dir, fasta_files)
            else:
                logging.info("[SCAN FASTA 4ESM: SCANNER] Everything is already merged.")
        else:
            logging.info("[SCAN FASTA 4ESM: SCANNER] Mode is 'separate'. Files and logs remain in part folders.")

if __name__ == "__main__":
    main()