import argparse
import os
import glob

def normalize_single_file(input_path, output_path, limit=2500):
    """Processes FASTA so that each sequence is on a single line."""
    seen_sequences = set()
    with open(input_path, 'r') as f_in, open(output_path, 'w') as f_out:
        header = None
        sequence = []
        
        def write_entry(h, s):
            seq_str = ''.join(s)
            # Cutting part below certain limit (ProtBert)
            if len(seq_str) > limit:
                seq_str = seq_str[:limit]
            
            if seq_str not in seen_sequences:
                f_out.write(f"{h}\n{seq_str}\n")
                seen_sequences.add(seq_str)
                return 1
            return 0

        total, written = 0, 0
        for line in f_in:
            line = line.strip()
            if not line: continue
            
            if line.startswith(">"):
                if header:
                    total += 1
                    written += write_entry(header, sequence)
                header = line
                sequence = []
            else:
                sequence.append(line)
        
        # Final sequence
        if header:
            total += 1
            written += write_entry(header, sequence)
        
        print(f"Stats: {total} total, {written} unique written (capped at {limit} aa).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Normalize FASTA to flat format (one line per sequence).")
    parser.add_argument("-i", "--input", nargs='+', required=True, help="Input files (e.g., file.fasta, folder/* or list of files)")
    parser.add_argument("-o", "--outdir", default="data/processed", help="Output directory")
    parser.add_argument("-l", "--limit", type=int, default=2500, help="Sequence length limit (default: 2500)")
    
    args = parser.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    # Expand wildcards (if the system hasn't expanded them already)
    files_to_process = []
    for pattern in args.input:
        files_to_process.extend(glob.glob(pattern))

    for f in files_to_process:
        if not os.path.isfile(f): continue
        base_name = os.path.basename(f)
        # Create output name: name_flat.fasta
        out_name = f"{os.path.splitext(base_name)[0]}_flat.fasta"
        out_path = os.path.join(args.outdir, out_name)
        
        print(f"Normalizing: {base_name} -> {out_name}")
        normalize_single_file(f, out_path, limit=args.limit)