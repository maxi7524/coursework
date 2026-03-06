import os 
import glob
import argparse
from pathlib import Path

# ------------------------
# helper functions
# ------------------------

def parse_fasta(file_path: Path):
    """
    Generator reading a FASTA file. 
    Returns a tuple: (header, sequence).
    Handles sequences split across multiple lines.
    """
    header = ""
    seq = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith(">"):
                if header:
                    # Yield the previous header and joined sequence
                    yield header, "".join(seq)
                header = line
                seq = []
            else:
                seq.append(line)
                
        # Yield the last sequence in the file
        if header:
            yield header, "".join(seq)

def write_fasta_chunk(output_file: Path, sequences: list):
    """Writes a list of sequences to a file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        for header, seq in sequences:
            f.write(f"{header}\n{seq}\n")

# ------------------------
# main functions
# ------------------------

def fasta_split(input_paths: list, output_path: str, max_length: int, size: int, mode: str) -> None:
    """Function that splits FASTA files into smaller chunks."""
    # parameters
    out_path = Path(output_path)
    ## Ensure the output directory exists
    out_path.mkdir(parents=True, exist_ok=True)
    
    # collect .fasta files 
    fasta_files_list = []
    for ipath in input_paths:
        ipath_str = str(ipath)

        ## regex check (wildcards)
        if '*' in ipath_str or '?' in ipath_str:
            matched = [Path(p) for p in glob.glob(ipath_str) if Path(p).suffix in ['.fasta']]
            fasta_files_list.extend(matched)
            continue

        p = Path(ipath)
        ## obtain file
        if p.is_file() and p.suffix in ['.fasta']:
            fasta_files_list.append(p)
        elif p.is_dir():
            fasta_files_list.extend(list(p.glob('*.fasta')))
        else:
            print(f"[CLI: fasta splitter]: Warning - '{p}' does not exist or is not a FASTA file.")
    
    ## remove duplicates 
    fasta_files_list = list(set(fasta_files_list))

    ## case: no files found
    if not fasta_files_list:
        print("[CLI: fasta splitter]: No FASTA files found to split. Exiting.")
        return
    
    ## summary
    print(f"[CLI: fasta splitter]: Found {len(fasta_files_list)} FASTA files to process. Mode: {mode.upper()}")

    # ------------------------
    # SPLITTING LOGIC
    # ------------------------
    
    if mode == 'separate':
        for file_path in fasta_files_list:
            file_stem = file_path.stem
            
            # First pass: collect all valid sequences to know the total count for dynamic zero-padding
            valid_seqs = []
            for header, seq in parse_fasta(file_path):
                # Skip sequences longer than max_length (if set)
                if max_length > 0 and len(seq) > max_length:
                    continue
                valid_seqs.append((header, seq))
            
            total_seqs = len(valid_seqs)
            if total_seqs == 0:
                continue
            
            # Calculate padding width based on the highest index (total_seqs - 1)
            pad_width = len(str(total_seqs - 1))
            
            # Split into chunks and save with correct index ranges
            for i in range(0, total_seqs, size):
                chunk = valid_seqs[i:i + size]
                start_idx = i
                end_idx = i + len(chunk) - 1
                
                # Format: prefix_000-019.fasta
                idx_str = f"{start_idx:0{pad_width}d}-{end_idx:0{pad_width}d}"
                out_name = out_path / f"{file_stem}_{idx_str}.fasta"
                write_fasta_chunk(out_name, chunk)
                
    elif mode == 'merge':
        # Collect all valid sequences from all files
        valid_seqs = []
        for file_path in fasta_files_list:
            for header, seq in parse_fasta(file_path):
                if max_length > 0 and len(seq) > max_length:
                    continue
                valid_seqs.append((header, seq))
        
        total_seqs = len(valid_seqs)
        if total_seqs > 0:
            pad_width = len(str(total_seqs - 1))
            
            for i in range(0, total_seqs, size):
                chunk = valid_seqs[i:i + size]
                start_idx = i
                end_idx = i + len(chunk) - 1
                
                # Format: merged_000-019.fasta
                idx_str = f"{start_idx:0{pad_width}d}-{end_idx:0{pad_width}d}"
                out_name = out_path / f"merged_{idx_str}.fasta"
                write_fasta_chunk(out_name, chunk)
            
    print(f"[CLI: fasta splitter]: Finished! Output files are located in: {out_path.absolute()}")

# ------------------------
# parser 
# ------------------------

def main():
    """
    argparser for CLI fasta_splitter
    """
    parser = argparse.ArgumentParser(description='Splits FASTA sequences into separate files.')

    # obtain args
    ## paths
    parser.add_argument(
        'paths', nargs='+', 
        help="Input .fasta files, folders or wildcards (e.g. *.fasta). The LAST path is the output folder."
    )
    
    parser.add_argument('-m', '--max_length', type=int, default=0, help="Maximum sequence length (longer sequences will be skipped). 0 = no limit.") 
    parser.add_argument('-s', '--size', type=int, default=20, help="Number of sequences in a single output file.")
    
    parser.add_argument('--mode', choices=['separate', 'merge'], default='separate', 
                        help="'separate' mode distinguishes input files. 'merge' mode merges everything together.")

    args = parser.parse_args()

    if len(args.paths) < 2:
        parser.error("You must provide at least one input path and one output path at the end.")

    if args.size <= 0:
        parser.error("Size must be greater than 0!")

    ## split paths (last value)
    output_path = args.paths[-1]
    input_paths = args.paths[:-1]

    fasta_split(
        input_paths=input_paths, 
        output_path=output_path,
        max_length=args.max_length,
        size=args.size,
        mode=args.mode
    )

if __name__ == "__main__":
    main()